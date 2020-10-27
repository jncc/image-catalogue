import os
import subprocess

import time


exiftoolloc = r"W:\ImageCatalogue_prep\Admin\image-catalogue-master\exiftool\exiftool.exe"

if __name__ == '__main__':
    rootpath = input("Paste parent folder of images here: ")

    for root, dirs, files in os.walk(rootpath):
        for f in files:
            if '.jpg' in f.lower():
                filepath = os.path.join(root, f)
                print("Correcting file {}".format(f))
                subprocess.Popen([exiftoolloc, '-exif:all= -tagsfromfile @ -exif:all -thumbnailimage -unsafe', filepath], shell=True)
                time.sleep(5)
