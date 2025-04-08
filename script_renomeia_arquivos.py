import os

folderPath = "C:/Users/Navarro/Desktop/Faculdade/6 sem/Inteligencia Artificial/projeto 1 bim/AI_Training_Images"
fileList = sorted(os.listdir(folderPath))
counter = 1
for fileName in fileList:
    fullPath = os.path.join(folderPath, fileName)
    if os.path.isfile(fullPath):
        extension = os.path.splitext(fileName)[1]
        newName = "face_{:02d}{}".format(counter, extension)
        newFullPath = os.path.join(folderPath, newName)
        os.rename(fullPath, newFullPath)
        counter += 1