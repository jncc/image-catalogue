import os
import subprocess
import multiprocessing
import time

def subprocess_cmd(args):
    """Execute sub-processing commands to the command line tool ExifTool.
    This enables the action to be called from the config file and executed by the command line via python.
    This function uses Popen to simultaneously execute multiple executions and passes the outputs into subsequent
    sub-processes through a pipe"""
    print(f'Working on image: {args[-1]}')
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    print(f'Response: {proc.stdout}')
    return([args[-1],proc.stdout])

exiftoolloc = r"W:\ImageCatalogue_prep\Admin\image-catalogue-master\exiftool\exiftool.exe"

if __name__ == '__main__':
    rootpath = input("Paste parent folder of images here: ")
    p = multiprocessing.Pool(4)
    processArgs = []
    
    for root, dirs, files in os.walk(rootpath):
        for f in files:
            if '.jpg' in f.lower():
                filepath = os.path.join(root, f)
                processArgs.append([exiftoolloc, '-exif:all= -tagsfromfile @ -exif:all -thumbnailimage -unsafe', filepath])
    p.map(subprocess_cmd, processArgs)
