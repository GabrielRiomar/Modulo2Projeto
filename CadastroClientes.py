from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re
import pycep_correios
from pycep_correios import viacep
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

janela = Tk()

class GradientFrame(Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="#FFFFFF", color2="#6495ED", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)
    def _draw_gradient(self, event=None):
            '''Draw the gradient'''
            self.delete("gradient")
            width = self.winfo_width()
            height = self.winfo_height()
            limit = width
            (r1,g1,b1) = self.winfo_rgb(self._color1)
            (r2,g2,b2) = self.winfo_rgb(self._color2)
            r_ratio = float(r2-r1) / limit
            g_ratio = float(g2-g1) / limit
            b_ratio = float(b2-b1) / limit

            for i in range(limit):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))
                color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
                self.create_line(i,0,i,height, tags=("gradient",), fill=color)
            self.lower("gradient")

#Adicionando uma classe para geração de relatorios
class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    
    def gerarRelatorio(self):
        self.c = canvas.Canvas("cliente.pdf")  
        self.codigoRel = self.entry_codigo.get()
        self.nomeRel = self.entry_nome.get()
        self.cpfRel = self.entry_cpf.get()
        self.cepRel = self.entry_cep.get()
        self.cidadeRel = self.entry_cidade.get()
        self.complementoRel = self.entry_complemento.get()
        self.ufRel = self.entry_uf.get()
        self.bairroRel = self.entry_bairro.get()
        self.logradouroRel = self.entry_logradouro.get()
        self.numeroRel = self.entry_numero.get()
        self.telefoneRel = self.entry_telefone.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        #Criando os campos na ficha
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawString(50, 700, 'Codigo ')
        self.c.drawString(50, 680, 'Nome: ')
        self.c.drawString(50, 660, 'CPF: ')
        self.c.drawString(50, 640, 'CEP: ')
        self.c.drawString(50, 620, 'Cidade: ')
        self.c.drawString(50, 600, 'Complemento: ')
        self.c.drawString(50, 580, 'UF: ')
        self.c.drawString(50, 560, 'Bairro: ')
        self.c.drawString(50, 540, 'Logradouro: ')
        self.c.drawString(50, 520, 'Número: ')
        self.c.drawString(50, 500, 'Telefone: ')

        #Chamando os dados de acordo com a entry do banco
        self.c.setFont("Helvetica", 14)
        self.c.drawString(105, 700, self.codigoRel)
        self.c.drawString(100, 680, self.nomeRel)
        self.c.drawString(90, 660, self.cpfRel)
        self.c.drawString(90, 640, self.cepRel)
        self.c.drawString(105, 620, self.cidadeRel)
        self.c.drawString(150, 600, self.complementoRel)
        self.c.drawString(80, 580, self.ufRel)
        self.c.drawString(100, 560, self.bairroRel)
        self.c.drawString(135, 540, self.logradouroRel)
        self.c.drawString(110, 520, self.numeroRel)
        self.c.drawString(115, 500, self.telefoneRel)

        #Um detalhe a mais para deixa a ficha bonita
        self.c.rect(185, 780, 215, 35, fill=False, stroke=True)
        self.c.rect(50, 730, 500, 1, fill=True, stroke=True)
        self.c.rect(50, 480, 500, 1, fill=True, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

#Adicionando validadores nas entrys
class Validadores():

    def validar_entry2(self, text): 
        if text == '':
            return True #Para poder trabalhar na entry
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100000 #Os 0 do são o número de caracteres

    def validarNum(self, text): #Limite de 9 caracteres
        if text == '':
            return True #Para poder trabalhar na entry
        if ' ' in text:
            texto = text.replace(' ','')
            if texto.isnumeric():
                return True
            else:
                return False
        else:
            if text.isnumeric():
                return True
            else:
                return False
        


    def validaLetra(self, text):
        if text == '':
            return True
        if ' ' in text:
            texto = text.replace(' ','')
            if texto.isalpha():
                return True
            else:
                return False
        else:
            if text.isalpha():
                return True
            else:
                return False
        
        
###### Função pra validar as entradas ######### 

    def valida_entrada(self):
        self.val_entry2 = (self.janela.register(self.validar_entry2),'%P')
        self.val_entryNum = (self.janela.register(self.validarNum),'%P')
        self.val_entryLet = (self.janela.register(self.validaLetra),'%P')
        
#######   Função pro número do telefone já sair bonitinho, mas não deu certo tenho que ver ainda #####
    def validaTel(self, padrao, tel, validarNum):
        padrao = '([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})'

        tel = re.search(padrao, validarNum())
        return '+{}({}){}-{}'.format(tel.group(1),  tel.group(2), tel.group(3), tel.group(4))
######## A gente pode pensar em algo pra botar no menu ################

#Adicionando função aos Botões[]
class Funcs():
#Função para o botão Limpar
    def limpa_tela(self):
        self.entry_codigo.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_cpf.delete(0, END)
        self.entry_cep.delete(0, END)
        self.entry_cidade.delete(0, END)
        self.entry_complemento.delete(0, END)
        self.entry_uf.delete(0, END)
        self.entry_bairro.delete(0, END)
        self.entry_logradouro.delete(0, END)
        self.entry_numero.delete(0, END)
        self.entry_telefone.delete(0, END)
        
#Função para conectar o banco de dados
    def conecta_bd(self):
        self.conn = sqlite3.connect('clientes.bd')
        self.cursor = self.conn.cursor() 
        print('Conectando ao Banco de Dados')

#Função para desconectar o banco de dados
    def desconecta_bd(self):
        self.conn.close()
        print('Desconectando o Banco de Dados')

#Função para criar o banco de dados
    def montaTabelas(self):
        self.conecta_bd()
        ###Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
             cod INTEGER PRIMARY KEY,
             nome_cliente CHAR(40) NOT NULL,
             cpf INTEGER(11) NOT NULL,
             cep INTEGER(9),
             cidade CHAR(40),
             uf CHAR(2) NOT NULL,
             bairro CHAR(20),
             logradouro CHAR(40),
             complemento CHAR(40),
             numero INTEGER(5),
             telefone INTEGER(20)
            );
        """)
        #Validar a informação no banco de dados
        self.conn.commit(); print('Banco de Dados criado')
        #Desconectar o banco de dados
        self.desconecta_bd(); print('Banco de Dados Desconectado')

#Função que possui todas as variaveis
    def dados(self):
        self.codigo = self.entry_codigo.get()
        self.nome = self.entry_nome.get()
        self.cpf = self.entry_cpf.get()
        self.cep = self.entry_cep.get()
        self.cidade = self.entry_cidade.get()
        self.complemento = self.entry_complemento.get()
        self.uf = self.entry_uf.get()
        self.bairro = self.entry_bairro.get()
        self.logradouro = self.entry_logradouro.get()
        self.numero = self.entry_numero.get()
        self.telefone = self.entry_telefone.get()   

#Função para adiconar dados do cliente    
    def add_cliente(self):
        self.dados()
        #Adicionando mensagem de erro para campos OBRIGATORIOS
        if self.entry_nome.get() == "":
            msg = "Campo Nome é obrigatorio"
            messagebox.showinfo("Erro de cadastro", msg)
        elif self.entry_cpf.get() == "":
            msg = "Campo CPF é obrigatorio"
            messagebox.showinfo("Erro de cadastro", msg)
        elif self.entry_uf.get() == "":
            msg = "Campo UF é obrigatorio"
            messagebox.showinfo("Erro de cadastro", msg)
        else:    
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes(nome_cliente, cpf, cep, cidade, uf, bairro, logradouro, complemento, numero, telefone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.nome, self.cpf, self.cep, self.cidade, self.uf, self.bairro, self.logradouro, self.complemento, self.numero, self.telefone))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()       

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, cpf, cep, cidade, uf, bairro, logradouro, complemento, numero, telefone FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i) 
        self.desconecta_bd()   

#Função para Duplo Click
    def OnDoubleClick(self, event):  
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = self.listaCli.item(n, 'values')
            self.entry_codigo.insert(END, col1)
            self.entry_nome.insert(END, col2)
            self.entry_cpf.insert(END, col3)
            self.entry_cep.insert(END, col4)
            self.entry_cidade.insert(END, col5)
            self.entry_uf.insert(END, col6)
            self.entry_bairro.insert(END, col7)
            self.entry_logradouro.insert(END, col8)
            self.entry_complemento.insert(END, col9)
            self.entry_numero.insert(END, col10)
            self.entry_telefone.insert(END, col11)

    def deleta_cliente(self):
        self.dados()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.dados()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, cpf = ?, cep = ?, cidade = ?, uf = ?, bairro = ?, logradouro = ?, complemento = ?, numero = ?, telefone = ? WHERE cod = ? """, (self.nome, self.cpf, self.cep, self.cidade, self.uf, self.bairro, self.logradouro, self.complemento, self.numero, self.telefone, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children()) #limpa a lista

        self.entry_nome.insert(END, '%') #Busca (% é coringa por isso coloquei aqui, pra ñ ficar digitando)
        nome = self.entry_nome.get() #Variável pra identificar o nome digitado
        self.cursor.execute(
            """ SELECT cod, nome_cliente, cpf, cep, cidade, uf, bairro, logradouro, complemento, numero, telefone FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" %nome) 
        #LIKE vai fazer a pesquisa de algo que tenha o que foi digitado, ñ somente o que foi digitado
        #Order By vai fazer a pesquisa em ordem ASC de ascendente
        busca_cliente = self.cursor.fetchall() #fecha a busca
        for i in busca_cliente:
            self.listaCli.insert('', END, values=i) #Vai inserir a pesquisa na lista
        self.limpa_tela() #Limpar as entrys
        self.desconecta_bd()   
        

class App(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.janela = janela
        self.valida_entrada() #chamando a função valida a entrada
        self.tela() #chamando a funçao tela
        self.frames_tela() #chamando a funçao frames tela
        self.widgets_frame1() #chamando a funçao widgets tela
        self.lista_frame2() #chamando a tabela Clientes
        self.montaTabelas() #chamando a função monta tabelas
        self.select_lista() #chamando para atualizar a lista com o clientes cadastrados
        self.menus() #chamando a função mostrar Menu
        janela.mainloop()

#Função para pegar informações de CEP do correio
    def correios_cep(self):
        self.entry_cidade.delete(0, END)
        self.entry_logradouro.delete(0, END)
        self.entry_uf.delete(0, END)
        self.entry_complemento.delete(0, END)
        self.entry_bairro.delete(0, END)
        
        zipcode = self.entry_cep.get()
        dados_cep = pycep_correios.get_address_from_cep(zipcode)
        print(dados_cep)

        self.entry_cidade.insert(END, dados_cep['cidade'])
        self.entry_logradouro.insert(END, dados_cep['logradouro'])
        self.entry_uf.insert(END, dados_cep['uf']) 
        self.entry_complemento.insert(END, dados_cep['complemento'])
        self.entry_bairro.insert(END, dados_cep['bairro'])   

    def tela(self):
        self.janela.title('Cadastro de Clientes') #titulo
        self.janela.configure(background='#1e3743') #Cor de fundo
        self.janela.geometry('1200x900') #tamanho da tela
        self.janela.resizable(True, True) #tamanho ajustável
        self.janela.maxsize(width=1200, height=1000) #tamanho máximo
        self.janela.minsize(width=800, height=600) #tamanho mínimo

    def frames_tela(self):
        #Criando o Frame 1
        self.frame_1 = Frame(self.janela, bd=4, bg='#FFFFFF', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        #Criando o frame 2
        self.frame_2 = Frame(self.janela, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)    


    def widgets_frame1(self):
    ##Criando Botões##  
        #Criando o Botão Limpar
        self.btn_limpar = Button(self.frame_1, text='Limpar', bd=2, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command = self.limpa_tela)
        self.btn_limpar.place(relx=0.23, rely=0.8, relwidth=0.08, relheight=0.08)

        #Criando o Botão Buscar
        self.btn_buscar = Button(self.frame_1, text='Buscar', bd=2, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.btn_buscar.place(relx=0.39, rely=0.8, relwidth=0.08, relheight=0.08)

        #Criando o Botão Salvar
        self.btn_salvar = Button(self.frame_1, text='SALVAR', bd=2, bg='#008000', fg='white',
                                font=('verdana', 8, 'bold'), command = self.add_cliente)                  
        self.btn_salvar.place(relx=0.03, rely=0.8, relwidth=0.08, relheight=0.08)

        #Criando o Botão Alterar
        self.btn_alterar = Button(self.frame_1, text='Alterar', bd=2, bg='#107db2', fg='white',
                                 font=('verdana', 8, 'bold'), command = self.altera_cliente)
        self.btn_alterar.place(relx=0.31, rely=0.8, relwidth=0.08, relheight=0.08)

        #Criando o Botão Deletar
        self.btn_deletar = Button(self.frame_1, text='DELETAR', bd=2, bg='#DC143C', fg='white',
                                font=('verdana', 8, 'bold'), command = self.deleta_cliente)
        self.btn_deletar.place(relx=0.13, rely=0.8, relwidth=0.08, relheight=0.08)

        # #Criando o Botão Deletar
        # self.btn_procuracep = Button(self.frame_1, text='DELETAR', bd=2, bg='#DC143C', fg='white',
        #                         font=('verdana', 8, 'bold'), command = self.correios_cep)
        # self.btn_procuracep.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)


    ##Criando Labels e Entrys##
        #Criando Label Titulo
        self.lb_cadastro = Label(self.frame_1, text='Cadastro de Cliente', bg='#FFFFFF', fg='#6495ED', font=('arial', 20, 'italic', 'bold'))
        self.lb_cadastro.place(relx=0.03, rely=0.04)

        #Criando Label Observação
        self.lb_cadastro = Label(self.frame_1, text='Campos Obrigatórios*', bg='#FFFFFF', fg='#b2102c', font=('arial', 10, 'italic'))
        self.lb_cadastro.place(relx=0.26, rely=0.07)


        self.lb_cadastro = Label(self.frame_1, text='-'*100, bg='#FFFFFF', fg='#6495ED', font=('arial', 10))
        self.lb_cadastro.place(relx=0.03, rely=0.11)

        #Criando Label e Entry Código
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_codigo.place(relx=0.03, rely=0.17)

        self.entry_codigo = Entry(self.frame_1, validate='key', validatecommand=self.val_entryNum, bg='#dfe3ee')
        self.entry_codigo.place(relx=0.03, rely=0.22, relwidth=0.05)

        #Criando Label e Entry Nome
        self.lb_nome = Label(self.frame_1, text='Nome*', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_nome.place(relx=0.03, rely=0.29)

        self.entry_nome = Entry(self.frame_1, validate='key', validatecommand=self.val_entryLet, bg='#dfe3ee')
        self.entry_nome.place(relx=0.03, rely=0.34, relwidth=0.27)

        #Criando Label e Entry CPF
        self.lb_cpf = Label(self.frame_1, text='CPF*', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_cpf.place(relx=0.32, rely=0.29)

        self.entry_cpf = Entry(self.frame_1, validate='key', validatecommand=self.val_entryNum, bg='#dfe3ee')
        self.entry_cpf.place(relx=0.32, rely=0.34, relwidth=0.2)

        #Criando Label e Entry CEP
        self.lb_cep = Button(self.frame_1, text='CEP', bg='#dfe3ee', fg='#6495ED', font=('verdana', 10, 'bold'), command = self.correios_cep)
        self.lb_cep.place(relx=0.03, rely=0.42)

        self.entry_cep = Entry(self.frame_1, validate='key', validatecommand=self.val_entryNum, bg='#dfe3ee')
        self.entry_cep.place(relx=0.03, rely=0.47, relwidth=0.1)

        #Criando Label e Entry Cidade
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_cidade.place(relx=0.16, rely=0.42)

        self.entry_cidade = Entry(self.frame_1, bg='#dfe3ee')
        self.entry_cidade.place(relx=0.16, rely=0.47, relwidth=0.25)
       
        #Criando Label e Entry Complemento
        self.lb_complemento = Label(self.frame_1, text='Complemento', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_complemento.place(relx=0.43, rely=0.55)

        self.entry_complemento = Entry(self.frame_1, bg='#dfe3ee')
        self.entry_complemento.place(relx=0.43, rely=0.6, relwidth=0.20)

        #Criando Label e Entry Unidade Federativa
        self.lb_uf = Label(self.frame_1, text='UF*', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_uf.place(relx=0.45, rely=0.42)

        self.entry_uf = Entry(self.frame_1, bg='#dfe3ee')
        self.entry_uf.place(relx=0.45, rely=0.47, relwidth=0.03)
        
        #Criando Label e Entry Bairro
        self.lb_bairro = Label(self.frame_1, text='Bairro', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_bairro.place(relx=0.5, rely=0.42)

        self.entry_bairro = Entry(self.frame_1, bg='#dfe3ee')
        self.entry_bairro.place(relx=0.5, rely=0.47, relwidth=0.2)
        
        #Criando Label e Entry Logradouro
        self.lb_logradouro = Label(self.frame_1, text='Logradouro', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_logradouro.place(relx=0.03, rely=0.55)

        self.entry_logradouro = Entry(self.frame_1, bg='#dfe3ee')
        self.entry_logradouro.place(relx=0.03, rely=0.6, relwidth=0.25)

        #Criando Label e Entry Número
        self.lb_numero = Label(self.frame_1, text='Número', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_numero.place(relx=0.31, rely=0.55)

        self.entry_numero = Entry(self.frame_1, validate='key', validatecommand=self.val_entryNum, bg='#dfe3ee')
        self.entry_numero.place(relx=0.31, rely=0.6, relwidth=0.08)        

        #Criando Label e Entry Telefone
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#FFFFFF', fg='#6495ED', font=('verdana', 10, 'bold'))
        self.lb_telefone.place(relx=0.56, rely=0.29)

        self.entry_telefone = Entry(self.frame_1, validate='key', validatecommand=self.val_entryNum, bg='#dfe3ee')
        self.entry_telefone.place(relx=0.56, rely=0.34, relwidth=0.2)

    def lista_frame2(self):
    ##Criando a tabela Clientes    
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Código')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='CPF')
        self.listaCli.heading('#4', text='CEP')
        self.listaCli.heading('#5', text='Cidade')
        self.listaCli.heading('#6', text='UF')
        self.listaCli.heading('#7', text='Bairro')
        self.listaCli.heading('#8', text='Logradouro')
        self.listaCli.heading('#9', text='Complemento')
        self.listaCli.heading('#10', text='Número')
        self.listaCli.heading('#11', text='Telefone')


        self.listaCli.column('#0', width=0)
        self.listaCli.column('#1', width=45)
        self.listaCli.column('#2', width=150)
        self.listaCli.column('#3', width=90)
        self.listaCli.column('#4', width=90)
        self.listaCli.column('#5', width=80)
        self.listaCli.column('#6', width=70)
        self.listaCli.column('#7', width=50)
        self.listaCli.column('#8', width=125)
        self.listaCli.column('#9', width=125)
        self.listaCli.column('#10', width=50)
        self.listaCli.column('#11', width=100)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        #criando Barra de rolagem
        self.scrolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscrollcommand=self.scrolLista.set)
        self.scrolLista.place(relx=0.96, rely=0.1, relwidth=0.025, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
        style=ttk.Style(janela)
        style.theme_use('clam')
        
    #Criando a barra com menu de opções
    def menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        menu1 = Menu(menubar)
        menu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label= "Opções", menu = menu1)
        menubar.add_cascade(label= "Ficha", menu = menu2)

        menu1.add_command(label= "Sair", command = Quit)
        menu1.add_command(label= "Limpa Cliente", command = self.limpa_tela)
        
        menu2.add_command(label= "Cliente Específico", command = self.gerarRelatorio)

App()