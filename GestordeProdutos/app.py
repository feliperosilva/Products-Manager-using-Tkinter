from tkinter import ttk
from tkinter import *
import sqlite3


class Produto:
    db = 'database/produtos.db'

    def __init__(self, root):
        self.janela = root
        self.janela.title('Gestor de Produtos') # título da janela
        self.janela.resizable(1,1) # (1,1) ativa o redirecionamento da janela.
        # (1,0) permite apenas redirecionamento horizontal
        # (0,1) permite apenas redirecionamento vertical
        # (0,0) para desativar
        self.janela.wm_iconbitmap('recursos/icon.ico')
        root.geometry('400x650') # Redimensionamento da janela (width x height)
        # criação do recipiente Frame principal
        # LabelFrame é um widget filho de Frame, desenha um limite em volta do seu tamanho
        frame = LabelFrame(self.janela, text= 'Registar um novo Produto', font=('Calibri', 16, 'bold'))
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        # inicía na posição 0.0 e columnspan indica quantas colunas do grid vai utilizar
        # pady é a margem usada

        #Criação de Label e Entry
        #Label Nome
        self.etiqueta_nome = Label(frame, text = 'Nome: ', font=('Calibri', 13)) # Etiqueta localizada no frame
        self.etiqueta_nome.grid(row = 1, column = 0) # Posicionamento através de grid
        #Entry Nome (caixa de texto que irá receber o nome)
        self.nome = Entry(frame, font=('Calibri', 13)) # caixa de texto (input) localizada no frame
        self.nome.focus() # para que o foco do rato volte ao início
        self.nome.grid(row = 1, column = 1)
        #Label Preço
        self.etiqueta_preco = Label(frame, text= 'Preço: ', font=('Calibri', 13))
        self.etiqueta_preco.grid(row = 2, column = 0)
        #Entry Preço
        self.preco = Entry(frame, font=('Calibri', 13))
        self.preco.focus()
        self.preco.grid(row = 2, column = 1)

        # Criação de botão Guardar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text = 'Guardar Produto', command= self.add_produto, style='my.TButton')
        # sticky refere-se à quanto o botao ocupa de espaço
        # W = West, E = East, ocupa o espaço inteira da direita à esquerda da janela
        self.botao_adicionar.grid(row = 3, columnspan = 2, sticky = W + E)

        # Mensagem informativa para o utilizador
        self.mensagem = Label(text = '', fg = 'red')
        self.mensagem.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        # modifica-se a fonte da tabela
        style.configure('mystyle.Treeview', highlightthickness = 0, bd = 0, font = ('Calibri', 11))
        # modifica-se a fonte das cabeceiras
        style.configure('mystyle.Treeview.Heading', font = ('Calibri', 13, 'bold'))
        # Eliminar as bordas
        style.layout('mystyle.Treeview',[('mystyle.Treeview.treearea', {'sticky':'nswe'})])

        # Estrutura da tabela
        self.tabela = ttk.Treeview(height = 20, columns = 2, style = 'mystyle.Treeview') # altura = 20 linhas
        self.tabela.grid(row = 4, column = 0, columnspan = 2)
        self.tabela.heading('#0', text = 'Nome', anchor = CENTER) # cabeçalho 0
        self.tabela.heading('#1', text = 'Preço', anchor = CENTER) # cabeçalho 1

        # Botões de Eliminar e Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        botao_eliminar = ttk.Button(text='ELIMINAR', command=self.del_produto, style='my.TButton')
        botao_eliminar.grid(row=5, column=0, sticky=W + E)
        botao_editar = ttk.Button(text='EDITAR', command = self.edit_produto, style='my.TButton')
        botao_editar.grid(row=5, column=1, sticky=W + E)

        # Chamada ao método get_produtos() para obter a listagem de produtos ao início da app
        self.get_produtos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con: # inicia-se uma conexão com a base de dados (alias con)
            cursor = con.cursor() # criamos um cursor de conexão para poder operar na db
            resultado = cursor.execute(consulta, parametros) # Preparar a consulta SQL (com parametros, se houver)
            con.commit() # Executar a consulta SQL
        return resultado # Restituir resultado da consulta SQL

    def get_produtos(self):
        # Primeiro vamos limpar a tabela se tiver dados residuais ou antigos
        registo_tabela = self.tabela.get_children() #obter todos os dados da tabela
        for linha in registo_tabela:
            self.tabela.delete(linha)

        #Consulta SQL
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registos_db = self.db_consulta(query) # Chama-se o método

        # Escrever os dados no ecrã
        for linha in registos_db:
            print(linha) # print para verificar por consola os dados
            self.tabela.insert('',0, text=linha[1], values=linha[2])

    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)' #Consulta SQL sem os dados
            parametros = (self.nome.get(), self.preco.get()) # Parametros da consulta SQL
            self.db_consulta(query,parametros)
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get())
            # Label localizado entre o botão e a tabela
            self.nome.delete(0, END) # apagar o campo nome do formulário
            self.preco.delete(0, END) # apagar o campo preço do formulário
            # print('Dados Guardados') este print foi substituído pela mensagem acima
            # Para debug
            # print(self.nome.get())
            # print(self.preco.get())
        elif self.validacao_nome() and self.validacao_preco() == False:
            print("O preço é obrigatório")
            self.mensagem['text'] = "O preço é obrigatório"
        elif self.validacao_nome() == False and self.validacao_preco():
            print("O nome é obrigatório")
            self.mensagem['text'] = "O nome é obrigatório"
        else:
            print("O nome e o preço são obrigatórios")
            self.mensagem['text'] = "O nome e o preço são obrigatórios"

        self.get_produtos() # Quando se finalizar a inserção de dados voltamos a invocar este método para atualizar o conteúdo e ver as alterações

    def del_produto(self):
        # Debug
        #print(self.tabela.item(self.tabela.selection()))
        #print(self.tabela.item(self.tabela.selection())['text'])
        #print(self.tabela.item(self.tabela.selection())['values'])
        #print(self.tabela.item(self.tabela.selection())['values'][0])

        self.mensagem['text'] = ''  # Mensagem inicialmente vazia
        # Comprovação de que se selecione um produto para poder eliminá-lo
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return

        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = 'DELETE FROM produto WHERE nome = ?' # Consulta SQL
        self.db_consulta(query, (nome,)) # Executar a consulta
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        self.get_produtos() # Atualizar a tabela de produtos

    def edit_produto(self):
        self.mensagem['text'] = '' # Mensagem inicialmente vazia
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        nome = self.tabela.item(self.tabela.selection())['text']
        old_preco = self.tabela.item(self.tabela.selection())['values'][0] # O preço encontra-se dentro de uma lista

        self.janela_editar = Toplevel() # Criar uma janela à frente da principal
        self.janela_editar.title = 'Editar Produto' # Título da janela
        self.janela_editar.resizable(1,1) # Ativar a redimensão da janela. Para desativar: (0,0)
        self.janela_editar.wm_iconbitmap('recursos/icon.ico') # Ícone da janela

        titulo = Label(self.janela_editar, text = 'Edição de Produtos', font = ('Calibri', 50, 'bold'))
        titulo.grid(column = 0, row = 0)

        # Criação do recipiente Frame da janela de Edição de Produtos
        frame_ep = LabelFrame(self.janela_editar, text = 'Editar o seguinte Produto', font=('Calibri', 16, 'bold')) # frame_ep = Frame Editar Produto
        frame_ep.grid(row = 1, column = 0, columnspan = 20, pady = 20)

        #Label Nome Antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text = 'Nome Antigo: ', font=('Calibri', 13)) # Etiqueta de text localizada no frame
        self.etiqueta_nome_antigo.grid(row = 2, column = 0)
        #Entry nome antigo (texto que não poderá se modificar)
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome), state='readonly', font=('Calibri', 13))
        self.input_nome_antigo.grid(row = 2, column = 1)

        #Label Nome Novo
        self.etiqueta_nome_novo = Label(frame_ep, text = 'Nome Novo: ', font=('Calibri', 13))
        self.etiqueta_nome_novo.grid(row = 3, column = 0)
        #Entry nome novo (texto que poderá se modificar)
        self.input_nome_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nome_novo.grid(row = 3, column = 1)
        self. input_nome_novo.focus() # Para que a seta do rato vá a esta Entry ao início

        # Label Preço Antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text='Preço Antigo: ', font=('Calibri', 13))  # Etiqueta de text localizada no frame
        self.etiqueta_preco_antigo.grid(row=4, column=0)
        # Entry preço antigo (texto que não poderá se modificar)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco),
                                       state='readonly', font=('Calibri', 13))
        self.input_preco_antigo.grid(row=4, column=1)

        # Label Preço Novo
        self.etiqueta_preco_novo = Label(frame_ep, text='Preço Novo: ', font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry preço novo (texto que poderá se modificar)
        self.input_preco_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text = 'Atualizar Produto', style='my.TButton', command = lambda:self.atualizar_produtos(self.input_nome_novo.get(),
                                                                  self.input_nome_antigo.get(),
                                                                  self.input_preco_novo.get(),
                                                                  self.input_preco_antigo.get()))
        self.botao_atualizar.grid(row = 6, columnspan = 2, sticky = W + E)

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '' and novo_preco != '':
            #Se o utilizador escreve novo nome e novo preço, mudam-se ambos
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            #Se o utilizador deixa vazio o novo preço, mantêm-se o anterior
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            #Se o utilizador deixa vazio o novo nome, mantêm-se o anterior
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        if (produto_modificado):
            self.db_consulta(query, parametros)
            self.janela_editar.destroy() #Fechar a janela de edição de Produtos
            self.mensagem['text'] = 'O Produto {} foi atualizado com êxito'.format(antigo_nome) #Mostrar mensagem ao utilizador
            self.get_produtos() #Atualizar a tabela
        else:
            self.janela_editar.destroy()  # Fechar a janela de edição de Produtos
            self.mensagem['text'] = 'O Produto {} NÃO foi atualizado com êxito'.format(antigo_nome)  # Mostrar mensagem ao utilizador



if __name__ == '__main__':
    root = Tk() # instância da janela principal
    app = Produto(root) # envia-se para a classe Produto o controlo da janela root
    root.mainloop() # começamos o ciclo de aplicação, comparado a while True