# Publishing Guide for Yojana.AI

Your platform is ready for deployment. Since it uses a **FastAPI** backend and serves a static **Vanilla JS** frontend, the best way to publish it as a single unit is using **Render** or **Railway**.

## Option 1: One-Click Deploy with Render (Recommended)

1. **Push your code to GitHub** (Done! ✅).
2. Go to [Render.com](https://render.com) and sign in with GitHub.
3. Click **New +** > **Web Service**.
4. Select your `Yojana.AI` repository.
5. Use the following settings:
   - **Language**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Click **Deploy Web Service**.

## Option 2: Railway Deployment

1. Go to [Railway.app](https://railway.app/).
2. Select **New Project** > **Deploy from GitHub**.
3. Choose your repository.
4. Railway will auto-detect the Python environment.
5. In **Variables**, ensure you set the port if needed, but usually it auto-detects.

---

### Important Notes for Production

- **Environment Variables**: If you add API keys later (for advanced AI features), add them in the "Environment Variables" section of your hosting provider.
- **Port Management**: The `backend/main.py` is configured to run on `8000` by default. The start command above uses `--port $PORT` which is standard for cloud providers.

> [!NOTE]
> Since your `main.py` already mounts the `frontend/` folder, once the backend is live, your entire website will be available at the URL provided by the hosting service (e.g., `yojana-ai.onrender.com`).
