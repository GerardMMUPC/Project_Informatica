from navPoint import NavPoint
from navSegment import NavSegment

def test_navsegment():
    p1 = NavPoint(6063, "IZA.D", 38.8731546833, 1.37242975)
    p2 = NavPoint(6937, "LAMPA", 38.8016666667, 1.9241666667)
    seg = NavSegment(p1, p2, 48.55701)

    print(f"Segmento desde {seg.origin} a {seg.destination} con distancia {seg.distance} km")

if __name__ == "__main__":
    test_navsegment()
