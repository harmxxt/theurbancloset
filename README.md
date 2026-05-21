# Veloria — Cloud-Based Luxury Clothing E-Commerce & Business Automation System
### MCA Final Year Django Project

---

## 📁 Project Structure

```
veloria/
├── veloria/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/            # User registration, login, profile
├── products/            # Product catalog, categories
├── cart/                # Shopping cart
├── orders/              # Checkout, order management
├── invoices/            # PDF generation, Firebase, email
├── dashboard/           # Admin analytics dashboard
├── templates/           # All HTML templates
├── static/              # CSS, JS
├── media/               # Uploaded files, local invoice PDFs
├── manage.py
├── requirements.txt
├── .env.example
├── Procfile
└── render.yaml
```

---

## ⚡ Quick Setup (Local)

### Step 1: Clone and setup virtual environment
```bash
git clone <your-repo>
cd veloria
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure environment
```bash
cp .env.example .env
# Edit .env with your values (see Configuration section below)
```

### Step 4: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Seed sample products
```bash
python manage.py seed_products
```

### Step 6: Create admin user
```bash
python manage.py createsuperuser
```

### Step 7: Run the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🔧 Configuration (.env)

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-very-long-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Gmail SMTP (see Gmail setup below)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=Veloria <your-email@gmail.com>

# Firebase Storage (see Firebase setup below)
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com

# Store Details
STORE_NAME=Veloria
STORE_ADDRESS=123 Fashion Avenue, Mumbai, India
STORE_PHONE=+91 98765 43210
STORE_EMAIL=contact@veloria.com
TAX_RATE=0.18
DELIVERY_CHARGE=99
```

---

## 📧 Gmail SMTP Setup

1. Go to your Google Account → Security
2. Enable **2-Step Verification** (required for app passwords)
3. Go to Security → **App Passwords**
4. Select "Mail" and "Windows Computer" (or any device)
5. Google will generate a **16-character password**
6. Copy that password into `EMAIL_HOST_PASSWORD` in your `.env`

> ⚠️ Do NOT use your regular Gmail password. Use the 16-char App Password.

---

## 🔥 Firebase Storage Setup

1. Go to https://console.firebase.google.com/
2. Create a new project (e.g., "veloria-invoices")
3. Go to **Project Settings** → **Service Accounts**
4. Click **Generate new private key** → Download JSON
5. Rename the file to `firebase-credentials.json`
6. Place it in your project root (same folder as manage.py)
7. Go to **Storage** in Firebase Console
8. Click **Get Started** and set rules to allow reads:
   ```
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /{allPaths=**} {
         allow read: if true;
         allow write: if request.auth != null;
       }
     }
   }
   ```
9. Copy your bucket name (e.g., `your-project.appspot.com`) to `.env`

> ✅ If Firebase is not configured, the system still works — invoices are saved locally and emails still send (if Gmail is set up).

---

## 🤖 Automation Flow (How it Works)

When a customer places an order:

```
Customer Places Order
        ↓
Order created in database (order_number auto-generated)
        ↓
Django Signal fires → orders/signals.py
        ↓
invoices/services.py::create_invoice_for_order()
        ↓
1. Invoice record created (invoice_number auto-generated)
2. PDF generated with ReportLab (professional luxury design)
3. PDF uploaded to Firebase Storage
4. Firebase URL saved in Invoice model
5. Invoice PDF emailed to customer via Gmail SMTP
6. Dashboard analytics update automatically
        ↓
Customer sees Order Success page with invoice download button
```

Each step has error handling — if Firebase or email fails, the order is NEVER affected.

---

## 🛠 Django Admin

Visit: http://127.0.0.1:8000/admin/

- Manage products, categories, orders, invoices
- Update order status
- View all data

## 📊 Business Dashboard

Visit: http://127.0.0.1:8000/dashboard/ (staff/admin only)

- Total orders, revenue, expenses, net profit
- Monthly sales chart (Chart.js)
- Order status distribution chart
- Low stock alerts
- Expense tracking
- Revenue vs Expense reports

---

## 🚀 Deploy to Render

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Veloria initial commit"
git remote add origin https://github.com/your-username/veloria.git
git push -u origin main
```

### Step 2: Create Render account
- Go to https://render.com
- Sign up and connect your GitHub

### Step 3: Create New Web Service
- Click **New → Web Service**
- Connect your GitHub repo
- Settings:
  - **Environment**: Python
  - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_products`
  - **Start Command**: `gunicorn veloria.wsgi:application`

### Step 4: Add Environment Variables in Render
Add all variables from your `.env` file in the Render dashboard under **Environment**.

> ⚠️ Set `DEBUG=False` and add your Render URL to `ALLOWED_HOSTS` on Render.

### Step 5: Upload Firebase credentials
On Render, add the contents of `firebase-credentials.json` as an environment variable named `FIREBASE_CREDENTIALS_JSON`, and update your settings to read from it.

---

## 🐛 Common Error Fixes

### Error: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Error: "TemplateDoesNotExist"
Make sure `DIRS` in `TEMPLATES` in settings.py points to `BASE_DIR / 'templates'`

### Error: "CSRF verification failed"
Make sure your form has `{% csrf_token %}` inside the `<form>` tag.

### Error: Email not sending
- Check your `.env` has the correct Gmail App Password (not your regular password)
- Make sure 2FA is enabled on your Google account
- Try: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` for testing (prints to terminal)

### Error: Firebase credentials not found
- Make sure `firebase-credentials.json` is in the project root
- Check the path in `.env`: `FIREBASE_CREDENTIALS_PATH=firebase-credentials.json`
- If not using Firebase, the system still works — invoices are saved locally

### Error: PDF download shows blank
- Make sure `reportlab` is installed: `pip install reportlab`
- Check `MEDIA_ROOT` in settings.py is writable

### Error: Static files not loading on Render
```bash
python manage.py collectstatic --noinput
```
And make sure `whitenoise` is in `INSTALLED_APPS` and `MIDDLEWARE`.

### Error: "relation does not exist" (database)
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📋 Features Summary

### Customer Features
- ✅ Register, Login, Logout
- ✅ Luxury fashion homepage with hero, featured products
- ✅ Product listing with category filter, search, sort
- ✅ Product detail with size selector, zoom, related products
- ✅ Add to cart, update quantities, remove items
- ✅ Checkout with shipping form + COD/Demo payment
- ✅ Order history and order detail pages
- ✅ Download invoice PDF

### Business Automation
- ✅ Auto invoice generation on order placement
- ✅ Professional PDF invoice (ReportLab)
- ✅ Firebase cloud storage for invoices
- ✅ Gmail SMTP invoice email to customer
- ✅ Dashboard with Chart.js analytics
- ✅ Inventory management with low stock alerts
- ✅ Expense tracking
- ✅ Revenue vs Expense reports

---

## 🎓 MCA Project Details

**Project Title:** Cloud-Based Luxury Clothing E-Commerce and Business Automation System

**Tech Stack:**
- Backend: Django 4.2, Python 3.x
- Database: SQLite (development) / PostgreSQL (production)
- Frontend: HTML5, CSS3, Bootstrap 5, Vanilla JS
- PDF: ReportLab
- Cloud: Firebase Storage
- Email: Gmail SMTP
- Charts: Chart.js
- Deployment: Render (PaaS)

**Apps:** accounts, products, cart, orders, invoices, dashboard
