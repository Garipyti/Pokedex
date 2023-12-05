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
    #root.configure(background='#5b5a57')

##################################################
    #création boutons :
    #relwidth=0.4,relheight=0.1
    frameRadio=Frame(root)
    frameRadio.place(relx=0,rely=0.1,relwidth=0.4,relheight=0.1)
    #Menu déroulant pour choisir critère de classement
    listeAttribut=list(pokemon.columns)
    choixClassement=ttk.Combobox(frameRadio,values=listeAttribut)
    def action(event): #méthode qui stocke le choix dans le menu déroulant
        select = choixClassement.get()

    choixClassement.pack()
    choixClassement.bind("<<ComboboxSelected>>", action)
    choixClassement.grid(row=1,column=0,sticky=W,columnspan=2)
    choixClassementLabel=Label(frameRadio,text="Classer selon :")
    choixClassementLabel.grid(row=0,column=0)

    #radio buttons pour choisir si classement croissant ou décroissant
    labelSensclassement=Label(frameRadio, text="dans l'ordre")
    labelSensclassement.grid(row=0,column=3,sticky=W,columnspan=2)
    cStringVar=StringVar(root,'sensclassement')
    classementC=Radiobutton(frameRadio, variable=cStringVar, value="C" )
    classementC.grid(row=1,column=3,sticky=W)
    labelclassementC=Label(frameRadio,text='croissant')
    labelclassementC.grid(row=1,column=4,sticky=W)
    classementD=Radiobutton(frameRadio,variable=cStringVar,value="D")
    classementD.grid(row=2,column=3,sticky=W)
    labelclassementD=Label(frameRadio,text='décroissant')
    labelclassementD.grid(row=2,column=4,sticky=W)

    #Check button pour choisir le ou les critères de filtre
    rootHeight = root.winfo_height()
    rootWidth = root.winfo_width()
    frameCheck = Frame(root)
    frameCheck.place(relx=0.5,rely=0.1,relheight=0.35,relwidth=0.4)
    dicofiltres={}

    class checkbutton : #classe de boutons cochables
            def __init__(self,texte,a,b,zt,mdRO):
                self.texte=texte
                self.a=a
                self.b=b
                self.zt=zt
                self.mdRO=mdRO
            def creerCheckbutton(self):  # on définit une fonction qui crée et place un bouton cochable et son entrée associée
                self.cbVar = IntVar()
                self.ztVar= StringVar()
                self.mdVar= StringVar()
                self.dico={self.texte:[self.cbVar,self.ztVar,self.mdVar]} #on crée un item propre à chaque bouton, qui a pour key le nom du filtre et en value une liste avec l'etat et l'attribut de tri

                self.checkbox = Checkbutton(frameCheck, variable=self.cbVar, text=str(self.texte), offvalue=0, onvalue=1) #on crée le bouton cochable
                self.checkbox.place(relx=self.a, rely=self.b)

                def entrymtd(self): #méthode qui met à jour le dico général dès qu'il y a une modif dans la zone de texte
                    nvlentree=self.zt.get()
                    self.dico={self.texte:[self.cbVar,nvlentree]}
                    dicofiltres.update(self.dico)
                self.zt=Entry(frameCheck, command=entrymtd(self)) #crée la zone de texte associée au bouton
                self.zt.place(relx=a+0.24,rely=b,relheight=0.08,relwidth=0.1)

                listeRelOrdre=["<",">","="]
                self.mdRO = ttk.Combobox(frameCheck, values=listeRelOrdre) #création du menu déroulant des relaitions d'ordre
                def actionmdRO(event):
                    mdVar = self.mdRO.get()
                    self.dico={self.texte:[self.cbVar,self.ztVar,mdVar]}
                self.mdRO.bind("<<ComboboxSelected>>", actionmdRO)
                self.mdRO.place(relx=a+0.35,rely=b,relheight=0.07,relwidth=0.08  )

    for i in range (0,len(listeAttribut)) : #boucle qui crée autant de boutons cochables qu'il y a de colonnes dans le dataframe
        texte=str(listeAttribut[i])
        zt=Entry(frameCheck)
        mdRO=ttk.Combobox(frameCheck)
        if i*0.1 < 1 :
            a=0.05
            b=i*0.1
        else :
            a=0.51
            b=i*0.1 % 1
        nvbouton=checkbutton(texte,a,b,zt,mdRO)
        nvbouton.creerCheckbutton()

    #Création du bouton d'affichage du résultat
    boutonResultat=Label(root,text="Afficher DataFrame")
    def clique_label():
        sdf=pokemon
        print(dicofiltres)
        for i in dicofiltres:
            print (i)

    boutonResultat.bind("<Button-1>", clique_label())
    boutonResultat.place(relx=0.8,rely=0.4)
affichage()


mainloop()







#def favori(cible):
    #créer sous dataframe


