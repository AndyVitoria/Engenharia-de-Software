#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Trabalho de LFA
Aluno: Andre barbosa da Vitoria
Esse arquivo cuida do processo de IO de arquivos.
"""


def abrir(dir):
    """ Metodo de abertura de arquivo.

    Abre, lê e armazena os dados de um arquivo como strings dentro de uma lista.
    """
    arq = open(dir, 'rt', encoding='utf8')
    linha = arq.readline()
    lst = []
    while linha != '':
        lst.append(linha.strip('\n'))
        linha = arq.readline()
    arq.close()
    return lst


def escrever(dir, lst):
    """ Metodo de escrita de arquivo.

    Recebe o diretorio de um arquivo e uma lista de strings e escreve no caminho fornecido a lista de strings.
    """
    arq = open(dir, 'wt', encoding='utf8')
    for elem in lst:
        arq.write(str(elem) + '\n')
    arq.close()
    return


def set_metadados(automato):
    """ Metodo de inserção de metadados dos automatos.

    Insere em uma lista que será fornecida para ser gravada em arquivo os metadados do automato.
    """
    ordem = ['states', 'alfabeth', 'init', 'finals', 'trans']
    listaSaida = [automato['version']]
    for item in ordem[:-1]:
        stringTemp = str(item)
        # Tratamento de linhas com mais de um valor
        if type(automato[item]) is list:
            for elem in automato[item]:
                stringTemp += ' ' + str(elem)
        else:
            stringTemp += ' ' + str(automato[item])

        listaSaida.append(stringTemp)
    return listaSaida + ['trans']


def set_transicoes(automato):
    """ Metodo de inserção de transições dos automatos.

    Insere em uma lista que será fornecida para ser gravada em arquivo as trasições do automato.
    """
    trans = 'trans'
    listaTransicoes = []
    for chave in automato[trans]:
        stringTemp = str(chave[0]) + ' ' + str(chave[1])
        # Tratamento de Automatos com mais de uma trasição por caractere
        if type(automato[trans][chave]) is list:
            for elem in automato[trans][chave]:
                stringTemp += ' ' + str(elem)
        else:
            stringTemp += ' ' + str(automato[trans][chave])

        listaTransicoes.append(stringTemp)
    return sorted(listaTransicoes) + ['end']


def salva_automato(dir, automato):
    """ Metodo trasitorio de gravação de automato em arquivo.

    Trata o automato e converte-o para lista de strings para ser gravado em arquivo.
    """
    listaSaida = set_metadados(automato) + set_transicoes(automato)
    escrever(dir, listaSaida)


def abrir_automato(diretorio):
    """ Metodo de abertura de automato

    Abre o arquivo contendo o automato e o converte para a estrutura de automato usada no trabalho.
    """
    try:
        arquivo = abrir(diretorio)
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
        if ['alfabeth', 'finals', 'init', 'states', 'trans', 'version'] != sorted(automatoFN.keys()):
            automatoFN = None
    except:
        automatoFN = None
    return automatoFN
