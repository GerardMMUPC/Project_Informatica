from Node import *


class Segment:
    def __init__(self, name, origin, destination): # No fiquem cost pq no es un input
        self.name = str(name)
        self.origin = origin
        self.destination = destination
        self.cost = Distance(self.origin, self.destination) # No és cost de diners :)

    def __str__(self):
        return f"Segment {self.name}: {self.origin.name} to {self.destination.name}, Cost: {self.cost}"
