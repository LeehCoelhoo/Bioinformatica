import re
import math

box_D = "D.motif"
box_C = "C.motif"

#função exibe matriz
def exibir_matriz(matriz):
    for linha in matriz:
        print(linha)
        
def matriz_freq(arquivo, filename):

    #lendo o arquivo .motif
    with open(arquivo) as f:
        arquivo = f.readlines()

    #transformando o arquivo em string
    string = ''.join(arquivo)

    #dividindo cada fita
    sequencia = re.split('\n', string)

    for i in range(len(sequencia )):
        if(sequencia [i] == ''):
            sequencia .pop(i)#deleta

    s = re.split('\t', sequencia [0])
    f = re.split('\t',sequencia [1])

    tam_coluna = len(s[0])
    tam_linha = len(sequencia)

    #criando uma matriz vazia
    matriz = []

    for i in range(tam_linha): #linha
        linha = []
        for j in range(tam_coluna): #coluna 
            elemento = sequencia [i][j]
            linha.append(elemento)
        matriz.append(linha)

    pos_a = []
    pos_t = []
    pos_g = []
    pos_c = []
    a = int(0) 
    t = int(0) 
    g = int(0) 
    c = int(0) 

    #verificação        
    for j in range(tam_coluna): 
        for i in range(tam_linha): 
            if(matriz[i][j] == 'A'):
                a = a+1
            if(matriz[i][j] == 'T'):
                t = t+1
            if(matriz[i][j] == 'G'):
                g = g+1
            if(matriz[i][j] == 'C'):
                c = c+1

        pos_a.append(a)
        pos_t.append(t)
        pos_g.append(g)
        pos_c.append(c)
        a = 0
        t = 0
        g = 0
        c = 0
        
    lista_atgc = []
    lista_atgc.append(pos_a)
    lista_atgc.append(pos_t)
    lista_atgc.append(pos_g)
    lista_atgc.append(pos_c)

    matriz_seq = []

    lista_nu = ['A', 'T', 'G', 'C']
    for i in range(5):
        linha = []
        for j in range(tam_coluna+1):
            elemento = ''
            linha.append(elemento)
        matriz_seq.append(linha)

    for j in range(tam_coluna+1):
        for i in range(5):
            matriz_seq[0][0] = ' '
            if(i == 0):
                matriz_seq[0][j] = j
            elif(j == 0):
                matriz_seq[i][0] = lista_nu[i-1]
            else:
                matriz_seq[i][j] = (lista_atgc[i-1][j-1] ) / (len(sequencia))
    
    print('\nfrequências de cada resíduo em cada posição do alinhamento múltiplo:\n')
    exibir_matriz(matriz_seq)

    #matriz frequências normalizadas
    overall_freq = []
    aux = int(0)

    for i in range(5): 
            for j in range(tam_coluna+1):
            
                if(i != 0 and j != 0):
                    aux = aux + matriz_seq[i][j]
            if(i != 0 and j != 0):
                overall_freq.append(aux / tam_coluna)
            aux = 0        

    for i in range(5):
        for j in range(tam_coluna+1): 
            if(i != 0 and j != 0):
                aux = matriz_seq[i][j]
                matriz_seq[i][j] = (aux / overall_freq[i-1])
    
    print('\nmatriz com as frequências normalizadas:\n')
    exibir_matriz(matriz_seq)
    
    #matriz com os scores normalizados para escala logarítmica na base 2

    for i in range(5): 
        for j in range(tam_coluna+1): 
             if(i != 0 and j != 0):
                aux = matriz_seq[i][j]
                if(aux == 0):
                    matriz_seq[i][j] = '-'
                else:
                    matriz_seq[i][j] = math.log(matriz_seq[i][j], 2)
    
    print('\nmatriz com os scores normalizados para escala logarítmica na base 2:\n')                
    exibir_matriz(matriz_seq)

    #Arquivo tabular com os scores totais de cada amostra
    lista_score = []
    lista_soma = []

    for i in range(5):
             if(i != 0):
                lista_score.append(matriz_seq[i])

    for i in range(len(lista_score)): 
        lista_score[i].pop(0)

    lista_nome = []
    soma = int(0)
    
    for i in range(tam_linha):
        for j in range(tam_coluna): 
            teste = re.split('\t', sequencia [i])
        lista_nome.append(teste[0])

    for i in range(tam_linha): #quantidade de seq.
        for j in range(tam_coluna):
            if(lista_nome[i][j] == 'A'):
                if(lista_score[0][j] != '-'):
                    soma = lista_score[0][j] + soma 
                else:
                     soma = soma
            elif (lista_nome[i][j] == 'T'):
                if(lista_score[1][j] != '-'):
                    soma = soma + lista_score[1][j]
            
            elif (lista_nome[i][j] == 'G'):
                if(lista_score[2][j] != '-'):
                     soma = lista_score[2][j] + soma
                else:
                    soma = soma
            elif (lista_nome[i][j] == 'C'):
                if(lista_score[3][j] != '-'):
                    soma = lista_score[3][j]+ soma 
        lista_soma.append(soma)
        soma = 0

    #escrevendo no arquivo
    filename = filename + ".scores"
    with open(filename, "w") as fp:
        for i in range(tam_linha): #quantidade de seq.
            fp.write(lista_nome[i] + '\t' + str(lista_soma[i])+ '\n')

matriz_freq(box_D, str(box_D))
print('\n')
matriz_freq(box_C, str(box_C))
