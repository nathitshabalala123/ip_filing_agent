from app.main import app as _app

# Vercel Python serverless function entrypoint expects a module-level variable
# named `app` that is a WSGI/ASGI callable. FastAPI app is ASGI-compatible.
app = _app

