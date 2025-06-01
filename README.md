# Detecção de Boca Aberta e Acionamento de Macro

## Visão Geral do Projeto

Este projeto utiliza um modelo YOLOv8, treinado especificamente para esta tarefa, para detectar bocas abertas em tempo real através da imagem da webcam. Quando uma boca aberta é detectada com um nível de confiança suficiente, o sistema aciona uma macro pré-definida do Windows (um script batch).

O pacote inclui os scripts necessários para:
1.  Baixar o conjunto de dados (dataset) necessário do Roboflow.
2.  Treinar um modelo YOLOv8 customizado com esse dataset.
3.  Executar a detecção em tempo real usando a webcam e acionar a macro.

## Pré-requisitos

Para que tudo funcione direitinho, você vai precisar de:

*   **Python:** Versão 3.8 ou superior é recomendada. Você pode baixar em [python.org](https://www.python.org/downloads/).
*   **pip:** O instalador de pacotes do Python (geralmente já vem junto com o Python).
*   **Conta e Chave de API do Roboflow:** Essencial para baixar o dataset. Crie sua conta e pegue sua chave de API *privada* nas [Configurações do Roboflow](https://app.roboflow.com/settings/api).
*   **Webcam:** Necessária para a detecção em tempo real.
*   **(Opcional) Placa de Vídeo NVIDIA (GPU):** Acelera *bastante* o treinamento do modelo e a detecção. Se você não tiver uma, os scripts usarão a CPU (o que será mais lento).
*   **Git:** (Opcional) Útil para clonar o repositório, caso ele seja fornecido dessa forma.

## Instruções de Configuração

1.  **Obtenha os Arquivos:** Baixe ou clone todos os arquivos fornecidos (`download_dataset.py`, `train_yolov8.py`, `detect_mouth_webcam.py`, `macros/example_macro.bat`, `README.md`) para uma única pasta (diretório) no seu computador.

2.  **Abra o Terminal/Prompt de Comando:** Navegue até a pasta do projeto usando o terminal ou prompt de comando 

3.  **Crie um Ambiente Virtual (Recomendado):** É uma boa prática para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    # Para ativar (Windows)
    .\\venv\\Scripts\\activate
    # Para ativar (macOS/Linux)
    # source venv/bin/activate
    ```

4.  **Instale as Dependências:** Instale os pacotes Python necessários.
    ```bash
    pip install roboflow ultralytics opencv-python torch torchvision torchaudio
    ```
    *Observação: Este comando instala o PyTorch com suporte a CUDA, se disponível. Se você precisar especificamente de uma versão apenas para CPU ou uma versão diferente do CUDA, consulte o [guia de instalação do PyTorch](https://pytorch.org/get-started/locally/).*

## Passo a Passo para Usar

**Passo 1: Baixar o Dataset**

1.  **Edite `download_dataset.py`:** Abra o script `download_dataset.py` em um editor de texto (como Bloco de Notas, VS Code, etc.).
2.  **Adicione sua Chave de API:** Substitua `"YOUR_ROBOFLOW_API_KEY"` pela sua chave de API privada real do Roboflow.
3.  **Execute o Script:** No terminal, execute o comando:
    ```bash
    python download_dataset.py
    ```
4.  **Verifique:** O script vai baixar o dataset para uma pasta chamada `Open-Mouth-Dataset` (por padrão) dentro do diretório do seu projeto. Dentro dela, você deve encontrar as subpastas `train`, `valid`, `test` e um arquivo essencial chamado `data.yaml`.

**Passo 2: Treinar o Modelo**

1.  **Edite `train_yolov8.py`:** Abra o script `train_yolov8.py`.
2.  **Confira o `DATA_YAML_PATH`:** Garanta que o caminho aponta corretamente para o arquivo `data.yaml` baixado no Passo 1 (por exemplo, `./Open-Mouth-Dataset/data.yaml`).
3.  **(Opcional) Configure o Treinamento:** Ajuste `EPOCHS` (épocas), `BATCH_SIZE` (tamanho do lote), `DEVICE` (`cpu`, `0` para a primeira GPU, `auto`), etc., conforme seu hardware e o tempo/qualidade de treinamento desejado. Treinar na CPU levará *bem mais tempo* do que na GPU.
4.  **Execute o Script:** Execute o script de treinamento:
    ```bash
    python train_yolov8.py
    ```
5.  **Aguarde:** O treinamento pode demorar, dependendo do seu hardware e do número de épocas. Acompanhe a saída no terminal.
6.  **Localize o Modelo:** Ao final do treinamento, o script informará o caminho para os pesos do melhor modelo (algo como `runs/detect/yolov8_open_mouth_custom/weights/best.pt`). **Copie este caminho.**

**Passo 3: Executar a Detecção em Tempo Real e Acionar a Macro**

1.  **Edite `detect_mouth_webcam.py`:** Abra o script `detect_mouth_webcam.py`.
2.  **Atualize o `MODEL_PATH`:** Substitua o caminho de exemplo em `MODEL_PATH` pelo caminho real do seu arquivo `best.pt` (aquele que você copiou no passo anterior).
3.  **Confira o `MACRO_SCRIPT_PATH`:** Verifique se este caminho aponta para a macro que você quer executar (por exemplo, `./macros/example_macro.bat`).
4.  **(Opcional) Configure a Detecção:** Ajuste `CONFIDENCE_THRESHOLD` (limiar de confiança), `TRIGGER_COOLDOWN` (tempo de espera entre acionamentos), `WEBCAM_INDEX` (índice da webcam) e `DEVICE` conforme necessário.
5.  **Execute o Script:** Execute o script de detecção:
    ```bash
    python detect_mouth_webcam.py
    ```
6.  **Observe:** A imagem da sua webcam deve aparecer em uma janela. Quando você abrir a boca e o modelo detectar com confiança acima do limiar definido, o script da macro especificada será executado (após o período de cooldown).
7.  **Sair:** Pressione a tecla 'q' com a janela da webcam ativa para parar o script.

## Customizando a Macro

1.  **Localize a Macro:** Encontre o arquivo `example_macro.bat` dentro da pasta `macros`.
2.  **Edite o Script:** Abra o `example_macro.bat` com um editor de texto (como o Bloco de Notas).
3.  **Modifique os Comandos:** O script contém comentários explicando como alterar a ação. Substitua `start notepad.exe` pelo(s) comando(s) que você deseja executar no seu Windows quando uma boca aberta for detectada.
    *   Você pode iniciar aplicativos, executar outros scripts, usar ferramentas de linha de comando (como o `nircmd` para simular teclas, embora o `nircmd` não esteja incluído aqui), etc.
4.  **Salve:** Salve suas alterações no arquivo `.bat`.
5.  **Atualize o Caminho (Se Necessário):** Se você renomear o arquivo da macro ou salvá-lo em outro lugar, lembre-se de atualizar o `MACRO_SCRIPT_PATH` no script `detect_mouth_webcam.py`.

## Solução de Problemas (Troubleshooting)

*   **Webcam não abre:**
    *   Verifique se a webcam está conectada e funcionando.
    *   Tente mudar o `WEBCAM_INDEX` em `detect_mouth_webcam.py` (tente 0, 1, 2...).
    *   Certifique-se de que nenhum outro aplicativo esteja usando a webcam.
*   **Modelo não encontrado (`best.pt`):**
    *   Confirme se você completou o Passo 2 com sucesso.
    *   Verifique se o `MODEL_PATH` em `detect_mouth_webcam.py` corresponde *exatamente* ao caminho gerado pelo script de treinamento.
*   **Macro não encontrada:**
    *   Garanta que o arquivo `.bat` existe no local especificado por `MACRO_SCRIPT_PATH` em `detect_mouth_webcam.py`.
*   **Desempenho Lento:**
    *   A detecção (inferência) será muito mais lenta na CPU do que na GPU. Verifique se o `DEVICE` está configurado corretamente em `detect_mouth_webcam.py` (`auto` ou o índice da sua GPU, como `0`) se você tiver uma GPU compatível.
*   **Erros de Dependência:**
    *   Certifique-se de que instalou todos os pacotes corretamente usando `pip install ...` conforme a seção de configuração.
    *   Verifique se você está executando os scripts dentro do ambiente virtual ativado (se você criou um).
*   **Erro na Chave de API do Roboflow:**
    *   Confirme se você substituiu o texto placeholder em `download_dataset.py` pela sua chave de API privada do Roboflow *correta* e *ativa*.

