
# ░██████╗██╗░░░██╗██████╗░███████╗██████╗░██████╗░███████╗███████╗
# ██╔════╝██║░░░██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
# ╚█████╗░██║░░░██║██████╔╝█████╗░░██████╔╝██████╦╝█████╗░░█████╗░░
# ░╚═══██╗██║░░░██║██╔═══╝░██╔══╝░░██╔══██╗██╔══██╗██╔══╝░░██╔══╝░░
# ██████╔╝╚██████╔╝██║░░░░░███████╗██║░░██║██████╦╝███████╗███████╗
# ╚═════╝░░╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚══════╝╚══════╝
###
### Trabalho 03 de Metodos Numericos Para Equacoes Diferenciais II
### UERJ - IPRJ - 2023.2
### Professor: Grazione Souza
### Alunos: Manoel Rodrigues e Gabriel 
###
### Lembre-se de instalar o matplotlib (pip install matplotlib ou pip3 install matplotlib)
###


import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def superBee(comprimento, numeroVolumes, t_inicial, t_final, velocidade, ca, cb, cc):
    tempoDeInicio = datetime.now()
    DeltaX = comprimento / numeroVolumes
    DeltaT = 0.95* DeltaX/ (velocidade)
    tempo = np.arange(t_inicial, t_final, DeltaT)
    espaco = np.arange(0, comprimento, DeltaX)
    Q = np.zeros(numeroVolumes)
    Qfinal = np.zeros(numeroVolumes)

   
    for i in range(numeroVolumes):
        if espaco[i] <= comprimento / 2:
            Q[i] = ca
        else:
            Q[i] = cb

    for n in range(len(tempo)):
        QnMaisUm = np.copy(Q)  
        for i in range(1,numeroVolumes-1):
            if tempo[n] >= t_final / 2:
                QnMaisUm[0] = cc 

            denominador_max = Q[i + 1] - Q[i]
            denominador_min = Q[i] - Q[i - 1]
            C = (velocidade*DeltaT)/DeltaX

            # evitar divisão por zero
            if denominador_max == 0 or denominador_min == 0:
                psiMaisMeio = 0.0
                psiMenosMeio = 0.0
            else:
                psiMaisMeio = max(0 , min(1, 2*((Q[i]-Q[i-1])/(Q[i+1]-Q[i]))), min(2, ((Q[i]-Q[i-1])/(Q[i+1]-Q[i]))))
                psiMenosMeio = max(0, min(1, 2*((Q[i-1]-Q[i-2])/(Q[i]-Q[i-1]))), min(2, ((Q[i-1]-Q[i-2])/(Q[i]-Q[i-1]))))
            

            
            if i == 0:
                Qaux = Q[i] - (C  * (Q[i] - (2 * ca - Q[i])))
            elif i==1: 
                Qaux = Q[i] - (C  * (Q[i] - Q[i-1]))
            elif(i == numeroVolumes - 1): 
                Qaux = Q[i] - (C  * (Q[i] - Q[i-1]))
            else: 
                Qaux = Q[i] - (C  * (Q[i] - Q[i-1])) - (C/2)*(1-C)*(psiMaisMeio*(Q[i+1] - Q[i]) - psiMenosMeio*(Q[i]-Q[i-1]))

            QnMaisUm[i] = Qaux

        Q = np.copy(QnMaisUm)  
        Qfinal = np.copy(QnMaisUm)

        tempoDeFim = datetime.now()

    tempoDeExecucao = (tempoDeFim - tempoDeInicio).total_seconds() 

    return espaco, Qfinal, tempoDeExecucao


def plotaGrafico(comprimento,  numeroVolumes, tInicial, tFinal, velocidade,ca, cb, cc):
    volume, dados, tempoDeExecucao = superBee(comprimento,  numeroVolumes, tInicial, tFinal, velocidade,ca, cb, cc)
    plt.title('Concentração x Comprimento')
    plt.plot(volume,dados, label='$T_{total}$')
    plt.xlabel('Comprimento')
    plt.ylabel('Concentração')
    plt.legend(title = r'$t$', loc=0)
    plt.legend(title = r'$Tempo_{execução}$ = '+str(tempoDeExecucao)+" s", loc=0)

    plt.show()


