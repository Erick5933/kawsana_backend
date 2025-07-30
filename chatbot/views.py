from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Usuario, Proyecto, Actividad, Noticia
import openai
from django.conf import settings
import re

@api_view(['POST'])
def chat(request):
    user_message = request.data.get('message', '').lower()
    lang = request.data.get('lang', 'es').lower()

    redes_msg_es = "\n\nPara más información, puedes dirigirte a nuestras redes sociales que están en la parte inferior."
    redes_msg_en = "\n\nFor more information, you can visit our social media links at the bottom."

    # Normalize message - remove accents and special characters
    def normalize_text(text):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            ("ü", "u"),
            ("ñ", "n"),
            ("¿", ""),
            ("?", ""),
            ("¡", ""),
            ("!", ""),
            (",", ""),
            (".", ""),
        )
        for a, b in replacements:
            text = text.replace(a, b)
        return text

    normalized_message = normalize_text(user_message)

    responses_es = {
        "usuarios": lambda: f"Actualmente hay {Usuario.objects.count()} usuarios registrados en la plataforma Kawsana." + redes_msg_es,
        "proyectos": lambda: f"Tenemos {Proyecto.objects.count()} proyectos activos enfocados en desarrollo comunitario y sostenibilidad." + redes_msg_es,
        "actividades": lambda: f"Hay {Actividad.objects.count()} actividades registradas, incluyendo {Actividad.objects.filter(tipo='reciclaje').count()} específicas de reciclaje." + redes_msg_es,
        "noticias": lambda: (
            ("Aquí tienes los títulos de las últimas noticias sobre sostenibilidad:\n" +
             "\n".join(f"- {n.titulo}" for n in Noticia.objects.order_by('-actualizados_en')[:5]))
            if Noticia.objects.exists() else "No hay noticias disponibles por ahora."
        ) + redes_msg_es,
        "que es kawsana": lambda: (
            "Kawsana es una plataforma colaborativa diseñada para fomentar el desarrollo comunitario "
            "y social, facilitando la gestión de proyectos, actividades y la difusión de noticias "
            "que impactan positivamente en las comunidades. Ofrecemos:\n"
            "- Sistema de puntos por actividades ecológicas\n"
            "- Red comunitaria de reciclaje\n"
            "- Información sobre gestión de residuos\n"
            "- Eventos de sostenibilidad local\n"
            "- Proyectos de impacto ambiental"
        ) + redes_msg_es,
        "que significa kawsana": lambda: (
            "La palabra 'Kawsana' proviene del Kichwa (quechua) y significa 'vida' o 'vivir'. "
            "Representa el espíritu de vitalidad y colaboración que impulsa nuestra plataforma. "
            "Elegimos este nombre porque:\n"
            "- Simboliza la conexión con la naturaleza\n"
            "- Representa la vida comunitaria\n"
            "- Refleja nuestro enfoque en sostenibilidad\n"
            "- Honra las raíces indígenas de la región"
        ) + redes_msg_es,
        "por que elegir kawsana": lambda: (
            "10 razones para elegir Kawsana:\n"
            "1. Plataforma 100% enfocada en impacto comunitario real\n"
            "2. Sistema de recompensas por acciones ecológicas\n"
            "3. Red de más de 100 puntos de reciclaje mapeados\n"
            "4. Talleres gratuitos sobre sostenibilidad\n"
            "5. Transparencia en todos nuestros proyectos\n"
            "6. Comunidad activa de más de 10,000 miembros\n"
            "7. App móvil con funciones exclusivas\n"
            "8. Alianzas con organizaciones ambientales\n"
            "9. Reportes de impacto mensuales\n"
            "10. Soporte personalizado 24/7"
        ) + redes_msg_es,
        "redes sociales": lambda: (
            "Puedes seguirnos y contactarnos a través de nuestras redes sociales:\n"
            "📸 Instagram: https://www.instagram.com/kawsana_oficial (Consejos diarios de reciclaje)\n"
            "👍 Facebook: https://www.facebook.com/kawsana.oficial (Eventos y talleres)\n"
            "🐦 Twitter: https://twitter.com/kawsana_eco (Noticias ambientales)\n"
            "📹 YouTube: https://youtube.com/kawsana (Tutoriales de reciclaje)\n"
            "💼 LinkedIn: https://linkedin.com/company/kawsana (Oportunidades de voluntariado)\n\n"
            "¡Estamos para ayudarte! Responde preguntas en menos de 1 hora."
        ),
        "hola": lambda: "¡Hola! 😊 Soy el asistente de Kawsana. ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre:\n- Reciclaje\n- Nuestros proyectos\n- Actividades en tu zona\n- Cómo ganar puntos\n- Información sobre residuos",
        "que tipo de residuo es": lambda: handle_waste_question(user_message, 'es'),
        "donde boto": lambda: handle_waste_question(user_message, 'es'),
        "contenedor azul": lambda: (
            "📘 CONTENEDOR AZUL - PAPEL Y CARTÓN 📘\n\n"
            "✅ QUÉ SÍ VA:\n"
            "- Periódicos, revistas, folletos publicitarios\n"
            "- Cajas de cartón (aplanadas)\n"
            "- Bolsas de papel\n"
            "- Envases de cartón para líquidos (tetrabrik)\n"
            "- Libretas, cuadernos (sin espirales)\n"
            "- Sobres (sin ventanilla de plástico)\n\n"
            "❌ QUÉ NO VA:\n"
            "- Papel sucio o con restos de comida\n"
            "- Papel encerado o plastificado\n"
            "- Papel de fax o fotográfico\n"
            "- Briks con restos de líquido\n"
            "- Pañales o papel higiénico\n\n"
            "💡 DATO: Reciclar 1 tonelada de papel salva 17 árboles y ahorra 26,000 litros de agua."
        ) + redes_msg_es,
        "residuo organico": lambda: (
            "🍏 RESIDUOS ORGÁNICOS 🍏\n\n"
            "Estos son biodegradables y provienen de seres vivos:\n\n"
            "✅ QUÉ INCLUYE:\n"
            "- Restos de comida, fruta y verdura\n"
            "- Cáscaras de huevo, frutos secos\n"
            "- Posos de café e infusiones\n"
            "- Papel de cocina y servilletas usadas\n"
            "- Restos de jardinería (hojas, flores)\n"
            "- Pelo, plumas, huesos pequeños\n\n"
            "♻️ DÓNDE VA:\n"
            "- Contenedor marrón (orgánico)\n"
            "- Donde no hay marrón: contenedor verde (basura normal)\n"
            "- Puedes hacer compost casero\n\n"
            "⚠️ IMPORTANTE:\n"
            "- No mezclar con otros residuos\n"
            "- Usar bolsas compostables\n"
            "- Enjuagar envases de comida antes de reciclar\n\n"
            "🌱 El compost resultante se usa como abono natural."
        ) + redes_msg_es,
        "como reciclar correctamente una lata": lambda: (
            "🥫 GUÍA PARA RECICLAR LATAS 🥫\n\n"
            "PASOS:\n"
            "1. Vacía completamente la lata\n"
            "2. Enjuaga con un poco de agua\n"
            "3. Comprime la lata si es posible\n"
            "4. Deposita en el contenedor AMARILLO\n\n"
            "📊 DATOS IMPORTANTES:\n"
            "- Las latas de acero se reciclan infinitamente\n"
            "- Reciclar una lata ahorra energía para 3h de TV\n"
            "- El aluminio tarda 200 años en degradarse\n"
            "- 670 latas = suficiente aluminio para una bicicleta\n\n"
            "TIPOS DE LATAS RECICLABLES:\n"
            "- Latas de bebidas\n"
            "- Latas de conservas\n"
            "- Botes de aerosol vacíos\n"
            "- Tapas de frascos\n"
            "- Papel de aluminio limpio"
        ) + redes_msg_es,
        "que hago con el aceite usado": lambda: (
            "🛢️ GESTIÓN DE ACEITE USADO 🛢️\n\n"
            "❌ NUNCA viertas por el fregadero:\n"
            "- 1 litro contamina 1,000 litros de agua\n"
            "- Obstruye tuberías\n"
            "- Genera costosos problemas en depuradoras\n\n"
            "✅ CORRECTA DISPOSICIÓN:\n"
            "1. Deja enfriar el aceite\n"
            "2. Filtra restos de comida\n"
            "3. Vierte en botella de plástico\n"
            "4. Cierra bien y lleva a:\n"
            "   - Punto limpio\n"
            "   - Contenedor específico (naranja)\n"
            "   - Algunos supermercados lo recogen\n\n"
            "♻️ BENEFICIOS DEL RECICLAJE:\n"
            "- Se convierte en biodiesel\n"
            "- 1 litro = combustible para 10km\n"
            "- Se usa para jabones y velas\n\n"
            "📅 En Kawsana organizamos recolecciones mensuales de aceite."
        ) + redes_msg_es,
        "como reducir la basura en casa": lambda: (
            "🏡 GUÍA PARA CERO RESIDUOS EN CASA 🏡\n\n"
            "📉 REGLA DE LAS 5 R:\n"
            "1. RECHAZAR lo innecesario\n"
            "2. REDUCIR el consumo\n"
            "3. REUTILIZAR envases y productos\n"
            "4. RECICLAR correctamente\n"
            "5. ROT (compostar)\n\n"
            "🛒 COMPRA SOSTENIBLE:\n"
            "- Usa bolsas reutilizables\n"
            "- Compra a granel\n"
            "- Elige productos sin embalaje\n"
            "- Prioriza envases retornables\n\n"
            "🍽️ EN LA COCINA:\n"
            "- Usa paños en lugar de papel\n"
            "- Composta los orgánicos\n"
            "- Usa tuppers de vidrio\n"
            "- Evita productos desechables\n\n"
            "🧴 EN EL BAÑO:\n"
            "- Pastillas de jabón en lugar de gel\n"
            "- Cepillos de bambú\n"
            "- Copa menstrual/toallas reutilizables\n"
            "- Maquinillas recargables\n\n"
            "📱 APPS QUE AYUDAN:\n"
            "- Too Good To Go (evita desperdicio comida)\n"
            "- Olio (comparte excedentes)\n"
            "- Kawsana (puntos reciclaje cercanos)"
        ) + redes_msg_es,
        "actividades en mi barrio": lambda: (
            f"🗓️ ACTIVIDADES EN TU ZONA 🗓️\n\n"
            f"Próximos eventos:\n"
            f"{Actividad.objects.filter(tipo='reciclaje').order_by('fecha')[:3]}\n\n"
            "Tipos de actividades disponibles:\n"
            "- Talleres de reciclaje creativo\n"
            - "Recolecciones comunitarias\n"
            - "Charlas sobre sostenibilidad\n"
            - "Intercambios de ropa/usados\n"
            - "Limpieza de espacios públicos\n\n"
            "📍 Usa nuestro mapa en la app para ver puntos cercanos"
        ) + redes_msg_es,
        "cuantos puntos tengo": lambda: (
            f"Actualmente tienes {request.user.puntos if request.user.is_authenticated else 'X'} puntos Kawsana.\n\n"
            "💎 NIVELES:\n"
            "0-100: Semilla\n"
            "101-500: Brote\n"
            "501-1000: Árbol\n"
            "1001+: Bosque\n\n"
            "🎯 CÓMO GANAR MÁS:\n"
            "- Participar en actividades (+10-50pts)\n"
            "- Invitar amigos (+25pts c/u)\n"
            "- Completar desafíos ecológicos\n"
            "- Subir fotos reciclando (+5pts)\n"
            "- Asistir a talleres (+30pts)"
            if request.user.is_authenticated 
            else "🔒 Debes iniciar sesión para ver tus puntos. ¡Regístrate y comienza a acumular puntos por acciones ecológicas!"
        ),
        "como gano insignias": lambda: (
            "🏅 SISTEMA DE INSIGNIAS KAWSANA 🏅\n\n"
            "Insignias disponibles:\n"
            "🌱 Principiante Ecológico (primer reciclaje)\n"
            "♻️ Reciclador Consistente (10 actividades)\n"
            "📢 Embajador (invita 5 amigos)\n"
            "🏆 Cero Residuos (1 mes sin basura)\n"
            "💧 Guardián del Agua (ahorra 1000L)\n"
            "🌍 Ciudadano Global (participa en 3 eventos)\n\n"
            "BENEFICIOS:\n"
            "- Descuentos en tiendas ecológicas\n"
            "- Acceso a eventos exclusivos\n"
            "- Reconocimiento público\n"
            "- Prioridad en talleres\n\n"
            "Ver tus insignias: Perfil > Logros"
        ) + redes_msg_es,
        "el papel higienico es reciclable": lambda: (
            "🧻 PAPEL HIGIÉNICO Y RECICLAJE 🧻\n\n"
            "❌ NO es reciclable porque:\n"
            "- Está contaminado biológicamente\n"
            - "Las fibras son demasiado cortas\n"
            - "Puede contener químicos no reciclables\n\n"
            "✅ CORRECTA DISPOSICIÓN:\n"
            "- Contenedor general (verde)\n"
            "- En zonas con orgánico: contenedor marrón\n\n"
            "🌿 ALTERNATIVAS ECOLÓGICAS:\n"
            "- Papel reciclado sin blanquear\n"
            - "Toallas reutilizables\n"
            - "Bidets o toallitas húmedas compostables\n\n"
            "¡Has ganado 5 puntos por aprender sobre reciclaje! 💚"
        ),
        "contenedor amarillo": lambda: handle_yellow_bin_info('es'),
        "punto limpio": lambda: handle_clean_point_info('es'),
        "reciclar electronica": lambda: handle_electronic_waste('es'),
        "reciclar ropa": lambda: handle_clothing_recycling('es'),
        "reciclar pilas": lambda: handle_battery_recycling('es'),  # Intentional typo handling
        "reciclar medicamentos": lambda: handle_medicine_recycling('es'),
        "reciclar vidrio": lambda: handle_glass_recycling('es'),
        "reciclar plastico": lambda: handle_plastic_recycling('es'),
        "compostaje": lambda: handle_composting_info('es'),
        "que va en el contenedor verde": lambda: handle_green_bin_info('es'),
        "como reciclar correctamente": lambda: handle_general_recycling_tips('es'),
        "beneficios del reciclaje": lambda: handle_recycling_benefits('es'),
        "que es economia circular": lambda: handle_circular_economy('es'),
        "como reciclar en casa": lambda: handle_home_recycling('es'),
        "errores comunes al reciclar": lambda: handle_recycling_mistakes('es'),
    }

    responses_en = {
        "users": lambda: f"There are currently {Usuario.objects.count()} registered users on Kawsana platform." + redes_msg_en,
        "projects": lambda: f"We have {Proyecto.objects.count()} active projects focused on community development and sustainability." + redes_msg_en,
        "activities": lambda: f"There are {Actividad.objects.count()} registered activities, including {Actividad.objects.filter(tipo='reciclaje').count()} specific to recycling." + redes_msg_en,
        "news": lambda: (
            ("Here are the titles of the latest sustainability news:\n" +
             "\n".join(f"- {n.titulo}" for n in Noticia.objects.order_by('-actualizados_en')[:5]))
            if Noticia.objects.exists() else "No news available at this time."
        ) + redes_msg_en,
        "what is kawsana": lambda: (
            "Kawsana is a collaborative platform designed to promote community "
            "and social development by facilitating project management, activities "
            "and dissemination of news that positively impact communities. We offer:\n"
            "- Point system for ecological activities\n"
            "- Community recycling network\n"
            "- Waste management information\n"
            "- Local sustainability events\n"
            "- Environmental impact projects"
        ) + redes_msg_en,
        "meaning of kawsana": lambda: (
            "The word 'Kawsana' comes from Kichwa (Quechua) and means 'life' or 'to live'. "
            "It represents the spirit of vitality and collaboration that drives our platform. "
            "We chose this name because:\n"
            "- Symbolizes connection with nature\n"
            "- Represents community life\n"
            "- Reflects our focus on sustainability\n"
            "- Honors indigenous roots of the region"
        ) + redes_msg_en,
        "why choose kawsana": lambda: (
            "10 reasons to choose Kawsana:\n"
            "1. 100% platform focused on real community impact\n"
            "2. Reward system for ecological actions\n"
            "3. Network of over 100 mapped recycling points\n"
            "4. Free sustainability workshops\n"
            "5. Transparency in all our projects\n"
            "6. Active community of over 10,000 members\n"
            "7. Mobile app with exclusive features\n"
            "8. Partnerships with environmental organizations\n"
            "9. Monthly impact reports\n"
            "10. 24/7 personalized support"
        ) + redes_msg_en,
        "social media": lambda: (
            "You can follow and contact us through our social networks:\n"
            "📸 Instagram: https://www.instagram.com/kawsana_oficial (Daily recycling tips)\n"
            "👍 Facebook: https://www.facebook.com/kawsana.oficial (Events and workshops)\n"
            "🐦 Twitter: https://twitter.com/kawsana_eco (Environmental news)\n"
            "📹 YouTube: https://youtube.com/kawsana (Recycling tutorials)\n"
            "💼 LinkedIn: https://linkedin.com/company/kawsana (Volunteer opportunities)\n\n"
            "We're here to help! We respond to questions in less than 1 hour."
        ),
        "hello": lambda: "Hello! 😊 I'm Kawsana's assistant. How can I help you today? You can ask me about:\n- Recycling\n- Our projects\n- Activities in your area\n- How to earn points\n- Waste information",
        "what type of waste is": lambda: handle_waste_question(user_message, 'en'),
        "where to throw": lambda: handle_waste_question(user_message, 'en'),
        "blue bin": lambda: (
            "📘 BLUE BIN - PAPER AND CARDBOARD 📘\n\n"
            "✅ WHAT GOES IN:\n"
            "- Newspapers, magazines, flyers\n"
            "- Cardboard boxes (flattened)\n"
            "- Paper bags\n"
            "- Liquid cardboard containers (tetrapak)\n"
            "- Notebooks (without spirals)\n"
            "- Envelopes (without plastic windows)\n\n"
            "❌ WHAT DOESN'T:\n"
            "- Dirty paper or with food remains\n"
            "- Waxed or laminated paper\n"
            "- Fax or photographic paper\n"
            "- Cartons with liquid residue\n"
            "- Diapers or toilet paper\n\n"
            "💡 FACT: Recycling 1 ton of paper saves 17 trees and 26,000 liters of water."
        ) + redes_msg_en,
        "organic waste": lambda: (
            "🍏 ORGANIC WASTE 🍏\n\n"
            "These are biodegradable and come from living beings:\n\n"
            "✅ WHAT INCLUDES:\n"
            "- Food scraps, fruits and vegetables\n"
            "- Egg shells, nuts\n"
            "- Coffee grounds and tea bags\n"
            "- Used kitchen paper and napkins\n"
            "- Gardening waste (leaves, flowers)\n"
            "- Hair, feathers, small bones\n\n"
            "♻️ WHERE IT GOES:\n"
            "- Brown bin (organic)\n"
            "- Where no brown bin: green bin (general waste)\n"
            "- You can make home compost\n\n"
            "⚠️ IMPORTANT:\n"
            "- Don't mix with other waste\n"
            "- Use compostable bags\n"
            "- Rinse food containers before recycling\n\n"
            "🌱 The resulting compost is used as natural fertilizer."
        ) + redes_msg_en,
        "how to recycle a can": lambda: (
            "🥫 GUIDE TO RECYCLE CANS 🥫\n\n"
            "STEPS:\n"
            "1. Empty the can completely\n"
            "2. Rinse with a little water\n"
            "3. Crush the can if possible\n"
            "4. Put in the YELLOW bin\n\n"
            "📊 IMPORTANT FACTS:\n"
            "- Steel cans can be recycled infinitely\n"
            "- Recycling one can saves energy for 3h of TV\n"
            "- Aluminum takes 200 years to decompose\n"
            "- 670 cans = enough aluminum for a bicycle\n\n"
            "TYPES OF RECYCLABLE CANS:\n"
            "- Beverage cans\n"
            "- Food cans\n"
            "- Empty aerosol cans\n"
            "- Jar lids\n"
            "- Clean aluminum foil"
        ) + redes_msg_en,
        "what to do with used oil": lambda: (
            "🛢️ USED OIL MANAGEMENT 🛢️\n\n"
            "❌ NEVER pour down the drain:\n"
            "- 1 liter contaminates 1,000 liters of water\n"
            "- Clogs pipes\n"
            "- Causes expensive problems in treatment plants\n\n"
            "✅ CORRECT DISPOSAL:\n"
            "1. Let the oil cool\n"
            "2. Filter food residues\n"
            "3. Pour into a plastic bottle\n"
            "4. Close well and take to:\n"
            "   - Recycling center\n"
            "   - Specific container (orange)\n"
            "   - Some supermarkets collect it\n\n"
            "♻️ RECYCLING BENEFITS:\n"
            "- Converted into biodiesel\n"
            "- 1 liter = fuel for 10km\n"
            "- Used for soaps and candles\n\n"
            "📅 Kawsana organizes monthly oil collections."
        ) + redes_msg_en,
        "how to reduce waste at home": lambda: (
            "🏡 ZERO WASTE HOME GUIDE 🏡\n\n"
            "📉 5 R RULE:\n"
            "1. REFUSE what you don't need\n"
            "2. REDUCE consumption\n"
            "3. REUSE containers and products\n"
            "4. RECYCLE correctly\n"
            "5. ROT (compost)\n\n"
            "🛒 SUSTAINABLE SHOPPING:\n"
            "- Use reusable bags\n"
            "- Buy in bulk\n"
            "- Choose unpackaged products\n"
            "- Prefer returnable containers\n\n"
            "🍽️ IN THE KITCHEN:\n"
            "- Use cloths instead of paper\n"
            "- Compost organic waste\n"
            "- Use glass containers\n"
            "- Avoid disposable products\n\n"
            "🧴 IN THE BATHROOM:\n"
            "- Bar soap instead of liquid\n"
            "- Bamboo toothbrushes\n"
            "- Menstrual cup/reusable pads\n"
            "- Refillable razors\n\n"
            "📱 HELPFUL APPS:\n"
            "- Too Good To Go (food waste)\n"
            "- Olio (share surpluses)\n"
            "- Kawsana (nearby recycling points)"
        ) + redes_msg_en,
        "activities in my neighborhood": lambda: (
            f"🗓️ ACTIVITIES IN YOUR AREA 🗓️\n\n"
            f"Upcoming events:\n"
            f"{Actividad.objects.filter(tipo='reciclaje').order_by('fecha')[:3]}\n\n"
            "Types of available activities:\n"
            "- Creative recycling workshops\n"
            "- Community collections\n"
            "- Sustainability talks\n"
            "- Clothing swaps\n"
            "- Public space cleanups\n\n"
            "📍 Use our app map to see nearby points"
        ) + redes_msg_en,
        "how many points do i have": lambda: (
            f"You currently have {request.user.puntos if request.user.is_authenticated else 'X'} Kawsana points.\n\n"
            "💎 LEVELS:\n"
            "0-100: Seed\n"
            "101-500: Sprout\n"
            "501-1000: Tree\n"
            "1001+: Forest\n\n"
            "🎯 HOW TO EARN MORE:\n"
            "- Participate in activities (+10-50pts)\n"
            "- Invite friends (+25pts each)\n"
            "- Complete eco challenges\n"
            "- Upload recycling photos (+5pts)\n"
            "- Attend workshops (+30pts)"
            if request.user.is_authenticated 
            else "🔒 You must log in to see your points. Sign up and start earning points for eco actions!"
        ),
        "how to earn badges": lambda: (
            "🏅 KAWSANA BADGE SYSTEM 🏅\n\n"
            "Available badges:\n"
            "🌱 Eco Beginner (first recycling)\n"
            "♻️ Consistent Recycler (10 activities)\n"
            "📢 Ambassador (invite 5 friends)\n"
            "🏆 Zero Waste (1 month without trash)\n"
            "💧 Water Guardian (save 1000L)\n"
            "🌍 Global Citizen (participate in 3 events)\n\n"
            "BENEFITS:\n"
            "- Discounts in eco stores\n"
            "- Access to exclusive events\n"
            "- Public recognition\n"
            "- Workshop priority\n\n"
            "View your badges: Profile > Achievements"
        ) + redes_msg_en,
        "is toilet paper recyclable": lambda: (
            "🧻 TOILET PAPER AND RECYCLING 🧻\n\n"
            "❌ NOT recyclable because:\n"
            "- Biologically contaminated\n"
            "- Fibers are too short\n"
            "- May contain non-recyclable chemicals\n\n"
            "✅ CORRECT DISPOSAL:\n"
            "- General waste bin\n"
            "- In areas with organic: brown bin\n\n"
            "🌿 ECO ALTERNATIVES:\n"
            "- Unbleached recycled paper\n"
            "- Reusable cloths\n"
            "- Bidets or compostable wipes\n\n"
            "You've earned 5 points for learning about recycling! 💚"
        ),
        "yellow bin": lambda: handle_yellow_bin_info('en'),
        "recycling center": lambda: handle_clean_point_info('en'),
        "recycle electronics": lambda: handle_electronic_waste('en'),
        "recycle clothes": lambda: handle_clothing_recycling('en'),
        "recycle batteries": lambda: handle_battery_recycling('en'),
        "recycle medicine": lambda: handle_medicine_recycling('en'),
        "recycle glass": lambda: handle_glass_recycling('en'),
        "recycle plastic": lambda: handle_plastic_recycling('en'),
        "composting": lambda: handle_composting_info('en'),
        "what goes in the green bin": lambda: handle_green_bin_info('en'),
        "how to recycle properly": lambda: handle_general_recycling_tips('en'),
        "benefits of recycling": lambda: handle_recycling_benefits('en'),
        "what is circular economy": lambda: handle_circular_economy('en'),
        "how to recycle at home": lambda: handle_home_recycling('en'),
        "common recycling mistakes": lambda: handle_recycling_mistakes('en'),
    }

    # Topic mapping with flexible matching
    topics_es = {
        "usuarios|usuario|personas|miembros|comunidad": responses_es["usuarios"],
        "proyectos|proyecto|iniciativas|programas": responses_es["proyectos"],
        "actividades|actividad|eventos|talleres|charlas": responses_es["actividades"],
        "noticias|novedades|actualizaciones|informacion": responses_es["noticias"],
        "kawsana|que es kawsana|qué es kawsana|acerca de kawsana|informacion sobre kawsana": responses_es["que es kawsana"],
        "significa kawsana|significado|origen del nombre|etimologia": responses_es["que significa kawsana"],
        "por que elegir kawsana|ventajas|beneficios|razones para usar kawsana": responses_es["por que elegir kawsana"],
        "redes|contacto|instagram|facebook|twitter|youtube|linkedin|social media": responses_es["redes sociales"],
        "hola|buenas|saludos|buenos dias|buenas tardes|buenas noches": responses_es["hola"],
        "botar|desechar|boto|tirar|tipo de residuo|qué tipo de residuo|clase de basura|qué basura es": responses_es["que tipo de residuo es"],
        "contenedor azul|azul|papel|carton|donde va el papel|reciclar papel": responses_es["contenedor azul"],
        "residuo organico|basura organica|organico|comida|restos de comida|compost": responses_es["residuo organico"],
        "reciclar lata|reciclar una lata|latas|botes|conservas": responses_es["como reciclar correctamente una lata"],
        "aceite usado|botar aceite|desechar aceite|reciclar aceite|olio": responses_es["que hago con el aceite usado"],
        "reducir basura|menos basura|generar menos basura|residuo cero|zero waste": responses_es["como reducir la basura en casa"],
        "actividades barrio|eventos barrio|mi barrio|mi zona|mi ciudad|eventos cercanos": responses_es["actividades en mi barrio"],
        "cuantos puntos tengo|mis puntos|puntos|puntuacion|mi nivel|recompensas": responses_es["cuantos puntos tengo"],
        "insignias|como gano insignias|medallas|logros|trofeos|reconocimientos": responses_es["como gano insignias"],
        "papel higienico|toilet paper|papel del baño|reciclar papel higienico": responses_es["el papel higienico es reciclable"],
        "contenedor amarillo|amarillo|envases|plasticos|briks|tetrabrik|donde va el plastico": responses_es["contenedor amarillo"],
        "punto limpio|limpio|punto verde|recogida especial|donde llevar electrodomesticos": responses_es["punto limpio"],
        "reciclar electronica|electronico|electrodomestico|movil|celular|computador|ordenador|pc|tv": responses_es["reciclar electronica"],
        "reciclar ropa|ropa|textil|zapatos|calzado|prendas|donar ropa": responses_es["reciclar ropa"],
        "reciclar pilas|pila|bateria|baterias|acumulador|donde tirar las pilas": responses_es["reciclar pilas"],
        "reciclar medicamentos|medicina|farmacia|pastillas|medicamento|farmacos": responses_es["reciclar medicamentos"],
        "reciclar vidrio|vidrio|botella|frascos|vasos|cristal": responses_es["reciclar vidrio"],
        "reciclar plastico|plastico|bolsa|film|envoltorio|packaging": responses_es["reciclar plastico"],
        "compostaje|compost|compostar|humus|abono organico": responses_es["compostaje"],
        "contenedor verde|verde|basura normal|resto|no reciclable": responses_es["que va en el contenedor verde"],
        "como reciclar|reciclaje correcto|buenas practicas reciclaje|separar residuos": responses_es["como reciclar correctamente"],
        "beneficios reciclaje|por que reciclar|importancia reciclar|impacto reciclaje": responses_es["beneficios del reciclaje"],
        "economia circular|circular|sostenibilidad|modelo circular|cradle to cradle": responses_es["que es economia circular"],
        "reciclar en casa|hogar|apartamento|departamento|reciclaje domestico": responses_es["como reciclar en casa"],
        "errores reciclaje|fallos|equivocaciones|mitos|falsas creencias": responses_es["errores comunes al reciclar"],
    }

    topics_en = {
        "users|user|members|community|people": responses_en["users"],
        "projects|project|initiatives|programs": responses_en["projects"],
        "activities|activity|events|workshops|talks": responses_en["activities"],
        "news|updates|information|latest": responses_en["news"],
        "what is kawsana|about kawsana|kawsana information|kawsana platform": responses_en["what is kawsana"],
        "meaning of kawsana|name origin|etymology|what does kawsana mean": responses_en["meaning of kawsana"],
        "why choose kawsana|advantages|benefits|reasons to use kawsana": responses_en["why choose kawsana"],
        "social media|contact|instagram|facebook|twitter|youtube|linkedin|social networks": responses_en["social media"],
        "hello|hi|greetings|good morning|good afternoon|good evening": responses_en["hello"],
        "throw away|dispose|where to throw|type of waste|what kind of waste|waste type": responses_en["what type of waste is"],
        "blue bin|blue|paper|cardboard|where does paper go|recycle paper": responses_en["blue bin"],
        "organic waste|organic|food waste|food scraps|compost": responses_en["organic waste"],
        "recycle can|recycle a can|cans|tins|food cans": responses_en["how to recycle a can"],
        "used oil|dispose oil|recycle oil|cooking oil|fry oil": responses_en["what to do with used oil"],
        "reduce waste|less waste|zero waste|waste reduction": responses_en["how to reduce waste at home"],
        "activities neighborhood|events near me|my area|my city|local events": responses_en["activities in my neighborhood"],
        "how many points|my points|points|score|my level|rewards": responses_en["how many points do i have"],
        "badges|how to earn badges|achievements|medals|trophies": responses_en["how to earn badges"],
        "toilet paper|recycle toilet paper|bathroom tissue": responses_en["is toilet paper recyclable"],
        "yellow bin|yellow|packaging|plastics|tetrapak|where does plastic go": responses_en["yellow bin"],
        "recycling center|clean point|special collection|where to take appliances": responses_en["recycling center"],
        "recycle electronics|electronic|appliance|mobile|cell phone|computer|pc|tv": responses_en["recycle electronics"],
        "recycle clothes|clothing|textile|shoes|footwear|garments|donate clothes": responses_en["recycle clothes"],
        "recycle batteries|battery|where to throw batteries|dispose batteries": responses_en["recycle batteries"],
        "recycle medicine|medication|pharmacy|pills|drugs|pharmaceuticals": responses_en["recycle medicine"],
        "recycle glass|glass|bottle|jars|drinking glasses|crystal": responses_en["recycle glass"],
        "recycle plastic|plastic|bag|film|wrapper|packaging": responses_en["recycle plastic"],
        "composting|compost|organic fertilizer|humus": responses_en["composting"],
        "green bin|green|general waste|residual waste|non recyclable": responses_en["what goes in the green bin"],
        "how to recycle|proper recycling|recycling best practices|waste separation": responses_en["how to recycle properly"],
        "recycling benefits|why recycle|importance of recycling|recycling impact": responses_en["benefits of recycling"],
        "circular economy|circularity|sustainability|circular model|cradle to cradle": responses_en["what is circular economy"],
        "recycle at home|household|apartment|home recycling|domestic recycling": responses_en["how to recycle at home"],
        "recycling mistakes|errors|myths|false beliefs|common errors": responses_en["common recycling mistakes"],
    }

    def match_topic(message, topics):
        for keyword, func in topics.items():
            if any(re.search(r'\b'+k+r'\b', message) for k in keyword.split('|')):
                return func()
        return None

    # Select language
    if lang == 'en':
        topics = topics_en
        default_response = "I'm sorry, I didn't understand. Could you rephrase your question or be more specific?"
    else:
        topics = topics_es
        default_response = "Lo siento, no entendí. ¿Puedes reformular tu pregunta o ser más específico?"

    # Try exact matches first
    answer = match_topic(normalized_message, topics)
    
    # If no exact match, try with spelling variations
    if not answer:
        answer = match_topic(user_message, topics)
    
    # If still no match, use OpenAI for complex questions
    if not answer and len(user_message.split()) > 4:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            prompt = (f"Responde brevemente en {lang} sobre reciclaje y sostenibilidad:\nPregunta: {user_message}\nRespuesta:")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()
            answer += redes_msg_es if lang == 'es' else redes_msg_en
        except:
            answer = default_response
    
    if not answer:
        answer = default_response

    return Response({'response': answer})

