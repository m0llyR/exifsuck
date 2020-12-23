import json

samp_feature_geojson = """
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
} """

# empty_feature_geojson = {"type": "Feature", "geometry": {"type": "Point", "coordinates": []}, "properties": {"numi": 0}}

def new_geojson():
    str_empty_point_fc = """{
                            "type": "FeatureCollection",
                            "features": [
                            { "type": "Feature", "properties": null, "geometry": {"type":"Point","coordinates":[]} }
                            ]
                            }"""
    str_empty_fc = '{"type": "FeatureCollection","features": []}'
    return json.loads(str_empty_fc)


def _validate_or_make_feature(dic_fc, num_img):
    """ Validate that feature number 'num_f' exist in feature collection
    if not, then make it """
    # bol_found_numf = False
    num_il = -999  # number in list initialise
    if isinstance(dic_fc, dict):
        if isinstance(num_img, int):
            print(f" = dic_fc: {dic_fc}")
            if "type" in dic_fc.keys() and dic_fc["type"] == "FeatureCollection":
                if "features" in dic_fc.keys() and isinstance(dic_fc["features"], list):
                    num_feat = -1
                    for fet in dic_fc["features"]:
                        num_feat += 1
                        if isinstance(fet, dict):
                            if fet["type"] == "Feature":
                                if "properties" in fet.keys():
                                    if dic_fc["features"][num_feat]["properties"]["numi"] == num_img:
                                        num_il = num_feat
                                        break
                                else:
                                    print(f"ERR: in _val_or_make...() dic_fc feature has no properties key")
                                    return dic_fc
                            else:
                                print(f"ERR: in _val_or_make...() dic_fc has element of not-Feature type: {fet['type']}")
                                return dic_fc
                        else:
                            print(f"ERR: in _val_or_make...() dic_fc feature is not dict: {str(type(fet))}")
                            return dic_fc
                else:
                    print(f"ERR: in _val_or_make...() dic_fc has no key: features of type list")
                    return dic_fc
            else:
                print(f"ERR: in _val_or_make...() dic_fc has no key: type == FeatureCollection")
                return dic_fc
        else:
            print(f"ERR: in _val_or_make...() received non-int as num_f")
            return dic_fc
    else:
        print(f"ERR: in _val_or_make...() received non-dict as dict_fc")
        return dic_fc
    if num_il < 0:
        new_feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": []}, "properties": {"numi": 0}}
        new_feature["properties"]["numi"] = num_img
        dic_fc["features"].append(new_feature)
        num_il = len(dic_fc["features"]) - 1
    return dic_fc, num_il


def _add_att(tup_tag, dic_fc, num_img):
    dic_fc, num_il = _validate_or_make_feature(dic_fc, num_img)
    bol_added = False
    for fet in dic_fc["features"]:
        if "properties" in fet.keys():
            if isinstance(fet["properties"], dict):

                dic_fc["features"][num_il]["properties"][tup_tag[0]] = tup_tag[1]
                bol_added = True
        else:
            print(f"ERR: in _add_att(), feature has no properties: {fet}")
    return dic_fc


def _add_geo():
    pass


def add_tag(tup_tag, dic_fc, num_f):
    """ Adds a TAG (key, val) to feature number 'num_f', in  a geojson (dic) feature collection
    returns the updated geojson (dic) feature collection. """
    if isinstance(tup_tag, tuple) and len(tup_tag) == 2:
        if isinstance(dic_fc, dict):
            if isinstance(num_f, int):
                if tup_tag[0].lower() == "make":
                    pass
                elif tup_tag[0].lower() == "model":
                    pass
                elif tup_tag[0].lower().startswith("datetime"):
                    dic_fc = _add_att(tup_tag, dic_fc, num_f)
                elif tup_tag[0].lower().startswith("gps"):
                    print(" at : GPS")
            else:
                print(f"ERR: add_tag() received non-int as num_f")
        else:
            print(f"ERR: add_tag() received non-dict as dic_fc")
    else:
        print(f"ERR: add_tag() received non-tuple as tup_tag")
    return dic_fc