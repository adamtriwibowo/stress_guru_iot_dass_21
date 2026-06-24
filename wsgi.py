"""
WSGI entry point untuk Vercel deployment
"""
from app import app

if __name__ == "__main__":
    app.run()
