from imutils import paths
import shutil
import os


p1 = os.path.sep.join(["/Volumes","BirdPics2", "pictures-processed"])
dirs1 = os.listdir(p1)

p2 = os.path.sep.join(["/","Volumes","BirdPics2", "pictures-selected"])
dirs2 = os.listdir(p2)

finList = list(set(dirs1).intersection(dirs2))
print(len(finList))

path1 = "output/finPath/1"
path0 = "output/finPath/0"

if os.path.exists(path1):
    print("Exists")
else:
    os.mkdir("output/finPath")
    os.mkdir(path1)
    os.mkdir(path0)

total = 0
for file in finList:
    if file in dirs1:
        filePath = p1 + "/" + file
        imagePaths = list(paths.list_images(filePath))
        total = total + len(imagePaths)
        for imagePath in imagePaths:
            shutil.copy(imagePath, path0)
    if file in dirs2:
        filePath = p2 + "/" + file
        imagePaths = list(paths.list_images(filePath))
        total = total + len(imagePaths)
        for imagePath in imagePaths:
            shutil.copy(imagePath, path1)
        
print(total)



