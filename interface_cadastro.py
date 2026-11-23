import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from funções import fechar_programa
from cam_ia import ligar_camera, desligar_camera, detectar_uso_oculos, verificar_rosto_cadastrado
from pathlib import Path
from datetime import datetime
from tkinter import messagebox
from banco import cadastrar_usuario



# cores
PRETO = "#0D0D0D"
PAINEL = "#171717"
CINZA = "#242424"
BRANCO = "#F2F2F2"
CINZA_TEXTO = "#999999"
BORDA = "#303030"

FONTE = "Segoe UI"


def voltar (cadastroJan, menu):
    fechar_programa(cadastroJan)
    menu.deiconify()

def abrir_cadastro(menu):

    cam = None
    after_id = None
    label_camera = None
    foto_capturada = None #pra foto capturada, que vai ser salva no banco, e que vai ser usada pra cadastrar o usuario
    usa_oculos_capturado = None
    
    def voltar_tela():
    
            nonlocal cam, label_camera, after_id
    
        # Verifica se a câmera do cadastro está ligada
            if cam is not None:
    
                desligar_camera(
                    cam,
                    label_camera,
                    after_id,
                    tela_camera
                )
    
                cam = None
                label_camera = None
                after_id = None
    
            # Fecha a tela de cadastro
            cadastroJan.destroy()
    
            # Mostra novamente a tela inicial
            menu.deiconify()

    menu.withdraw() 

    cadastroJan = ctk.CTkToplevel(menu)
    cadastroJan.geometry("1100x720")
    cadastroJan.minsize(950, 650)
    cadastroJan.configure(fg_color="#0D0D0D")
    
   # Cabeçalho da tela de cadastro
    header = ctk.CTkFrame(cadastroJan,fg_color=PAINEL,corner_radius=0,height=65)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Botão de voltar
    botao_voltar = ctk.CTkButton(
        header,
        text="←",
        font=(FONTE, 28, "bold"),
        width=50,
        height=45,
        fg_color="transparent",
        text_color=BRANCO,
        hover_color=CINZA,
        command=voltar_tela
    )
    botao_voltar.pack(side="left", padx=20, pady=10)

    # Título do cabeçalho
    ctk.CTkLabel(
        header,
        text="FACE ID / CADASTRO",
        font=(FONTE, 18, "bold"),
        text_color=BRANCO
    ).pack(side="left", padx=10)
    
    # Área com rolagem
    conteudo = ctk.CTkScrollableFrame(
        cadastroJan,
        fg_color="transparent",
        scrollbar_button_color=CINZA,
        scrollbar_button_hover_color="#444444"
    )

    conteudo.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )


