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
            # print(f" = dic_fc: {dic_fc}")
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
        new_feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}, "properties": {"numi": 0}}
        new_feature["properties"]["numi"] = num_img
        dic_fc["features"].append(new_feature)
        num_il = len(dic_fc["features"]) - 1
    return dic_fc, num_il


def _add_att(tup_tag, dic_fc, num_img):
    dic_fc, num_il = _validate_or_make_feature(dic_fc, num_img)
    ## bol_added = False
    for fet in dic_fc["features"]:
        if "properties" in fet.keys():
            if isinstance(fet["properties"], dict):
                dic_fc["features"][num_il]["properties"][tup_tag[0]] = tup_tag[1]
                ## bol_added = True
        else:
            print(f"ERR: in _add_att(), feature has no properties: {fet}")
    return dic_fc


def make_ne_dd(tup_geo):
    tup_ret = (90.0, -180.0)
    # print(f" - geo raw: {str(type(tup_geo))} {tup_geo}")
    if isinstance(tup_geo, tuple) and len(tup_geo) == 2:  # This is what we expect to receive
        if tup_geo[0] == 'GPSInfo':
            # print(f" - GPSInfo: {str(type(tup_geo[1]))} {tup_geo[1]}")
            dic_geo = tup_geo[1]
            if isinstance(dic_geo, dict) and all(val in dic_geo.keys() for val in [1, 2, 3, 4]):
                if dic_geo[1].upper() in ['N', 'S'] and dic_geo[3].upper() in ['E', 'W']:
                    if all((isinstance(dic_geo[key], tuple) and len(dic_geo[key]) == 3) for key in [2, 4]):
                        try:
                            latd, latm, lats = float(dic_geo[2][0]), float(dic_geo[2][1]), float(dic_geo[2][2])
                        except ValueError:
                            print(f"ERR: Latitude values are not floats: {dic_geo}")
                            return tup_ret
                        try:
                            lond, lonm, lons = float(dic_geo[4][0]), float(dic_geo[4][1]), float(dic_geo[4][2])
                        except ValueError:
                            print(f"ERR: Latitude values are not floats: {dic_geo}")
                            return tup_ret
                        num_dd_lat = latd + latm/60.0 + lats/3600.0
                        if dic_geo[1].upper() == 'S':  # South counts negative
                            num_dd_lat *= -1
                        num_dd_lon = lond + lonm/60.0 + lons/3600.0
                        if dic_geo[3].upper() == 'W':  # West counts negative
                            num_dd_lon *= -1
                        tup_ret = num_dd_lat, num_dd_lon
                    else:
                        print(f"ERR: Not as expected tuples of 3 DMS values: {dic_geo}")
                else:
                    print(f"ERR: Not as expected N, S, E or W tags: {dic_geo}")
            else:
                print(f"Warning: Insufficient geo info: {dic_geo}")
        else:
            print(f"ERR: in make_ne_dd() received unknown key: {tup_geo[0]}")
    return tup_ret


def _add_geo(tup_geo, dic_fc, num_img):
    dic_fc, num_il = _validate_or_make_feature(dic_fc, num_img)
    tup_ne_dd = make_ne_dd(tup_geo)
    for fet in dic_fc["features"]:
        if "geometry" in fet.keys():
            if isinstance(fet["geometry"], dict):
                if all(tok in fet["geometry"].keys() for tok in ["type", "coordinates"]):
                    if fet["geometry"]["type"].lower() == "point":
                        dic_fc["features"][num_il]["geometry"]["coordinates"] = tup_ne_dd[1], tup_ne_dd[0]
                    else:
                        print(f"ERR: in _add_geo(), geometry is not type 'point'")
                else:
                    print(f"ERR: in _add_geo(), geometry lacks type or coordinates")
        else:
            print(f"ERR: in _add_geo(), feature has no geometry: {fet}")
    return dic_fc


def add_tag(tup_tag, dic_fc, num_f):
    """ Adds a TAG (key, val) to feature number 'num_f', in  a geojson (dic) feature collection
    returns the updated geojson (dic) feature collection. """
    if isinstance(tup_tag, tuple) and len(tup_tag) == 2:
        if isinstance(dic_fc, dict):
            if isinstance(num_f, int):
                if tup_tag[0].lower() == "make" \
                        or tup_tag[0].lower() == "model":
                    dic_fc = _add_att(tup_tag, dic_fc, num_f)
                elif tup_tag[0].lower() == "filename":
                    val = tup_tag[1].replace("\\", "/")  # Smooth the path
                    tup_tag = (tup_tag[0], val)
                    dic_fc = _add_att(tup_tag, dic_fc, num_f)
                elif tup_tag[0].lower().startswith("datetime"):
                    dic_fc = _add_att(tup_tag, dic_fc, num_f)
                elif tup_tag[0].lower().startswith("gps"):
                    dic_fc = _add_geo(tup_tag, dic_fc, num_f)
                else:
                    print(f"Warning: unknown tag name NOT added: {tup_tag[0]}")
            else:
                print(f"ERR: add_tag() received non-int as num_f")
        else:
            print(f"ERR: add_tag() received non-dict as dic_fc")
    else:
        print(f"ERR: add_tag() received non-tuple as tup_tag")
    return dic_fc


def write_2_json_file(dic_fc, str_ffn):
    with open(str_ffn, 'w') as fp:
        json.dump(dic_fc, fp, indent=2)