import csv

class CRUD:
    def __init__(self):
        self.nomesTabelas = None
        self.numeroTabelas = 0

    #não retorna nada, apenas carrega na memória os arquivos do banco escolhido
    #def carregarBanco(self,nomeBanco):

    #retorna todos os bancos salvos
    #def getDataBases(self):

    def CREATE(self,consulta):
        consulta = "Feita"

    def READ(self,consulta):
        consulta = "Feita"
    
    def UPDATE(self,consulta):
        consulta = "Feita"

    def DELETE(self,consulta):
        consulta = "Feita"

    #teste
    def PRINTCSV(self,nomeTabela):
        with open(nomeTabela + ".csv", 'r') as arquivo:
            reader = csv.reader(arquivo)
            for linha in reader:
                print(linha)
    #def INSERT(self,nomeTabela,elemento):
        
