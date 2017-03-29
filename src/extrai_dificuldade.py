#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Arquivo
import Acentos

def disciplinaPorcentagem(lista_Disciplinas):
    dicionario_Disciplina = {}
    lstTemp = []

    for linha in lista_Disciplinas:
        lstTemp = linha.split(";")
        # Montagem da tabela com Tupla (Disciplina, Situação) e lista com qtd de alunos em cada disciplina naquela situação
        if (lstTemp[0][1:-1], lstTemp[2][1:-1]) in dict.keys(dicionario_Disciplina):
            dicionario_Disciplina[(lstTemp[0][1:-1], lstTemp[2][1:-1])][0] += int(lstTemp[3])
        else:
            dicionario_Disciplina[(lstTemp[0][1:-1], lstTemp[2][1:-1])] = [int(lstTemp[3])]
    return dicionario_Disciplina


def calculaTotal(dicionario_Disciplinas):
    dicionario_Total = {}

    for chave in dict.keys(dicionario_Disciplinas):
        # Ignora o estado do aluno (Cursando, Aprovado, Reprovado e etc.) e calcula o total de alunos das disciplinas
        if chave[0] in dict.keys(dicionario_Total):
            dicionario_Total[chave[0]] += dicionario_Disciplinas[chave][0]
        else:
            dicionario_Total[chave[0]] = dicionario_Disciplinas[chave][0]

    return dicionario_Total


def calculaPorcentagem(dicionario_Disciplinas):
    dicionario_Total = calculaTotal(dicionario_Disciplinas)

    for chave in dict.keys(dicionario_Disciplinas):
        # Calcula Porcentagem de alunos aprovados, reprovados, cursando e etc.
        porcentagem = dicionario_Disciplinas[chave][0] / dicionario_Total[chave[0]]
        # Insere porcentagem na tabela com as disciplinas
        dicionario_Disciplinas[chave].append(porcentagem)
    return


def toList(dicionario_Disciplinas):
    lista_Chave = []

    for chave in dicionario_Disciplinas:
        lista_Chave.append(chave)

    lista_Chave.sort()

    return lista_Chave


def toString(chave, dicionario_Disciplinas):
    return chave[0] + ";" + chave[1] + ";" + str(dicionario_Disciplinas[chave][0]) + ";" + str(
        dicionario_Disciplinas[chave][1])


def criaTabela(dicionario_Disciplinas):
    lista_Chaves = toList(dicionario_Disciplinas)
    tabela = []
    for chave in lista_Chaves:
        # Constroi uma String com Disciplina;Situacao;Quantidade;Porcentagem e insere na tabela
        tabela.append(toString(chave, dicionario_Disciplinas))
    return tabela


#Escrever metodo que separa binariamente (aprovado/reprovado)
def aprovadoReprovado(relacao_disciplinas):
    aprovado = {}
    reprovado = {}
    dic_Binario = {}

    for chave in dict.keys(relacao_disciplinas):
        nova_chave = Acentos.remover_acentos(chave[0])

        if chave[1].lower() == 'aprovado':
            if nova_chave in dict.keys(aprovado):
                aprovado[nova_chave] += relacao_disciplinas[chave][0]
            else:
                aprovado[nova_chave] = relacao_disciplinas[chave][0]
        else:
            if nova_chave in dict.keys(reprovado):
                reprovado[nova_chave] += relacao_disciplinas[chave][0]
            else:
                reprovado[nova_chave] = relacao_disciplinas[chave][0]

    for chave in reprovado:
        dic_Binario[chave, "Aprovado"] = [aprovado[chave]]
        dic_Binario[chave, "Reprovado"] = [reprovado[chave]]

    return dic_Binario


def main():
    cabecalho = ["desc_historico;situacao;qtd_aluno;percet_aluno"]
    lista_Disciplinas = Arquivo.abrir("../tabela/entrada/IFES[Disciplinas, Situacao, Qtd].csv")[1:]
    relacao_Disciplinas = disciplinaPorcentagem(lista_Disciplinas)
    calculaPorcentagem(relacao_Disciplinas)

    tabela_Disciplinas = cabecalho + criaTabela(relacao_Disciplinas)
    Arquivo.escrever("../tabela/saida/IFES[Disciplinas, Situacao, Qtd, Percent].csv", tabela_Disciplinas)

    relacao_Disci_Binaria = aprovadoReprovado(relacao_Disciplinas)
    calculaPorcentagem(relacao_Disci_Binaria)
    tabela_Disci_Binaria = cabecalho + criaTabela(relacao_Disci_Binaria)
    Arquivo.escrever("../tabela/saida/IFES[Disciplinas, Aprovado-Reprovado, Qtd, Percent].csv", tabela_Disci_Binaria)
    return 0


if __name__ == '__main__':
    main()
