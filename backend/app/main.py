from flask import Flask
from app.api.routes import api_bp
from dotenv import load_dotenv
import os

load_dotenv()  #Load.env file

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)
