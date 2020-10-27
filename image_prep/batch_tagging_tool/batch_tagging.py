########################################################################################################################

# Title: Image Catalogue Exif Data Writing

# Authors: Matear, L., Duncan, G. (2018)                                                  Email:
# Version Control: 1.0

# Script description:


########################################################################################################################

# Section 1:                   Loading, manipulating and formatting the data within Python

########################################################################################################################


#   1a) Load in all required packages for script:
#       If required install packages using 'pip install package name command in terminal

import os
import pandas as pd
import subprocess
from PIL import Image
import datetime
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path, PurePath
import shutil

print("Loaded modules")

def subprocess_cmd(command):
    """Execute sub-processing commands to the command line tool ExifTool.
    This enables the action to be called from the config file and executed by the command line via python.
    This function uses Popen to simultaneously execute multiple executions and passes the outputs into subsequent
    sub-processes through a pipe"""
    print(command)
    process = subprocess.call(command, stdout=subprocess.PIPE, shell=True, encoding="utf8")

def rewritePath(fp, wd):
    imageName = os.path.basename(fp)
    outputPath = os.path.join(wd, imageName)
    return outputPath

if __name__ == '__main__':
    ########################################################################################################################

    #   1b) Setting a working directory for file access - this must be set to the final file path destination for the output
    #       log files. Please not that this should also be where the image proforma file is saved.

    #root = tk.Tk()
    #root.withdraw()
    print("In main loop")
    #wd = filedialog.askdirectory(title = "Select output directory")
    wd = input("Paste output directory here")
    os.chdir(wd)
    print(f"Changed working directory to: {wd}")

    exiftoolPath = str(Path(__file__).parents[2] / 'exiftool' / 'exiftool.exe')

    #       Read in metadata from .xlsx format files as Pandas (pd) DataFrames

    #proformaLoc = filedialog.askopenfilename(title = "Select image proforma metadata spreadsheet for survey in question")
    proformaLoc = input("Paste location of image proforma metadata spreadsheet here:")
    imageProforma = pd.read_excel(proformaLoc, 'Image_Proforma')
    
    #copyfiles = messagebox.askyesno("Copy files or edit insitu","Would you like to make copies of the input image files?\r\n(Select 'No' only if you're sure you're already working on copies)")
    #        Double check!!
    #if not copyfiles:
    #    copyfiles = not messagebox.askyesno("Copy files or edit insitu","Are you sure you want to work directly on the files defined in the spreadsheet?")

    copyFilesResponse = input("Do you want to [copy] files or work on [originals]?")
    if copyFilesResponse.lower() == "originals":
        copyfiles = False
    else:
        copyfiles = True

    #       Set preliminary ExifTool args

    #initialExifToolArgs = [r'Z:\Marine\Evidence\BenthicDataMgmt\Image catalogue\batch_tagging_tool\exiftool\exiftool.exe']
    initialExifToolArgs = [exiftoolPath]
    #   1c) Load in proforma template and set up arguments for static terms.

    templateLoc = str(Path(__file__).parents[2] / 'reference_templates' / 'image_proforma_template.xlsx')
    staticFieldTable = pd.read_excel(templateLoc, 'Additional_auto_terms')
    for index, row in staticFieldTable.iterrows():
        arg = '-' + row['Field'] + '=' + str(row['Value'])
        initialExifToolArgs.append(arg)

    if copyfiles:
        #   1c) If user has selected to copy files (the default), create new column in pd dataframe to store new filepath
        # TODO - identify common root of all images, and create output folders as necessary.
        #commonRoot = os.path.commonpath([imageProforma['FilePath']])

        imageProforma['NewPath'] = imageProforma['FilePath'].apply(lambda fp: rewritePath(fp, wd))

        #   1d) Copy across files to new directory
        print("Copying files across!")
        for index, row in imageProforma.iterrows():
            oldPath = row['FilePath']
            print(f'    copying {oldPath}')
            shutil.copy2(oldPath, row['NewPath'])
    
    else:
        #   1x) If user has selected to not copy files, set NewPath as FilePath to continue as normal
        print("User selected to not copy files, working on originals files defined in spreadsheet")
        imageProforma['NewPath'] = imageProforma['FilePath']
        

    #   2) Identify list features within image proforma, change data type, and remove identifier flag from column name

    for eachVal in imageProforma.columns.values:
        if '|list' in eachVal:
            print('Converting list column: {}'.format(eachVal))
            imageProforma[eachVal] = imageProforma[eachVal].str.split('|')
            imageProforma.rename(columns={eachVal: eachVal.replace('|list', '')}, inplace=True)

    #   2a) Loop through each value in each row
    time = datetime.datetime.now()
    with open('{}_error_log.csv'.format(time.strftime('%Y%m%d%H%M')), 'w', newline='') as errorLog:
        logWriter = csv.writer(errorLog, delimiter=",")
        logWriter.writerow(["NewPath", "Error"])
        for index, row in imageProforma.iterrows():
            filePath = row['NewPath']
            try:
                im = Image.open(filePath)
                fileExifToolArgs = list(initialExifToolArgs)
                for colName in [x for x in row.index if x != 'NewPath' and x != 'FilePath']:
                    cellVal = row[colName]
                    if type(cellVal) == list:
                        for x in cellVal:
                            if not pd.isnull(x):
                                argStr = '-{}+={}'.format(colName, x)
                                fileExifToolArgs.append(argStr)
                    else:
                        if not pd.isnull(cellVal):
                            argStr = '-{}={}'.format(colName, cellVal)
                            fileExifToolArgs.append(argStr)
                fileExifToolArgs.append(filePath)

                ## running subprocess.call instead rather than contained function to wait for each exiftool call individually and stop runaway processes opening!
                #subprocess_cmd(fileExifToolArgs)
                print(fileExifToolArgs)
                subprocess.Popen(fileExifToolArgs, encoding="utf8")
                time.sleep(5)
                # print(fileExifToolArgs)
            except Exception as e:
                print(str(e) + '{}'.format(filePath))
                logWriter.writerow([filePath, str(e)])