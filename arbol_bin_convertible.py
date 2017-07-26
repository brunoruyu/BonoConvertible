# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:26:50 2017
@author: bruno
"""
import numpy as np
import math

s0=100 #precio inicial
T=5 #Tiempo de Expiración
v=0.1 #volatilidad
rf=0.048790 #risk free rate
n=5 #pasos binomiales
CR=1 #Convertion Ratio
coup=0.1 #Coupon
cs=0.1   #Credit Spread
par= 100

def arbol_bin(s0,T,v,rf,n,CR,coup,cs,par):
    #Calculos básicos
    dt=T/n
    print(dt)
    u=math.exp((rf-0.5*v**2)*dt+v*math.sqrt(dt))
    d=math.exp((rf-0.5*v**2)*dt-v*math.sqrt(dt))
    drift=math.exp(rf*dt)    
    q=(drift - d)/(u-d)
       
    stkval = np.zeros((n+1,n+1)) # árbol del Stock - matriz de n+1 x n+1
    optval = np.zeros((n+1,n+1)) #árbol de la Opción
    p= np.zeros((n+1,n+1)) #árbol de la probabilidad
    disc= np.zeros((n+1,n+1)) #árbol del adjusted discount rate
    stkval[0,0]=s0
    #Armo el árbol del Stock
    for i in range(1,n+1): #i es el paso temporal
        stkval[0,i]=stkval[0,i-1]*u
        for j in range(1,i+1): #j es la altura en el arbol (menor j, más alto) 
            stkval[j,i]=stkval[j-1,i-1]*d
    #print((stkval))
    
    #Recursión para atrás en el arbol de la Opción    
    for j in range(0,n+1):
        optval[j,n]=max(par*(1+coup),CR*stkval[j,n])
        if(par*(1+coup)<CR*stkval[j,n]):
            p[j,n]=1
        else:        
            p[j,n]=0
          
    for i in range(n-1,-1,-1):
        for j in range(0,i+1):
            p[j,i]=(p[j,i+1]+p[j+1,i+1])/2.0
            disc[j,i]=1+p[j,i]*rf+(1-p[j,i])*cs
            
            optval[j,i]=max((q*optval[j,i+1]+(1-q)*optval[j+1,i+1])/disc[j,i]
            +par*coup,CR*stkval[j,i])
            
    #print((p))
    #print((disc))
    #print((optval))        
    return optval[0,0]


opt0=arbol_bin(s0,T,v,rf,n,CR,coup,cs,par)
print("Valor de la Opción =",opt0)