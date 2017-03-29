#!/usr/bin/env python
# -*- coding: utf-8 -*-

juju = ''

def mudaJuju(str):
    juju = str

def pegaJuju():
    return juju

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