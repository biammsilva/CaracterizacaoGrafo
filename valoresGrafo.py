# -*- coding: utf-8 -*-
from igraph import Graph

#this function generate a Matrix with the shortest paths between the nodes
#this matrix help us to know a lot of indices, for example
#vulnerability, global efficiency, straightness centrality
def matrizMenorCaminho(g, valor):
    nova=[]
    valor=valor+1
    for i in range(valor):
        lista=[]
        menores=g.shortest_paths(i)
        nova.append(menores[0])
    return nova

def menorCaminhoMedio(x, g):
    lista=g.shortest_paths(x)
    y=float((sum(lista[0])))/(len(lista[0])-1)
    return y

def eficienciaGlobal(g, matriz):
    return calculosEficiencia(matriz, g, g)

def calculosEficiencia(matriz, y, g):
    i=0
    x=0.0
    while i<len(matriz):
        j=0
        while j<len(matriz[i]):
            if matriz[i][j]!=0:
                x+=1.0/matriz[i][j]
            j+=1
        
        i+=1
    n=g.vcount()
    return x/((n)*(n-1))

#this function generate another Graph equals the basic one to delete the node in
#question to make some calculations to discover how eficient is the node
#and what happens if it is not there
def eficienciaVertice(g, n, matriz):
    gr = Graph()
    gr.add_vertices(g.vcount()-1)
    gr.add_edges(g.get_edgelist())
    gr.delete_vertices(n)
    return calculosEficiencia(matrizMenorCaminho(gr, gr.vcount()-1), gr, g)

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
            if i!=j and mShort[i][j]!=0: 
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
            div=1/(float(cont)-1)
            total=div*soma
        lista.append((i, total))
        i+=1
    return lista


############################ Base functions ####################################

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

############################### Limiar Matriz ###################################

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


########################################## main ###################################

def gerarDados(cidade, limiar):
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
        fileNo = open('rio/valoresGrafo/ValoresPorVerticeRioLimiar'+str(limiar)+'.txt', 'w')


    if cidade=='pipaVovo':

        arquivoEucl = open('pipaVovo/euclidiana_pipavovo.txt','r')

        arquivo = open('pipaVovo/matrizpipavovo.txt','r')
        fileGlobais = open('pipaVovo/valoresPipaLimiar'+str(limiar)+'.txt', 'w')
        fileNo = open('pipaVovo/ValoresPorVerticePipaLimiar'+str(limiar)+'.txt', 'w')



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
    t='no grau aglomeracao minimoCaminho eficiencia vulnerabilidade straightness\n'
    while i<n:
        t+=(str(i))
        print i
        t+=(' '+str(g.degree(i)))
        t+=(' '+str(g.transitivity_local_undirected(i)))
        t+=(' '+str(menorCaminhoMedio(i,g)))
        t+=(' '+ str(eficienciaVertice(g, i, mShort)))
        t+=(' ' + str(vulnerabilidade(eficienciaVertice(g, i, mShort), efg)))
        t+=(' '+ str(stra[i][1]))
        t+='\n'
        i+=1

    fileNo.write(t)
    fileNo.close()
    
    print('Arquivo com caracterização por vértice gerado')

#gerarDados('rio',1)
#gerarDados('rio',58)
gerarDados('rio',4646)
#gerarDados('rio',5000)
