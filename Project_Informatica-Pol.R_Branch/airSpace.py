from navPoint import NavPoint
from navSegment import NavSegment
from navAirpoint import NavAirport

import math

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []

    def load_from_files(self, Cat_nav, Cat_seg, Cat_aer): #Populate lists
        id_to_navpoint = {} #Create empty dictionary

        #To load navigation file:
        with open(Cat_nav,"r") as file:
            for line in file:
                elements = line.strip().split()
                if len(elements) != 4:
                    print(f"Invalid line: {line.strip()}")
                    continue

                try: #We use try/except to check variable types
                    number = int(elements[0])
                    name = elements[1]
                    lat = float(elements[2])
                    lon = float(elements[3])

                    navpoint = NavPoint(number, name, lat, lon) #Use class
                    self.navpoints.append(navpoint)
                    id_to_navpoint[number] = navpoint #Save in dictionary
                except ValueError as ve:
                    print(f"Bad data: {line.strip()} - {ve}")

        #To load segment file:
        with open(Cat_seg, "r") as file:
            for line in file:
                elements = line.strip().split()
                if len(elements) != 3:
                    print(f"Invalid line: {line.strip()}")
                    continue
                try:
                    origin = int(elements[0])
                    destination = int(elements[1])
                    distance = float(elements[2])

                    if origin in id_to_navpoint and destination in id_to_navpoint: #If nodes exist
                        segment = NavSegment(origin, destination, distance)
                        self.navsegments.append(segment)
                    else:
                        print(f"Navpoint ID not recognised: {origin}, {destination}")
                except ValueError as ve:
                    print(f"Bad data: {line.strip()} - {ve}")

        #To load airports files:
        with open(Cat_aer, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        i = 0
        while i < len(lines):
            name = lines[i]
            i += 1
            SIDs = []
            STARs = []

            while i < len(lines) and lines[i].endswith(".D"): #SIDs case
                SID_name = lines[i]
                #We find navpoint match with SID
                sid = next((p for p in self.navpoints if p.name == SID_name), None)
                if sid:
                    SIDs.append(sid)
                else:
                    print(f"[AIRPORT WARNING] SID '{SID_name}' not found")
                i += 1

            while i < len(lines) and lines[i].endswith(".A"): #STARs case
                star_name = lines[i]
                # We find navpoint match with STAR
                star = next((p for p in self.navpoints if p.name == star_name), None)
                if star:
                    STARs.append(star)
                else:
                    print(f"[AIRPORT WARNING] STAR '{star_name}' not found")
                i += 1

            airport = NavAirport(name, SIDs, STARs)
            self.navairports.append(airport)

        for segment in self.navsegments:
            origin = id_to_navpoint.get(segment.origin)
            destination = id_to_navpoint.get(segment.destination)
            if origin and destination:
                origin.neighbors.append(destination)

    def neighbour_of(self, start_name):
        start = None #Find starting navpoint
        for p in self.navpoints:
            if p.name == start_name:
                start = p
                break

        if start is None:
            print("Start point not found.")
            return []

        visited = [] #Avoids reapeting navpoints
        queue = [] #Not yet visited navpoints

        visited.append(start)
        queue.append(start)

        while len(queue) > 0:
            current = queue.pop(0)

            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)

        return visited

    def find_shortest_path(self, origin_name, destination_name):
        origin = None
        destination = None

        for p in self.navpoints:
            if p.name == origin_name:
                origin = p
            if p.name == destination_name:
                destination = p

        if origin is None or destination is None:
            print("Origin or destination not found.")
            return None

        paths = [[origin]]
        costs = {}
        costs[origin] = 0

        while len(paths) > 0:
            #Find path with lowest cost
            best_path = None
            best_score = float('inf')

            for path in paths:
                last_point = path[-1]
                cost_so_far = costs[last_point]
                estimate = math.hypot(destination.longitude - last_point.longitude, destination.latitude - last_point.latitude)
                total_cost = cost_so_far + estimate

                if total_cost < best_score:
                    best_score = total_cost
                    best_path = path

            paths.remove(best_path)
            current = best_path[-1]

            if current == destination:
                return best_path

            for neighbor in current.neighbors:
                if neighbor in best_path:
                    continue  # Skip if already visited in this path

                new_cost = costs[current] + math.hypot(neighbor.longitude - current.longitude, neighbor.latitude - current.latitude)

                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    new_path = best_path + [neighbor]
                    paths.append(new_path)

        # If no path was found
        return None
