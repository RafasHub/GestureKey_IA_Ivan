import cv2
from ultralytics import YOLO
import subprocess
import time
import os
import torch 

CAMINHO_MODELO = r"runs\detect\yolov8_open_mouth_custom\weights\best.pt"
CAMINHO_MACRO = r"macros\example_macro.bat"
LIMIAR_CONFIANCA = 0.70
GATILHO_COOLDOWN = 2.0
INDEX_WEBCAM = 0

# ("cpu", "0", "auto")
DEVICE = "auto"


ultimaAtivacao = 0

def detectar():
    global ultimaAtivacao

    if not os.path.exists(CAMINHO_MACRO):
        macroExiste = False
    else:
        macroExiste = True

    melhorProcessamento = DEVICE
    if DEVICE == "auto":
        melhorProcessamento = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"encontrado: {melhorProcessamento}")
    elif DEVICE != "cpu":
        try:
            indexGpu = int(DEVICE)
            if not torch.cuda.is_available() or indexGpu >= torch.cuda.device_count():
                print(f"Warning: GPU'{DEVICE}' nao disponivel. Rodando na CPU.")
                melhorProcessamento = "cpu"
            else:
                melhorProcessamento = indexGpu
                print(f"Usando a gpu")
        except ValueError:
            print(f"Warning: dispositivo invalido (	'{DEVICE}'). Rodando na CPU")
            melhorProcessamento = "cpu"
    else:
        print("Usando a cpu uspecificada.")

    print(f"Carregando modelo: {CAMINHO_MODELO}")
    try:
        modelo = YOLO(CAMINHO_MODELO)
        modelo.to(melhorProcessamento)
        print("Modelo carregado.")
    except Exception as e:
        print(f"Erro carregando modelo: {e}")
        return
    
    print(f"Iniciando webcam (index: {INDEX_WEBCAM})...")
    cap = cv2.VideoCapture(INDEX_WEBCAM)
    if not cap.isOpened():
        print(f"Erro: nao foi possivel abrir a webcam {INDEX_WEBCAM}.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro: nao foi possivel capturar frame da webcam")
            break

      
        resultados = modelo(frame, device=melhorProcessamento, verbose=False)
        boca_detectada = False
        maior_confianca = 0

        for result in resultados:
            if result.boxes is not None:
                for box in result.boxes:
                    id_da_classe = int(box.cls[0])
                    confianca = float(box.conf[0])

                    if id_da_classe == 0 and confianca > LIMIAR_CONFIANCA:
                        boca_detectada = True
                        maior_confianca = max(maior_confianca, confianca)
                        break
                if boca_detectada:
                    break

        momentoAtual = time.time()
        if boca_detectada and macroExiste and (momentoAtual - ultimaAtivacao > GATILHO_COOLDOWN):
            try:
                subprocess.run(["cmd", "/c", "start", "", CAMINHO_MACRO], check=True, shell=True)
                ultimaAtivacao = momentoAtual
            except FileNotFoundError:
                print(f"Error: Macro'{CAMINHO_MACRO}' nao encontrada durante execucao.")
            except subprocess.CalledProcessError as e:
                print(f"Erro executando macro: {e}")
            except Exception as e:
                print(f"Um erro inesperado ocorreu na execucao da macro: {e}")

        frame_anotado = resultados[0].plot()
        cv2.imshow("Deteccao de boca aberta - Aperte \'q\' para sair", frame_anotado)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Saindo...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detectar()

