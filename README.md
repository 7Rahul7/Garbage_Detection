
---

````markdown
# ♻️ GarbageDetector - AI-Powered Waste Classification App

GarbageDetector is a Django web application that uses a TensorFlow model to classify garbage into recyclable and non-recyclable categories. It features email-based user registration with OTP verification, Google Login integration, and a token-based prediction system.

---

## 🚀 Features

- ♻️ **Garbage Classification** using a trained AI model
- 🔐 **Email Registration** with OTP verification
- 🔑 **Google Login** (OAuth 2.0)
- 🪙 **Token System** (Users get 1000 free tokens on signup; each prediction costs 5 tokens)
- 🖼️ **Image Upload & Live Prediction**
- 🌐 **Beautiful UI** using Tailwind CSS
- 📁 User images stored in `media/`

---

## 🧠 Model Training

- The AI model was developed using **TensorFlow**.
- Due to limited local resources, **model training was done in Kaggle Notebooks**, which provides **free access to GPUs (NVIDIA Tesla T4/P100/V100)**.
- Trained model files are stored in the `AI_model/` directory and used for prediction via `tensorflow.keras`.

---

## 📁 Project Structure

```bash
.
├── AI_model/                  # Trained model (.h5 or SavedModel)
├── GarbageDetectionApp/       # Main Django app (urls.py, admin.py)
├── GarbageDetector/           # Core app (views.py, templates/, settings.py)
├── media/                     # Uploaded images
├── .env                       # Environment variables (email credentials, secrets)
├── db.sqlite3                 # SQLite DB
├── README.md                  # You are here
├── requirements.txt           # Project dependencies
├── main.py / manage.py        # Django run and management commands
└── uv.lock / pyproject.toml   # uv-based virtual environment files
````

---

## ⚙️ Installation Guide

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/yourusername/GarbageDetector.git
cd GarbageDetector
```

### 2. 🐍 Set Up Virtual Environment (using [uv](https://github.com/astral-sh/uv))

```bash
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

Here’s how you can write a clear section in your `README.md` file to explain the required environment variables and how to create a `.env` file:

---

## 🔐 Environment Variables Setup

To keep sensitive information secure and out of your source code, this project uses a `.env` file to store environment variables. You **must create a `.env` file** in the root directory of your project with the following variables:

### Required Environment Variables

```env
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret

EMAIL_HOST_USER=your_email_address@example.com
EMAIL_HOST_PASSWORD=your_email_app_password

OPENWEATHER_API_KEY=your_openweather_api_key
```

### 📌 Instructions to Create a `.env` File

1. In the root of your Django project, create a new file named `.env` (note the dot at the beginning).
2. Open the `.env` file in your code editor.
3. Paste the variable names and add your actual keys/secrets as shown above.
4. **DO NOT** commit this file to Git. The `.env` file should be listed in your `.gitignore`.

### Example `.env` File

```env
GOOGLE_CLIENT_ID=12345-example-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=abcdeExampleSecret123

EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here

OPENWEATHER_API_KEY=abcdef1234567890examplekey
```

> ✅ Make sure your Django project is configured to load environment variables using a package like `python-decouple` or `django-environ`.

---


### 4. 🔧 Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 5. 🛠️ Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 🏃 Run the App

```bash
python manage.py runserver
```

---

## ✅ Requirements

Install from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

Or regenerate it with:

```bash
uv pip freeze > requirements.txt
```

---

## 📸 Sample Prediction Flow

1. Register with email → Receive OTP
2. Verify OTP → Get 1000 tokens
3. Upload an image of garbage
4. The model predicts the category and tells if it’s **Recyclable** or **Non-Recyclable**
5. 5 tokens are deducted per prediction

---

## 🔐 Google OAuth Login

Google Login is integrated using `social-auth-app-django`. You’ll need to:

* Set up credentials in Google Cloud Console
* Add your client ID/secret to `.env`

---

## 🧪 Model Classes

The model supports the following 12 classes:

* **Recyclable**: `battery`, `cardboard`, `green-glass`, `metal`, `paper`, `plastic`, `white-glass`, `brown-glass`
* **Non-Recyclable**: `clothes`, `trash`, `shoes`, `biological`

---

## Model File Link

* **link**: https://drive.google.com/file/d/10EOxMPrvc-_ZoRFoEZlHpNF-I7Ltx_FG/view?usp=sharing

## 🙏 Acknowledgements

* Trained on [Garbage Classification Dataset](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)
* Hosted on Django
* Training powered by **Kaggle Notebooks with free GPUs**

---

## 📬 Contact

Made with 💚 by \Keshab Adhikari
Email: [jbadhikari1@gmail.com](mailto:jbadhikari@gmail.com)
GitHub: [@7Rahul7](https://github.com/7Rahul7)

```
