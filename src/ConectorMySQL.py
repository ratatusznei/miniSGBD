
#comandos em git
#mostra o status dos arquivos, se foram upados ou não
#git status
# adciciona todos arquivos a fila de push
#git add .
#comentário para fazer o push
#git commit -m "comentarios"
#push sobe todos os arquivos
#git push


import mysql.connector

class MySQLConnection:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def getConexao(self):
        return self.connection
    
    #Quando for pegar a tabela, faça algo como nomeTabelaa =  tabelas[6][0]
    #pois o retorno dos nomes das tabelas é uma tupla.
    def getTabela(self,nomeTabela):
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
            return False

    #desconecta o banco de dados
    def desconectar(self):
        if self.connection:
            self.connection.close()
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
        
    #tabelas selecionadas deve ser um vetor de True e False, que indica se deve-se importar aquela tabela
    def setTabelasImportar(self,tabelasSelecionadas):
        tabelas = self.getTodasTabelas()
        i = 0
        for tabela in tabelas:
            if(tabelasSelecionadas[i]):
                self.importarTabelaCSV(tabela)
            i+=1

            
    def importarTabelaCSV(self,nomeTabela):
        novaTabela = open(nomeTabela,"w")


# Exemplo de uso:
#connection = MySQLConnection('localhost', 'root', '033002970', 'employees')
#connection.conectar()
#
#tabelas = connection.getTodasTabelas()
#
#nomeTabelaa =  tabelas[6][0]
#print(nomeTabelaa)
#salaries = connection.getTabela(nomeTabelaa)
#
#for salario in salaries:
#    print(salario)
#
#connection.desconectar()
