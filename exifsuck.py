
import os

from PIL import Image, ExifTags

import exif2geojson

PATH = r"data/"
EXT = ".jpg"

dic_fc = exif2geojson.new_geojson()

for path, subdir, files in os.walk(PATH):
    for file in files:
        if file.lower().endswith(EXT):
            ffn = os.path.join(path, file)
            img = Image.open(ffn)
            img_exif = img.getexif()
            if img_exif is None:
                print(f"{ffn}\tSorry, image has no exif data.")
            else:
                img_exif_dict = dict(img_exif)
                for key, val in img_exif_dict.items():
                    if key in ExifTags.TAGS:
                        print(f"{ffn}   {ExifTags.TAGS[key]}:{repr(val)}")
                    else:
                        print(f"{ffn} % {ExifTags.TAGS[key]}:{repr(val)}")

print(f"fc: {str(type(dic_fc))}: {dic_fc}")