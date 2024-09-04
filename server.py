# server.py
from flask import Flask
from simulation import simulation_bp
from vision.vision import image_processing_bp

# Create the Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(simulation_bp, url_prefix='/simulation')
app.register_blueprint(image_processing_bp, url_prefix='/image')

@app.route('/')
def home():
    return "Welcome to the Drone Security System!"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
