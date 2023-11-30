import pandas as pd
from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from IPython.display import display
pokemon = pd.read_csv("pokemon.csv") # il y aura peut-être besoin d'enlever les NaN plus tard

##########méthodes de tri##########
class filtre(ABC) : #méthode de filtre générale

    @abstractmethod
    def filtre(self):
        pass

class filtrec(filtre): #méthode pour chercher les pokémons avec un attribut = valeur
    def filtre(self, attribut, valeur):
        return (self[self[attribut] == valeur])

class filtreinf(filtre): #méthode pour chercher les pokémons avec un attribut < valeur
    def filtre(self,attribut,valeur):
        return self[self[attribut] < valeur]

#méthode pour chercher les pokémons avec un attribut > valeur
class filtresup(filtre):
    def filtre(self,attribut,valeur):
        return (self[self[attribut] > valeur])

class classement(ABC): #méthode de classement générale qui prend en argument l'attribut de classement

    @abstractmethod
    def classement(self,attribut):
        pass

class cd(classement) : #méthode de classement par ordre décroissant
    def classement(self,attribut):
        return (pd.DataFrame.sort_values(self,attribut, ascending=False))

class cc(classement) : #méthode de classement par ordre croissant
    def classement(self,attribut):
        return (pd.DataFrame.sort_values(self,attribut, ascending=True))



# ex syntaxe : print(filtrec.filtre(pokemon,"Speed",180))

#######Vue########
def affichage():
##################################################
    #création fenêtre
    root=Tk()
    sdf=pokemon
    root.geometry('1000x1000')
    #root.attributes('-fullscreen',True)
    root.configure(background='#DB261D')

##################################################
    #création boutons :

    #Menu déroulant pour choisir critère de classement
    listeAttribut=list(pokemon.columns)
    choixClassement=ttk.Combobox(root,values=listeAttribut)
    def action(event):
        select = choixClassement.get()

    choixClassement.pack()
    choixClassement.bind("<<ComboboxSelected>>", action)
    choixClassement.place(relx=0.1,rely=0.1)


    #radio buttons pour choisir si classement croissant ou décroissant
    cStringVar=StringVar(root,'sensclassement')
    classementC=Radiobutton(root, variable=cStringVar, value="C" )
    classementC.place(relx=0.35,rely=0.1)
    labelclassementC=Label(root,text='croissant')
    labelclassementC.place(relx=0.4,rely=0.1)
    classementD=Radiobutton(root,variable=cStringVar,value="D")
    classementD.place(relx=0.35,rely=0.12)
    labelclassementD=Label(root,text='décroissant')
    labelclassementD.place(relx=0.4,rely=0.12)

    #Check button pour choisir le ou les critères de filtre
    rootHeight = root.winfo_height()
    rootWidth = root.winfo_width()
    frameCheck = Frame(root,background='grey')
    frameCheck.place(relx=0.5,rely=0.3,relheight=0.35,relwidth=0.3)
    frameCheckHeight=frameCheck.winfo_height()
    frameCheckWidth = frameCheck.winfo_width()
    dicofiltres={}

    class checkbutton : #classe de boutons cochables
        def __init__(self,texte,a,b):
            self.texte=texte
            self.a=a
            self.b=b

        def creerCheckbutton(self):  # on définit une fonction qui crée et place un bouton cochable et son entrée associée
            self.cbVar = IntVar()
            self.ztVar= StringVar()
            self.dico={self.texte:[self.cbVar,self.ztVar]} #on crée un item propre à chaque bouton, qui a pour key le nom du filtre et en value une liste avec l'etat et l'attribut de tri
            checkbox = Checkbutton(frameCheck, variable=self.cbVar, text=str(self.texte), offvalue=0, onvalue=1)
            checkbox.place(relx=self.a, rely=self.b)
            #def updatedico(self,VarTexte,dicofiltres):
                #dicofiltres.update(self.dico)
            #zt=Entry(frameCheck, variable=self.ztVar, command=updatedico(self,self.ztVar,dicofiltres))
            #zt.place(relx=a+0.1,rely=b)





    for i in range (0,len(listeAttribut)) : #boucle qui crée autant de boutons cochables qu'il y a de colonnes dans le dataframe
        texte=str(listeAttribut[i])
        if i*0.1 < 1 :
            a=0.1
            b=i*0.1
        else :
            a=0.6
            b=i*0.1 % 1
        nvbouton=checkbutton(texte,a,b)
        nvbouton.creerCheckbutton()


affichage()


mainloop()







#def favori(cible):
    #créer sous dataframe


