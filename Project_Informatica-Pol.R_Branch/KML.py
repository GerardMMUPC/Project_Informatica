import os


def generate_point_kml(node, output_file="point.kml"):
    """Generate KML for a single point"""
    # Get coordinates whether it's a Node or NavPoint
    lon = node.longitude if hasattr(node, 'longitude') else node.x
    lat = node.latitude if hasattr(node, 'latitude') else node.y

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>{node.name}</name>
    <Point>
      <coordinates>{lon},{lat},0</coordinates>
    </Point>
  </Placemark>
</kml>"""

    with open(output_file, 'w') as f:
        f.write(kml_content)


def generate_path_kml(nodes, output_file="path.kml"):
    """Generate KML for a path (sequence of nodes)"""
    coordinates = []
    for node in nodes:
        # Handle both Node (x,y) and NavPoint (longitude,latitude)
        lon = node.longitude if hasattr(node, 'longitude') else node.x
        lat = node.latitude if hasattr(node, 'latitude') else node.y
        coordinates.append(f"{lon},{lat},0")

    if not coordinates:
        raise ValueError("No valid coordinates found for KML export")

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>Flight Path</name>
    <LineString>
      <coordinates>{" ".join(coordinates)}</coordinates>
    </LineString>
  </Placemark>
</kml>"""

    with open(output_file, 'w') as f:
        f.write(kml_content)