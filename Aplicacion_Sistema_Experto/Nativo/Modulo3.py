import numpy as np

def EYE_1():
    Error=0.0
    tolerancia=0.0
    Numero_pailas=0.0
    tolerancia = 0.000001
    Numero_pailas=np.zeros((5,4))
    #Numero_pailas = Cells(5, 4) #' valor fijo
    #Error = Range("M182")
    
    while Error > tolerancia:
        for i in range(0,Numero_pailas):
            print(9)
            #Cells(114, i + 4) = Cells(180, i + 4)
        #Error = Range("M182")
    print(9)

def EYE_2():
    Error = 0.0
    tolerancia = 0.0
    Xp1 = 0.0
    Xp2 = 0.0
    Fx = 0.0
    Fxc = 0.0
    Bz = 0.0
    Bz2 = 0.0
    Numero_pailas = 0.0
    #Numero_pailas=np.zeros((5,4)) #' valor fijo
    for i in range(0,Numero_pailas):
        #Cells(114, i + 4) = Cells(41, i + 4)
        print(1)
    tolerancia = 0.000001
    Xp1 = Cells(12, 4) #' valor fijo
    Xp2 = Cells(76, 5)
    Error = abs(Xp1 - Xp2)
    Bz = 3
    Niter = 0   
    
    while Error > tolerancia and Niter < 50.0:
        Niter = Niter + 1
        #Range("l183") = Niter
        
        #Cells(4, 4) = Bz
        EYE_1()
        Fx = Cells(76, 5) - Cells(12, 4)
        Cells(4, 4) = Bz + tolerancia
        EYE_1()
        Fxc = Cells(76, 5) - Cells(12, 4)
        Der = (Fxc - Fx) / tolerancia
        B = Fx - Der * Bz
        Bz2 = -B / Der
        Error = abs(Bz - Bz2)
        if Error < 0.5:
            Bz = Bz2
        else:
            if Bz - Bz2 > 0.5:
                Bz = Bz - 0.5
            else:
                Bz = Bz + 0.5