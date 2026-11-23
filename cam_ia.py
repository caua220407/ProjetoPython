
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
from pathlib import Path
import threading
import queue
import time
from banco import listar_usuarios_com_oculos


# ==================================================
# CAMINHOS E MODELOS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

IA = YOLO(str(BASE_DIR / "models" / "best.pt"))

modelo_yunet = BASE_DIR / "modelos_reconhecimento" / "face_detection_yunet_2023mar.onnx"
modelo_sface = BASE_DIR / "modelos_reconhecimento" / "face_recognition_sface_2021dec.onnx"

detector = cv2.FaceDetectorYN_create(
    str(modelo_yunet),
    "",
    (320, 320),
    0.8,
    0.3,
    5000
)

reconhecedor = cv2.FaceRecognizerSF_create(
    str(modelo_sface),
    ""
)

LIMIAR_RECONHECIMENTO = 0.363
CONFIANCA_YOLO = 0.40


# ==================================================
# CARREGAMENTO DOS ROSTOS CADASTRADOS
# ==================================================

def carregar_usuarios():

    usuarios = listar_usuarios_com_oculos()

    rostos_cadastrados = []

    for id_usuario, nome, caminho_foto, usa_oculos in usuarios:

        if not caminho_foto:
            continue

        caminho_foto = Path(caminho_foto)

        if not caminho_foto.is_absolute():
            caminho_foto = BASE_DIR / caminho_foto

        imagem = cv2.imread(str(caminho_foto))

        if imagem is None:
            print(f"Não foi possível carregar a foto de {nome}")
            continue

        altura, largura = imagem.shape[:2]

        detector.setInputSize((largura, altura))

        _, rostos = detector.detect(imagem)

        if rostos is None or len(rostos) == 0:
            print(f"Nenhum rosto encontrado na foto de {nome}")
            continue

        rosto = max(rostos, key=lambda r: r[2] * r[3])

        rosto_alinhado = reconhecedor.alignCrop(
            imagem,
            rosto
        )

        caracteristicas = reconhecedor.feature(
            rosto_alinhado
        )

        rostos_cadastrados.append({
            "id": id_usuario,
            "nome": nome,
            "caracteristicas": caracteristicas,
            "usa_oculos": None if usa_oculos is None else bool(usa_oculos)
        })

    print(f"Usuários carregados: {len(rostos_cadastrados)}")

    return rostos_cadastrados


# ==================================================
# RECONHECIMENTO FACIAL
# ==================================================

