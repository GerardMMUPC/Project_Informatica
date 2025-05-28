from navPoint import NavPoint

def test_navpoint():
    p1 = NavPoint(4954, "GIR", 41.9313888889, 2.7716666667)
    p2 = NavPoint(5129, "GODOX", 39.3725, 1.4108333333)

    print(f"NavPoint 1: {p1.name} at ({p1.latitude}, {p1.longitude})")
    print(f"NavPoint 2: {p2.name} at ({p2.latitude}, {p2.longitude})")

if __name__ == "__main__":
    test_navpoint()
