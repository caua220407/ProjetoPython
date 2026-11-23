import customtkinter as ctk
from cam_ia import ligar_camera, desligar_camera
from funções import fechar_programa

        
def janela_identificar(menu):
    
   
    
    menu = ctk.CTkToplevel()
    menu.title("Cadastro")
    menu.geometry("900x700")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    
    cam = None
    tela_camera = None
    after_id = None

    def ligar():
        nonlocal cam, tela_camera, after_id, menu
        if cam is not None:
                print("Câmera já está ligada!")
                return
        cam, tela_camera, after_id = ligar_camera(menu)

    def desligar():
        nonlocal cam, tela_camera, after_id, menu

        desligar_camera(cam, tela_camera, after_id, menu)
        cam = None
    
        cam = None
        tela_camera = None
        after_id = None
            
    
    frame_botoes = ctk.CTkFrame(menu, fg_color="transparent")
    frame_botoes.pack(pady=10)

    
    ctk.CTkButton(frame_botoes, text="Desligar câmera", font=("Courier New", 16), command=lambda: desligar()).pack(side=ctk.LEFT, padx=20, pady=10)
    ctk.CTkButton(frame_botoes, text="Ligar câmera", font=("Courier New", 16), command=lambda: ligar()).pack(side=ctk.LEFT, padx=20, pady=10)
    

    
    menu.protocol("WM_DELETE_WINDOW", lambda: fechar_programa(menu))






    # Então rapaz, isso aqui se tornou inutil já que ta tudo rolando no code principal, lá no interface inicial, mas to com medo de apagar pq não sei se vai dar ruim, então vou deixar comentado, mas é isso, a camera ta funcionando e tals, dale nessa magreza