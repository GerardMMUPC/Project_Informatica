def generate_point_kml(node, output_file="point.kml"):
    #Consigue las cordenadas, sea un punto o navpoint
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
    coordinates = []
    for node in nodes:
        lon = node.longitude if hasattr(node, 'longitude') else node.x
        lat = node.latitude if hasattr(node, 'latitude') else node.y
        coordinates.append(f"{lon},{lat},0")

    if not coordinates:
        raise ValueError("No hay coordenadas validas a exportar")

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