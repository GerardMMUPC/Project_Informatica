from airSpace import AirSpace

def test_airspace_loading():
    airspace = AirSpace()
    airspace.cargar_de_ficheros("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

    print(f"Loaded {len(airspace.navpoints)} NavPoints")
    print(f"Loaded {len(airspace.navsegments)} NavSegments")
    print(f"Loaded {len(airspace.navairports)} NavAirports")

    # Muestra un aeropuerto especifico
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
        print("LEIB encontrado")

    # Comprovamos un punto especifico
    godox = next((p for p in airspace.navpoints if p.name == "GODOX"), None)
    if godox:
        print(f"\nGODOX encontrado en: ({godox.latitude}, {godox.longitude})")
    else:
        print("GODOX no encontrado")

if __name__ == "__main__":
    test_airspace_loading()
