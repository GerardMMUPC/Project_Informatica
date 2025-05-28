def generar_punto_kml(node, output_file="point.kml"):
    lon = node.longitude if hasattr(node, 'longitude') else node.x #Comprobamos que tengan los atributos
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


def generar_camino_kml(nodes, output_file="path.kml"):
    coordinates = []
    for node in nodes:
        lon = node.longitude if hasattr(node, 'longitude') else node.x
        lat = node.latitude if hasattr(node, 'latitude') else node.y
        coordinates.append(f"{lon},{lat},0")

    if not coordinates:
        raise ValueError("No hay coordenadas validas para exportar a KML")

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