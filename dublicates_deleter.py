import os
import sys
from os import listdir, makedirs
from os.path import isfile, join
import hashlib
from typing import Counter
from PIL import Image
from send2trash import send2trash

directory = ""
def main():
    # delete (send to trach) dublicates inside every subfolder of the current directory the .py file placed in 
    # then delete the dublicates over subfolders:
    directory = os.getcwd()
    subs = []

    print('current directory:',directory)
    print("Started deleting (sending to trach) inside subfolders..")

    for folderfile in os.listdir(directory):
        if not folderfile.endswith(".py"):
            print(os.fsdecode(folderfile),":")
            subs.append(os.fsdecode(folderfile))
            folder = getAllImageHashes(folderfile)
            printDifferences(folder, None)

    print("Started deleting (sending to trach) over subfolders....")

    for index in range(len(subs)):
        print(os.fsdecode(subs[index]),":")
        for sub_fold in (subs[index+1:]):
            print(os.fsdecode(subs[index]),'-',os.fsdecode(sub_fold),":")
            firstFolder = getAllImageHashes(subs[index])
            secondFolder = getAllImageHashes(sub_fold)
            printDifferences(firstFolder, secondFolder)

    print("Done. All dublicates sent to trach.")


def printDifferences(folder1, folder2):
    matchFound = False
    matchCount = 0
    del_count = 0
    # Only dissalow matching filenames if in the same directory
    if folder2 == None:
        for f1 in folder1:
            for f2 in folder1:
                if f1[1] == f2[1] and f1[0] != f2[0]:
                    try:
                        matchCount += 1
                        matchFound = True
                        # print("{ Match found: ")
                        # print("\t" + f1[0])
                        # print("\t" + f2[0])
                        # print("}")
                        
                        #delete dublicated file:

                        #os.remove(os.path.join(os.getcwd(),f2[0]))
                        send2trash(os.path.join(directory,f2[0]))
                        del_count +=1
                    except:
                        continue
        print('found and deleted ', str(int(del_count/2)),' matches.')
    else:
        for f1 in folder1:
            for f2 in folder2:
                if f1[1] == f2[1]:
                    matchCount += 1
                    matchFound = True
                    processMatchedImages(f1, f2)
                    del_count +=1
        print('found and deleted ', str(del_count),' matches.')
    if not matchFound:
        print("No matches found!")


def processMatchedImages(img1, img2):
    # print("{ Match #" + str(matchCount) + " found: ")
    # print("  " + img1[0])
    # print("  " + img2[0])
    # print("}")

    #delete dublicated file:
    #os.remove(os.path.join(os.getcwd(),f2[0]))
    send2trash(os.path.join(directory,img2[0]))

def getOnlyFilename(fullpath):
    return fullpath.split("\\")[-1]

def getAllImageHashes(folder):
    onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and not f.endswith(".ini") and not f.endswith(".db")]
    hashedFiles = []
    fileLength = len(onlyfiles)
    for f in onlyfiles:
        hashedFiles.append((f, dhash(Image.open(f))))
    #print("Hashed all files from folder: "+ folder)
    return hashedFiles

def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

if __name__ == '__main__':
    main()
