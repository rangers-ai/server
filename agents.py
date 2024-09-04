import agentpy as ap
from owlready2 import *
import random


class Guard(ap.Agent):
    def setup(self):
        self.agentType = 1

    def info_receptor(self, message):
        print(f"Guard received message: {message}")

    def next(self):
        pass

    def step(self):
        self.next()


class Drone(ap.Agent):
    def setup(self):
        self.intruders = []
        self.agentType = 0
        self.actions = {0: self.detect_intruder, 1: self.talk_to_guard}

    def detect_intruder(self):
        print("Detect intruder")
        self.intruders.append(1)

    def next(self):
        action = random.randint(0, 1)
        self.actions[action]()

    def step(self):
        self.next()

    def talk_to_guard(self):
        random.choice(self.model.guard).info_receptor("Intruder detected!")


class SimulationModel(ap.Model):
    def setup(self):
        print("Running simulation!!!")
        self.drone = ap.AgentList(self, 1, Drone)
        self.guard = ap.AgentList(self, 1, Guard)

    def update(self):
        pass

    def step(self):
        self.drone.step()
        self.guard.step()

    def end(self):
        pass
        # print(f"There were {sum(self.drone.intruders)} detected. \n")


if __name__ == "__main__":
    parameters = {
        "steps": 300,
    }
    sim = SimulationModel(parameters)
    sim.run()
