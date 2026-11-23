from tkinter import messagebox

def fechar_programa(janela, menu=None, cam=None):

    if cam is not None:
        cam.release()

    if menu is not None:
        menu.destroy()

    janela.destroy()
    