def refinamentoDeMalha(comprimento, tInicial, tFinal, velocidade,ca, cb, cc):
    volumes = [12,24,48,96,192]
    for i in range(len(volumes)):
        volume, dados, tempoDeExecucao = superBee(comprimento,  volumes[i], tInicial, tFinal, velocidade,ca, cb, cc)
        plt.plot(volume,dados, label=str(volumes[i]))
        plt.legend(title = r'$Numero$ $de$ $Volumes$', loc=0)
        plt.legend(title = r'$Tempo_{execução}$ = '+str(tempoDeExecucao)+" s", loc=0)
        
    plt.title('Refinamento de malha')
    plt.xlabel('Comprimento')
    plt.ylabel('Concentração')
    plt.show()

def variacaoComprimento(numeroVolumes, tInicial, tFinal, velocidade,ca, cb, cc):
    comprimentos = [200,250,300,350,400]
    for i in range(len(comprimentos)):
        volume, dados, tempoDeExecucao = superBee(comprimentos[i],  numeroVolumes, tInicial, tFinal, velocidade, ca, cb, cc)
        plt.plot(volume,dados, label=str("%.2f" %comprimentos[i]))
        plt.legend(title = r'$L_x$', loc=0)
        plt.legend(title = r'$Tempo_{execução}$ = '+str(tempoDeExecucao)+" s", loc=0)
        
    plt.title('Variação de Comprimento')
    plt.xlabel('Comprimento')
    plt.ylabel('Concentração')
    plt.show()  


def variacaoVelocidade(comprimento,  numeroVolumes, tInicial, tFinal, ca, cb, cc,):
    velocidades = [0.25,0.5,1,1.5,1.75]
    for i in range(len(velocidades)):
        volume, dados, tempoDeExecucao = superBee(comprimento,  numeroVolumes, tInicial, tFinal, velocidades[i], ca, cb, cc)
        plt.plot(volume,dados, label=str("%.2f" %velocidades[i]))
        plt.legend(title = r'$ \overline{u}$', loc=0)
        plt.legend(title = r'$Tempo_{execução}$ = '+str(tempoDeExecucao)+" s", loc=0)
        
    plt.title('Variação de Velocidade')
    plt.xlabel('Comprimento')
    plt.ylabel('Concentração')
    plt.show()

def variacaoTempo(comprimento,  numeroVolumes, tInicial, tFinal, velocidade,ca, cb, cc, qtdComparacoes):
    passoTempo=float((tFinal-tInicial)/qtdComparacoes)
    tempos = np.arange(tInicial+passoTempo, tFinal+passoTempo, passoTempo)
    for i in range(len(tempos)):
        volume, dados, tempoDeExecucao = superBee(comprimento,  numeroVolumes, tInicial, tempos[i], velocidade, ca, cb, cc)
        plt.plot(volume,dados, label=str(tempos[i]))
        plt.legend(title = r'$T_f$', loc=0)
        plt.legend(title = r'$Tempo_{execução}$ = '+str(tempoDeExecucao)+" s", loc=0)
        
    plt.title('Variação de Tempo')
    plt.xlabel('Comprimento')
    plt.ylabel('Concentração')
    plt.show()   


plotaGrafico(comprimento=300, numeroVolumes=128,tInicial= 0,tFinal=20,velocidade=1,ca=0.9,cb= 0.2,cc= 1.1)
refinamentoDeMalha(comprimento=300, tInicial=0,tFinal= 5,velocidade=1,ca=0.9, cb=0.2, cc=1.1)
variacaoComprimento( numeroVolumes=128, tInicial=0, tFinal=20, velocidade=1, ca=0.9, cb=0.2, cc=1.1 )
variacaoTempo(comprimento=300, numeroVolumes=128, tInicial=0, tFinal=20, velocidade=1, ca=0.9, cb=0.2, cc=1.1, qtdComparacoes=5 )
variacaoVelocidade(comprimento = 300,numeroVolumes= 128,tInicial=0,tFinal=20, ca=0.9,cb= 0.2, cc=1.1)
