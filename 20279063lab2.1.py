# -*- coding: utf-8 -*-
"""
"""

n=input("Veuillez choisir un nombre entre 0 et 1000") #ici on demande à l'utilisateur de choisir un nombre entre 0 et 1000
n=int(n) #on change le type d'objet du input pour pouvoir faire des operations mathématique dessus
nlist=[n] #la liste nlist est la valeur de n

while(n>=0): #on defini une boucle que tant que la variable n est plus grande que 0 on  reccommence la boucle suivante
    if(n==0): #si l'utilisateur rentre 0 comme input le programme va fermer la boucle avec la fonction break et conséquamment se terminer
        print("Le programme est fini!")
        break
    
    else: #si la valeur rentrée est différente de 0 alors le programme va effecteur la deuxieme boucle
    
        while(n!=0): #la deuxieme boucle va etre repeter tant que n est pas égal à 0
            if(1<n<1000): 
                while(1<n): #ici on defini la troisieme boucle qui est fonctionnelle tant que n est plus grand que 1
                    if(n==0):
                        break
                    
                    else: #si la valeur de n est differente de 0 alors la 4ieme boucle va faire les operations mathématique
                        while(n!=1): #si la valeur de n est 1 alors la boucle va se fermer
                        
                            if(n%2==0): #si n est pair alors n+1 va etre n diviser par 2
                                (n:=n/2 )
                                nlist.append(n) #on rajoute la valeur de n+1 a la liste 'nlist'
                            else: #si n est pas pair (alors n est impair) alors n+1 va etre n fois 3 plus 1
                                (n:=n*3+1)
                                nlist.append(n) #on rajoute la valeur de n+1 a la liste 'nlist'
                print(nlist) 
                
            elif(1000<n): #si la valeur de n est plus grande que 1000 alors un message d'erreur va etre affiché et va demander à l'utilisateur de rentrer une valeur entre 0 et 1000
                n=input("Erreur! Veuillez choisir un nombre entre 0 et 1000")
                n=int(n)
                nlist=[n]    
                
            elif(n<0): #si la valeur de n est plus petite que 0 alors un message d'erreur va etre affiché et va demander à l'utilisateur de rentrer une valeur entre 0 et 1000
                n=input("Erreur! Veuillez choisir un nombre entre 0 et 1000")
                n=int(n)
                nlist=[n]
                
            else: #lorsque toutes les boucles on fini le programme va afficher ce message et va continuer. Ceci fait que tant que la valeur rentrer par l'utilisteur n'est pas 0 alors le programme reccomence.
                n=input("Veuillez choisir un nombre entre 0 et 1000")
                n=int(n)
                nlist=[n]