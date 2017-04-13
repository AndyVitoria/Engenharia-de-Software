#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Exercicio 2 Trabalho de LFA
# Aluno: Andre barbosa da Vitoria
# Lógica aplicada no Programa:
#    Conversão de um AFNe para AFD facilitando assim a verificação do reconhecimento palavras pelo Automato.


import afn2afd
import sys


def arquivo_afz(dir):
    return afn2afd.arquivo_afn(dir)


def get_trans(chave, trans):
    if chave in trans:
        return trans[chave]
    return []


def trans_vazia_antes(elem, caractere, trans, lst):
    if (elem, '[]') in trans:
        for node in trans[(elem, '[]')]:
            if (node, caractere) in trans:
                lst += trans[(node, caractere)]
            if (node, '[]') in trans:
                trans_vazia_antes(node, caractere, trans, lst)


def trans_vazia_apos(elem, trans, nodes):
    # Adição de trasições vazia apos o processamento do caractere
    if (elem, '[]') in trans:
        nodes += trans[(elem, '[]')]
    for node in get_trans((elem, '[]'), trans):
        trans_vazia_apos(node, trans, nodes)


def trans_vazia(chave, trans):
    antes = []
    caminho = get_trans(chave, trans)
    apos = []
    trans_vazia_antes(chave[0], chave[1], trans, antes)
    for elem in caminho:
        trans_vazia_apos(elem, trans, apos)

    return antes + caminho + apos

# Remoção de Trasições vazias
def remove_vazio(automatoFZ):
    listaChaves = []
    listaChaves[:] = sorted(automatoFZ['trans'].keys())
    for chave in listaChaves:
        if '[]' in chave[1]:
            del(automatoFZ['trans'][chave])


def afz2afn(automatoFZ):
    listaChaves = sorted(automatoFZ['trans'].keys())
    for chave in listaChaves:
        if chave[1] == '[]':
            for caractere in automatoFZ['alfabeth']:
                if not (chave[0], caractere) in automatoFZ['trans']:
                    automatoFZ['trans'][(chave[0], caractere)] = []
                automatoFZ['trans'][(chave[0], caractere)] = trans_vazia((chave[0], caractere), automatoFZ['trans'])
                afn2afd.remove_repeticoes(automatoFZ['trans'][(chave[0], caractere)])

    remove_vazio(automatoFZ)
    return automatoFZ


def afz2afd(automatoFZ):
    automatoFN = afz2afn(automatoFZ)
    automatoFD = afn2afd.afn2afd(automatoFN)
    return automatoFD


def percorre_grafo(node, automato, palavra):
    if len(palavra) == 0:
        return node
    if (node, palavra[0]) not in automato:
        return None
    else:
        return percorre_grafo(automato[(node, palavra[0])], automato, palavra[1:])


def verifica_palavra(automatoFD, palavra):
    inicio = automatoFD['init'][0]
    #Retonar uma comparação do ultimo nó ou None com a lista de nós finais
    return percorre_grafo(inicio, automatoFD['trans'], palavra) in automatoFD['finals']


def main():
    automatoFZ = arquivo_afz(sys.argv[1])
    automatoFD = afz2afd(automatoFZ)
    if verifica_palavra(automatoFD, sys.argv[2]):
        print("ACEITA")
    else:
        print("REJEITADA")
    return


if __name__ == '__main__':
    main()
