from navPoint import NavPoint
from navSegment import NavSegment
from navAirpoint import NavAirport

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





