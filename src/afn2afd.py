#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Arquivo
import sys


def arquivo_afn(diretorio):
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


def get_node(chave, trans):
    if chave in trans:
        return trans[chave]
    return None


def remove_repeticoes(lista):
    dic = {}
    for elem in lista:
        dic[elem] = None
    lista[:] = sorted(dic.keys())


def print_matriz(dic):
    print()
    for elem in sorted(dic.keys()):
        print(elem, end='')
        print(':', end='')
        print(dic[elem], end='\n')


def node_inicial(listaInicial):
    nodes = []
    for linha in listaInicial:
        nodes.append(tuple(linha))
    return nodes


def preenche_matriz(automatoFN):
    # Carrega todos os nós iniciais
    nodes = node_inicial(automatoFN['init'])
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
                result = get_node((node, caractere), trans)
                if not (result is None):
                    listaTemp += result
            remove_repeticoes(listaTemp)

            matrizConversao[chave].append(tuple(listaTemp))
            # Se for um novo nó adiciona a lista a ser percorrida
            if not tuple(listaTemp) in nodes:
                nodes.append(tuple(listaTemp))

        index += 1
    return matrizConversao


def set_final(nodes, init):
    lst = []
    for index in range(0, len(nodes), 1):
        check = False
        for inicio in init:
            if inicio in nodes[index]:
                check = True
        if check:
            lst.append(nodes[index])
    return lst


def troca_nomeclatura(nodes):
    dic = {}
    i = 0
    for elem in nodes:
        dic[elem] = i
        i += 1
    return dic


def gera_afd(alfa, nodes, init, finals, matriz, dicNomes):
    automatoFD = {'alfabeth': alfa, 'init': [dicNomes[init]], 'finals': [], 'trans': {}, 'version': 'AFD version 1', 'states': 0}

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


def afn2afd(automatoFN):
    nodes = []

    matrizConversao = preenche_matriz(automatoFN)
    nodes[:] = sorted(matrizConversao.keys())
    # Inserção dos novos nós iniciais e finais
    init = tuple(automatoFN['init'])
    finals = set_final(nodes, automatoFN['finals'])
    # Renomea os nós
    dicNomes = troca_nomeclatura(nodes)

    return gera_afd(automatoFN['alfabeth'], nodes, init, finals, matrizConversao, dicNomes)


def main():
    # ========================================#
    sys.argv.append(sys.argv[1][:-3] + 'afd')
    # ========================================#
    print("Abrindo arquivo AFN")
    automatoFN = arquivo_afn(sys.argv[1])
    print("Convertendo para AFD")
    automatoFD = afn2afd(automatoFN)

    Arquivo.salva_automato(sys.argv[2], automatoFD)
    return


if __name__ == '__main__':
    main()
