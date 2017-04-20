#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""Exercicio 3 Trabalho de LFA
Aluno: Andre barbosa da Vitoria
"""

import afztx
import sys
import Arquivo


def afz2afn(automato_fz):
    """Função de conversão de Automato Finito com Movimentos Vazios para Automato Finito Não Deterministico

    Como os metodos necessários para resolução deste exercico ja foram implementados na resolução do excercicio anterior (afztx.py) bastou apenas chama-los.
    """
    return afztx.afz2afn(automato_fz)


def main():
    """Tratamento para caso de ser informado um arquivo de saida

    Insere um elemento a mais na lista ARGV, dessa forma garantindo que exista um elemento na posição 2 e este será usado como arquivo de saia.
    """
    sys.argv.append(sys.argv[1][:-3] + 'afn')

    automato_fz = Arquivo.abrir_automato(sys.argv[1])

    if automato_fz is not None:
        automato_fn = afz2afn(automato_fz)
        Arquivo.salva_automato(sys.argv[2], automato_fn)
    else:
        print("Erro ao abrir o arquivo " + sys.argv[1])
        print("Processo Abortado.")
    return 0


if __name__ == '__main__':
    main()
