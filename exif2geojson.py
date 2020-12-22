import json

def new_geojson():
    str_empty_point_fc = """{
                            "type": "FeatureCollection",
                            "features": [
                            { "type": "Feature", "properties": null, "geometry": {"type":"Point","coordinates":[]} }
                            ]
                            }"""
    str_empty_fc = '{"type": "FeatureCollection","features": []}'
    return json.loads(str_empty_fc)
