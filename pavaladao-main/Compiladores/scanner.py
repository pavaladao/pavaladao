import pandas as pd
from static import palavras_reservadas

class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo


class Scanner:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self, tabela_estados, entrada):
        self.estados_finais = {
            (1,'Num'),
            (3,'Num'),
            (6,'Num'),
            (8,'Lit'),
            (9,'id'),
            (10,'EOF'),
            (12,'Comentario'),
            (13,'OPR'),
            (14,'OPR'),
            (15,'OPR'),
            (16,'RCB'),
            (17,'OPR'),
            (18,'OPR'),
            (19,'OPR'),
            (20,'OPM'),
            (21,'AB_P'),
            (22,'FC_P'),
            (23,'PTV'),
            (24,'VIR'),
            (25,'Ignorar')
        }

        with open(entrada,"r") as arquivo:
            self.cadeia = arquivo.read()
        self.indice_leitura = 0
        self.indice_pos_x = 1
        self.indice_pos_y = 1
        self.tabela_estados = pd.read_csv(tabela_estados, sep=",", quotechar="@").astype(int)
        self.ultima_classe = ''

    def pertence_alfabeto(self, caractere, estado_corrente) -> (bool, str):
        if str(caractere) in [",",";",":",".","!","?","\\","*","+","-","/","(",")","{","}","[","]","<",">","=","'",'"',"_","EOF"]:
            
            return caractere
        elif str(caractere) >= "0" and str(caractere) <= "9":
            
            return "D"
        elif (str(caractere) >= "A" and str(caractere) <= "Z") or (str(caractere) >= "a" and str(caractere) <= "z"):
            
            if estado_corrente == 3 or estado_corrente == 1:
                if str(caractere) == "E":
                    return "E"
                elif str(caractere) == "e":
                    return "e"
            else :
                return "L"
        elif str(caractere).isspace():
            # if str(caractere) == '\n':
            #     print('quebra de linha')
            return 'espaco'
        else:
            
            return None
    
    def e_estado_final(self,estado):
        for estadof in self.estados_finais:
            if estadof[0] == estado:
                return True , estadof[1]
        else:
            return False, None
        
    def atualiza_coordenadas(self,caractere):
        if caractere == '\n':
            self.indice_pos_x +=1
            self.indice_pos_y = 1
        else :
            self.indice_pos_y +=1

    def recursao_estados(self,estado_corrente):

        if self.indice_leitura >= len(self.cadeia):

            caractere = 'EOF'
        else:
            caractere = self.cadeia[self.indice_leitura]

        
        coluna = self.pertence_alfabeto(caractere,estado_corrente)
        
        # print("----------------------------------------")
        # print("coluna",coluna)
        # print("estado",estado_corrente)
        # print("caractere",caractere)
        # print("pertence",pertence)
        # print("----------------------------------------")
        # print("tipo na tabela",type(self.tabela_estados[coluna][estado_corrente]))
        if coluna: 

            if self.tabela_estados[coluna][estado_corrente] == -1:

                e_final, classe = self.e_estado_final(estado_corrente)

                if e_final:
                    self.ultima_classe = classe
                    return ''
                else:
                    self.ultima_classe = 'ERRO sintaxe' #erro de sintaxe
                    return ''
            else:

                self.indice_leitura += 1
                self.atualiza_coordenadas(caractere)
                estado_corrente = self.tabela_estados[coluna][estado_corrente]

                return caractere + self.recursao_estados(estado_corrente)
        else: #erro de caractere invalido na linguagem
            if estado_corrente > 0:

                e_final, classe = self.e_estado_final(estado_corrente)

                if e_final:
                    self.ultima_classe = classe
                    return ''
                else :
                    self.ultima_classe = 'ERRO sintaxe ' #
                    return ''
            else:
                self.indice_leitura += 1
                self.atualiza_coordenadas(caractere)
                self.ultima_classe = 'ERRO caractere'  #erro caractere
                return caractere

    def gerar_token(self,tabela_simbolos):
        classe = 'Comentario'
        tipo = None

        while classe == 'Ignorar' or classe == 'Comentario':
            lexema = self.recursao_estados(0)
            classe = self.ultima_classe

        if classe == 'Num':

            if '.' in lexema:

                tipo = 'real'
            else:

                tipo = 'inteiro'
        elif classe == 'Lit':

            tipo = 'literal'
        elif classe == 'id':

            if lexema in tabela_simbolos:
                return tabela_simbolos[lexema]
            else:
                tabela_simbolos[lexema] = Token(classe,lexema,tipo)
        elif classe.find('ERRO') > -1 :
            print(classe + ' na linha :' + str(self.indice_pos_x) + " coluna : " + str(self.indice_pos_y))
        return Token(classe,lexema,tipo)


if __name__ == "__main__":
    # inicializa tabela de simbolos:
    tabela_simbolos = {}
    for item in palavras_reservadas:
        tabela_simbolos[item] = Token(item, item, item)
    
    with Scanner("automato lexico tabela.csv","teste.txt") as scanner:
        n = ''
        while n != 'EOF':
            token = scanner.gerar_token(tabela_simbolos)
            n = token.classe
            print("Classe : ",token.classe,"|Lexema : ",token.lexema,"|Tipo : ",token.tipo)