#design da tela de cadastro
    titulo = ctk.CTkLabel(
        conteudo,
        text="CADASTRO DE USUÁRIO",
        font=(FONTE, 22, "bold")
    )
    titulo.pack(pady=20)

    campo_nome = ctk.CTkEntry(
        conteudo,
        placeholder_text="Nome do usuário",
        width=300
    )
    campo_nome.pack(pady=15)

    tela_camera = ctk.CTkFrame(
    conteudo,
    width=640,
    height=480,
    fg_color="black")
    tela_camera.pack(pady=15)
    tela_camera.pack_propagate(False)


    aviso_camera = ctk.CTkLabel(
    tela_camera,
    text="CÂMERA DESATIVADA",
    font=(FONTE, 16, "bold"),
    text_color=CINZA_TEXTO)
    aviso_camera.pack(expand=True)

    #aqui começa essa desgraça de tirar foto

    
    def tirar_foto():

        nonlocal foto_capturada, usa_oculos_capturado

        if cam is None:
            messagebox.showwarning(
                "Atenção",
                "Ligue a câmera primeiro!"
            )
            return

        if not hasattr(tela_camera, "frame_atual"):
            messagebox.showwarning(
                "Atenção",
                "Aguarde a câmera iniciar!"
            )
            return

        # Obtém o último frame da câmera
        frame = tela_camera.frame_atual.copy()

        # Verifica se a pessoa está usando óculos
        usa_oculos = detectar_uso_oculos(frame)
        
        # Verifica se o rosto já está cadastrado
        rosto_existente = verificar_rosto_cadastrado(frame)

        if rosto_existente is not False and rosto_existente is not None:

            nome_existente, id_existente, similaridade = rosto_existente

            messagebox.showwarning(
                "Cadastro duplicado",
                f"Esta pessoa já está cadastrada!\n\n"
                f"Nome: {nome_existente}\n"
                f"ID: {id_existente}\n"
                f"Similaridade: {similaridade:.2f}"
            )

            return

        if rosto_existente is None:
            messagebox.showwarning(
                "Atenção",
                "Não foi possível verificar o rosto. Tente novamente."
            )
            return

        if usa_oculos is None:

            messagebox.showwarning(
                "Atenção",
                "Nenhum rosto foi detectado. Posicione-se diante da câmera!"
            )

            return

        # Cria a pasta de fotografias
        pasta_fotos = Path(__file__).resolve().parent / "fotos"
        pasta_fotos.mkdir(exist_ok=True)

        # Cria um nome único para a fotografia
        nome_arquivo = datetime.now().strftime(
            "foto_%Y%m%d_%H%M%S_%f.jpg"
        )

        caminho_foto = pasta_fotos / nome_arquivo

        # Salva a fotografia
        sucesso = cv2.imwrite(str(caminho_foto), frame)

        if sucesso:

            foto_capturada = str(caminho_foto)
            usa_oculos_capturado = usa_oculos

            situacao = (
                "Está usando óculos"
                if usa_oculos
                else "Não está usando óculos"
            )

            messagebox.showinfo(
                "Sucesso",
                f"Foto capturada com sucesso!\n\n"
                f"Detecção: {situacao}"
            )

        else:

            messagebox.showerror(
                "Erro",
                "Não foi possível salvar a foto."
            )


    def salvar_cadastro():

        nome = campo_nome.get().strip()

        if nome == "":
            messagebox.showwarning("Atenção", "Digite o nome do usuário!")
            return

        if foto_capturada is None:
            messagebox.showwarning("Atenção", "Tire uma foto primeiro!")
            return
        
        if usa_oculos_capturado is None:
            messagebox.showwarning(
                "Atenção",
                "Capture uma fotografia válida primeiro!"
            )
            return

        resultado = cadastrar_usuario(nome, foto_capturada, int(usa_oculos_capturado))

        if resultado is None:
            messagebox.showwarning("Atenção","Este usuário já está cadastrado!")
            return

        messagebox.showinfo(
            "Sucesso",
            f"Usuário {nome} cadastrado com sucesso!"
        )


    #botao
    botoes = ctk.CTkFrame(
        conteudo,
        fg_color="transparent")
    botoes.pack(pady=15)


    #ligar/desligar aqui - mesmo esquema que a camera do menu

    def alternar_camera():
        nonlocal cam, label_camera, after_id

        if cam is None:

            resultado = ligar_camera(tela_camera, usar_lolo=False)

            if resultado is None:
                return

            cam, label_camera, after_id = resultado

            aviso_camera.pack_forget()

            botao_camera.configure(
                text="DESLIGAR CÂMERA",
                fg_color="#333333",
                text_color="#FFFFFF",
                hover_color="#444444")

        else:

            desligar_camera(cam, label_camera, after_id, tela_camera)

            cam = None
            label_camera = None
            after_id = None

            aviso_camera.configure(text="CÂMERA DESATIVADA")

            aviso_camera.pack(expand=True)

            botao_camera.configure(
                text="LIGAR CÂMERA",
                fg_color="#F2F2F2",
                text_color="#0D0D0D",
                hover_color="#CCCCCC")

    botao_camera = ctk.CTkButton(
        botoes,
        text="LIGAR CÂMERA",
        font=(FONTE, 13, "bold"),
        height=43,
        width=230,
        corner_radius=5,
        fg_color="#F2F2F2",
        text_color="#0D0D0D",
        hover_color="#CCCCCC",
        command=alternar_camera)
    botao_camera.pack(side="left", padx=5)

    botao_foto = ctk.CTkButton(
        botoes,
        text="TIRAR FOTO",
        font=(FONTE,13, "bold"),
        height=43,
        width=230,
        fg_color="#F2F2F2",
        text_color="#0D0D0D",
        hover_color="#CCCCCC",
        command=tirar_foto)
    botao_foto.pack(side="left", padx=5)

    botao_salvar = ctk.CTkButton(
        botoes,
        text="SALVAR CADASTRO",
        font=(FONTE, 13, "bold"),
        height=43,
        width=230,
        fg_color="#F2F2F2",
        text_color="#0D0D0D",
        hover_color="#CCCCCC",
        command=salvar_cadastro)
    botao_salvar.pack(side="left", padx=5)

    
        

    cadastroJan.protocol("WM_DELETE_WINDOW", voltar_tela)