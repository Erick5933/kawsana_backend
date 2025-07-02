from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

class Barrio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ciudad = models.CharField(max_length=100, default="Cuenca")
    num_habitantes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ("ciudadano", "Ciudadano"),
        ("lider", "Líder"),
        ("organizacion", "Organización"),
    ]

    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)  # Recuerda manejar hashing en la lógica
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios")
    fecha_registro = models.DateField(default=timezone.now)
    estado = models.BooleanField(default=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Cédula debe tener 10 dígitos numéricos')]
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?\d{7,15}$', 'Número de teléfono inválido')]
    )
    direccion = models.CharField(max_length=255, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.email})"

class Organizacion(models.Model):
    nombre = models.CharField(max_length=150)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre or "Organización sin nombre"

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="proyectos")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre or "Proyecto sin nombre"

class Actividad(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="actividades")
    estado = models.BooleanField(default=True)
    puntos = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"{self.nombre} ({proyecto_nombre})"

class EvidenciaActividad(models.Model):
    TIPO_ARCHIVO_CHOICES = [
        ("imagen", "Imagen"),
        ("video", "Video"),
        ("otro", "Otro"),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="evidencias")
    archivo_url = models.URLField()
    tipo_archivo = models.CharField(max_length=10, choices=TIPO_ARCHIVO_CHOICES)
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateField(default=timezone.now)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="evidencias")

    def __str__(self):
        return f"Evidencia {self.tipo_archivo} por {self.usuario} en {self.actividad}"

class ReconocimientoResiduo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="residuos_reconocidos")
    fecha = models.DateField(default=timezone.now)
    tipo_residuo = models.CharField(max_length=100)
    porcentaje_confianza = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    imagen = models.URLField()

    def __str__(self):
        return f"{self.tipo_residuo} reconocido por {self.usuario} con {self.porcentaje_confianza}%"

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen_url = models.URLField(blank=True)
    actualizados_en = models.DateField(auto_now=True)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="noticias")

    def __str__(self):
        return self.titulo or "Noticia sin título"

class ProgresoBarrio(models.Model):
    ultima_actualizacion = models.DateField(default=timezone.now)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="progresos")
    progreso = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=0.0)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, related_name="progresos")

    class Meta:
        unique_together = ("proyecto", "barrio")

    def __str__(self):
        return f"Progreso {self.progreso}% en {self.barrio} para {self.proyecto}"

class ProyectoBarrio(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, related_name="proyectos_asociados")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="barrios_asociados")

    class Meta:
        unique_together = ("barrio", "proyecto")

    def __str__(self):
        barrio_nombre = self.barrio.nombre if self.barrio else "Sin barrio"
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"{barrio_nombre} en proyecto {proyecto_nombre}"

class LiderProyecto(models.Model):
    lider = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="liderazgos")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="lideres")

    class Meta:
        unique_together = ("lider", "proyecto")

    def __str__(self):
        lider_nombre = str(self.lider) if self.lider else "Sin líder"
        proyecto_nombre = self.proyecto.nombre if self.proyecto else "Sin proyecto"
        return f"Líder {lider_nombre} en proyecto {proyecto_nombre}"

class Insignia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre or "Insignia sin nombre"

class UsuarioInsignia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="insignias")
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE, related_name="usuarios")
    fecha_obtenida = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("usuario", "insignia")

    def __str__(self):
        usuario_str = str(self.usuario) if self.usuario else "Usuario desconocido"
        insignia_str = self.insignia.nombre if self.insignia else "Insignia desconocida"
        return f"{usuario_str} obtuvo {insignia_str} el {self.fecha_obtenida}"

#hola
