#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Arquivo, sys


def arquivoAFN(diretorio):
    arquivo = Arquivo.abrir(diretorio)
    automatoFN = {}

    # Captura os elementos entre sates e trans
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

def removeRepetidos(lista):
    dic = {}
    lst = []
    for elem in lista:
        dic[elem] = None
    lst[:] = dic.keys()
    return lst

def printM(dic):
    print()
    for elem in dic:
        print(elem, end='')
        print(':', end='')
        print(dic[elem], end='\n')

def preencheMatriz(automatoFN):
    nodes = []
    for i in automatoFN['init']:
        nodes.append(tuple(i))

    check = True
    matrizConversao = {}
    trans = automatoFN['trans']

    index = 0
    while index < len(nodes):
        chave = nodes[index]

        if not chave in matrizConversao:
            matrizConversao[chave] = []
        for caractere in automatoFN['alfabeth']:
            listaTemp = []
            for node in chave:
                result = getNode((node, caractere), trans)
                if result != None and not result in listaTemp:
                    listaTemp += result
            listaTemp = sorted(removeRepetidos(listaTemp))
            matrizConversao[chave].append(tuple(listaTemp))
            if not tuple(listaTemp) in nodes:
                nodes.append(tuple(listaTemp))
        index += 1
    printM(matrizConversao)
    return matrizConversao

def setInicioFinal(nodes, init):
    print(nodes, init)
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
    automatoFD  = {'alfabeth': alfa, 'init': [], 'finals' : [], 'trans' : {}}

    for chave in nodes:
        if chave in init:
            automatoFD['init'].append(dicNomes[chave])
        if chave in finals:
            automatoFD['finals'].append(dicNomes[chave])
        if chave in matriz:
            trans = []
            index = 0
            for elem in matriz[chave]:
                automatoFD['trans'][(dicNomes[chave], alfa[index])] = dicNomes[elem]
                index += 1
    return automatoFD

def toAFD(automatoFN):
    nodes = []
    automatoFD = {}
    matrizConversao = preencheMatriz(automatoFN)
    nodes[:] = matrizConversao.keys()

    init = setInicioFinal(nodes, automatoFN['init'])
    finals = setInicioFinal(nodes, automatoFN['finals'])
    dicNomes = trocaNomeclatura(nodes)
    print(dicNomes)
    return geraAFD(automatoFN['alfabeth'], nodes, init, finals, matrizConversao ,dicNomes)

def main():
    # ========================================#
    sys.argv.append(sys.argv[1][:-3] + 'afd')
    # ========================================#
    automatoFN = arquivoAFN(sys.argv[1])
    print(automatoFN)
    automatoFD = toAFD(automatoFN)
    print(automatoFD)





    return


if __name__ == '__main__':
    main()
