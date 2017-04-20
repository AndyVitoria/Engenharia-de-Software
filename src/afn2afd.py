#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exercicio 1 Trabalho de LFA
Aluno: Andre Barbosa da Vitoria
"""
import Arquivo
import sys


def get_node(chave, trans):
    """Função de captura de transição

    Função que dada uma chave contendo o nó inicial e o caractere a ser processado retorna o nó de destino
    """
    if chave in trans:
        return trans[chave]
    return None


def remove_repeticoes(lista):
    """Função de remoção de elementos repetidos em uma lista

    Função que dada uma lista que não contenha listas ou dicionários remove elementos repetidos.
    """
    dic = {}
    for elem in lista:
        dic[elem] = None
    lista[:] = sorted(dic.keys())


def preenche_matriz(automato_fn):
    """Função de geração de matriz de conversão de AFN para AFD

    Função que dada um AFN gera uma matriz com as novas transições (como visto em sala de aula) para ser usada no AFD.
    """
    # Carrega todos os nós iniciais
    nodes = [tuple(automato_fn['init'][0])]
    matriz_conversao = {}
    trans = automato_fn['trans']
    index = 0

    # Percorre a lista com os novos nós e adiciona um novo nó que não esta
    # nela, se encontrado.
    while index < len(nodes):
        chave = nodes[index]
        if not chave in matriz_conversao:
            matriz_conversao[chave] = []

        for caractere in automato_fn['alfabeth']:
            lista_temp = []
            # Percorre os nós dento do conjunto de nós da nova chave gerada.
            for node in chave:
                result = get_node((node, caractere), trans)
                if result is not None:
                    lista_temp += result
            remove_repeticoes(lista_temp)

            matriz_conversao[chave].append(tuple(lista_temp))
            # Se for um novo nó adiciona a lista a ser percorrida
            if not tuple(lista_temp) in nodes and len(lista_temp) > 0:
                nodes.append(tuple(lista_temp))

        index += 1
    return matriz_conversao


def set_final(nodes, init):
    """Função de inserção de nós finais

    Função que dada o AFD gerado a partir de um AFN insere no campo finals, o nós finais do automato.
    """
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
    """Função de renomeação de nós no AFD

    Função que dada o AFD renomeia os nos afim de facilitar a leitura e compreenção do mesmo.
    """
    dic = {}
    i = 0
    for elem in nodes:
        dic[elem] = i
        i += 1
    return dic


def gera_afd(alfa, nodes, init, finals, matriz, dic_nomes):
    """Função de criação de AFD

    Função que dada o as informações de um AFD gerada a partir de um AFN, trata e insere na estrutura de um AFD definida neste trabalho, os dados gerados.
    """
    automato_fd = {'alfabeth': alfa, 'init': [dic_nomes[init]], 'finals': [], 'trans': {}, 'version': 'AFD version 1',
                  'states': 0}

    for chave in nodes:

        if chave in finals:
            automato_fd['finals'].append(dic_nomes[chave])
        if chave in matriz.keys():
            trans = []
            index = 0
            for elem in matriz[chave]:
                if elem != ():
                    automato_fd['trans'][(dic_nomes[chave], alfa[index])] = dic_nomes[elem]
                index += 1

    if len(automato_fd['trans']) > 0:
        automato_fd['states'] += max(automato_fd['trans'].keys())[0] + 1

    return automato_fd


def afn2afd(automato_fn):
    """Função de conversão de AFN para AFD

    Função que dado um AFN converte para AFD.
    """
    nodes = []

    matriz_conversao = preenche_matriz(automato_fn)
    nodes[:] = sorted(matriz_conversao.keys())
    # Inserção dos novos nós iniciais e finais
    init = tuple(automato_fn['init'])
    finals = set_final(nodes, automato_fn['finals'])
    # Renomea os nós
    dic_nomes = troca_nomeclatura(nodes)

    return gera_afd(automato_fn['alfabeth'], nodes, init, finals, matriz_conversao, dic_nomes)


def main():
    """Tratamento para caso de ser informado um arquivo de saida

    Insere um elemento a mais na lista ARGV, dessa forma garantindo que exista um elemento na posição 2 e este será usado como arquivo de saia.
    """
    sys.argv.append(sys.argv[1][:-3] + 'afd')

    print("Abrindo arquivo AFN")
    automato_fn = Arquivo.abrir_automato(sys.argv[1])
    if automato_fn is not None:
        print("Convertendo para AFD")
        automato_fd = afn2afd(automato_fn)

        Arquivo.salva_automato(sys.argv[2], automato_fd)
    else:
        print("Erro ao abrir o arquivo " + sys.argv[1])
        print("Processo Abortado.")
    return


if __name__ == '__main__':
    main()