# ========== DETAILED WASTE HANDLERS ==========

def handle_yellow_bin_info(lang):
    if lang == 'es':
        return (
            "🟡 CONTENEDOR AMARILLO - ENVASES 🟡\n\n"
            "✅ QUÉ SÍ VA:\n"
            "- Envases de plástico (botellas, bandejas, film)\n"
            "- Latas y botes de metal\n"
            "- Briks de bebidas (tetrabrik)\n"
            "- Bolsas de plástico (excepto las biodegradables)\n"
            "- Tapones y tapas de plástico/metal\n"
            "- Envases de yogur, mantequilla\n\n"
            "❌ QUÉ NO VA:\n"
            "- Juguetes de plástico\n"
            "- Cubos de plástico\n"
            "- Utensilios de cocina\n"
            "- Cepillos de dientes\n"
            "- Objetos que no sean envases\n\n"
            "💡 DATO: Solo el 30% de los plásticos se reciclan correctamente. ¡Sé parte del cambio!"
        )
    else:
        return (
            "🟡 YELLOW BIN - PACKAGING 🟡\n\n"
            "✅ WHAT GOES IN:\n"
            "- Plastic containers (bottles, trays, film)\n"
            "- Metal cans and tins\n"
            "- Drink cartons (tetrapak)\n"
            "- Plastic bags (except biodegradable ones)\n"
            "- Plastic/metal lids and caps\n"
            "- Yogurt, butter containers\n\n"
            "❌ WHAT DOESN'T:\n"
            "- Plastic toys\n"
            "- Plastic buckets\n"
            "- Kitchen utensils\n"
            "- Toothbrushes\n"
            "- Non-packaging items\n\n"
            "💡 FACT: Only 30% of plastics are recycled correctly. Be part of the change!"
        )

