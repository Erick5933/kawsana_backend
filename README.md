# Kawsana — Backend

> Smart waste classification system. Users photograph waste from their mobile device, an AI chatbot identifies the waste type, and the system directs it to the correct bin — logging every detection in real time.

"Kawsana" means *living well* in Quechua.

---

## What it does

Kawsana is a waste management platform with AI classification at its core. A user points their phone camera at a piece of waste, the chatbot module processes the image and returns the waste category (organic, inorganic, recyclable), and the system registers which bin it belongs to. Administrators monitor all registered bins and detection history from a web dashboard.

---

## Tech stack

| Layer | Technology |
|---|---|
| Framework | Django 5.2.3 + Django REST Framework |
| Auth | JWT (djangorestframework-simplejwt) |
| Database | MySQL (mysqlclient + PyMySQL) |
| Image processing | Pillow |
| AI module | Chatbot app (waste image classification) |
| Password reset | django-rest-passwordreset |
| Media storage | Local media/ directory |

---

## Project structure

```
kawsana_backend/
├── core/              # Main app: users, bins, detections
├── chatbot/           # AI classification module
├── media/             # Uploaded images
├── kawsana_backend/   # Django settings and URL routing
├── env/               # Environment config
├── manage.py
└── requirements.txt
```

---

## Key features

- Mobile-first REST API — designed for phone camera input
- AI chatbot module that classifies waste from images
- Smart bin management — register bins by location and type
- Detection history — every classification logged with timestamp and bin assignment
- Role-based access (admin / user)
- JWT authentication with password reset flow
- Image upload and processing via Pillow

---

## Getting started

### Prerequisites
- Python 3.11+
- MySQL running locally

### Run locally

```bash
git clone https://github.com/Erick5933/kawsana_backend
cd kawsana_backend

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

pip install -r requirements.txt

# Configure your DB in kawsana_backend/settings.py
# DATABASES → NAME, USER, PASSWORD

python manage.py migrate
python manage.py runserver
```

API available at `http://localhost:8000/`

---

## Related repositories

- [kawsana_frontend](https://github.com/Erick5933/kawsana_frontend) — React web dashboard

---

## Authors

Developed at Instituto Tecnológico del Azuay — Cuenca, Ecuador (2025)
