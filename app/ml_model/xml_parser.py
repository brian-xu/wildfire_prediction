import xml.etree.ElementTree as ET
from collections import defaultdict


def layer_values(row) -> [str, str]:
    """
    Extracts the attribute name and value from LANDFIRE XML documentation generated by GDAL.
    """
    layer_name = row[3].text
    layer_value = row[0].text
    if '-' in layer_name:
        layer_name = layer_name[:layer_name.index('-')].strip()
    if '>=' in layer_name:
        layer_name = layer_name[:layer_name.index('>=')].strip()
    return layer_name, layer_value


def parse_layers(xml_path: str) -> {str: [int, ]}:
    """
    Creates a dictionary that groups LANDFIRE data into groups based on their IDs.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    layers = defaultdict(list)
    for band in root:
        for table in band:
            for row in table:
                if row.tag == 'Row':
                    layer_name, layer_value = layer_values(row)
                    layers[layer_name].append(int(layer_value))
    return dict(layers)