import os
import csv


# essa parte eu não utilizo ainda
class Tabela:
    def __init__(self,nome,arquivo):
        self.nome = nome
        self.arquivo = arquivo

class ListaTabelas:
    def __init__(self):
        self.tabelas = []
    
    def add(self,nome,tabela):
        i = 0
        while i < len(self.tabelas): 
            if self.tabelas[i].nome == nome:
                self.tabelas.pop(i)
                break
            i += 1

        nova = Tabela(nome,tabela)
        self.tabelas.append(nova)

    def find(self,nomeTabela):
        for tab in self.tabelas:
            if( tab.nome == nomeTabela):
                return tab.arquivo
        
        return None

    


#Classe responsável por criar e sobrepor os arquivos existentes ou não

class GerenciadorArquivos:
    #Como controle geral, existe um csv com nome bancos.cvs que salva os nomes dos bancos salvos.
    def __init__(self):
        self.arquivo = "bancos.dat"
        self.bancoAtual = ""
        self.tabelaAtual = ""
        self.listaTabelas = ListaTabelas()

        # Verificando se existe
        if os.path.isfile(self.arquivo) == False:
            # Criando
            with open(self.arquivo, 'w', newline='') as arquivo:
                # Escrevendo
                arquivo.write('')
                arquivo.close()
            

    #O arquivo que será criado tem como nome o banco de dados, e guarda na primeira coluna os nomes das tabelas
    #que foram salvas em .csv, nas colunas subsequentes estão as colunas da tabela
    #banco_university.csv (nome do arquivo)
    #instructor |   id   | dept_name | ...
    #strudent   |   id   | name      | ...
    #...
    def CREATEDATABASE(self,nomeDB,nomesTabelas,nomesColunas) -> bool:
        self.bancoAtual = nomeDB
        #verifica se o nome é uma string, se for ela vira um vetor de uma só posicao
        if isinstance(nomeDB,str):
            nomeDB = [nomeDB]
        #verificamos se já exite em bancos.csv
        existe = False
        with open(self.arquivo,"r") as bancos:
            for banco in bancos:
                if nomeDB[0] in banco:
                    existe = True

        if(existe == False):
            self.SOBREPORBANCO_PRIVADO(nomeDB,nomesTabelas,nomesColunas)
            return True
        #se o arquivo já existe, apagamos e substituimos ele
        else:
            print("O banco de dados " + nomeDB[0] +" já existe, deseja sobrepor?")
            sobrepor = input("S/N")
            if(sobrepor == "S" or sobrepor == "s"):
                self.SOBREPORBANCO_PRIVADO(nomeDB,nomesTabelas,nomesColunas)
                return True
            else:
                return False
                ## terminar...........................

    #nomeTabela é o nome do arquivo e o próprio nome da tabela
    #cabecalho refere-se aos nomes das colunas das tabelas
    #linhas são os elementos da tabela
    def CREATETABLE(self,banco, tabela, linhas):
        self.tabelaAtual = tabela
        #abro o arquivo do banco 
        with open(banco + ".dat", 'r', newline='') as arquivo:
            leitor = csv.reader(arquivo)
            cabecalho = []
            #percorro procurando a tabela
            for i in leitor:
                #se foi encontrada eu salvo o resto da linha
                #que contem as colunas da tabela
                if(tabela in i[0]):
                    jota = False
                    for coluna in i:
                        if(jota):
                            cabecalho.append(coluna)
                        jota = True
                    break
            
            with open(tabela + ".csv", 'w', newline='') as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(cabecalho)

                for linha in linhas:
                    escritor.writerow(linha)


    def SOBREPORBANCO_PRIVADO(self,nomeDB,nomesTabelas,nomesColunas):
            # Abrir o arquivo em modo de leitura e ler o conteúdo existente
            with open(self.arquivo, 'r') as arquivo:
                leitor = csv.reader(arquivo)
                conteudo_existente = list(leitor)

            # Abrir o arquivo em modo de escrita e reescrever todo o conteúdo
            with open(self.arquivo, 'w', newline='') as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerows(conteudo_existente)
                escritor.writerow(nomeDB)

            #criar o arquivo deste banco em específico
            with open( nomeDB[0] + ".dat", 'w', newline='') as arquivo:
                escritor = csv.writer(arquivo)
                i = 0
                for linha in nomesColunas:
                    aux = [nomesTabelas[i]] + linha
                    escritor.writerow(aux)
                    i += 1
            #deixa ele salvo em memória
            with open(nomeDB[0] + ".dat", 'r') as arquivo:
                self.bancoAtual =  csv.reader(arquivo)
            
            

    def GETDATABASES(self):
        with open(self.arquivo, 'r') as arquivo:
            leitor = csv.reader(arquivo)
            conteudo = list(leitor)
            return conteudo
        return None
    
    def GETDATABASE(self,nomeBanco):
        with open( nomeBanco + ".dat", 'r') as arquivo:
            leitor = csv.reader(arquivo)
            conteudo = list(leitor)
            return conteudo
        return None

    def GETTABLE(self,nomeTabela):
        retorno = self.listaTabelas.find(nomeTabela)
        if(retorno == None):
            with open(nomeTabela + ".csv", 'r') as arquivo:
                leitor = csv.reader(arquivo)
                conteudo = list(leitor)
                self.listaTabelas.add(nomeTabela,conteudo)
                return conteudo
            return None
        return retorno

    def SAVETABLE(self,nomeTabela,tabela):
        self.listaTabelas.add(nomeTabela,tabela)
        with open(nomeTabela + ".csv", 'w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            for linha in tabela:
                escritor.writerow(linha)

         
#banco = "employees"
#tabelas = [
#    ['instructor','id','dept_name'],
#    ['strudent','id','name']
#]
#gerente = GerenciadorArquivos()
#gerente.__init__()
#gerente.CREATEDATABASE(banco,tabelas)
