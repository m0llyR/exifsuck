
import os

from PIL import Image, ExifTags

import exif2geojson

PATH = r"data/"
EXT = ".jpg"
TAGS = ["Make","Model","BodySerialNumber","DateTime","DateTimeOriginal","GPSInfo",]

dic_fc = exif2geojson.new_geojson()
num_img = 0  # Initialising image count

for path, subdir, files in os.walk(PATH):
    for file in files:
        if file.lower().endswith(EXT):
            num_img += 1
            ffn = os.path.join(path, file)
            print(f" ------ Open: {num_img} : {ffn} -------------")
            img = Image.open(ffn)
            img_exif = img.getexif()
            if img_exif is None:
                print(f"{ffn}\tSorry, image has no exif data.")
            else:
                img_exif_dict = dict(img_exif)
                for key, val in img_exif_dict.items():
                    if key in ExifTags.TAGS:
                        pass  # print(f"{ffn}   {ExifTags.TAGS[key]}:{repr(val)}")
                        if ExifTags.TAGS[key] in TAGS or ExifTags.TAGS[key].upper().startswith("GPS"):
                            print(f"{ffn}   {ExifTags.TAGS[key]}: {repr(val)}")  # Just for shows, move to log file XXX
                            # print(f"{ffn}   {ExifTags.TAGS[key]}: {str(type(val))} {repr(val)}")  # Just for shows, move to log file XXX
                            dic_fc = exif2geojson.add_tag((ExifTags.TAGS[key], val), dic_fc, num_img)
                        else:
                            pass  # print(f"key: {ExifTags.TAGS[key]} not in {TAGS}")
                    else:
                        pass  # print(f"{ffn} % {ExifTags.TAGS[key]}:{repr(val)}")
            dic_fc = exif2geojson.add_tag(("filename", ffn), dic_fc, num_img)

exif2geojson.write_2_json_file(dic_fc, 'pics.json')