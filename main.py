import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#valores
dias = 20

custoA = 60
custoB = 135

vendaA = 150
vendaB = 280

limEstoqueX = 300
limEstoqueY = 250

compraEstoqueX = 500
compraEstoqueY = 400

listaDias = np.arange(dias) + 1

# gera o estoque inical de acordo com a regra necessária dita no problema
estoqueInicial = [np.random.randint(limEstoqueX, limEstoqueX + compraEstoqueX),
                   np.random.randint(limEstoqueY, limEstoqueY + compraEstoqueY)]

#variaveis
demandaA= []
demandaB = []

producaoA = []
producaoB = []

estoqueX = []
estoqueY = []

lucroA = []
lucroB = []

#criando dataFrame
simulacao = pd.DataFrame()
simulacao["Dia"] = listaDias
#cria as colunas no dataFrame
path = os.path.abspath(__file__)


#cria as colunas no dataFrame
for id, i in simulacao.iterrows():    
    
    # inserindo os valores aleatorios à lista a partir da tabela de probabilidades 
    demandaA.append(np.random.choice([70, 80, 90, 100, 120, 130], p=[0.1, 0.25, 0.2, 0.3, 0.1, 0.05])) 
    demandaB.append(np.random.choice([80, 95, 110, 130, 140, 160], p=[0.15, 0.20, 0.25, 0.30, 0.05, 0.05])) 
    producaoA.append(np.random.choice([60, 75, 80, 150, 180, 200],p=[0.1, 0.2, 0.25, 0.25, 0.1, 0.1]))
    producaoB.append(np.random.choice([60, 75, 90, 110, 130, 170], p=[0.1, 0.2, 0.2, 0.3, 0.1, 0.1]))
    
    # adiciona o valor inical do estoque de X e Y no inicio de cada dia
    if id == 0:
        estoqueX.append(estoqueInicial[0])
        estoqueY.append(estoqueInicial[1])

    else:
        #calcula o que restou do estoque X no dia anterior menos o que foi produzido no dia anterior
        restoEstoqueX = estoqueX[id - 1] - 2 * (producaoA[id] + producaoB[id])
        #se o estoque for menor que o limite, faz pedido de compra
        if restoEstoqueX <= limEstoqueX:
            #se for menor que 0, adiciona as 500 unidades, se não soma o que sobrou com as 500 unidades
            if restoEstoqueX < 0:
                estoqueX.append(compraEstoqueX)
            else:
                estoqueX.append((restoEstoqueX) + compraEstoqueX)
        else:
            estoqueX.append(restoEstoqueX)

        #calcula o que restou do estoque Y no dia anterior menos o que foi produzido no dia anterior
        restoEstoqueY = estoqueY[id - 1] - producaoA[id - 1] - (3*producaoB[id - 1])

        if restoEstoqueY <= limEstoqueY:
            if restoEstoqueY < 0:
                if id == 1:
                    estoqueY.append(0)
                else:
                    estoqueY.append(compraEstoqueY)
            else:
                estoqueY.append(restoEstoqueY + compraEstoqueY)
        else:
            estoqueY.append(restoEstoqueY)

    # Lucros
    # se a demanda for menor que a produção, o lucro é a demanda vezes o valor de venda menos a produção vezes o custo
    if demandaA[id] <= producaoA[id]:
        lucroA.append((demandaA[id] * vendaA) - (producaoA[id] * custoA))
    # caso não seja, o lucro é a produção vezes o valor de venda menos a produção vezes o custo
    else:
        lucroA.append((producaoA[id] * vendaA) - (producaoA[id] * custoA))

    #faz a mesma coisa só que para o produto B
    if demandaB[id] <= producaoB[id]:
        lucroB.append((demandaB[id] * vendaB) - (producaoB[id] * custoB))
    else:
        lucroB.append((producaoB[id] * vendaB) - (producaoB[id] * custoB))


## Construindo planilha da simulação
simulacao["Demanda A"] = np.array(demandaA)
simulacao["Demanda B"] = np.array(demandaB)
simulacao["Produção A"] = np.array(producaoA)
simulacao["Produção B"] = np.array(producaoB)
simulacao["Estoque Inicial do Dia X"] = np.array(estoqueX)
simulacao["Estoque Inicial do Dia Y"] = np.array(estoqueY)
simulacao["Lucro A"] = np.array(lucroA)
simulacao["Lucro B"] = np.array(lucroB)
simulacao.set_index(simulacao["Dia"], inplace=True)
simulacao.drop("Dia", axis=1, inplace=True)

# criando o grafico da produção x demanda
fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
fig.set_figheight(10)
fig.set_figwidth(15)

for ax in axs:
    ax.set_xticks(listaDias)
    ax.set_xlabel("Dias")
    ax.set_ylabel("Quantidades")

fig.suptitle('Produção x Demanda', fontsize = 15)
#plotando grafico de produção e demanda A e B
axs[0].bar(listaDias + 0.15, simulacao["Demanda A"], width= 0.15 * 2.5, color= "greenyellow", label= "Demanda")
axs[0].bar(listaDias - 0.15, simulacao["Produção A"], width= 0.15 * 2.5, color= "coral", label= "Produção")
axs[0].set_title("Produto A")
axs[1].bar(listaDias + 0.15, simulacao["Demanda B"], width= 0.15 * 2.5, color= "greenyellow")
axs[1].bar(listaDias - 0.15, simulacao["Produção B"], width= 0.15 * 2.5, color= "coral")
axs[1].set_title("Produto B")
fig.legend()
#salvando o grafico
fig.savefig(os.path.realpath(__file__).replace(__file__.split("\\")[-1], "producaoXdemanda.png"))
#limpando o grafico
plt.clf()

## Gerando gráfico de receita por dia de cada produto
plt.title("Lucro")
plt.bar(listaDias + 0.15, simulacao["Lucro A"], width=0.15 * 2, color="teal", label="Lucro A")
plt.bar(listaDias - 0.15, simulacao["Lucro B"], width=0.15 * 2,  color="darkviolet", label="Lucro B")
plt.xlabel("Dias")
plt.ylabel("Lucro")
plt.xticks(listaDias)
plt.legend()
plt.savefig(os.path.realpath(__file__).replace(__file__.split("\\")[-1], "lucro.png"))