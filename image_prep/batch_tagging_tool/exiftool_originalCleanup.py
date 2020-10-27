import os

if __name__ == '__main__':
    rootDir = input("Paste parent folder of images here: ")

    for root, dirs, files in os.walk(rootDir):
        for f in files:
            if f.endswith("_original"):
                os.remove(os.path.join(root,f))
    print("Fin!")
