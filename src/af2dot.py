#!/usr/bin/env python
# -*- coding: utf-8 -*-
# """
"""
Exercicio 4 Trabalho de LFA
Aluno: Andre barbosa da Vitoria
"""

import Arquivo
import sys


def gera_grafo(automato):
    """Função de conversão de automato em grafo

    Função que converte um automato (dicionário) em um grafo (um dicionário onde as chaves são
    o no inicial e o no de destino, e o valor armazenado são os caracteres para trasição).
    """
    trans = automato['trans']
    graph = {}
    nodes = []

    for chave in trans:
        for destino in trans[chave]:
            nova_chave = (chave[0], destino)
            if chave[1] == '[]':
                caractere = '&epsilon;'
            else:
                caractere = chave[1]
            if nova_chave in graph:
                graph[nova_chave] += ',' + caractere
            else:
                graph[nova_chave] = caractere
    return graph


def gera_dot(graph):
    """Função de inserção do grafo

    Função que trata e insere em uma lista de string o grafo gerado pela função gera_grafo().
    """
    dot = []
    lista_chaves = sorted(graph.keys())
    for chave in lista_chaves:
        dot.append('\t' + chave[0] + '->' + chave[1] + '[label="' + graph[chave] + '"];')
    dot.append('}')
    return dot


def cabecalho(inicio, final):
    """Função de inserção das primeiras linhas do arquivo .dot

    Função que insere as primeiras linhas do arquivo .dot, sendo elas o tipo de grafo, a orientação a estrutura do nó inicial e a estrutura dos nós finais.
    """
    dot = ['digraph{', '\trankdir=LR;', '\tnode [shape=point]; start', '\tnode [shape=doublecircle];',
           '\tnode [shape=circle];\n', '\tstart->' + str(inicio[0]) + ';']
    for node in final:
        dot[3] += ' ' + str(node)
    return dot


def af2dot(automato):
    """Função de estruturação da conversão de automato em arquivo .dot

    Função que chama as demais funções que fazem a conversão de automato em grafo e grafo em arquivo dot.
    """
    graph = gera_grafo(automato)
    return cabecalho(automato['init'], automato['finals']) + gera_dot(graph)


def main():
    """Tratamento para caso de ser informado um arquivo de saida

    Insere um elemento a mais na lista ARGV, dessa forma garantindo que exista um elemento na posição 2 e este será usado como arquivo de saia.
    """
    sys.argv.append(sys.argv[1][:-3] + 'dot')
    print("Carregando automato")

    automato = Arquivo.abrir_automato(sys.argv[1])
    if automato is not None:
        print("Convertendo para .dot")
        dot = af2dot(automato)
        Arquivo.escrever(sys.argv[2], dot)
    else:
        print("Erro ao abrir o arquivo " + sys.argv[1])
        print("Processo Abortado.")
    return


if __name__ == '__main__':
    main()