def handle_clean_point_info(lang):
    if lang == 'es':
        return (
            "♻️ PUNTO LIMPIO - RESIDUOS ESPECIALES ♻️\n\n"
            "📍 QUÉ PUEDES LLEVAR:\n"
            "- Electrodomésticos grandes y pequeños\n"
            "- Muebles y escombros (pequeñas cantidades)\n"
            "- Aceites (cocina y motor)\n"
            "- Pilas y baterías\n"
            "- Pinturas y disolventes\n"
            "- Radiografías\n"
            "- Lámparas y fluorescentes\n"
            "- Ropa y textiles\n"
            "- Medicamentos (mejor en puntos SIGRE)\n\n"
            "ℹ️ INFORMACIÓN:\n"
            "- Gratuito para particulares\n"
            "- Horario ampliado los sábados\n"
            "- Algunos aceptan residuos peligrosos\n"
            "- Lleva tu DNI/NIE\n\n"
            "🔍 Encuentra tu punto más cercano en nuestra app Kawsana"
        )
    else:
        return (
            "♻️ RECYCLING CENTER - SPECIAL WASTE ♻️\n\n"
            "📍 WHAT YOU CAN TAKE:\n"
            "- Large and small appliances\n"
            "- Furniture and rubble (small amounts)\n"
            "- Oils (cooking and motor)\n"
            "- Batteries\n"
            "- Paints and solvents\n"
            "- X-rays\n"
            "- Lamps and fluorescent lights\n"
            "- Clothes and textiles\n"
            "- Medicines (better at SIGRE points)\n\n"
            "ℹ️ INFORMATION:\n"
            "- Free for individuals\n"
            "- Extended hours on Saturdays\n"
            "- Some accept hazardous waste\n"
            "- Bring your ID\n\n"
            "🔍 Find your nearest point in our Kawsana app"
        )

