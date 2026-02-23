# Yojana.AI 🚜🎓 – Intelligent Government Scheme Assistant

Yojana.AI is a premium, AI-powered platform designed to bridge the information gap between the Indian government and its citizens. It helps users discover eligible schemes and provides localized guides in multi-languages.

## ✨ Features

- **🚀 AI Eligibility Engine**: High-accuracy prediction of eligible schemes using Machine Learning (Decision Trees) and a robust rules-based engine.
- [x] **New**: Interactive Particle Hero Background
- [x] **🌐 Multilingual Support**: Real-time translation of scheme benefits into **Hindi, Bengali, Tamil, and Marathi**.
- **🌐 Multilingual Support**: Real-time translation of scheme benefits into **Hindi, Bengali, Tamil, and Marathi**.
- **📄 Personalized PDF Guides**: Download custom "How to Apply" checklists for every eligible scheme.
- **🎨 Premium Experience**: Professional glassmorphism UI with smooth animations and perfect mobile responsiveness.
- **💳 Monetization Ready**: Tiered access models (Free, Pro, NGO) with a subscription-ready landing page.

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy (SQLite)
- **AI/ML**: Scikit-learn, joblib
- **Frontend**: Vanilla HTML5, CSS3, Modern JavaScript
- **Libraries**: `reportlab` (PDF), `deep-translator` (i18n)

## 📦 Setup & Installation

### 1. Prerequisites
- Python 3.8+

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
# Set up the SQLite database and load 30+ verified schemes
python backend/seed.py
```

### 4. Train the ML Engine (Optional)
```bash
python ml/train_model.py
```

### 5. Run the Application
```bash
python -m uvicorn backend.main:app --reload
```
Server will be live at `http://127.0.0.1:8000`.

## 📁 Project Structure
- `backend/`: API Routes, Database Models, and Eligibility Logic.
- `frontend/`: Premium UI assets, styles, and client-side logic.
- `ml/`: Model training scripts and synthetic datasets.
- `data/`: SQLite database storage.

## ✍️ Credits & Acknowledgments

- **Lead Developer**: [Souvik Dey](https://github.com/Souvik-Dey-2029)
- **Development Partner**: Built with extensive collaborative assistance from **Antigravity (Google DeepMind)**. This project showcases the synergy between human creativity and advanced AI orchestration in building professional-grade software.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
