# -*- coding: utf-8 -*-
from igraph import *

#this function generate a Matrix with the shortest paths between the nodes
#this matrix help us to know a lot of indices, for example
#vulnerability, global efficiency, straightness centrality
def matrizMenorCaminho(g, valor):
    nova=[]
    valor=valor+1
    for elemento in range(valor):
        nova.append([0]*valor)
    for i in range(valor):
        lista=[]
        menores=g.get_all_shortest_paths(i)
        for linha in range(len(menores)):
            nova[menores[linha][0]][menores[linha][-1]]=len(menores[linha])-1
    return nova

def eficienciaGlobal(g, matriz):
    return calculosEficiencia(matriz, g)

def calculosEficiencia(matriz, g):
    i=0
    x=0.0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if matriz[i][j]!=0 and i<=j:
                x+=1.0/matriz[i][j]
            j+=1
        i+=1
    n=g.vcount()
    return x/(n*(n-1))

#this function generate another Graph equals the basic one to delete the node in
#question to make some calculations to discover how eficient is the node
#and what happens if it is not there
def eficienciaVertice(g, n, matriz):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    return calculosEficiencia(matriz, g)

#this function makes exactly what the previous one but where the nodes do not
#connect the value 0 is replaced by a value not possible. one more the number of
#nodes
def eficienciaVerticeComMax(g, n):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    matriz = matrizMenorCaminho(gr, g.vcount())
    i=0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if matriz[i][j]==0:
                matriz[i][j]=g.vcount()
            j+=1
        i+=1
    return calculosEficiencia(matriz, g)

#this function make the vulnerability calculation with the node efficiency and
#the global efficiency
def vulnerabilidade(ef, efg):
    if efg!=0:
        return (efg-ef)/efg
    else:
        return 0


#Quando o straightness de um é maior quer dizer que ele chega mais rápido
#no mesmo lugar por vias expressas, passa por menos pontos.
#Ou com a mesma quantidade de passos, vai mais longe.
def straightness(mShort, mEucl, g):
    cont=0.0
    soma=0.0
    n=g.vcount()

    lista=[]
    i=0
    while i<n:
        j=0
        soma=0
        cont=0
        while j<n:
            #quando mShort é igual a zero, ou i é igual a j
            #ou é um ponto que não se conecta com o i
            if mShort[i][j]!=0:
                soma+=(mEucl[i][j]/mShort[i][j])
                #conta a quantidade de nós que i é conectado
                cont+=1
            j+=1
        #o fator de normalização é 1/(ncc-1), onde ncc é o número de
        #vertices da componente conexa incluindo o proprio vertice em analise

        #se cont for igual a zero quer dizer que o nó i não se conecta com os
        #demais nós, assim atribuímos a ele um valor padrão, no caso -1
        if cont==0:
            total=-1
        else:
            div=1/(float(cont))
            total=div*soma
        lista.append((i, total))
        i+=1
    return lista


#### Base functions ####

def strtoint(x):
    lista = []
    for i in x:
        lista.append((int(i[0]), int(i[1])))
    return lista

def mediaGraus(lista):
    soma=0.0
    cont=0.0
    for x in lista:
        cont+=1
        soma+=x;
    return soma/cont

def arquivoParaOd(arquivo):
    m=[]
    for linha in arquivo:
        ls=linha.replace(' \n','').split(' ')
        m.append(ls)

    valores=[]
    i=0
    while i<len(m):
        j=0
        while j<len(m[i]):
            if m[i][j]=='1':
                valores.append((i, j))
            j+=1
        i+=1

        valor=(len(m))
    return (valores, valor)

### Limiar Matriz ###

def gerarMatrizLimiar(limiar, cidade):

    if cidade=='sjc':
        arquivo = open('sjc/matriz_sjc.txt', 'r')
        escrita = open('sjc/matrizes/MatrizLimiar'+str(limiar)+'.txt', 'w')
        od = open('sjc/listas/OdLimiar'+str(limiar)+'.txt', 'w')

    if cidade=='rio':
        arquivo = open('rio/ODM_RJ.txt', 'r')
        escrita = open('rio/matrizes/MatrizLimiar'+str(limiar)+'.txt', 'w')
        od = open('rio/listas/odLimiar'+str(limiar)+'.txt', 'w')
        
    matriz=[]
    lista=[]

    for linha in arquivo:
        lista=linha.split(' ')[:-1]
        matriz.append(lista)

    arquivo.close()

    s=''
    t=''
    i=0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if int(matriz[i][j])<=limiar or i==j:
                s+='0 '
            else:
                t+=str(i)+' '+str(j)+'\n'
                s+='1 '
            j+=1
        s+='\n'
        i+=1


    escrita.write(s)
    escrita.close()
    od.write(t)
    od.close()
    print('Matriz com limiar '+str(limiar)+' gerada')


###### main #######

limiar=1
cidade='sjc'

if cidade=='sjc':

    gerarMatrizLimiar(limiar, cidade)
    
    arquivoEucl = open('sjc/matrizes/euclidianaCentroidesSJC.txt','r')

    arquivo = open('sjc/matrizes/MatrizLimiar'+str(limiar)+'.txt','r')
    fileGlobais = open('sjc/valoresGrafo/valoresSjcLimiar'+str(limiar)+'.txt', 'w')
    fileNo = open('sjc/valoresGrafo/ValoresPorVerticeSjcLimiar'+str(limiar)+'.txt', 'w')

if cidade=='rio':

    gerarMatrizLimiar(limiar, cidade)

    arquivoEucl = open('rio/matrizes/matrizEuclidianaRJ.txt','r')

    arquivo = open('rio/matrizes/MatrizLimiar'+str(limiar)+'.txt','r')
    fileGlobais = open('rio/valoresGrafo/valoresRioLimiar'+str(limiar)+'.txt', 'w')
    filleNo = open('rio/valoresGrafo/ValoresPorVerticeRioLimiar'+str(limiar)+'.txt', 'w')



res = arquivoParaOd(arquivo)
valores=res[0]
valor=res[1]-1


ls=[]
lista=[]
m=[]



m = []
for l in arquivoEucl:
    x=l.replace('\n', '').split(' ')
    m.append(x[:-1])

matrizEucli=[]
for el in m:
    lista=[]
    for e in el:
        lista.append(float(e))
    matrizEucli.append(lista)


arquivo.close()
arquivoEucl.close()

g = Graph()
g.add_vertices(valor)
g.add_edges(strtoint(valores))

mShort=matrizMenorCaminho(g, valor)
mEucl=matrizEucli


s='Nos Arestas Diametro GrauMedio MenorCaminho EficienciaGlobal\n'

s+=(str(len(g.degree())))

s+=(' '+str(len(g.get_edgelist())))

s+=(' '+str(g.diameter()))

s+=(' '+str(mediaGraus(g.degree())))

s+=(' '+str(g.average_path_length()))

efg=eficienciaGlobal(g, mShort)
s+=(' '+str(efg))


fileGlobais.write(s)
fileGlobais.close()
print('Arquivo com caracterização global gerado')

i=0
n=len(g.degree())

stra=straightness(mShort, mEucl, g)
t='no eficiencia vulnerabilidade straightness\n'
while i<n:
    t+=(str(i))
    
    t+=(' '+ str(eficienciaVertice(g, i, mShort)))
    t+=(' ' + str(vulnerabilidade(eficienciaVertice(g, i, mShort), efg)))
    t+=(' '+ str(stra[i][1]))
    t+='\n'
    i+=1

fileNo.write(t)
fileNo.close()
print('Arquivo com caracterização por vértice gerado')
