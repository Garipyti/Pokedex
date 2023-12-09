import pandas as pd
from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from IPython.display import display
pokemon = pd.read_csv("pokemon.csv") # il y aura peut-être besoin d'enlever les NaN plus tard

##########méthodes de tri##########
class filtre(pd.DataFrame,ABC) : #méthode de filtre générale

    @abstractmethod
    def filtre(self, attribut, valeur):
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

class classement(pd.DataFrame, ABC): #méthode de classement générale qui prend en argument l'attribut de classement

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
    root.title("Pokédex")
    root.geometry('1000x1000')
    #root.attributes('-fullscreen',True)
    #root.configure(background='#5b5a57')
#################################################
    #création affichage df
    frameViewer=Frame(root,width=1,height=0.4)
    frameViewer.place(relx=0,rely=0.6)
    class DataFrameViewer:
        instances = []  # Liste pour stocker les instances actives
        def __init__(self, master, dataframe):
            self.master = master

            self.dataframe = dataframe
            self.current_row = 0

            # Création du Treeview pour afficher le DataFrame
            self.tree = ttk.Treeview(self.master)
            self.tree["columns"] = list(self.dataframe.columns)
            self.tree["show"] = "headings"

            for column in self.dataframe.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=100)  # Ajustez la largeur des colonnes selon vos besoins

            self.tree.bind("<Up>", self.navigate_up)
            self.tree.bind("<Down>", self.navigate_down)

            # Remplissage du Treeview avec les données du DataFrame
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.tree.pack(expand=YES, fill=BOTH)

        def navigate_up(self, event):
            if self.current_row > 0:
                self.current_row -= 1
                self.tree.see(self.current_row)
                self.tree.selection_set(self.current_row)
                self.tree.focus(self.current_row)

        def navigate_down(self, event):
            if self.current_row < len(self.dataframe) - 1:
                self.current_row += 1
                self.tree.see(self.current_row)
                self.tree.selection_set(self.current_row)
                self.tree.focus(self.current_row)

        def update_dataframe(self, new_dataframe):
            # Met à jour le DataFrame et recharge le Treeview
            self.dataframe = new_dataframe
            self.current_row = 0

            for i in self.tree.get_children():
                self.tree.delete(i)

            for index, row in self.dataframe.iterrows():
                self.tree.insert("", "end", values=list(row))

        def close(self):
            # Fermer la fenêtre et retirer l'instance de la liste des instances actives
            self.master.destroy()
            DataFrameViewer.instances.remove(self)
#################################################
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
            def __init__(self,texte,a,b,zt,mdRO,checkbox):
                self.texte=texte
                self.a=a
                self.b=b
                self.zt=zt
                self.mdRO=mdRO
                self.checkbox=checkbox
            def creerCheckbutton(self):  # on définit une fonction qui crée et place un bouton cochable et son entrée associée
                self.cbVar = BooleanVar(frameCheck)
                self.ztVar= StringVar(frameCheck,value="")
                self.mdVar= StringVar(frameCheck,value=">")
                self.dico={self.texte:[self.cbVar.get(),self.ztVar.get(),self.mdVar.get()]} #on crée un item propre à chaque bouton, qui a pour key le nom du filtre et en value une liste avec l'etat et l'attribut de tri

                def commandCB():
                    #nvletat = self.cbVar.get()
                    print(self.cbVar.get())
                    self.dico = {self.texte: [self.cbVar.get(), self.ztVar.get(), self.mdVar.get()]}
                    dicofiltres.update(self.dico)
                    #print(f"{self.texte} a changé d'état")
                    #print(self.dico)

                self.checkbox = Checkbutton(frameCheck, variable=self.cbVar, text=str(self.texte), command=commandCB)
                #self.checkbox = Checkbutton(frameCheck, variable=self.cbVar, text=str(self.texte), offvalue=0, onvalue=1, command=commandCB(self)) #on crée le bouton cochable
                self.checkbox.place(relx=self.a, rely=self.b)

                def entrymtd(self): #méthode qui met à jour le dico général dès qu'il y a une modif dans la zone de texte
                    nvlentree=self.zt.get()
                    self.dico={self.texte:[self.cbVar.get(),nvlentree,self.mdVar.get()]}
                    #print(f"{self.texte} a été mis à jour zdt")
                    dicofiltres.update(self.dico)
                self.zt=Entry(frameCheck, command=entrymtd(self)) #crée la zone de texte associée au bouton
                self.zt.place(relx=a+0.24,rely=b,relheight=0.08,relwidth=0.1)

                listeRelOrdre=["<",">","="]
                self.mdRO = ttk.Combobox(frameCheck, values=listeRelOrdre) #création du menu déroulant des relaitions d'ordre
                def actionmdRO(event):
                    mdVar = self.mdRO.get()
                    self.dico={self.texte:[self.cbVar,self.ztVar,mdVar]}
                    dicofiltres.update(self.dico)
                self.mdRO.bind("<<ComboboxSelected>>", actionmdRO)
                self.mdRO.place(relx=a+0.35,rely=b,relheight=0.07,relwidth=0.1)

    for i in range (0,len(listeAttribut)) : #boucle qui crée autant de boutons cochables qu'il y a de colonnes dans le dataframe
        texte=str(listeAttribut[i])
        zt=Entry(frameCheck)
        mdRO=ttk.Combobox(frameCheck)
        checkbox=Checkbutton(frameCheck)

        if i*0.1 < 1 :
            a=0.05
            b=i*0.1
        else :
            a=0.51
            b=i*0.1 % 1
        nvbouton=checkbutton(texte,a,b,zt,mdRO,checkbox)
        nvbouton.creerCheckbutton()

    #Création du bouton d'affichage du résultat

    def clique_bouton():
        sdf = pokemon.copy()
        listeobjets = dicofiltres.items()
        for i in listeobjets:
            listeauxi = list(i)
            texte = listeauxi[0]
            stockinfo = listeauxi[1]
            #print(str(stockinfo[0]))
            if stockinfo[0] == True:
                #print(texte)
                if stockinfo[2] == "<":
                    sdf = filtreinf.filtre(sdf, texte, stockinfo[1])
                    #print("tri inf effectué")
                    print(sdf)
                if stockinfo[2] == ">":
                    print(sdf)
                    print(texte)
                    print(stockinfo[1])
                    sdf = filtresup.filtre(sdf, texte, stockinfo[1])
                    print(sdf)
                if stockinfo[2] == "=":
                    sdf = filtrec.filtre(sdf, texte, stockinfo[1])
                    print(sdf)
        CC=str(choixClassement.get())
        Sens=cStringVar.get()
        if str(Sens)=="C":
            sdf=cc.classement(sdf,CC)
        if str(Sens)=="D":
            sdf=cd.classement(sdf,CC)
        #print("It lives !")
        data_frame_viewer.update_dataframe(sdf)
    boutonResultat = Button(root, text="Afficher DataFrame", command=clique_bouton)
    boutonResultat.place(relx=0.8, rely=0.4)
    data_frame_viewer = DataFrameViewer(frameViewer, pokemon)




#Affichage du DataFrame#


affichage()


mainloop()






print(filtrec.filtre(pokemon,"Speed",180))

#def favori(cible):
    #créer sous dataframe


