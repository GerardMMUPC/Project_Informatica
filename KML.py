import os
from datetime import datetime

def generate_point_kml(node, output_file="point.kml", color="FF0000FF", name=None):
    """Generate KML for a single point with customizable color"""
    lon = node.longitude if hasattr(node, 'longitude') else node.x
    lat = node.latitude if hasattr(node, 'latitude') else node.y
    name = name if name else node.name

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>{name}</name>
    <Style>
      <IconStyle>
        <color>{color}</color>
        <scale>1.2</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
        </Icon>
      </IconStyle>
    </Style>
    <Point>
      <coordinates>{lon},{lat},0</coordinates>
    </Point>
  </Placemark>
</kml>"""

    with open(output_file, 'w') as f:
        f.write(kml_content)


def generate_path_kml(nodes, output_file="path.kml", name="Flight Path", color="FF0000FF", width=4,
                      altitude_mode="relativeToGround"):
    """Generate enhanced KML for a path with more customization options"""
    coordinates = []
    for node in nodes:
        lon = node.longitude if hasattr(node, 'longitude') else node.x
        lat = node.latitude if hasattr(node, 'latitude') else node.y
        alt = getattr(node, 'altitude', 0)  # Default altitude is 0 if not specified
        coordinates.append(f"{lon},{lat},{alt}")

    if not coordinates:
        raise ValueError("No valid coordinates found for KML export")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{name}</name>
    <description>Generated on {timestamp}</description>
    <Style id="pathStyle">
      <LineStyle>
        <color>{color}</color>
        <width>{width}</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>{name}</name>
      <styleUrl>#pathStyle</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>{altitude_mode}</altitudeMode>
        <coordinates>{" ".join(coordinates)}</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>"""

    with open(output_file, 'w') as f:
        f.write(kml_content)


def generate_complete_kml(graph, path_nodes=None, output_file="complete_map.kml"):
    """Generate a complete KML with all nodes, segments and highlighted path"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    kml_content = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<kml xmlns="http://www.opengis.net/kml/2.2">',
                   '<Document>',
                   f'<name>Flight Navigation Map - {timestamp}</name>']

    # Add styles
    kml_content.extend([
        '<Style id="normalNode">',
        '  <IconStyle>',
        '    <color>FF00FF00</color>',  # Green
        '    <scale>0.8</scale>',
        '    <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>',
        '  </IconStyle>',
        '</Style>',
        '<Style id="pathNode">',
        '  <IconStyle>',
        '    <color>FF0000FF</color>',  # Red
        '    <scale>1.2</scale>',
        '    <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>',
        '  </IconStyle>',
        '</Style>',
        '<Style id="normalSegment">',
        '  <LineStyle>',
        '    <color>7F00FFFF</color>',  # Light blue with transparency
        '    <width>2</width>',
        '  </LineStyle>',
        '</Style>',
        '<Style id="pathSegment">',
        '  <LineStyle>',
        '    <color>FF0000FF</color>',  # Red
        '    <width>4</width>',
        '  </LineStyle>',
        '</Style>'
    ])

    # Add all nodes
    for node in graph.nodes:
        lon = getattr(node, 'longitude', node.x)
        lat = getattr(node, 'latitude', node.y)
        style = "pathNode" if (path_nodes and node in path_nodes) else "normalNode"

        kml_content.extend([
            '<Placemark>',
            f'<name>{node.name}</name>',
            f'<styleUrl>#{style}</styleUrl>',
            '<Point>',
            f'<coordinates>{lon},{lat},0</coordinates>',
            '</Point>',
            '</Placemark>'
        ])

    # Add all segments
    for seg in graph.segments:
        lon1 = getattr(seg.origin, 'longitude', seg.origin.x)
        lat1 = getattr(seg.origin, 'latitude', seg.origin.y)
        lon2 = getattr(seg.destination, 'longitude', seg.destination.x)
        lat2 = getattr(seg.destination, 'latitude', seg.destination.y)

        # Check if this segment is part of the path
        is_path_segment = False
        if path_nodes:
            for i in range(len(path_nodes) - 1):
                if (seg.origin == path_nodes[i] and seg.destination == path_nodes[i + 1]) or \
                        (seg.destination == path_nodes[i] and seg.origin == path_nodes[i + 1]):
                    is_path_segment = True
                    break

        style = "pathSegment" if is_path_segment else "normalSegment"

        kml_content.extend([
            '<Placemark>',
            f'<name>{seg.origin.name} to {seg.destination.name}</name>',
            f'<styleUrl>#{style}</styleUrl>',
            '<LineString>',
            '<tessellate>1</tessellate>',
            '<coordinates>',
            f'{lon1},{lat1},0 {lon2},{lat2},0',
            '</coordinates>',
            '</LineString>',
            '</Placemark>'
        ])

    # Close document
    kml_content.extend(['</Document>', '</kml>'])

    with open(output_file, 'w') as f:
        f.write('\n'.join(kml_content))