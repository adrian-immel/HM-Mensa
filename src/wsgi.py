from src.main import app

"""
This file is used to run the application in production mode using Gunicorn WSGI server.
It should not be used during development. For development, use main.py directly.
"""
if __name__ == "__main__":
    app.run()
