import os
import shutil

file = r'H:\Columbus\unzip'
dfile = r"H:\Columbus\tif\2013"

def copyalltiflist(orginfpath,destinationpath,year):

    for root, dirs, files in os.walk(orginfpath):
        for file in files:
            if year in root:
                if file.endswith(".tif"):
                    orginfile=os.path.join(root,file)
                    destinfile=os.path.join(destinationpath,file)
                    if year in orginfile:
                        shutil.copyfile(orginfile,destinfile)
                        print(orginfile)

if __name__=="__main__":
    copyalltiflist(file, dfile, "\\2013\\")



