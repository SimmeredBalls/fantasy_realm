# 🐉 The Dragon's Hoard - Fantasy Shop

A Django-based RPG shop system featuring user registration, gold-based economy, inventory stock management, and order history.

## 🛠️ Installation Guide

Follow these steps to set up the realm on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/fantasy_realm.git](https://github.com/YOUR_USERNAME/fantasy_realm.git)
   cd fantasy_realm

2. **Create and activate a Virtual Environment**
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate

3. **Install Dependencies**
    pip install -r requirements.txt

4. **Initalize the Database**
    python manage.py migrate

5. **Create Admin**
    python manage.py createsuperuser

6. **Start the Server**
    python manage.py runserver
    