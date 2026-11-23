
import customtkinter as ctk
from funções import fechar_programa
from cam_ia import ligar_camera, desligar_camera
from interface_cadastro import abrir_cadastro

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

menu = ctk.CTk()
menu.title("FACE ID")
menu.geometry("1100x720")
menu.minsize(950, 650)
menu.configure(fg_color="#0D0D0D")

# Cores
PRETO = "#0D0D0D"
PAINEL = "#171717"
CINZA = "#242424"
BRANCO = "#F2F2F2"
CINZA_TEXTO = "#999999"
BORDA = "#303030"

FONTE = "Segoe UI"


# cabeçailo

header = ctk.CTkFrame(
    menu,
    fg_color=PAINEL,
    corner_radius=0,
    height=65)
header.pack(fill="x")
header.pack_propagate(False)

ctk.CTkLabel(
    header,
    text="FACE ID",
    font=(FONTE, 25, "bold"),
    text_color=BRANCO
).pack(side="left", padx=30)

ctk.CTkLabel(
    header,
    text="FACIAL_RECOGNITION_SYSTEM",
    font=(FONTE, 11),
    text_color=CINZA_TEXTO
).pack(side="left", padx=5)

ctk.CTkLabel(
    header,
    text="● SISTEMA INICIALIZADO",
    font=(FONTE, 11, "bold"),
    text_color=BRANCO
).pack(side="right", padx=30)


# TRECOS DO MENU

principal = ctk.CTkFrame(menu, fg_color="transparent")
principal.pack(fill="both", expand=True, padx=25, pady=20)

# titulo
ctk.CTkLabel(
    principal,
    text="Painel de monitoramento",
    font=(FONTE, 24, "bold"),
    text_color=BRANCO
).pack(anchor="w")

ctk.CTkLabel(
    principal,
    text="Visualização e identificação de pessoas em tempo real",
    font=(FONTE, 12),
    text_color=CINZA_TEXTO
).pack(anchor="w", pady=(3, 18))

# Criação da area prinicipal do menu 
area = ctk.CTkFrame(principal, fg_color="transparent")
area.pack(fill="both", expand=True)

area.grid_columnconfigure(0, weight=7)
area.grid_columnconfigure(1, weight=3)
area.grid_rowconfigure(0, weight=1)


# area da camera 

painel_camera = ctk.CTkFrame(
    area,
    fg_color=PAINEL,
    corner_radius=8,
    border_width=1,
    border_color=BORDA)

painel_camera.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10))

ctk.CTkLabel(
    painel_camera,
    text="VISUALIZAÇÃO DA CÂMERA",
    font=(FONTE, 13, "bold"),
    text_color=BRANCO
    ).pack(anchor="w", padx=20, pady=(18, 12))

tela_camera = ctk.CTkFrame(
    painel_camera,
    fg_color="#090909",
    corner_radius=5)

tela_camera.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)

aviso_camera = ctk.CTkLabel(
    tela_camera,
    text="CÂMERA DESATIVADA",
    font=(FONTE, 14, "bold"),
    text_color="#888888"
)
aviso_camera.pack(expand=True)


# painel de identificação -- isso aqui vou mexer dps, pq não tem banco ainda, então só deixei pela aura

painel_info = ctk.CTkFrame(
    area,
    fg_color=PAINEL,
    corner_radius=8,
    border_width=1,
    border_color=BORDA
)
painel_info.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(10, 0)
)

ctk.CTkLabel(
    painel_info,
    text="IDENTIFICAÇÃO",
    font=(FONTE, 13, "bold"),
    text_color=BRANCO
).pack(anchor="w", padx=18, pady=(18, 25))

# pessoa identificada- tbm mexer dps
ctk.CTkLabel(
    painel_info,
    text="PESSOA DETECTADA",
    font=(FONTE, 10, "bold"),
    text_color=CINZA_TEXTO
).pack(anchor="w", padx=18)

label_identificacao = ctk.CTkLabel(
    painel_info,
    text="Aguardando...",
    font=(FONTE, 19, "bold"),
    text_color=BRANCO
)

label_identificacao.pack(
    anchor="w",
    padx=18,
    pady=(5, 20)
)

ctk.CTkFrame(
    painel_info,
    height=1,
    fg_color=BORDA
).pack(fill="x", padx=18, pady=5)

# detecção de óculos - tbm mexer dps
label_oculos = ctk.CTkLabel(
    painel_info,
    text="Não identificado",
    font=(FONTE, 15),
    text_color=BRANCO
)

label_oculos.pack(anchor="w", padx=18)

ctk.CTkLabel(
    painel_info,
    text="CONFORMIDADE DO CADASTRO",
    font=(FONTE, 10, "bold"),
    text_color=CINZA_TEXTO
).pack(anchor="w", padx=18, pady=(15, 5))

label_conformidade = ctk.CTkLabel(
    painel_info,
    text="Aguardando...",
    font=(FONTE, 13, "bold"),
    text_color=CINZA_TEXTO,
    wraplength=230,
    justify="left"
)

label_conformidade.pack(anchor="w", padx=18)

ctk.CTkFrame(
    painel_info,
    height=1,
    fg_color=BORDA
).pack(fill="x", padx=18, pady=20)

# só pra ficar maneiro
ctk.CTkLabel(
    painel_info,
    text="STATUS DO SISTEMA",
    font=(FONTE, 10, "bold"),
    text_color=CINZA_TEXTO
).pack(anchor="w", padx=18)

