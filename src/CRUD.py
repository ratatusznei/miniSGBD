import csv

class CRUD:
    def __init__(self):
        self.nomesTabelas = None
        self.numeroTabelas = 0

    def CREATETABLE(self,nomeTabela,elementos):
        try:
            with open(nomeTabela,"w") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerows(elementos)
                
            self.nomesTabelas[self.numeroTabelas] = nomeTabela
            self.numeroTabelas += 1
        except:
            print("Não foi possível criar o arquivo CSV.")