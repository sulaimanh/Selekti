from imutils import paths
import shutil
import os

# This is the path to the harddrive
p1 = os.path.sep.join(["/Volumes","BirdPics2", "pictures-processed"])
dirs1 = os.listdir(p1)

p2 = os.path.sep.join(["/Volumes","BirdPics2", "pictures-selected"])
dirs2 = os.listdir(p2)

finList = list(set(dirs1).intersection(dirs2))

path1 = "output/finPath/1"
path0 = "output/finPath/0"

if os.path.exists(path1):
    print("Exists")
else:
    os.mkdir("output/finPath")
    os.mkdir(path1)
    os.mkdir(path0)

total0 = 0
total1 = 0
for file in finList:
    # 0 rating
    filePath1 = p1 + "/" + file
    imagePaths1 = list(paths.list_images(filePath1))
    
    # 1 rating
    filePath2 = p2 + "/" + file
    imagePaths2 = list(paths.list_images(filePath2))
    rated1 = []
    for image in imagePaths2:
        imageName = image[37:]
        rated1.append(imageName)
        shutil.copy(image, path1)
    total1 = total1 + len(rated1)
    for image in imagePaths1:
        imageName = image[38:]
        if imageName in rated1:
            print("Exists")
        else:
            total0 = total0 + 1
            shutil.copy(image, path0)
    rated1.clear()

print(total1)
print(total0)