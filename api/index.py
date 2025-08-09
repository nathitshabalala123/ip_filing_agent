from app.main import app as _app
from fastapi import FastAPI
import os

# Vercel Python serverless function entrypoint expects a module-level variable
# named `app` that is a WSGI/ASGI callable. FastAPI app is ASGI-compatible.
app = _app

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Vercel"}

# Required for Vercel's ASGI handler
def handler(event, context):
    from mangum import Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)


