# Yojana.AI 🚜🎓 – Intelligent Government Scheme Assistant

Yojana.AI is a premium, AI-powered platform designed to bridge the information gap between the Indian government and its citizens. It helps users discover eligible schemes and provides localized guides in multi-languages.

## ✨ Features

- **🚀 Advanced Eligibility Engine**: High-accuracy, robust matching logic with **Decision Tree ML** and rules-based filtering. Now with 100% case-insensitivity and specialized category checks (SC/ST/OBC/General).
- **🧠 Application Success Predictor (NEW)**: High-fidelity risk analysis using a **Random Forest Classifier** to calculate approval probability based on document compliance (Aadhaar match, certificate validity, etc.).
- **📊 Expanded Database**: Includes **52 verified high-impact schemes** covering Finance, Agriculture, Education, Health, and Skill Development.
- **⚡ High-Performance Translation**: Real-time parallel translation using `ThreadPoolExecutor`, making multilingual results (Hindi, Bengali, Tamil, Marathi, and English) appear instantly.
- **📄 Intelligent PDF Roadmaps**: Instant generation of professional application guides now featuring **Application Success Analysis** with AI compliance suggestions.
- **🎨 Premium UX/UI**: Professional glassmorphism design with interactive particle backgrounds, compliance questionnaire flow, and real-time risk badges (LOW/MEDIUM/HIGH).
- **📱 Mobile Responsive**: Fully optimized for a seamless experience across all devices.
- **🛡️ Secure & Reliable**: Built with FastAPI and SQLAlchemy for a high-performance, secure backend.

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy (SQLite)
- **AI/ML**: Scikit-Learn, Joblib (Decision Trees & Random Forest)
- **Frontend**: Modern JavaScript, HTML5, Vanilla CSS3 (Glassmorphism)
- **Concurrency**: Python `concurrent.futures` (ThreadPoolExecutor)
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
# Set up the SQLite database and load 52 verified schemes
python -m backend.seed
```

### 4. Train the ML Engines (Optional)
```bash
# Train the Eligibility Engine
python ml/train_model.py

# Train the Rejection Prediction Engine
python ml/train_rejection_model.py
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
