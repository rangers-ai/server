# simulation.py
from flask import Blueprint, request, jsonify
from agents import SimulationModel
import threading
import queue

# Create a blueprint for simulation routes
simulation_bp = Blueprint('simulation', __name__)

# Globals for simulation management
sim = None
sim_thread = None
message_queue = queue.Queue()

# Function to run the simulation in a separate thread
def run_simulation():
    global sim
    parameters = {
        "message_queue": message_queue
    }
    sim = SimulationModel(parameters)
    sim.run()

# Route to handle simulation data
@simulation_bp.route("/", methods=["POST"])
def main():
    global sim, sim_thread, message_queue
    
    data = request.json
    camera_id = data.get('camera_id')
    intruder_detected = data.get('intruder_detected', False)

    # Start the simulation thread if it's not running
    if sim_thread is None or not sim_thread.is_alive():
        sim_thread = threading.Thread(target=run_simulation)
        sim_thread.start()

    # Queue incoming data for processing by the simulation
    message_queue.put((camera_id, intruder_detected))

    # Count detected intruders
    intruders_detected = sum(drone.intruders for drone in sim.drone) if sim else 0

    return jsonify({
        "status": "success",
        "message": f"Processed data for camera {camera_id}",
        "intruders_detected": intruders_detected
    })
