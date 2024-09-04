import agentpy as ap
from owlready2 import *
import random
from flask import jsonify


class Guard(ap.Agent):
    def setup(self):
        self.agentType = 1
        self.alert_checks = 0
        self.actions = {}
        self.rules = {}
        self.alarmCount_begin = 0
        self.droneOverride = False
        self.alarmCount_end = 0
        self.callTheCops = False

    def info_receptor(self, message):
        print(f"Guard received message: {message}")

    def control_drone(self):
        print("Drone, go to the location!")
        self.model.drone[0].info_receptor("Go to the location!")

    def next(self):
        for action in self.actions:
            for rule in self.rules:
                if rule(action):
                    action()

    def step(self):
        self.next()

    def give_info(self):
        return jsonify(
            {
                "countAlarm_begin": self.alarmCount_begin,
                "countAlarm_end": self.alarmCount_end,
                "droneOverride": self.droneOverride,
                "callTheCops": self.callTheCops,
            }
        )


class Camera(ap.Agent):
    def setup(self):
        self.agentType = 2
        self.alert_checks = 0
        self.rules = {}
        self.actions = {}
        self.id = None
        self.detection = None
        self.locked = False

    def detect_intruder(self):
        print("Detect intruder")
        self.intruders.append(1)

    def next(self):
        for action in self.actions:
            for rule in self.rules:
                if rule(action):
                    action()

    def step(self):
        self.next()

    def give_info(self):
        return jsonify(
            {"id": self.id, "detection": self.detection, "locked": self.locked}
        )


class Drone(ap.Agent):
    def setup(self):
        self.intruders = []
        self.agentType = 3
        self.actions = {0: self.detect_intruder, 1: self.talk_to_guard}
        self.rules = {}
        self.detection = None
        self.pos = []
        self.panoramic = False

    def rule_alert(self, action):
        pass

    def detect_intruder(self):
        print("Detect intruder")
        self.intruders.append(1)

    def next(self):
        for action in self.actions:
            for rule in self.rules:
                if rule(action):
                    action()

    def step(self):
        self.next()

    def talk_to_guard(self):
        random.choice(self.model.guard).info_receptor("Intruder detected!")

    def give_info(self):
        return jsonify(
            {"detection": self.detection, "pos": self.pos, "panoramic": self.panoramic}
        )