def handle_electronic_waste(lang):
    if lang == 'es':
        return (
            "📱 RECICLAJE DE ELECTRÓNICA - RAEE 📱\n\n"
            "🚫 NO lo tires a la basura normal:\n"
            "- Contiene metales pesados peligrosos\n"
            "- Pierdes materiales valiosos reciclables\n"
            "- Es ilegal en muchos países\n\n"
            "✅ CÓMO RECICLAR:\n"
            "1. Tiendas de electrónica están obligadas a aceptarlos\n"
            "2. Puntos limpios municipales\n"
            "3. Recogidas especiales en tu zona\n"
            "4. Donar si todavía funcionan\n\n"
            "📊 DATOS IMPACTANTES:\n"
            "- 1 móvil contamina 600,000 litros de agua\n"
            "- El 90% de sus componentes son reciclables\n"
            "- Se recupera oro, plata y cobre\n\n"
            "🔋 BATERÍAS: Llévalas por separado a contenedores específicos"
        )
    else:
        return (
            "📱 ELECTRONICS RECYCLING - WEEE 📱\n\n"
            "🚫 DON'T throw in regular trash:\n"
            "- Contains hazardous heavy metals\n"
            "- You lose valuable recyclable materials\n"
            "- It's illegal in many countries\n\n"
            "✅ HOW TO RECYCLE:\n"
            "1. Electronics stores are required to take them back\n"
            "2. Municipal recycling centers\n"
            "3. Special collections in your area\n"
            "4. Donate if still working\n\n"
            "📊 SHOCKING FACTS:\n"
            "- 1 phone pollutes 600,000 liters of water\n"
            "- 90% of its components are recyclable\n"
            "- Gold, silver and copper are recovered\n\n"
            "🔋 BATTERIES: Take them separately to specific containers"
        )

