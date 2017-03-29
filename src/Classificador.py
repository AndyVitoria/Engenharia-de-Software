#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Arquivo

def grauDificuldade(matriz_disciplinas):
    # Grau de dificuldade da disciplina
    grau = ["Baixo", "Medio", "Alto", "Muito Alto", "Critico"]
    indicador = -1

    for linha in range(1, len(matriz_disciplinas), 2):
        # Calculo que indica o gradu de dificuldade da disciplina
        indicador = int((matriz_disciplinas[linha][3] * 10) // 2)

        matriz_disciplinas[linha - 1].append(grau[indicador])
        matriz_disciplinas[linha].append(grau[indicador])

    return

def separaDados(lista_disciplinas):
    matriz = []
    for elem in lista_disciplinas:
        lista_temp = elem.split(";")
        matriz.append([lista_temp[0], lista_temp[1], lista_temp[2], float(lista_temp[3])])
    return matriz


def toString(lista):
    nova_string = str(lista[0])
    for index in range(1, len(lista)):
        nova_string += ';' + str(lista[index])
    return nova_string

def criaTabela(matriz):
    tabela = []
    for linha in matriz:
        tabela.append(toString(linha))
    return tabela


def main():
    lista_Disciplinas = Arquivo.abrir("../tabela/saida/IFES[Disciplinas, Aprovado-Reprovado, Qtd, Percent].csv")
    # Cabeçalho da tabela
    tabela_dificuldade = [lista_Disciplinas[0] + ";dificuldade"]
    del(lista_Disciplinas[0])

    matriz_Disciplinas = separaDados(lista_Disciplinas)

    grauDificuldade(matriz_Disciplinas)

    tabela_dificuldade += criaTabela(matriz_Disciplinas)
    Arquivo.escrever("../tabela/saida/IFES[Disciplinas, Aprovado-Reprovado, Qtd, Percent, Dificuldade].csv", tabela_dificuldade)
    return

if __name__ == '__main__':
    main()