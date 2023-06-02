

import mysql.connector

class MySQLConnection:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    #retorna verdadeiro se a conexão foi realizada
    def conectado(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return True
        except mysql.connector.Error as error:
            return False

    #desconecta o banco de dados
    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("Fim da conexão.")

    #retorna todas as tabelas existentes no banco de dados conectado
    def getTabelas(self):
        if self.conectado():
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            return cursor.fetchall()
        else:
            print("A conexão não está estabelecida.")
            return None
        
    #tabelas selecionadas deve ser um vetor de True e False, que indica se deve-se importar aquela tabela
    def setTabelasImportar(self,tabelasSelecionadas):
        tabelas = self.getTabelas()
        i = 0
        for tabela in tabelas:
            if(tabelasSelecionadas[i]):
                self.importarTabelaCSV(tabela)
            i+=1

    def importarTabelaCSV(self,nomeTabela):
        novaTabela = open(nomeTabela,"w")


# Exemplo de uso:
connection = MySQLConnection('localhost', 'root', '033002970', 'employees')

tabelas = connection.getTabelas()

for tabela in tabelas:
    print(tabela)

connection.desconectar()
