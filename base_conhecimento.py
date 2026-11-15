
import json
import unicodedata
from orientacao import Orientacao


def normalizar(texto):
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )

    for sinal in "?!.,;:()-_/":
        texto = texto.replace(sinal, " ")

    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.orientacoes = []

            for item in dados:
                orientacao = Orientacao(**item)
                self.orientacoes.append(orientacao)

            print("Base de conhecimento carregada!")
            print("Total de orientações:", len(self.orientacoes))

        except (FileNotFoundError, json.JSONDecodeError):
            print("Erro ao carregar a base de conhecimento.")
            self.orientacoes = []

        except (TypeError, AttributeError):
            print("A base de conhecimento possui dados inválidos.")
            self.orientacoes = []

    def categorias(self):
        lista = []

        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)

        return lista

    def por_categoria(self, categoria):
        resultado = []

        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                resultado.append(orientacao)

        return resultado

    
    def pontuar(self, pergunta, orientacao):
        pontos = 0

        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)

        palavras_pergunta = pergunta.split()

        for chave in orientacao.palavras_chave:
            chave = normalizar(chave)
            palavras_chave = chave.split()

            if all(palavra in palavras_pergunta for palavra in palavras_chave):
                pontos += 3

        for palavra in set(palavras_pergunta):
            if len(palavra) >= 4 and f" {palavra} " in titulo:
                pontos += 1

        return pontos


    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)

            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)

        return resultados
