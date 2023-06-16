
from ConectorMySQL import ConectorMySQL
from GerenciadorArquivos import GerenciadorArquivos
from CRUD import CRUD
import os
import time
import threading

tempo0 = 0.5
tempo2 = 2
senhaGeral = "033002970"

class Interface:
    def __init__(self):
        self.conexao = None
        self.bancoAtual = None
        self.gerente = GerenciadorArquivos()
        self.tabelas = []
        self.colunas = []
        self.loadConcluido = False
        self.crud = CRUD()

    #estado 0 
    def menuInicial(self):
        print("----------Bem vindo ao MiniSGBD.----------")
        print("Pressione 1 para importar um novo banco de dados;")
        print("Pressione 2 para abrir um banco de dados já importado.")
        print("")
        print("")
        print("")
        print("Desenvolvido por Robson e Fernando - nenhum direito reservado")
        novoEstado = input("")
        os.system("clear")
        if(int(novoEstado) == 1 or int(novoEstado) == 2):
            if(int(novoEstado) == 1):
                self.menuNovoBD()
            else :
                self.menuBancosSalvos()
        else:
            print("Entrada inválida.")
            time.sleep(tempo2)
            self.menuInicial()

    #estado 1  para adicionar um novo banco de dados
    def menuNovoBD(self):
        print("Digite 0 para voltar ao menu anterior.")
        print("Digite 1 para carregar o banco Employees. (testes)")
        print("Digite o usuário para conectar com o MySQL.")
        print("")
        user = input("")
        if(int(user) == 0):
            self.menuInicial()
        elif(int(user) == 1):
            self.conectarMySQL_PRIVADO("localhost","root",senhaGeral,"employees")
            if(self.conexao.conectar()):
                self.pegarTabelas_PRIVADO()
                os.system("clear")
                print("Conexao realizada com sucesso!.")
                time.sleep(tempo2)
                self.menuSelecionarTabelas()
        else:
            host = input("Digite o host : ")
            self.menuInicial()
            senha = input("Digite a senha : ")
            self.menuInicial()
            banco = input("Digite o nome do banco de dados : ")
            self.menuInicial()
            self.conectarMySQL_PRIVADO(host,user,senha,banco)
            if(self.conexao.conectar()):
                self.pegarTabelas_PRIVADO()
                os.system("clear")
                print("Conexao realizada com sucesso!.")
                time.sleep(tempo2)
                self.menuSelecionarTabelas()
            else:
                os.system("clear")
                print("Algo deu errado, a conexão falhou. :( ")
                time.sleep(tempo2)
                self.menuNovoBD()
            
    #estado 2  para selecionar um banco de dados já salvo
    def menuBancosSalvos(self):
        bancos = self.gerente.GETDATABASES()
        print("Abaixo estão todos os bancos já salvos:")
        i = 1
        for banco in bancos:
            print( str(i) + " : " + banco[i - 1])
            i += 1
        #terminar......... tem que permitir o usuário escolher o banco
        print("")
        selecionado = input("Digite o banco que deseja carregar para a memória.")
        print("")
        
        if(selecionado.isdigit()):
            self.bancoAtual = banco[int(selecionado) - 1]
            self.recuperarBancoLocal_PRIVADO()
            os.system("clear")
            self.menuConsultaSQL()
        else:
            print("Entrada inválida")
            time.sleep(tempo2)
            self.menuBancosSalvos()

    #estado 3  depois do menu Novo banco, vem para este, para selecionar as tabelas
    def menuSelecionarTabelas(self):
        

        entrada = 1
        selecionados = [0] * len(self.tabelas)
        marcador = ["","     OK"]
        while(entrada != 0):
            print("Digite END ara finalizar.")
            print("Digite ALL para importar todas.")
            print("")
            print("Abaixo então todas as tabelas que voce pode importar, digite o número correspondente para incluila.")

            #mostra as tabelas
            i = 1 
            
            for tabela in self.tabelas:
                print(str(i) + " : " + tabela + marcador[selecionados[i-1]])
                i += 1
            
            entrada = input("")
            os.system("clear")
            if "ALL" in entrada or "all" in entrada:
                for j in range(len(selecionados)):
                    selecionados[j] = 1
                    entrada = 0
                    os.system("clear")
                    print("Todas as tabelas foram selecionadas.")
                    print("Aquarde enquanto os dados são requisitados no MySQL.")
                    time.sleep(tempo2)
                    break
            elif entrada.isdigit():
                if(int(entrada) <= len(selecionados)):
                    selecionados[int(entrada) - 1] = 1
            elif "end" in entrada or "END" in entrada:
                entrada = 0
            else:
                print("Entrada inválida.")
                    
        self.loadConcluido = False
        thread = threading.Thread(target=self.telaLoad)
        thread.start()

        tabelaAux = []

        #adiciona as tabelas
        i = 0
        for select in selecionados:
            if select:
                tabelaAux.append(self.tabelas[i])
            i += 1

        self.tabelas.clear()
        self.tabelas = tabelaAux

        self.pegarColunas_PRIVADO()

        self.gerente.CREATEDATABASE(self.bancoAtual,self.tabelas,self.colunas)

        self.criarTabelas_PRIVADO()

        self.loadConcluido = True
        thread.join()

    #estado 4
    def menuConsultaSQL(self):
        os.system("clear")
        print("Sessão de consultas em SQL, digite sua consulta ou um dos valores abaixo para continuar.")
        print("")
        print("")
        print("Digite 0 para voltar ao inicio do programa.")
        print("Digite 1 para listar todos os comandos aceitos neste programa.")
        
        consulta = input("")

        if(consulta.isdigit()):
            consulta = int(consulta)
            if(consulta == 0):
                self.menuInicial()
            elif(consulta == 1):
                print("")
                print(" Básicos")
                print(" INSERT - DELETE - UPDATE - CREATE - READ ")
                print("")
                print("Digite 0 coisa para voltar a consulta.")
                consulta = input("")
                self.menuConsultaSQL()

        #parte do fernando
        #se a consulta for um simples CRUD, preciso dessa informação para fazer o que segue abaixo

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

    def telaLoad(self):
        texto = "Carregando."
        i = 0
        while(self.loadConcluido == False):
            if(i > 4):
                i = 0
                texto = "Carregando."
            os.system("clear")
            print(texto)
            time.sleep(tempo0)
            texto = texto + "."
            i += 1
            
        os.system("clear")
        print("Concluido !")
        time.sleep(tempo2)



inter = Interface()
inter.menuInicial()