def handle_clothing_recycling(lang):
    if lang == 'es':
        return (
            "👕 RECICLAJE DE ROPA Y TEXTILES 👕\n\n"
            "♻️ OPCIONES SOSTENIBLES:\n"
            "1. Contenedores específicos de ropa (busca los de ONGs serias)\n"
            "2. Tiendas de segunda mano\n"
            "3. Puntos limpios\n"
            "4. Donación directa a necesitados\n"
            "5. Upcycling (transforma en trapos, bolsas, etc.)\n\n"
            "⚠️ IMPORTANTE:\n"
            "- La ropa debe estar limpia y seca\n"
            "- Calzado por separado, atado por pares\n"
            "- Rota o manchada: al contenedor igual (se recicla el textil)\n\n"
            "🌍 IMPACTO:\n"
            "- La industria textil es la 2ª más contaminante\n"
            "- Cada español tira 12kg de ropa al año\n"
            "- El 95% podría reutilizarse o reciclarse"
        )
    else:
        return (
            "👕 CLOTHING AND TEXTILE RECYCLING 👕\n\n"
            "♻️ SUSTAINABLE OPTIONS:\n"
            "1. Specific clothing containers (look for reputable NGOs)\n"
            "2. Second-hand stores\n"
            "3. Recycling centers\n"
            "4. Direct donation to those in need\n"
            "5. Upcycling (transform into rags, bags, etc.)\n\n"
            "⚠️ IMPORTANT:\n"
            "- Clothes should be clean and dry\n"
            "- Shoes separately, tied in pairs\n"
            "- Torn or stained: put in container anyway (textile gets recycled)\n\n"
            "🌍 IMPACT:\n"
            "- Textile industry is the 2nd most polluting\n"
            "- Each Spaniard throws away 12kg of clothes per year\n"
            "- 95% could be reused or recycled"
        )

def handle_battery_recycling(lang):
    if lang == 'es':
        return (
            "🔋 RECICLAJE DE PILAS Y BATERÍAS 🔋\n\n"
            "🚫 PELIGROS:\n"
            "- 1 pila de botón contamina 600,000 litros de agua\n"
            "- Contienen mercurio, cadmio y otros metales pesados\n"
            "- En vertederos contaminan suelo y acuíferos\n\n"
            "✅ CÓMO RECICLAR:\n"
            "1. Contenedores específicos en supermercados\n"
            "2. Puntos limpios\n"
            "3. Tiendas de electrónica\n"
            "4. Algunos establecimientos tienen recogida\n\n"
            "💡 CONSEJOS:\n"
            "- Usa pilas recargables (se amortizan a los 10 usos)\n"
            "- Retira las pilas de aparatos que no uses\n"
            "- No mezcles pilas nuevas y usadas\n\n"
            "📈 En Kawsana recuperamos 5 toneladas de pilas al año"
        )
    else:
        return (
            "🔋 BATTERY RECYCLING 🔋\n\n"
            "🚫 DANGERS:\n"
            "- 1 button battery pollutes 600,000 liters of water\n"
            "- Contain mercury, cadmium and other heavy metals\n"
            "- In landfills they pollute soil and aquifers\n\n"
            "✅ HOW TO RECYCLE:\n"
            "1. Specific containers in supermarkets\n"
            "2. Recycling centers\n"
            "3. Electronics stores\n"
            "4. Some establishments have collection\n\n"
            "💡 TIPS:\n"
            "- Use rechargeable batteries (pay off after 10 uses)\n"
            "- Remove batteries from unused devices\n"
            "- Don't mix new and used batteries\n\n"
            "📈 At Kawsana we recover 5 tons of batteries per year"
        )

