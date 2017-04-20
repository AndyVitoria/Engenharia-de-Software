#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exercicio 2 Trabalho de LFA
Aluno: Andre Barbosa da Vitoria
Lógica aplicada no Programa:
    Conversão de um AFNe para AFD facilitando assim a verificação do reconhecimento palavras pelo Automato.
"""

import Arquivo
import afn2afd
import sys


def get_node(chave, trans):
    """Função de captura de transição

        Função que dada uma chave contendo o nó inicial e o caractere a ser processado retorna uma lista com os nós de destino
        """
    if chave in trans:
        return trans[chave]
    return []


def trans_vazia_antes(automato_fz):
    """Função de captura de transições vazia antes do processamento de um caractere

    Função que encontra e armazena em uma lista as trasições vazias que podem ser efetuadas antes do processamento de um caractere.
    """
    lista_chaves = sorted(automato_fz['trans'].keys())

    lista_nodes = count_states(automato_fz['trans'])
    for node in lista_nodes:
        for caractere in automato_fz['alfabeth']:
            transicoes = list()
            if (node, '[]') in lista_chaves:
                chave = (node, caractere)
                for elem in automato_fz['trans'][(node, '[]')]:
                    if (elem, caractere) in automato_fz['trans'].keys():
                        transicoes += automato_fz['trans'][(elem, caractere)]
            if len(transicoes) > 0:
                if chave not in automato_fz['trans'].keys():
                    automato_fz['trans'][chave] = []
                automato_fz['trans'][chave] += transicoes

                afn2afd.remove_repeticoes(automato_fz['trans'][chave])


def trans_vazia_apos(automato_fz):
    """Função de captura de transições vazia após o processamento de um caractere

    Função que encontra e armazena em uma lista as trasições vazias que podem ser efetuadas após o processamento de um caractere.
    """
    lista_chaves = sorted(automato_fz['trans'].keys())

    transicoes = list()
    for chave in lista_chaves:
        index = 0
        transicoes[:] = automato_fz['trans'][chave]
        while index < len(transicoes):
            if (transicoes[index], '[]') in automato_fz['trans']:
                transicoes += automato_fz['trans'][(transicoes[index], '[]')]
            afn2afd.remove_repeticoes(transicoes)
            index += 1
        automato_fz['trans'][chave] = sorted(transicoes)
        transicoes = list()


def remove_vazio(automato_fz):
    """Função que remove transições vazias

    Função que remove transições vazias na conversão de AFNe (Automato Finito com Movimentos Vazios) para AFN (Automato Finito Não Deterministico).
    """
    listaChaves = []
    listaChaves[:] = sorted(automato_fz['trans'].keys())
    for chave in listaChaves:
        if '[]' in chave[1]:
            del (automato_fz['trans'][chave])


def count_states(trans):
    """Função de contagem de estados

    Função que fornece os nós do automato.
    """
    states = []
    listaChave = sorted(trans.keys())
    for chave in listaChave:
        if chave[0] not in states:
            states.append(chave[0])
        for node in trans[chave]:
            if node not in states:
                states.append(node)

    return states


def set_metadados_afn(automato_fn):
    """Função de inserção de metadados de Automato Finito Não Deterministico

    Função que insere metadados de um Automato Finito Não Deterministico após a conversão de um Automato Finito com Movimentos Vazios.
    """
    automato_fn["version"] = 'AFN version 1'
    automato_fn["states"] = str(len(count_states(automato_fn['trans'])))
    return automato_fn


def afz2afn(automato_fz):
    """Função de conversão de Automato Finito com Movimentos Vazios para Automato Finito Não Deterministico

    Função de dado um Automato Finito com Movimentos Vazios converte este para Automato Finito Não Deterministico.
    """
    trans_vazia_apos(automato_fz)

    trans_vazia_antes(automato_fz)

    remove_vazio(automato_fz)
    return set_metadados_afn(automato_fz)


def afz2afd(automato_fz):
    """Função de conversão de Automato Finito com Movimentos Vazios para Automato Finito Deterministico

    Função de dado um Automato Finito com Movimentos Vazios converte este para Automato Finito Deterministico.
    """
    automato_fn = afz2afn(automato_fz)
    automato_fd = afn2afd.afn2afd(automato_fn)
    return automato_fd


def percorre_grafo(node, automato, palavra):
    """Função de percurso de Automato Finito Deterministico .

    Função que percorre um grafo seguindo uma palavra, onde se concluido rentorna o nó final ou None no caso da palavra não ser aceita.
    """
    if len(palavra) == 0:
        return node
    if (node, palavra[0]) not in automato:
        return None
    else:
        return percorre_grafo(automato[(node, palavra[0])], automato, palavra[1:])


def verifica_palavra(automato_fd, palavra):
    """Função de verificação de validade de palavra

    Função que dado um Automato Finito Deterministico verifica se a palavra informada retorna um inteiro se a palavra for reconhecida ou None caso contrário.
    """
    inicio = automato_fd['init'][0]
    return percorre_grafo(inicio, automato_fd['trans'], palavra) in automato_fd['finals']


def main():
    print("Carregando automato")
    automato_fz = Arquivo.abrir_automato(sys.argv[1])
    if automato_fz is not None:
        automato_fd = afz2afd(automato_fz)
        if verifica_palavra(automato_fd, sys.argv[2]):
            print("ACEITA")
        else:
            print("REJEITADA")
    else:
        print("Erro ao abrir o arquivo " + sys.argv[1])
        print("Processo Abortado.")
    return


if __name__ == '__main__':
    main()
