import csv
import re

from GerenciadorArquivos import GerenciadorArquivos

class CRUD:
    def __init__(self):
        self.nomesTabelas = None
        self.numeroTabelas = 0
        self.elementosValidos = []

    #não retorna nada, apenas carrega na memória os arquivos do banco escolhido
    #def carregarBanco(self,nomeBanco):

    #retorna todos os bancos salvos
    #def getDataBases(self):
    
    #retorna a intersecção de duas tabelas sem repetir elementos (A AND B)
    def AND_PRIVADA(self,tabelaA,tabelaB):
        i = 1
        j = 1
        tabelaC = []
        while(i < len(tabelaA)):
            while(j < len(tabelaB)):
                if(tabelaA[i][0] == tabelaB[j][0]):
                    tabelaC.append(tabelaA[i])
                j += 1
            i += 1
        
        return tabelaC
        
    #retorna a jução, sem repeticao, de duas tabelas (A OR B)
    def OR_PRIVADA(self,tabelaA,tabelaB):
        i = 1
        j = 1
        tabelaC = tabelaA
        while(i < len(tabelaB)):
            jaExiste = False
            j = 0
            while(j < len(tabelaC)):
                pos = j
                if(tabelaC[i][0] == tabelaB[j][0]):
                    jaExiste = True
                    break
                    
                j += 1
            if jaExiste == False:
                tabelaC.append(tabelaB[pos][0])
            i += 1
        
        return tabelaC

    #retorna o indice da linha que possue a tabela fornecida
    def getPosicaoNoBanco(self,banco,coluna = None,tabela = None,isTabela = True):
        i = 0
        j = 0
        pos = [-1,-1]
        while(i < len(banco)):
            if isTabela:
                j = 0
                if tabela in banco[i][0]:
                    pos = [i,j]
                    return pos
            else:
                j = 0
                while(j < len(banco[i])):
                    if( coluna in banco[i][j]):
                        pos = [i,j-1]
                        return pos
                    j += 1
            i += 1

        return pos

    
    #retorna uma lista de elementos válidos
    #consideracao : 
    #condicao = "coluna = 40000"
    #banco = "employees" ou banco = "university"

    def WHERE_PRIVADA(self,condicao,gerente:GerenciadorArquivos) :

        banco = gerente.GETDATABASE(gerente.bancoAtual)
        elementosValidos = []

        i = 0
        while i <= len(condicao) - 2:
            coluna1 = condicao[i]
            pos1 = self.getPosicaoNoBanco(banco=banco,coluna=coluna1,isTabela=False)
            i += 1
            operacao = condicao[i]
            i += 1
            coluna2 = condicao[i]
            pos2 = self.getPosicaoNoBanco(banco=banco,coluna=coluna2,isTabela=False)
            #caso sejam dois valores
            if(pos1[0] == -1 and pos1[1] == -1 and pos2[0] == -1 and pos2[1] == -1):
                print("CONDICÃO INVALIDA NO WHERE.")
            #caso seja um valor e uma coluna
            else:
                #a primeira coluna um valor e a segunda uma coluna de uma tabela
                if(pos1[0] == -1 and pos1[1] == -1):
                    tabela2 = gerente.GETTABLE(banco[pos2[0]][0])
                    elementosValidos = self.operadoresValor_PRIVADA(tabela2,pos2[1],coluna1,operacao)
                #a segunda coluna um valor e a primeira uma coluna de uma tabela
                elif(pos2[0] == -1 and pos2[1] == -1):
                    tabela1 = gerente.GETTABLE(banco[pos1[0]][0])
                    elementosValidos = self.operadoresValor_PRIVADA(tabela1,pos1[1],coluna2,operacao)
                
                return elementosValidos
                



    #efetua a verificação de comparação de um valor com um campo de uma tabela
    def operadoresValor_PRIVADA(self,tabela,coluna,valor,operacao):
        elementosValidos = []
        if operacao == "=":
            for tab in tabela:
                if(valor == tab[coluna]):
                    elementosValidos.append(tab)

        elif operacao == ">":
            for tab in tabela:
                if(valor > tab[coluna]):
                    elementosValidos.append(tab)

        elif operacao == "<":
            for tab in tabela:
                if(valor < tab[coluna]):
                    elementosValidos.append(tab)
        else:
            elementosValidos = self.operadoresValor_PRIVADA(tabela,coluna,valor,"=")
            if(operacao == ">"):
                elementosDiferentes = self.operadoresValor_PRIVADA(tabela,coluna,valor,">")
                for elemento in elementosDiferentes:
                    elementosValidos.append(elemento)
            if(operacao == "<"):
                elementosDiferentes = self.operadoresValor_PRIVADA(tabela,coluna,valor,"<")
                for elemento in elementosDiferentes:
                    elementosValidos.append(elemento)

        return elementosValidos
    
    #efetua a verificacao entre duas colunas de duas tabelas
    def operadoresTabela_PRIVADA(self,tabela1,tabela2,idexCol1,indexCol2,operador):
        return 0

    def READ(self,consulta):
        consulta = "Feita"
    
    def UPDATE(self,consulta):
        consulta = "Feita"

    def DELETE(self,consulta,gerente:GerenciadorArquivos):
        consulta = self.preTratamento_PRIVADA(consulta,True)
        tabela = gerente.GETTABLE(consulta[2])
        condicao = consulta[4:len(consulta)]

        listaDel = self.WHERE_PRIVADA(condicao,gerente)

        i = len(tabela) - 1
        j = 0
        elementosAlterados = 0
        while(i >= 0):
            j = 0
            while(j < len(listaDel)):
                if(listaDel[j][0] == tabela[i][0]):
                    tabela.pop(i)
                    elementosAlterados += 1
                j += 1
            i -= 1
        print("Um total de " + str(elementosAlterados) + " foram afetados.")

        gerente.CREATETABLE(gerente.bancoAtual,consulta[2],tabela)


    def INSERT(self,comandoSQL,gerente):
        comandos = self.preTratamento_PRIVADA(comandoSQL)
        cabecalho = self.quebraEmColunas_PRIVADA(comandos[2])
        valores = self.quebraEmColunas_PRIVADA(comandos[3])
        tabela = gerente.GETTABLE(cabecalho[0])

        novaLinha = []
        if len(cabecalho) <= 2 :
            pulaUm = False
            for valor in valores: 
                if pulaUm:
                    novaLinha.append(valor)
                pulaUm = True
            
        else:
            j = 0
            while j < len(tabela[0]):
                coluna = tabela[0][j]
                i = 1
                while i < len(cabecalho):
                    if coluna == cabecalho[i]:
                        novaLinha.append(valores[i])
                    i += 1
                j += 1

        tabela.append(novaLinha)
        gerente.SAVETABLE(cabecalho[0],tabela)


                    

    #quebra department(coluna1,coluna2) em vet = [department,coluna1,coluna2]
    def quebraEmColunas_PRIVADA(self,string) -> str:
        retorno = string.replace("(",",")
        retorno = retorno.replace(")","")
        retorno = retorno.replace("'","")
        retorno = retorno.replace('"',"")
        retorno = retorno.split(",")
        return retorno

    #trata da string para que ela tenha somente um espaço entre os comando, não tenha espaço entre o comando e o parenteses
    #e por fim devolva tudo em vetor da forma
    #INSERT , INTO , department(coluna1,coluna2) , VALUES(valor1,valor2)
    def preTratamento_PRIVADA(self,string,where = False):
        if(where == False):
            pattern = r"\s+(?= \()"
            string = re.sub(pattern, "", string)
            string = re.sub(r"\s+", " ", string)
            pattern = r"(\b\w+\b|\(.*?\)|VALUES\(.+?\))"
            vet = re.findall(pattern, string)

            i = 0
            retorno = []
            while(i < len(vet)):
                if(i == 2 or i == 4):
                    retorno.append(vet[i] + vet[i+1])
                    i += 1
                else:
                    retorno.append(vet[i])
                i += 1

            return retorno
        else:
            string = re.sub(r"\s+", " ", string)
            vet = string.split(" ")
            for v in vet:
                v = re.sub(r"\s+", "", v)
            return vet
    
    #teste
    def PRINTCSV(self,nomeTabela):
        with open(nomeTabela + ".csv", 'r') as arquivo:
            reader = csv.reader(arquivo)
            for linha in reader:
                print(linha)
    #def INSERT(self,nomeTabela,elemento):
        
# test = CRUD()
# test.INSERT("INSERT   INTO      gato (cor,especie,tamanho,ID) VALUES('pelado','pelado do imalaia','14cm',2315)")

# gerente = GerenciadorArquivos()
# gerente.bancoAtual = "employees"
# test = CRUD()
# test.DELETE("DELETE FROM salaries WHERE    salary = 60117",gerente)