def handle_medicine_recycling(lang):
    if lang == 'es':
        return (
            "💊 RECICLAJE DE MEDICAMENTOS 💊\n\n"
            "📍 LUGARES DE ENTREGA:\n"
            "- Farmacias (puntos SIGRE)\n"
            "- Puntos limpios (algunos)\n"
            "- Centros de salud (algunos programas)\n\n"
            "✅ QUÉ DEPOSITAR:\n"
            "- Medicamentos caducados\n"
            "- Medicamentos no utilizados\n"
            "- Cajas y prospectos (con restos)\n"
            "- Envases vacíos (con símbolo SIGRE)\n\n"
            "❌ QUÉ NO DEPOSITAR:\n"
            "- Agujas o objetos punzantes\n"
            "- Termómetros\n"
            "- Productos químicos\n"
            "- Radiografías\n\n"
            "🌿 BENEFICIOS:\n"
            "- Evita contaminación del agua\n"
            "- Previene intoxicaciones\n"
            "- Se recuperan materiales\n"
            "- Se destruyen correctamente los peligrosos"
        )
    else:
        return (
            "💊 MEDICINE RECYCLING 💊\n\n"
            "📍 WHERE TO TAKE:\n"
            "- Pharmacies (SIGRE points)\n"
            "- Recycling centers (some)\n"
            "- Health centers (some programs)\n\n"
            "✅ WHAT TO DEPOSIT:\n"
            "- Expired medicines\n"
            "- Unused medicines\n"
            "- Boxes and leaflets (with residues)\n"
            "- Empty containers (with SIGRE symbol)\n\n"
            "❌ WHAT NOT TO DEPOSIT:\n"
            "- Needles or sharp objects\n"
            "- Thermometers\n"
            "- Chemical products\n"
            "- X-rays\n\n"
            "🌿 BENEFITS:\n"
            "- Prevents water pollution\n"
            "- Avoids poisoning\n"
            "- Materials are recovered\n"
            "- Dangerous ones are properly destroyed"
        )

def handle_glass_recycling(lang):
    if lang == 'es':
        return (
            "🍾 RECICLAJE DE VIDRIO 🍾\n\n"
            "✅ CONTENEDOR VERDE - SÍ VA:\n"
            "- Botellas de vidrio (sin tapón)\n"
            "- Tarros y frascos de alimentos\n"
            "- Frascos de cosmética (limpios)\n"
            "- Vidrio de color (ámbar, verde)\n\n"
            "❌ NO VA:\n"
            "- Cristal (vasos, copas, ventanas)\n"
            "- Cerámica o porcelana\n"
            "- Espejos\n"
            "- Bombillas\n"
            "- Tapones (van al amarillo)\n\n"
            "♻️ PROCESO:\n"
            "1. Se tritura y limpia\n"
            "2. Se funde a 1500°C\n"
            "3. Se fabrican nuevos envases\n\n"
            "💡 DATO: El vidrio se recicla al 100% infinitas veces"
        )
    else:
        return (
            "🍾 GLASS RECYCLING �\n\n"
            "✅ GREEN BIN - YES:\n"
            "- Glass bottles (without cap)\n"
            "- Food jars\n"
            "- Cosmetic jars (clean)\n"
            "- Colored glass (amber, green)\n\n"
            "❌ NO:\n"
            "- Crystal (glasses, cups, windows)\n"
            "- Ceramic or porcelain\n"
            "- Mirrors\n"
            "- Light bulbs\n"
            "- Lids (go to yellow)\n\n"
            "♻️ PROCESS:\n"
            "1. Crushed and cleaned\n"
            "2. Melted at 1500°C\n"
            "3. New containers made\n\n"
            "💡 FACT: Glass is 100% recyclable infinitely"
        )

def handle_plastic_recycling(lang):
    if lang == 'es':
        return (
            "🔄 VERDAD SOBRE EL RECICLAJE DE PLÁSTICO 🔄\n\n"
            "♻️ TIPOS Y CÓMO RECICLARLOS:\n"
            "1. PET (1) - Botellas: Amarillo\n"
            "2. HDPE (2) - Envases rígidos: Amarillo\n"
            "3. PVC (3) - Tubos: Punto limpio\n"
            "4. LDPE (4) - Bolsas: Amarillo (algunas)\n"
            "5. PP (5) - Tapones: Amarillo\n"
            "6. PS (6) - Corcho blanco: Punto limpio\n"
            "7. Otros (7) - Mezclas: Generalmente no reciclable\n\n"
            "⚠️ PROBLEMAS:\n"
            "- Solo el 9% del plástico se recicla\n"
            "- Muchos van a vertederos o incineradoras\n"
            "- Microplásticos contaminan océanos\n\n"
            "💡 SOLUCIONES:\n"
            "- Reduce el uso de plásticos\n"
            "- Reutiliza todo lo posible\n"
            "- Elige productos sin plástico\n"
            "- Participa en limpiezas comunitarias"
        )
    else:
        return (
            "🔄 TRUTH ABOUT PLASTIC RECYCLING 🔄\n\n"
            "♻️ TYPES AND HOW TO RECYCLE:\n"
            "1. PET (1) - Bottles: Yellow\n"
            "2. HDPE (2) - Rigid containers: Yellow\n"
            "3. PVC (3) - Pipes: Recycling center\n"
            "4. LDPE (4) - Bags: Yellow (some)\n"
            "5. PP (5) - Lids: Yellow\n"
            "6. PS (6) - White cork: Recycling center\n"
            "7. Others (7) - Mixtures: Generally not recyclable\n\n"
            "⚠️ PROBLEMS:\n"
            "- Only 9% of plastic gets recycled\n"
            "- Many go to landfills or incinerators\n"
            "- Microplastics pollute oceans\n\n"
            "💡 SOLUTIONS:\n"
            "- Reduce plastic use\n"
            "- Reuse as much as possible\n"
            "- Choose plastic-free products\n"
            "- Join community cleanups"
        )

def handle_composting_info(lang):
    if lang == 'es':
        return (
            "🌱 COMPOSTAJE DOMÉSTICO PASO A PASO 🌱\n\n"
            "📍 QUÉ NECESITAS:\n"
            "- Compostera o espacio en jardín\n"
            "- Residuos orgánicos\n"
            "- Material seco (hojas, ramas)\n"
            "- Paciencia (3-6 meses)\n\n"
            "✅ QUÉ COMPOSTAR:\n"
            "- Restos de fruta y verdura\n"
            "- Cáscaras de huevo\n"
            "- Posos de café y té\n"
            "- Hojas y ramas pequeñas\n"
            "- Papel sin tintas\n\n"
            "❌ QUÉ NO:\n"
            "- Carne o pescado\n"
            "- Lácteos\n"
            "- Aceites\n"
            "- Heces de mascotas\n"
            "- Enfermos o con pesticidas\n\n"
            "💡 TIP: Remueve cada 2 semanas y mantén húmedo"
        )
    else:
        return (
            "🌱 HOME COMPOSTING STEP BY STEP 🌱\n\n"
            "📍 WHAT YOU NEED:\n"
            "- Compost bin or garden space\n"
            "- Organic waste\n"
            "- Dry material (leaves, branches)\n"
            "- Patience (3-6 months)\n\n"
            "✅ WHAT TO COMPOST:\n"
            "- Fruit and vegetable scraps\n"
            "- Egg shells\n"
            "- Coffee grounds and tea\n"
            "- Leaves and small branches\n"
            "- Unprinted paper\n\n"
            "❌ WHAT NOT:\n"
            "- Meat or fish\n"
            "- Dairy\n"
            "- Oils\n"
            "- Pet feces\n"
            "- Diseased or with pesticides\n\n"
            "💡 TIP: Turn every 2 weeks and keep moist"
        )

