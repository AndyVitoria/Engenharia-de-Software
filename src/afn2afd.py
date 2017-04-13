#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Arquivo
import sys


def arquivoAFN(diretorio):
    arquivo = Arquivo.abrir(diretorio)
    automatoFN = {'version': arquivo[0]}

    # Captura os elementos entre states e trans
    for linha in arquivo[1:5]:
        elementos = linha.split(' ')
        automatoFN[elementos[0]] = elementos[1:]
    automatoFN['trans'] = {}

    # Captura as transicoes
    for linha in arquivo[6:-1]:
        elementos = linha.split(' ')
        automatoFN['trans'][tuple(elementos[:2])] = elementos[2:]
    return automatoFN


def getNode(chave, trans):
    if chave in trans:
        return trans[chave]
    return None


def removeRepeticoes(lista):
    dic = {}
    for elem in lista:
        dic[elem] = None
    lista[:] = sorted(dic.keys())


def printM(dic):
    print()
    for elem in dic:
        print(elem, end='')
        print(':', end='')
        print(dic[elem], end='\n')


def nodeInicial(listaInicial):
    nodes = []
    for linha in listaInicial:
        nodes.append(tuple(linha))
    return nodes


def preencheMatriz(automatoFN):
    # Carrega todos os nós iniciais
    nodes = nodeInicial(automatoFN['init'])
    matrizConversao = {}
    trans = automatoFN['trans']
    index = 0

    # Percorre a lista com os novos nós e adiciona um novo nó que não esta
    # nela, se encontrado.
    while index < len(nodes):
        chave = nodes[index]
        if not chave in matrizConversao:
            matrizConversao[chave] = []

        for caractere in automatoFN['alfabeth']:
            listaTemp = []
            # Percorre os nós dento do conjunto de nós da nova chave gerada.
            for node in chave:
                result = getNode((node, caractere), trans)
                if not (result is None):
                    listaTemp += result
            removeRepeticoes(listaTemp)

            matrizConversao[chave].append(tuple(listaTemp))
            # Se for um novo nó adiciona a lista a ser percorrida
            if not tuple(listaTemp) in nodes:
                nodes.append(tuple(listaTemp))

        index += 1
    # printM(matrizConversao)
    return matrizConversao


def setFinal(nodes, init):
    lst = []
    for index in range(0, len(nodes), 1):
        check = False
        for inicio in init:
            if inicio in nodes[index]:
                check = True
        if check:
            lst.append(nodes[index])
    return lst


def trocaNomeclatura(nodes):
    dic = {}
    i = 0
    for elem in nodes:
        dic[elem] = i
        i += 1
    return dic


def geraAFD(alfa, nodes, init, finals, matriz, dicNomes):
    automatoFD = {'alfabeth': alfa, 'init': [], 'finals': [], 'trans': {}, 'version': 'AFD version 1', 'states': 0}
    automatoFD['init'].append(dicNomes[init])
    for chave in nodes:

        if chave in finals:
            automatoFD['finals'].append(dicNomes[chave])
        if chave in matriz.keys():
            trans = []
            index = 0
            for elem in matriz[chave]:
                automatoFD['trans'][(dicNomes[chave], alfa[index])] = dicNomes[elem]
                index += 1
    automatoFD['states'] = max(automatoFD['trans'].keys())[0] + 1
    return automatoFD


def toAFD(automatoFN):
    nodes = []

    matrizConversao = preencheMatriz(automatoFN)
    nodes[:] = sorted(matrizConversao.keys())
    # Inserção dos novos nós iniciais e finais
    init = tuple(automatoFN['init'])
    finals = setFinal(nodes, automatoFN['finals'])
    # Renomea os nós
    dicNomes = trocaNomeclatura(nodes)

    return geraAFD(automatoFN['alfabeth'], nodes, init, finals, matrizConversao, dicNomes)


def main():
    # ========================================#
    sys.argv.append(sys.argv[1][:-3] + 'afd')
    # ========================================#
    print("Abrindo arquivo AFN")
    automatoFN = arquivoAFN(sys.argv[1])
    print("Convertendo para AFD")
    automatoFD = toAFD(automatoFN)

    Arquivo.salvaAutomato(sys.argv[2], automatoFD)
    return


if __name__ == '__main__':
    main()
