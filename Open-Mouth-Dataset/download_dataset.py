import os
from roboflow import Roboflow

KEY_API_ROBOFLOW = "<INSIRA AQUI>"

def baixar_dataset():
    rf = Roboflow(api_key=KEY_API_ROBOFLOW)
    project = rf.workspace("open-mouth").project("open-mouth")
    version = project.version(2)
    if not os.path.exists("./Open-Mouth-Dataset" ):
        os.makedirs("./Open-Mouth-Dataset" )

    dataset = version.download("yolov8", location="./Open-Mouth-Dataset" )

if __name__ == "__main__":
    baixar_dataset()

