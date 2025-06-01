from ultralytics import YOLO
import os
import torch

CAMINHO_DATA_YAML = "./Open-Mouth-Dataset/data.yaml"

# ajuste os parametros de acordo com seu hardware
EPOCAS = 50       # Numero de epocas pra treinamento (30, 50, 100)
TAMANHO_BATCH = 16   #(8, 4)
TAMANHO_IMG = 640    
PROCESSAMENTO = "0"   # O que usar pra processamento: "cpu", "0" (para GPU 0), "auto" (ultralytics decide)
VARIANTE_DO_MODELO = "yolov8n.pt" # Modelo Base: yolov8n.pt (nano), yolov8s.pt (small), etc.
NOME_TREINAMENTO = "yolov8_open_mouth_custom" 


def treinarModelo():
    modelo = YOLO(VARIANTE_DO_MODELO)

    melhorProcessamento = PROCESSAMENTO
    if PROCESSAMENTO == "auto":
        melhorProcessamento = "cuda" if torch.cuda.is_available() else "cpu"
    elif PROCESSAMENTO != "cpu":
        try:
            indexGpu = int(PROCESSAMENTO)
            if not torch.cuda.is_available() or indexGpu >= torch.cuda.device_count():
                print("Warning: GPU nao ta disponivel. Rodando na CPU.")
                melhorProcessamento = "cpu"
            else:
                melhorProcessamento = indexGpu
                print("Usando a GPU")
        except ValueError:
            print("Warning: Dispositivo invalido. Rodando na CPU.")
            melhorProcessamento = "cpu"
    else:
        print("Usando a CPU especisicada.")

    results = modelo.train(
        data=CAMINHO_DATA_YAML,
        epoca=EPOCAS,
        imgsz=TAMANHO_IMG,
        batch=TAMANHO_BATCH,
        proc=melhorProcessamento,
        nome=NOME_TREINAMENTO,
        exist_ok=True
    )

    caminhoMelhorModelo = os.path.join("runs", "detect", NOME_TREINAMENTO, "weights", "best.pt")

if __name__ == "__main__":
    treinarModelo()

