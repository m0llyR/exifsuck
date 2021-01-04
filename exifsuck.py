
import os

from PIL import Image, ExifTags
import PIL  # Strange but necessary ...

import exif2geojson

# ToDo: Various combinations of (0,0) or (90,-180) = Investigate...

PATH = r"data/"
# PATH = r"C:\\"
EXT = ".jpg"
TAGS = ["Make","Model","BodySerialNumber","DateTime","DateTimeOriginal","GPSInfo",]

dic_fc = exif2geojson.new_geojson()
num_img = 0  # Initialising image count

for path, subdir, files in os.walk(PATH):
    for file in files:
        if file.lower().endswith(EXT):
            if r"\AppData\Local\ESRI\Index\Thumbnail" in path:  # Ugly quick-fix
                continue
            num_img += 1
            ffn = os.path.join(path, file)
            print(f"Open: {num_img} : {ffn} -------------")
            try:
                img = PIL.Image.open(ffn)
            except PIL.UnidentifiedImageError:
                print("\tPIL.UnidentifiedImageError")
                continue
            img_exif = img.getexif()
            if img_exif is None:
                print(f"{ffn}\tSorry, image has no exif data.")
            else:
                img_exif_dict = dict(img_exif)
                if len(img_exif_dict) > 0:
                    # print(f"exif: {img_exif_dict}")
                    for key, val in img_exif_dict.items():
                        if key in PIL.ExifTags.TAGS:
                            pass  # print(f"{ffn}   {ExifTags.TAGS[key]}:{repr(val)}")
                            if PIL.ExifTags.TAGS[key] in TAGS or PIL.ExifTags.TAGS[key].upper().startswith("GPS"):
                                # print(f"{ffn}   {ExifTags.TAGS[key]}: {repr(val)}")  # Just for shows, move to log file XXX
                                # print(f"{ffn}   {ExifTags.TAGS[key]}: {str(type(val))} {repr(val)}")  # Just for shows, move to log file XXX
                                dic_fc = exif2geojson.add_tag((PIL.ExifTags.TAGS[key], val), dic_fc, num_img)
                            else:
                                pass  # print(f"key: {ExifTags.TAGS[key]} not in {TAGS}")
                        else:
                            pass  # print(f"{ffn} % {ExifTags.TAGS[key]}:{repr(val)}")
                else:
                    print(f"Warning: {ffn} EXIF is Empty ...")
            dic_fc = exif2geojson.add_tag(("filename", ffn), dic_fc, num_img)

str_ofn = exif2geojson.write_2_json_file(dic_fc, 'pics.json')
print(f"\nWritten info to outfile: {str_ofn}")