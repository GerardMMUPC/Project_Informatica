from airSpace import AirSpace

def test_airspace_loading():
    airspace = AirSpace()
    airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

    print(f"Loaded {len(airspace.navpoints)} NavPoints")
    print(f"Loaded {len(airspace.navsegments)} NavSegments")
    print(f"Loaded {len(airspace.navairports)} NavAirports")

    # Display a specific airport
    airport = next((a for a in airspace.navairports if a.name == "LEIB"), None)
    if airport:
        print(f"\nAirport: {airport.name}")
        print("SIDs:")
        for sid in airport.SIDs:
            print(f"  {sid.name}")
        print("STARs:")
        for star in airport.STARs:
            print(f"  {star.name}")
    else:
        print("LEIB not found")

    # Check specific navpoint
    godox = next((p for p in airspace.navpoints if p.name == "GODOX"), None)
    if godox:
        print(f"\nGODOX found at ({godox.latitude}, {godox.longitude})")
    else:
        print("GODOX not found")

if __name__ == "__main__":
    test_airspace_loading()
