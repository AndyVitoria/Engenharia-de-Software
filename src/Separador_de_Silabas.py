'''
Aluno: André Barbosa da Vitória
Data: 21/09/2015
Exercicio 1. Sepaparador de Silabas.
'''

def f_separaSilaba(palavra):
    palavra = palavra.lower()
    if palavra.isalpha():
        check = False
        inicio = 0
        fim = 0
        vog = ['a','e','i','o','u']
        vogacent = ['á','â','ã','é','ê','í','î','ó','ô','õ','ú','û'] # Vogais acentuadas
        cons = ['b','c','d','f','g','j','k','l','m','n','p','q','r','s','t','v','w','x','z','ç']
        conscomp = ['ch','nh','lh','br','cr','dr','fr','gr','pr','tr','vr','bl','cl','fl','gl','pl','tl','vl']
        lst =[]
        pos = 0
        strbuffer = ""
        while pos < len(palavra):
            check = False
            if palavra[pos] in cons:
                if pos == 0:
                    inicio = pos
                elif pos+1 < len(palavra)-1:
                    if palavra[pos:pos+1] in conscomp:
                        inicio = pos
                        pos+=1
                    elif palavra[pos] in cons and palavra[pos+1] in cons:
                        fim = pos
                        check = True
                    elif pos == len(palavra)-1:
                        fim = pos
                        check = True
                    else:
                        inicio = pos
            if palavra[pos] in vog or palavra[pos] in vogacent:
                if pos == 0:
                    lst.append(palavra[0])
                elif pos+1 < len(palavra)-1 and palavra[pos] in vogacent and palavra[pos+1] in vog:
                    fim = pos+1
                    pos +=1
                    check = True
                elif pos+1 < len(palavra)-1 and palavra[pos-1] in vog and palavra[pos] in vogacent:
                    lst.append(palavra[pos])
                    inicio = pos+1
                    fim = pos
                elif pos == len(palavra)-1:
                    fim = pos
                    check = True
                elif pos +1 < len(palavra) -1 and palavra[pos+1] in cons and not (palavra[pos+1] in ['r','s']): #['ra','re','ri','ro','ru','sa','se','si','so','su']):
                    if pos +2 <= len(palavra)-1 and (palavra[pos+2] in vog or palavra[pos+2] in vogacent) and not(palavra[pos+1:pos+2] in conscomp):
                        fim = pos
                        check = True
                    else:
                        fim = pos + 1
                        pos += 1
                        check = True
                else:
                    fim = pos
            if check:
                lst.append(palavra[inicio:fim+1])
                inicio = fim+1
                fim = fim
            pos += 1
        return lst
    else:
        return None
def main():

    print(f_separaSilaba(input("Digite a Palavra: ")))
    return 0

if __name__ == '__main__':
    main()