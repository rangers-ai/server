from flask import Flask
from simulation import simulation
from vision.vision import image_processing_bp
from agents import Guard, Camera, Drone
import agentpy as ap
import random

app = Flask(__name__)
app.register_blueprint(simulation, url_prefix="/sim")
app.register_blueprint(image_processing_bp, url_prefix="/image")


class SecurityModel(ap.Model):
    def setup(self):
        self.guard = ap.AgentList(self, 1, Guard)  # Create one Guard agent
        self.cameras = ap.AgentList(self, 4, Camera)  # Create three Camera agents
        self.drone = ap.AgentList(self, 1, Drone)  # Create one Drone agent

        self.guard.setup()
        self.cameras.setup()
        self.drone.setup()

        for idx, camera in enumerate(self.cameras):
            camera.id = idx  # Assign ID as Camera_1, Camera_2, etc.

    def step(self):
        self.guard.step()
        self.cameras.step()
        self.drone.step()


@app.route("/")
def home():
    return "Hello \t Welcome to the Drone Security System!"


@app.route("/agents_info")
def agents_info():
    guard_info = model.guard[0].give_info().json
    cameras_info = [camera.give_info().json for camera in model.cameras]
    drone_info = model.drone[0].give_info().json

    model.step()
    return {
        "guard": guard_info,
        "cameras": cameras_info,
        "drone": drone_info,
    }


if __name__ == "__main__":
    parameters = {}  # Define any parameters needed for the model
    model = SecurityModel(parameters)
    model.setup()
    app.run(debug=True, host="0.0.0.0", port=8585)
