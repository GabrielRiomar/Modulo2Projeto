from tkinter import *
from tkinter import messagebox
import banco


def bt_Sair():
    login.destroy()

def criar_Cadastro():
    #Formulario de Registro
    cadastrar.place(x=1000)
    entrar.place(x=1000)
    
    estado.place(x=25, y=115)
    estado_entry.place(x=100, y=120)
    
    usuario.place(x=15, y=65)
    usuario_entry.place(x=100, y=70)
    
    senha.place(x=30, y=90)
    senha_entry.place(x=100, y=95)
    
    nome.place(x=30, y=40)
    nome_entry.place(x=100, y=45)
    
    #Base para o SQLite
    criarcad.place(x=80, y=150)
    retornar.place(x=80, y=180)

def retornar_login():
    #Retorna o necessario
    usuario.place(x=100, y=50)
    usuario_entry.place(x=80, y=75)
    
    senha.place(x=110, y=100)
    senha_entry.place(x=80, y=125)
    
    cadastrar.place(x=148, y=170)
    
    retornar.place(x=500)
    
    entrar.place(x=55, y=170)
    
    #Remover o desnecessario
    nome_entry.place(x=500)
    
    nome.place(x=500)
    
    estado_entry.place(x=500)
    estado.place(x=500)
    
    criarcad.place(x=500)

def registrar_Cadastro():
    #Pegar informações para o Banco
    NomeBanco = nome_entry.get()
    UsuarioBanco = usuario_entry.get()
    SenhaBanco = senha_entry.get()
    EstadoBanco = estado_entry.get()

    if(NomeBanco == "" and UsuarioBanco == "" and SenhaBanco == "" and EstadoBanco == ""):
        messagebox.showerror(title="Erro de Registro", message="Preencha todos os Campos")
    else:
        # Inserir no Banco
        banco.cursor.execute("""
        INSERT INTO Users(Nome, Usuario, Senha, Estado) VALUES(?, ?, ?, ?)
        """,(NomeBanco, UsuarioBanco, SenhaBanco, EstadoBanco))
        banco.conn.commit()
        messagebox.showinfo(title="Register Info", message="Conta criada com sucesso")

def acessando_Login():
    EmailLogin = usuario_entry.get()
    SenhaLogin = senha_entry.get()

    banco.cursor.execute("""
    SELECT * FROM Users
    WHERE Usuario = ? AND Senha = ?
    """,(EmailLogin, SenhaLogin))
    VerificarLogin = banco.cursor.fetchone()
    liberado = EmailLogin in VerificarLogin and SenhaLogin in VerificarLogin

    if liberado:
            messagebox.showinfo(title="Login", message="Seja Bem-vindo!")
            login.destroy()
            App()
    else:
        messagebox.showinfo(title="Login", message="Usuario ou senha incorretos! ")

login = Tk()

corDeFundo= '#FFFFFF'
login.title('LOGIN')
login["bg"] = corDeFundo
login.geometry("290x300+900+300")
login.resizable(width=False, height=False)
login.iconbitmap(default="Icones_Imagens/icone.ico")

image = PhotoImage(file="Icones_Imagens/imagelogin.png")
img = Label(login, image=image, bg='#FFFFFF')
img.place(x=110, y=205)

title = Label(login, text='LOGIN', bg=corDeFundo, foreground='#6495ED', font=('arial', 18, 'bold'))
title.pack(side=TOP, fill=X)

usuario = Label(login, text='Usuario', bg=corDeFundo, foreground='#6495ED', font=('arial', 14, 'bold'))
usuario.place(x=100, y=50)
usuario_entry = Entry(login, bg='#dfe3ee')
usuario_entry.place(x=80, y=75)

senha = Label(login, text='Senha', bg=corDeFundo, foreground='#6495ED', font=('arial', 14, 'bold'))
senha.place(x=110, y=100)
senha_entry = Entry(login, show="•", bg='#dfe3ee')
senha_entry.place(x=80, y=125)

entrar = Button(login, width='10', text='ENTRAR', foreground='#6495ED', command=acessando_Login, font=('verdana', 9, 'bold'))
entrar.place(x=55, y=160)

cadastrar = Button(login, width='10', text='CADASTRAR', foreground='#6495ED', command=criar_Cadastro, font=('verdana', 9, 'bold'))
cadastrar.place(x=148, y=160)

criarcad = Button(login, width='15', text='Criar Conta', foreground='#6495ED', command=registrar_Cadastro, font=('verdana', 9, 'bold'))
retornar = Button(login, width='15', text='Voltar', foreground='#6495ED', command=retornar_login, font=('verdana', 9, 'bold'))
estado = Label(login, text='Estado', bg='#FFFFFF', foreground='#6495ED', font=('arial', 14, 'bold'))
nome = Label(login, text='Nome', bg='#FFFFFF', foreground='#6495ED', font=('arial', 14, 'bold'))
estado_entry = Entry(login, bg='#dfe3ee')
nome_entry = Entry(login, bg='#dfe3ee')

login.mainloop()