
from ConectorMySQL import ConectorMySQL
from GerenciadorArquivos import GerenciadorArquivos
senhaGeral = "033002970"

class Interface:
    def __init__(self):
        self.conexao = None
        self.bancoAtual = None
        self.gerente = GerenciadorArquivos()
        self.tabelas = []
        self.colunas = []

    #estado 0
    def menuInicial(self):
        print("Bem vindo ao MiniSGBD.")
        print("Pressione 1 para importar um novo banco de dados;")
        print("Pressione 2 para abrir um banco de dados já importado.")
        print("Desenvolvido por Robson e Fernando - nenhum direito reservado")
        novoEstado = input("")
        if(novoEstado == 1 or novoEstado == 2):
            if(novoEstado == 1):
                self.menuNovoBD()
            else :
                self.menuBDSalvos()
        else:
            print("Entrada inválida.")
            self.menuInicial()

    #estado 1
    def menuNovoBD(self):
        print("Para adicionar um novo banco digite os dados do servidor MySQL como descrito abaixo:")
        print("Para voltar ao menu anterior digite 0 .")
        print("Caso de teste: Digite 1 para carregar o banco Employees.")
        print("")
        user = input("Digite o usuário : ")
        if(user != 1):
            if(user == 0):
                self.menuInicial()

            host = input("Digite o host : ")
            self.menuInicial()
            senha = input("Digite a senha : ")
            self.menuInicial()
            banco = input("Digite o nome do banco de dados : ")
            self.menuInicial()
            self.conectarMySQL_PRIVADO(host,user,senha,banco)
            if(self.coneccao.conectar()):
                print("Conexao realizada com sucesso!.")
            else:
                print("Algo deu errado, a conexão falhou. :( ")
        else:
            self.conectarMySQL_PRIVADO("localhost","root",senhaGeral,"employees")


    #estado 2
    def menuBDSalvos(self):
        print("Regiao ainda nao codada... :( ")
        self.menuInicial()

    #estado 3
    def menuSelecionarTabelas(self):
        print("Abaixo então todas as tabelas que voce pode importar.")
        print("Digite o número correspondente, para finalizar digite -1.")
        print("Digite 0 para importar todas.")
        print("")
        #parte para testes
        self.conectarMySQL_PRIVADO("localhost","root",senhaGeral,"employees")
        #fim da parte de testes

        #mostra as tabelas
        i = 0 
        self.pegarTabelas_PRIVADO()
        for tabela in self.tabelas:
            i+=1
            print(str(i) + " : " + tabela)

        selecionados = []
        selecionados.append(0)
        selecionados.append(3)
        selecionados.append(4)
        selecionados.append(6)
        tabelaAux = []

        #adiciona as tabelas
        for select in selecionados:
            tabelaAux.append(self.tabelas[select])

        self.tabelas.clear()
        self.tabelas = tabelaAux

        self.pegarColunas_PRIVADO()

        self.gerente.CREATEDATABASE(self.bancoAtual,self.tabelas,self.colunas)

        self.criarTabelas_PRIVADO()

        
    def menuBancosSalvos(self):
        bancos = self.gerente.GETDATABASES()
        print("Abaixo estão todos os bancos já salvos:")
        i = 1
        for banco in bancos:
            print( str(i) + " : " + banco[0])
            i += 1
        #terminar......... tem que permitir o usuário escolher o banco
        selecionado = "employees"
        self.bancoAtual = selecionado
        self.recuperarBancoLocal_PRIVADO()

        print(self.tabelas)
        print("")
        print(self.colunas)


    def recuperarBancoLocal_PRIVADO(self):
        banco = self.gerente.GETDATABASE(self.bancoAtual)
        self.tabelas.clear()
        self.tabelas = []
        for tabela in banco:
            self.tabelas.append(tabela[0])
            auxiliar = []
            jota = False
            for coluna in tabela:
                if(jota):
                    auxiliar.append(coluna)
                jota = True
            self.colunas.append(auxiliar)


    def conectarMySQL_PRIVADO(self,host,user,senha,banco):
        self.conexao = ConectorMySQL(host,user,senha,banco)
        self.conexao.conectar()
        self.bancoAtual = banco

    def pegarTabelas_PRIVADO(self):
        #verificando a conexao
        if(self.conexao):
            auxiliar = self.conexao.getTodasTabelas()
            self.tabelas.clear()
            self.tabelas = []
            for tabela in auxiliar:
                self.tabelas.append(tabela[0])
        else:
            print("Erro, conexao não estabelecida com o banco de dados. (pegarTabelas)")

    def criarTabelas_PRIVADO(self):
        for tabela in self.tabelas:
            elementos = self.conexao.getElementosTabela(tabela)
            self.gerente.CREATETABLE(self.bancoAtual,tabela,elementos)

    def pegarColunas_PRIVADO(self):
        if(self.conexao):
            for auxiliar in self.tabelas:
                self.colunas.append(self.conexao.getNomesColunas(auxiliar))

    def encerrar(self):
        self.conexao.desconectar()


inter = Interface()
inter.menuBancosSalvos()