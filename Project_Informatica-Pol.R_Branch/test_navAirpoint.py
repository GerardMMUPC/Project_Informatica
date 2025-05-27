from navPoint import NavPoint
from navAirpoint import NavAirport

def test_navairport():
    sid1 = NavPoint(6063, "IZA.D", 38.8731546833, 1.37242975)
    star1 = NavPoint(6062, "IZA.A", 38.8772804833, 1.36930455)

    airport = NavAirport("LEIB", [sid1], [star1])

    print(f"Airport: {airport.name}")
    print("SIDs:")
    for p in airport.SIDs:
        print(f" - {p.name} at ({p.latitude}, {p.longitude})")

    print("STARs:")
    for p in airport.STARs:
        print(f" - {p.name} at ({p.latitude}, {p.longitude})")

if __name__ == "__main__":
    test_navairport()