def identificar_rosto(frame, rosto, usuarios):

    rosto_alinhado = reconhecedor.alignCrop(
        frame,
        rosto
    )

    caracteristicas = reconhecedor.feature(
        rosto_alinhado
    )

    melhor_nome = "Desconhecido"
    melhor_id = None
    melhor_similaridade = 0
    usa_oculos_cadastrado = None

    for usuario in usuarios:

        similaridade = reconhecedor.match(
            usuario["caracteristicas"],
            caracteristicas,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if similaridade > melhor_similaridade:

            melhor_similaridade = similaridade
            melhor_nome = usuario["nome"]
            melhor_id = usuario["id"]
            usa_oculos_cadastrado = usuario["usa_oculos"]

    if melhor_similaridade >= LIMIAR_RECONHECIMENTO:

        return (melhor_nome, melhor_id, melhor_similaridade, usa_oculos_cadastrado)

    return "Desconhecido", None, melhor_similaridade, None

def verificar_rosto_cadastrado(frame):

    altura, largura = frame.shape[:2]

    # Detecta o rosto na fotografia
    detector.setInputSize((largura, altura))

    _, rostos = detector.detect(frame)

    if rostos is None or len(rostos) == 0:
        return None

    # Considera o maior rosto encontrado
    rosto = max(rostos, key=lambda r: r[2] * r[3])

    # Carrega os usuários cadastrados
    usuarios = carregar_usuarios()

    if not usuarios:
        return None

    # Compara o rosto com os registros do banco
    nome, id_usuario, similaridade, _ = identificar_rosto(
        frame,
        rosto,
        usuarios
    )

    if nome != "Desconhecido":
        return nome, id_usuario, similaridade

    return False


# ==================================================
# DETECÇÃO DE ÓCULOS
# ==================================================

def detectar_oculos(resultado_yolo, rosto):

    x, y, largura, altura = map(int, rosto[:4])

    # Região superior do rosto
    regiao_x1 = x
    regiao_x2 = x + largura
    regiao_y1 = y
    regiao_y2 = y + int(altura * 0.65)

    nomes_classes = IA.names

    for caixa in resultado_yolo[0].boxes:

        classe = int(caixa.cls.item())

        nome_classe = nomes_classes.get(classe, "").lower()

        if nome_classe not in ("eyeglasses", "sunglasses"):
            continue

        gx1, gy1, gx2, gy2 = map(
            int,
            caixa.xyxy[0].tolist()
        )

        # Verifica se o centro da detecção
        # está dentro da região dos olhos
        centro_x = (gx1 + gx2) // 2
        centro_y = (gy1 + gy2) // 2

        if (
            regiao_x1 <= centro_x <= regiao_x2
            and regiao_y1 <= centro_y <= regiao_y2
        ):

            return True

    return False


def detectar_uso_oculos(frame):

    altura, largura = frame.shape[:2]

    # Detecta o rosto
    detector.setInputSize((largura, altura))

    _, rostos = detector.detect(frame)

    if rostos is None or len(rostos) == 0:
        return None

    # Considera o maior rosto encontrado
    rosto = max(rostos, key=lambda r: r[2] * r[3])

    # Executa o YOLO
    resultado_yolo = IA.predict(
        frame,
        conf=CONFIANCA_YOLO,
        imgsz=416,
        device="cpu",
        verbose=False
    )

    # Verifica se existem óculos na região dos olhos
    usando_oculos = detectar_oculos(
        resultado_yolo,
        rosto
    )

    return usando_oculos



# ==================================================
# LIGAR CÂMERA
# ==================================================

def ligar_camera(area_camera, usar_lolo=True):

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():

        print("Não foi possível abrir a câmera.")

        cam.release()

        return None

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    tela_camera = tk.Label(area_camera, bg="black")
    tela_camera.pack(fill="both", expand=True)

    contador_frames = 0
    after_id = None

    # Resultados disponíveis para a interface principal
    area_camera.resultado_identificacao = "Aguardando..."
    area_camera.status_oculos = "Aguardando rosto"

    estado = {
        "parar": threading.Event(),
        "fila": queue.Queue(maxsize=1),
        "lock": threading.Lock(),
        "deteccoes": [],
        "identificacao": "Aguardando...",
        "oculos": "Aguardando rosto",
        "conformidade": "Aguardando..."
    }

    tela_camera.estado_camera = estado

    # Carrega os usuários antes de iniciar o processamento
    usuarios = carregar_usuarios() if usar_lolo else []

    # ==================================================
    # THREAD DE PROCESSAMENTO
    # ==================================================

    def processar_ia():

        while not estado["parar"].is_set():

            try:
                frame = estado["fila"].get(timeout=0.1)

            except queue.Empty:
                continue

            try:

                # YOLO: detecção de óculos
                conformidade_atual = "Aguardando..."
                
                resultado_yolo = IA.predict(
                    frame,
                    conf=CONFIANCA_YOLO,
                    imgsz=416,
                    device="cpu",
                    verbose=False
                )

                # YuNet: detecção facial
                altura, largura = frame.shape[:2]

                detector.setInputSize((largura, altura))

                _, rostos = detector.detect(frame)

                novas_deteccoes = []

                identificacao = "Nenhum rosto detectado"
                status_oculos = "Aguardando rosto"

                if rostos is not None and len(rostos) > 0:

                    nomes_identificados = []
                    resultados_oculos = []

                    for rosto in rostos:

                        nome, id_usuario, semelhanca, usa_oculos_cadastrado = identificar_rosto(
                            frame,
                            rosto,
                            usuarios
                        )
                        usando_oculos = detectar_oculos(
                            resultado_yolo,
                            rosto
                        )
                        
                        
                        
                        status = ("Está usando óculos"
                        if usando_oculos
                        else "Não está usando óculos"
                    )

                    if nome == "Desconhecido":
                        conformidade = "Pessoa desconhecida"

                    elif usa_oculos_cadastrado is None:
                        conformidade = "Cadastro sem informação de óculos"

                    elif usando_oculos == usa_oculos_cadastrado:
                        conformidade = "Situação conforme cadastro"

                    elif usa_oculos_cadastrado:
                        conformidade = "ATENÇÃO: ÓCULOS AUSENTES"

                    else:
                        conformidade = "ATENÇÃO: ÓCULOS NÃO CADASTRADOS"

                    nomes_identificados.append(nome)
                    resultados_oculos.append(status)

                    novas_deteccoes.append({
                            "rosto": rosto[:4].copy(),
                            "nome": nome,
                            "id": id_usuario,
                            "oculos": status,
                            "usa_oculos_cadastrado": usa_oculos_cadastrado,
                            "conformidade": conformidade
                        })

                    # Resultado principal para a interface
                    identificacao = nomes_identificados[0]
                    status_oculos = resultados_oculos[0]
                    conformidade_atual = novas_deteccoes[0]["conformidade"]

                with estado["lock"]:

                    estado["deteccoes"] = novas_deteccoes
                    estado["identificacao"] = identificacao
                    estado["oculos"] = status_oculos
                    estado["conformidade"] = conformidade_atual

            except Exception as erro:

                print("Erro no processamento das IAs:", erro)

    # Inicia o processamento somente quando necessário
    if usar_lolo:

        thread_ia = threading.Thread(
            target=processar_ia,
            daemon=True
        )

        thread_ia.start()

    else:
        thread_ia = None

    # ==================================================
    # ATUALIZAÇÃO DA CÂMERA
    # ==================================================

    def atualizar_camera():

        nonlocal after_id, contador_frames

        if not tela_camera.winfo_exists():
            return

        sucesso, frame = cam.read()

        if sucesso:

            area_camera.frame_atual = frame

            if usar_lolo:

                contador_frames += 1

                # Envia um frame a cada três capturas
                if contador_frames % 3 == 0:

                    try:
                        estado["fila"].put_nowait(frame.copy())

                    except queue.Full:

                        try:
                            estado["fila"].get_nowait()
                        except queue.Empty:
                            pass

                        try:
                            estado["fila"].put_nowait(frame.copy())
                        except queue.Full:
                            pass

                # Obtém os resultados mais recentes
                with estado["lock"]:

                    deteccoes = list(estado["deteccoes"])

                    identificacao = estado["identificacao"]
                    status_oculos = estado["oculos"]
                    conformidade = estado["conformidade"]

                # Disponibiliza os resultados à interface
                area_camera.resultado_identificacao = identificacao
                area_camera.status_oculos = status_oculos
                area_camera.conformidade = conformidade

                # Desenha somente as identificações faciais
                for deteccao in deteccoes:

                    x, y, largura, altura = map(
                        int,
                        deteccao["rosto"]
                    )

                    nome = deteccao["nome"]

                    cor = (
                        (0, 255, 0)
                        if nome != "Desconhecido"
                        else (0, 0, 255)
                    )

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + largura, y + altura),
                        cor,
                        2
                    )

                    cv2.putText(
                        frame,
                        nome,
                        (x, max(y - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        cor,
                        2
                    )

            # Conversão para exibição
            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            imagem = Image.fromarray(frame_rgb)
            imagem = imagem.resize((640, 480))

            imagem_tk = ImageTk.PhotoImage(imagem)

            tela_camera.config(image=imagem_tk)
            tela_camera.image = imagem_tk

        after_id = area_camera.after(
            10,
            atualizar_camera
        )

        return after_id

    after_id = area_camera.after(10, atualizar_camera)

    return cam, tela_camera, after_id


# ==================================================
# DESLIGAR CÂMERA
# ==================================================

def desligar_camera(cam, tela_camera, after_id, area_camera):

    if after_id is not None:

        try:
            area_camera.after_cancel(after_id)

        except tk.TclError:
            pass

    if tela_camera is not None:

        estado = getattr(
            tela_camera,
            "estado_camera",
            None
        )

        if estado is not None:
            estado["parar"].set()

    if cam is not None:
        cam.release()

    if tela_camera is not None:

        try:
            tela_camera.destroy()

        except tk.TclError:
            pass