def handle_green_bin_info(lang):
    if lang == 'es':
        return (
            "🟢 CONTENEDOR VERDE - RESTO 🟢\n\n"
            "🚫 QUÉ VA AQUÍ (cuando no hay otra opción):\n"
            "- Residuos no reciclables\n"
            "- Pañales y productos higiénicos\n"
            "- Polvo de barrer y pelo\n"
            "- Colillas y cenizas\n"
            "- Vajillas rotas\n"
            "- Juguetes rotos\n"
            "- Chicles\n\n"
            "⚠️ PROBLEMA:\n"
            "Este contenedor va a vertedero o incineradora\n"
            "Intenta reducir al máximo lo que pones aquí\n\n"
            "💡 ALTERNATIVAS:\n"
            "- Composta los orgánicos\n"
            "- Repara antes de tirar\n"
            "- Busca puntos de recogida específica\n"
            "- Participa en economía circular"
        )
    else:
        return (
            "🟢 GREEN BIN - RESIDUAL WASTE 🟢\n\n"
            "🚫 WHAT GOES HERE (when no other option):\n"
            "- Non-recyclable waste\n"
            "- Diapers and hygiene products\n"
            "- Sweeping dust and hair\n"
            "- Cigarette butts and ashes\n"
            "- Broken dishes\n"
            "- Broken toys\n"
            "- Chewing gum\n\n"
            "⚠️ PROBLEM:\n"
            "This bin goes to landfill or incinerator\n"
            "Try to minimize what you put here\n\n"
            "💡 ALTERNATIVES:\n"
            "- Compost organic waste\n"
            "- Repair before throwing\n"
            "- Look for specific collection points\n"
            "- Participate in circular economy"
        )

def handle_general_recycling_tips(lang):
    if lang == 'es':
        return (
            "♻️ 10 CONSEJOS PARA RECICLAR MEJOR ♻️\n\n"
            "1. LAVA los envases antes (restos contaminan)\n"
            "2. SEPARA correctamente cada material\n"
            "3. APLANA cajas y envases para ahorrar espacio\n"
            "4. QUITA tapones de botellas (van aparte)\n"
            "5. NO uses bolsas de plástico en los contenedores\n"
            "6. INFÓRMATE sobre puntos limpios en tu zona\n"
            "7. EDUCA a tu familia sobre reciclaje\n"
            "8. PARTICIPA en programas de recogida\n"
            "9. REDUCE tu generación de residuos\n"
            "10. REUTILIZA todo lo posible antes de reciclar\n\n"
            "💡 Recuerda: El mejor residuo es el que no se genera"
        )
    else:
        return (
            "♻️ 10 TIPS TO RECYCLE BETTER ♻️\n\n"
            "1. WASH containers first (residues contaminate)\n"
            "2. SEPARATE each material correctly\n"
            "3. FLATTEN boxes and containers to save space\n"
            "4. REMOVE bottle caps (they go separately)\n"
            "5. DON'T use plastic bags in recycling bins\n"
            "6. LEARN about recycling centers in your area\n"
            "7. EDUCATE your family about recycling\n"
            "8. PARTICIPATE in collection programs\n"
            "9. REDUCE your waste generation\n"
            "10. REUSE as much as possible before recycling\n\n"
            "💡 Remember: The best waste is the one not generated"
        )

def handle_recycling_benefits(lang):
    if lang == 'es':
        return (
            "🌍 10 BENEFICIOS CLAVE DEL RECICLAJE 🌍\n\n"
            "1. AHORRA energía (fabricar con reciclados usa menos)\n"
            "2. CONSERVA recursos naturales (menos extracción)\n"
            "3. REDUCE contaminación (aire, agua, suelo)\n"
            "4. DISMINUYE emisiones de CO2 (combate cambio climático)\n"
            "5. GENERA empleo verde (la economía circular crea puestos)\n"
            "6. AHORRA dinero (gestión de residuos es cara)\n"
            "7. REDUCE vertederos (ocupan espacio y contaminan)\n"
            "8. PRESERVA biodiversidad (menos impacto en ecosistemas)\n"
            "9. FOMENTA innovación (nuevos usos para materiales)\n"
            "10. EDUCA en sostenibilidad (futuras generaciones)\n\n"
            "📊 DATO: Reciclar una lata ahorra suficiente energía para 3 horas de TV"
        )
    else:
        return (
            "🌍 10 KEY BENEFITS OF RECYCLING 🌍\n\n"
            "1. SAVES energy (manufacturing with recycled uses less)\n"
            "2. CONSERVES natural resources (less extraction)\n"
            "3. REDUCES pollution (air, water, soil)\n"
            "4. DECREASES CO2 emissions (fights climate change)\n"
            "5. CREATES green jobs (circular economy generates jobs)\n"
            "6. SAVES money (waste management is expensive)\n"
            "7. REDUCES landfills (they take space and pollute)\n"
            "8. PRESERVES biodiversity (less ecosystem impact)\n"
            "9. PROMOTES innovation (new uses for materials)\n"
            "10. EDUCATES on sustainability (future generations)\n\n"
            "📊 FACT: Recycling one can saves enough energy for 3h of TV"
        )

def handle_circular_economy(lang):
    if lang == 'es':
        return (
            "🔄 ECONOMÍA CIRCULAR EXPLICADA 🔄\n\n"
            "📍 DEFINICIÓN:\n"
            "Sistema económico que elimina residuos y uso continuo de recursos, "
            "contrario al modelo lineal tradicional (producir-usar-tirar).\n\n"
            "🔧 CÓMO FUNCIONA:\n"
            "1. Diseño sostenible (para durar, reparar, reciclar)\n"
            "2. Producción con mínimo impacto\n"
            "3. Consumo responsable (compartir, reutilizar)\n"
            "4. Reparación y reutilización\n"
            "5. Reciclaje de materiales\n\n"
            "💡 EJEMPLOS PRÁCTICOS:\n"
            "- Tiendas de segunda mano\n"
            - "Reparación de electrónicos\n"
            - "Alquiler de ropa\n"
            - "Envases retornables\n"
            - "Energías renovables\n\n"
            "🌱 En Kawsana promovemos proyectos de economía circular"
        )
    else:
        return (
            "🔄 CIRCULAR ECONOMY EXPLAINED 🔄\n\n"
            "📍 DEFINITION:\n"
            "Economic system that eliminates waste and continuous use of resources, "
            "opposite to traditional linear model (make-use-dispose).\n\n"
            "🔧 HOW IT WORKS:\n"
            "1. Sustainable design (to last, repair, recycle)\n"
            "2. Production with minimal impact\n"
            "3. Responsible consumption (share, reuse)\n"
            "4. Repair and reuse\n"
            "5. Material recycling\n\n"
            "💡 PRACTICAL EXAMPLES:\n"
            "- Second-hand stores\n"
            - "Electronics repair\n"
            - "Clothing rental\n"
            - "Returnable packaging\n"
            - "Renewable energy\n\n"
            "🌱 At Kawsana we promote circular economy projects"
        )

def handle_home_recycling(lang):
    if lang == 'es':
        return (
            "🏠 GUÍA COMPLETA PARA RECICLAR EN CASA 🏠\n\n"
            "🗂️ ORGANIZACIÓN BÁSICA:\n"
            "1. Designa un espacio con 3-4 contenedores\n"
            "2. Etiqueta claramente (azul, amarillo, verde, orgánico)\n"
            "3. Usa cubos con tapa para evitar olores\n"
            "4. Coloca cerca de donde generas residuos\n\n"
            "📦 MATERIALES NECESARIOS:\n"
            "- Cubos o bolsas diferenciadas\n"
            "- Compostera si tienes espacio\n"
            "- Bolsas reutilizables para compras\n"
            "- Espacio para almacenar especiales (pilas, etc.)\n\n"
            "🔄 CONSEJOS PARA ÉXITO:\n"
            "- Hazlo fácil para toda la familia\n"
            "- Lava rápidamente los envases\n"
            "- Compacta para ahorrar espacio\n"
            "- Programa días de llevar a puntos limpios\n"
            "- Mide tu progreso (menos basura normal)"
        )
    else:
        return (
            "🏠 COMPLETE GUIDE TO RECYCLE AT HOME 🏠\n\n"
            "🗂️ BASIC ORGANIZATION:\n"
            "1. Designate a space with 3-4 bins\n"
            "2. Label clearly (blue, yellow, green, organic)\n"
            "3. Use lidded bins to prevent odors\n"
            "4. Place near where you generate waste\n\n"
            "📦 NECESSARY MATERIALS:\n"
            "- Differentiated bins or bags\n"
            "- Compost bin if you have space\n"
            "- Reusable shopping bags\n"
            "- Space to store special items (batteries, etc.)\n\n"
            "🔄 TIPS FOR SUCCESS:\n"
            "- Make it easy for the whole family\n"
            "- Quickly rinse containers\n"
            "- Compact to save space\n"
            "- Schedule trips to recycling centers\n"
            "- Measure your progress (less regular trash)"
        )

