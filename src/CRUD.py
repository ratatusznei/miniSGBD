import csv

class CRUD:
    def __init__(self):
        self.nomesTabelas = None
        self.numeroTabelas = 0

    #não retorna nada, apenas carrega na memória os arquivos do banco escolhido
    #def carregarBanco(self,nomeBanco):

    #retorna todos os bancos salvos
    #def getDataBases(self):

    #O arquivo que será criado tem como nome o banco de dados, e guarda na primeira coluna os nomes das tabelas
    #que foram salvas em .csv, nas colunas subsequentes estão as colunas da tabela
    #university.csv (nome do arquivo)
    #instructor |   id   | dept_name | ...
    #strudent   |   id   | name      | ...
    #...
    #
    #Como controle geral, existe um txt com nome bancos.txt que salva os nomes dos bancos salvos.
    def CREATEDATABASEFILE(self,nomeDB,linhas):
        with open(nomeDB + ".csv", 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            #writer.writerow(['Nome', 'Idade', 'Cidade'])  # Escreve o cabeçalho das colunas
            for linha in linhas:
                writer.writerow(linha)

    #As tabelas serão salvas como instructor.csv, onde suas colunas são as colunas das tabelas.
    def CREATETABLE(self,nomeTabela, colunas):
        with open(nomeTabela, 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(colunas)

    #teste
    def PRINTCSV(self,nomeTabela):
        with open(nomeTabela + ".csv", 'r') as arquivo:
            reader = csv.reader(arquivo)
            for linha in reader:
                print(linha)
    #def INSERT(self,nomeTabela,elemento):
        

cr = CRUD()
nomeBanco = "university"
linhas = [['instructor','id','dept_name'],
          ['student','id','name'],
          ['department','id','budget','title']]
#cr.CREATEDATABASEFILE(nomeBanco,linhas)
cr.PRINTCSV(nomeBanco)