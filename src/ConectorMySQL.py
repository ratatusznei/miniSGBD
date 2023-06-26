
#comandos em git
#mostra o status dos arquivos, se foram upados ou não
#git status
# adciciona todos arquivos a fila de push
#git add .
#comentário para fazer o push
#git commit -m "comentarios"
#push sobe todos os arquivos
#git push

from CRUD import CRUD

import mysql.connector

class ConectorMySQL:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.load = 0


    def bancoConectado(self) -> bool:
        return self.connection != None and self.connection.is_connected()

    def getConexao(self):
        return self.connection
    
    #Quando for pegar a tabela, faça algo como nomeTabelaa =  tabelas[6][0]
    #pois o retorno dos nomes das tabelas é uma tupla.
    def getElementosTabela(self,nomeTabela):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM " + nomeTabela + ";")
            return cursor.fetchall()
        else :
            print("Nenhuma conexão encontrada, não foi possível carregar a tabela.")

    #retorna verdadeiro se a conexão foi realizada
    def conectar(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return True
        except mysql.connector.Error as error:
            print("Erro ao conectar - MYSQL ERROR : ",error)
            return False

    #desconecta o banco de dados
    def desconectar(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Fim da conexão.")

    #retorna todas as tabelas existentes no banco de dados conectado
    def getTodasTabelas(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            return cursor.fetchall()
        else:
            print("A conexão não está estabelecida.")
            return None
    
    def getNomesColunas(self,nomeTabela):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW COLUMNS FROM " + nomeTabela + ";")
            retorno = []
            for cabecalho in cursor.fetchall():
                retorno.append(cabecalho[0])
            return retorno
        return None
    