def handle_recycling_mistakes(lang):
    if lang == 'es':
        return (
            "❌ ERRORES COMUNES AL RECICLAR Y CÓMO EVITARLOS ❌\n\n"
            "1. Tirar envases sucios (contamina lotes enteros)\n"
            "   SOLUCIÓN: Enjuaga rápidamente\n\n"
            "2. Bolsas de plástico en contenedores (atascan máquinas)\n"
            "   SOLUCIÓN: Usa el contenedor sin bolsa\n\n"
            "3. Cristal en el contenedor de vidrio (no es lo mismo)\n"
            "   SOLUCIÓN: Cristal va al punto limpio\n\n"
            "4. Papel manchado de grasa en azul (no es reciclable)\n"
            "   SOLUCIÓN: Al contenedor orgánico\n\n"
            "5. Pequeños objetos de metal en amarillo (no son envases)\n"
            "   SOLUCIÓN: Punto limpio para metales\n\n"
            "6. Briks sin abrir (ocupan espacio innecesario)\n"
            "   SOLUCIÓN: Aplasta y cierra bien\n\n"
            "7. Mezclar residuos por pereza (arruina el esfuerzo de otros)\n"
            "   SOLUCIÓN: Tómate 10 segundos más"
        )
    else:
        return (
            "❌ COMMON RECYCLING MISTAKES AND HOW TO AVOID THEM ❌\n\n"
            "1. Dirty containers (contaminates whole batches)\n"
            "   SOLUTION: Quick rinse\n\n"
            "2. Plastic bags in bins (jams machines)\n"
            "   SOLUTION: Use bin without bag\n\n"
            "3. Crystal in glass bin (not the same)\n"
            "   SOLUTION: Crystal goes to recycling center\n\n"
            "4. Greasy paper in blue bin (not recyclable)\n"
            "   SOLUTION: Organic bin\n\n"
            "5. Small metal objects in yellow (not packaging)\n"
            "   SOLUTION: Recycling center for metals\n\n"
            "6. Unopened cartons (take unnecessary space)\n"
            "   SOLUTION: Flatten and close well\n\n"
            "7. Mixing waste out of laziness (ruins others' effort)\n"
            "   SOLUTION: Take 10 extra seconds"
        )

def handle_waste_question(user_message, lang):
    waste_types = {
        'es': {
            'botella de vidrio|vidrio|frasco de vidrio': ("reciclable", "contenedor verde (vidrio)"),
            'plastico|envase plastico|botella plastico|bolsa plastico|film': ("reciclable", "contenedor amarillo (envases)"),
            'papel|carton|periodico|revista|caja de carton': ("reciclable", "contenedor azul (papel/cartón)"),
            'organico|comida|restos de comida|fruta|verdura|cascara': ("orgánico", "contenedor marrón o verde"),
            'pilas|bateria|baterias|acumulador': ("peligroso", "punto limpio o contenedor específico"),
            'electrodomestico|electronico|movil|celular|computador|tv': ("RAEE", "punto limpio o tienda de electrónica"),
            'ropa|textil|zapatos|calzado|prenda': ("reutilizable", "contenedor de ropa o punto limpio"),
            'medicamento|medicina|pastilla|farmaco': ("peligroso", "punto SIGRE en farmacias"),
            'aceite|aceite usado|aceite de cocina': ("peligroso", "contenedor de aceite o punto limpio"),
            'mueble|muebles|silla|mesa|armario': ("voluminoso", "punto limpio o recogida especial"),
            'espejo|cristal|vaso|copa|ventana': ("no reciclable", "punto limpio (no al contenedor verde)"),
            'pañal|toallita|producto higienico': ("no reciclable", "contenedor verde (resto)"),
            'cd|dvd|disco|vinilo': ("no reciclable", "punto limpio"),
            'juguete|peluche|juego': ("no reciclable", "dona si sirve, sino contenedor verde"),
            'brick|tetrabrik|envase de bebida': ("reciclable", "contenedor amarillo (envases)"),
            'corcho blanco|poliestireno|icopor': ("reciclable", "punto limpio (no al amarillo)"),
            'chicle|gomita|caramelo': ("no reciclable", "contenedor verde (resto)"),
            'colilla|cigarrillo|tabaco': ("contaminante", "contenedor verde (mejor usar ceniceros)"),
            'liquido|producto quimico|pintura|disolvente': ("peligroso", "punto limpio"),
            'neumatico|llanta|rueda': ("especial", "punto limpio o taller mecánico"),
        },
        'en': {
            'glass bottle|glass|jar': ("recyclable", "green bin (glass)"),
            'plastic|plastic container|plastic bottle|plastic bag|film': ("recyclable", "yellow bin (packaging)"),
            'paper|cardboard|newspaper|magazine|cardboard box': ("recyclable", "blue bin (paper/cardboard)"),
            'organic|food|food scraps|fruit|vegetable|peel': ("organic", "brown bin or green bin"),
            'batteries|battery|accumulator': ("hazardous", "recycling center or specific container"),
            'appliance|electronic|mobile|cell phone|computer|tv': ("WEEE", "recycling center or electronics store"),
            'clothes|clothing|textile|shoes|footwear|garment': ("reusable", "clothing bin or recycling center"),
            'medicine|pill|drug|pharmaceutical': ("hazardous", "pharmacy take-back"),
            'oil|used oil|cooking oil': ("hazardous", "oil container or recycling center"),
            'furniture|chair|table|wardrobe': ("bulky", "recycling center or special collection"),
            'mirror|crystal|drinking glass|window': ("not recyclable", "recycling center (not green bin)"),
            'diaper|wipe|hygiene product': ("not recyclable", "green bin (residual waste)"),
            'cd|dvd|disk|vinyl': ("not recyclable", "recycling center"),
            'toy|stuffed animal|game': ("not recyclable", "donate if usable, otherwise green bin"),
            'carton|tetrapak|drink container': ("recyclable", "yellow bin (packaging)"),
            'white cork|polystyrene|styrofoam': ("recyclable", "recycling center (not yellow bin)"),
            'gum|candy': ("not recyclable", "green bin (residual waste)"),
            'cigarette butt|tobacco': ("polluting", "green bin (better use ashtrays)"),
            'liquid|chemical|paint|solvent': ("hazardous", "recycling center"),
            'tire|wheel': ("special", "recycling center or mechanic shop"),
        }
    }

    waste_info = waste_types.get(lang, waste_types['es'])
    for waste_pattern, (waste_type, disposal) in waste_info.items():
        if re.search(waste_pattern, user_message):
            if lang == 'es':
                return (
                    f"El/La {waste_pattern.split('|')[0]} es {waste_type}. "
                    f"Debes depositarlo en el {disposal}.\n\n"
                    "Consejos adicionales:\n"
                    "- Limpia los envases antes de reciclarlos\n"
                    "- Separa los materiales compuestos\n"
                    "- Retira tapones y tapas de otros materiales\n\n"
                    "¿Necesitas más información sobre este residuo?"
                )
            else:
                return (
                    f"The {waste_pattern.split('|')[0]} is {waste_type}. "
                    f"You should dispose it in the {disposal}.\n\n"
                    "Additional tips:\n"
                    "- Clean containers before recycling\n"
                    "- Separate composite materials\n"
                    "- Remove lids and caps from other materials\n\n"
                    "Do you need more information about this waste?"
                )
    
    if lang == 'es':
        return (
            "No reconozco ese tipo de residuo. ¿Podrías ser más específico? Por ejemplo:\n"
            "- '¿dónde boto una botella de plástico?'\n"
            "- '¿qué tipo de residuo es un CD?'\n"
            "- '¿cómo reciclar un mueble viejo?'\n\n"
            "También puedes preguntarme por contenedores específicos como:\n"
            "- contenedor amarillo\n"
            "- punto limpio\n"
            "- contenedor de ropa"
        )
    else:
        return (
            "I don't recognize that type of waste. Could you be more specific? For example:\n"
            "- 'where to throw a plastic bottle?'\n"
            "- 'what type of waste is a CD?'\n"
            "- 'how to recycle old furniture?'\n\n"
            "You can also ask me about specific containers like:\n"
            "- yellow bin\n"
            "- recycling center\n"
            "- clothing bin"
        )