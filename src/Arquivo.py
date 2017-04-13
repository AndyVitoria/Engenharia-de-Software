#!/usr/bin/env python
# -*- coding: utf-8 -*-

def abrir(dir):
    arq = open(dir, 'rt', encoding='utf8')
    linha = arq.readline()
    lst = []
    while linha != '':
        lst.append(linha.strip('\n'))
        linha = arq.readline()
    arq.close()
    return lst

def escrever(dir, lst):
    arq = open(dir, 'wt', encoding='utf8')
    for elem in lst:
        arq.write(elem + '\n')
    arq.close()
    return

def setMetadados(automato):
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

def setTransicoes(automato):
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

def salvaAutomato(dir, automato):
    listaSaida = setMetadados(automato) + setTransicoes(automato)
    escrever(dir, listaSaida)