ctk.CTkLabel(
    painel_info,
    text="Pronto para iniciar",
    font=(FONTE, 13),
    text_color=BRANCO
).pack(anchor="w", padx=18, pady=(5, 20))


# botoes

botoes = ctk.CTkFrame(
    principal,
    fg_color="transparent"
)
botoes.pack(fill="x", pady=(15, 0))

botao_camera = ctk.CTkButton(
    botoes,
    text="LIGAR CÂMERA",
    font=(FONTE, 13, "bold"),
    height=43,
    width=230,
    corner_radius=5,
    fg_color="#F2F2F2",
    text_color="#0D0D0D",
    hover_color="#CCCCCC")
botao_camera.pack(side="left", padx=(0, 10))

# AQUI BIG FICA A AREA DA ARTE, VAI TOMANDOOOOOO
# explicando pós empolgação, ele alterna o botão de ligar e desligar a camera

cam = None
label_camera = None
after_id = None

def alternar_camera():
    global cam, label_camera, after_id  # permite mexer nas variaveis globais da camera

    if cam is None: #vê se a camera ta desligada, se sim, liga ela

        resultado = ligar_camera(tela_camera)

        if resultado is None:  # se não conseguir iniciar, encerra a função
            return

        cam, label_camera, after_id = resultado # guarda os dados retornados pela função

        aviso_camera.pack_forget() #esconde o aviso de camera desligada
    
        botao_camera.configure(  #muda o botão pra desligar a camera
            text="DESLIGAR CÂMERA",
            fg_color="#333333",
            text_color="#FFFFFF",
            hover_color="#444444"
        )

    else:

        desligar_camera(cam,label_camera,after_id,tela_camera) # desliga a câmera e interrompe sua atualização

        cam = None
        label_camera = None
        after_id = None

        aviso_camera.configure(
            text="CÂMERA DESATIVADA")

        aviso_camera.pack(expand=True) # chama o aviso de volta

        botao_camera.configure(    #muda o botão pra ligar a camera
            text="LIGAR CÂMERA",
            fg_color="#F2F2F2",
            text_color="#0D0D0D",
            hover_color="#CCCCCC")

botao_camera.configure(command=alternar_camera)

def atualizar_identificacao():

    if cam is not None:

        identificacao = getattr(
            tela_camera,
            "resultado_identificacao",
            "Aguardando..."
        )

        oculos = getattr(
            tela_camera,
            "status_oculos",
            "Aguardando rosto"
        )
        
        conformidade = getattr(
            tela_camera,
            "conformidade",
            "Aguardando..."
        )

        # Atualiza o nome da pessoa
        label_identificacao.configure(
            text=identificacao
        )

        # Atualiza a situação dos óculos
        if oculos == "Está usando óculos":

            label_oculos.configure(
                text="Está usando óculos",
                text_color="#00CC66"
            )

        elif oculos == "Não está usando óculos":

            label_oculos.configure(
                text="Não está usando óculos",
                text_color="#FF5555"
            )

        else:

            label_oculos.configure(
                text="Aguardando identificação...",
                text_color=CINZA_TEXTO
            )
            
        # Atualiza a conformidade do cadastro
        cor_conformidade = BRANCO

        if "ATENÇÃO" in conformidade:
            cor_conformidade = "#FF5555"

        elif conformidade == "Situação conforme cadastro":
            cor_conformidade = "#00CC66"

        label_conformidade.configure(
            text=conformidade,
            text_color=cor_conformidade
        )

    else:

        label_identificacao.configure(
            text="Aguardando..."
        )

        label_oculos.configure(
            text="Aguardando...",
            text_color=BRANCO
        )
        
        label_conformidade.configure(
            text="Aguardando...",
            text_color=CINZA_TEXTO
        )

    menu.after(200, atualizar_identificacao)

def abrir_tela_cadastro():
    global cam, label_camera, after_id

    if cam is not None:
        desligar_camera(cam, label_camera, after_id, tela_camera)

        cam = None
        label_camera = None
        after_id = None

        aviso_camera.configure(text="CÂMERA DESATIVADA")
        aviso_camera.pack(expand=True)

        botao_camera.configure(text="LIGAR CÂMERA",fg_color="#F2F2F2",text_color="#0D0D0D",hover_color="#CCCCCC")
        
    abrir_cadastro(menu)



ctk.CTkButton(
    botoes,
    text="CADASTRAR PESSOA",
    font=(FONTE, 13, "bold"),
    height=43,
    width=200,
    corner_radius=5,
    fg_color=CINZA,
    text_color=BRANCO,
    hover_color="#383838",
    border_width=1,
    border_color=BORDA,
    command=abrir_tela_cadastro
).pack(side="left")

# rodape
ctk.CTkLabel(
    botoes,
    text="FACE ID  /  VERSÃO 1.0",
    font=(FONTE, 10),
    text_color="#666666"
).pack(side="right", padx=5)


menu.protocol("WM_DELETE_WINDOW", lambda: fechar_programa(menu))

atualizar_identificacao()

menu.mainloop()



#6 - comparar com a imagem capturada em camera e identificar se é a mesma pessoa
#7 - Fazer a IA mostrar o resultado na tela do "Menu", mostrando o nome da pessoa e se está usando oculos ou não