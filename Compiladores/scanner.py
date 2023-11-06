import pandas as pd


class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo


class Scanner:
    def __init__(self, posicao_atual, buffer, tabela_estados):
        self.estados_finais = {
            1,
            3,
            6,
            8,
            9,
            10,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            23,
            22,
            23,
            24,
        }
        self.posicao_atual = posicao_atual
        self.buffer = buffer
        self.tabela_estados = pd.read_excel(tabela_estados)

    def pertence_alfabeto(self, caractere) -> (bool, str):
        if str(caractere) > "0" and str(caractere) < "9":
            return (True, "D")
        elif (str(caractere) >= "A" and str(caractere) <= "Z") or (
            str(caractere) >= "a" and str(caractere) <= "z"
        ):
            return (True, "L")
        elif str(caractere) in [
            ",",
            ";",
            ":",
            ".",
            "!",
            "?",
            "\\",
            "*",
            "+",
            "-",
            "/",
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            "<",
            ">",
            "=",
            "'",
            '"',
            "_",
        ]:
            return (True, caractere)
        else:
            return (False, None)

    def pegar_token(self):
        pass


if __name__ == "__main__":
    # scnr = Scanner()
    # while 1:
    #     entrada = input("Teste um caractere: ")
    #     print(scnr.pertence_alfabeto(entrada))
    tabela_token = pd.DataFrame()

    tabela_estados = pd.read_csv("automato lexico tabela.csv", sep=",", quotechar="@")
    print(tabela_estados)

    # with Scanner(0, 1, "teste") as scanner:
    #     with open("entrada.txt") as arquivo:
    #         entrada = arquivo.read()

    #         for caractere in entrada:
    #             if caractere.isspace():
    #                 pass
    #             else:
    #                 print(caractere)
