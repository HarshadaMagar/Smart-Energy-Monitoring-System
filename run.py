import os
import sys

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, BACKEND_DIR)

from app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
