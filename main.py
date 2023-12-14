import pandas as pd
from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import random
pokemon = pd.read_csv("pokemon.csv")
donnees_pokemon = pd.read_csv('pokemon.csv', index_col='Name')

##########méthodes de tri##########
class filtre(pd.DataFrame,ABC) : #méthode de filtre générale

    @abstractmethod
    def filtre(self, attribut, valeur):
        pass

class filtrec(filtre): #méthode pour chercher les pokémons avec un attribut = valeur
    def filtre(self, attribut, valeur):
        try:
            # Si la colonne est de type numérique, convertir la valeur en float
            if pd.api.types.is_numeric_dtype(self[attribut]):
                valeur = float(valeur)
            else:
                valeur = str(valeur)

            # Filtrer le dataframe
            sous_dataframe = self[self[attribut] == valeur]

            return sous_dataframe

        except ValueError:
            print(f"Erreur : La valeur '{valeur}' n'est pas compatible avec le type de la colonne '{attribut}'.")
        #if pd.api.types.is_numeric_dtype(self[attribut]) and pd.api.types.is_numeric_dtype(valeur):
            # Les deux sont des types numériques, effectuer la comparaison numérique
            #return self[self[attribut] == valeur]
        #else:
            # L'un des deux (ou les deux) n'est pas numérique, effectuer une comparaison de chaînes
            #return self[self[attribut].astype(str) == str(valeur)]

class filtreinf(filtre): #méthode pour chercher les pokémons avec un attribut < valeur
    def filtre(self,attribut,valeur):
        try:
            # Si la colonne est de type numérique, convertir la valeur en float
            if pd.api.types.is_numeric_dtype(self[attribut]):
                valeur = float(valeur)
            else:
                valeur = str(valeur)

            # Filtrer le dataframe
            sous_dataframe = self[self[attribut] < valeur]

            return sous_dataframe

        except ValueError:
            print(f"Erreur : La valeur '{valeur}' n'est pas compatible avec le type de la colonne '{attribut}'.")

        #if pd.api.types.is_numeric_dtype(self[attribut]) and pd.api.types.is_numeric_dtype(valeur):
            # Les deux sont des types numériques, effectuer la comparaison numérique
            #return self[self[attribut] < valeur]
        #else:
            # L'un des deux (ou les deux) n'est pas numérique, effectuer une comparaison de chaînes
            #return self[self[attribut].astype(str) < str(valeur)]


#méthode pour chercher les pokémons avec un attribut > valeur
class filtresup(filtre):
    def filtre(self,attribut,valeur):
        try:
            # Si la colonne est de type numérique, convertir la valeur en float
            if pd.api.types.is_numeric_dtype(self[attribut]):
                valeur = float(valeur)
            else:
                valeur = str(valeur)

            # Filtrer le dataframe
            sous_dataframe = self[self[attribut] > valeur]

            return sous_dataframe

        except ValueError:
            print(f"Erreur : La valeur '{valeur}' n'est pas compatible avec le type de la colonne '{attribut}'.")
        #if pd.api.types.is_numeric_dtype(self[attribut]) and pd.api.types.is_numeric_dtype(valeur):
            # Les deux sont des types numériques, effectuer la comparaison numérique
            #return self[self[attribut] > valeur]
        #else:
            # L'un des deux (ou les deux) n'est pas numérique, effectuer une comparaison de chaînes
            #return self[self[attribut].astype(str) > str(valeur)]


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

def affichage(pokemon):
##################################################
    #création fenêtre
    root=Tk()
    root.title("Pokédex")
    root.geometry('1000x1000')

#################################################
    #création affichage df
    frameViewer=Frame(root,width=1,height=0.5)
    frameViewer.place(relx=0,rely=0.72)

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

        def update_dataframe(self, nv_dataframe):
            # Met à jour le DataFrame et recharge le Treeview
            self.dataframe = nv_dataframe
            self.current_row = 0

            for i in self.tree.get_children():
                self.tree.delete(i)

            for index, row in self.dataframe.iterrows():
                self.tree.insert("", "end", values=list(row))

        def close(self): #Méthode pour s'assurer qu'un seul DF est affiché à la fois
            self.master.destroy()
            DataFrameViewer.instances.remove(self)
#################################################
#######méthode pour lancer un combat#####
    def combat_pokemon(pokemon1, pokemon2):
        # Copy pour éviter de modifier la Df d'origine
        donnees_combat = donnees_pokemon.copy()
        console=""

        stats_pokemon1 = donnees_combat.loc[pokemon1, ['HP', 'Attack', 'Defense', 'Speed']]
        stats_pokemon2 = donnees_combat.loc[pokemon2, ['HP', 'Attack', 'Defense', 'Speed']]

        # Le pokémon le plus rapide commence à attaquer
        if stats_pokemon1['Speed'] > stats_pokemon2['Speed']:
            pokemon_rapide, pokemon_lent = pokemon1, pokemon2
        elif stats_pokemon1['Speed'] < stats_pokemon2['Speed']:
            pokemon_rapide, pokemon_lent = pokemon2, pokemon1
        else:
            # Si égalité on tire au hasard
            import random
            if random.choice([True, False]) is True:
                pokemon_rapide, pokemon_lent = pokemon1, pokemon2
            else:
                pokemon_rapide, pokemon_lent = pokemon2, pokemon1

        while True:
            # On récupère les stats des deux pokémons
            stats_pokemon_rapide = donnees_combat.loc[pokemon_rapide, ['HP', 'Attack', 'Defense', 'Speed']]
            stats_pokemon_lent = donnees_combat.loc[pokemon_lent, ['HP', 'Attack', 'Defense', 'Speed']]

            # Les dégâts sont réduits grâce au log10 appliqué sur la défense
            degats = max(1, int(stats_pokemon_rapide['Attack'] / math.log10(stats_pokemon_lent['Defense'] + 1)))

            # On enlève les dégâts au défenseur
            donnees_combat.at[pokemon_lent, 'HP'] = max(0, stats_pokemon_lent['HP'] - degats)

            # Affichez les résultats du tour
            console+=(f"\n{pokemon_rapide} attaque {pokemon_lent} et inflige {degats} points de dégâts.")
            console+=(f"\n{pokemon_lent} a maintenant {donnees_combat.at[pokemon_lent, 'HP']} points de vie.")

            # Condition de victoire
            if donnees_combat.at[pokemon_lent, 'HP'] == 0:
                console+=(f"\n{pokemon_lent} a été vaincu! {pokemon_rapide} remporte le combat.")
                return(console)

            # Échangez les rôles pour le prochain tour
            pokemon_rapide, pokemon_lent = pokemon_lent, pokemon_rapide

    #création frame radiobuttons :
    frameRadio=Frame(root,relief='raised',highlightbackground='red',borderwidth=2)
    frameRadio.place(relx=0,rely=0.1,relwidth=0.4,relheight=0.1)

    #Menu déroulant pour choisir critère de classement
    listeAttribut=list(pokemon.columns)
    choixClassement=ttk.Combobox(frameRadio,values=listeAttribut)
    def action(event): #méthode qui stocke le choix dans le menu déroulant
        select = choixClassement.get()

    choixClassement.pack()
    choixClassement.bind("<<ComboboxSelected>>", action)
    choixClassement.place(relx=0,rely=0.3,relwidth=0.3,relheight=0.3)
    choixClassementLabel=Label(frameRadio,text="Classer selon :")
    choixClassementLabel.place(relx=0,rely=0,relwidth=0.3)

    #radio buttons pour choisir si classement croissant ou décroissant
    labelSensclassement=Label(frameRadio, text="dans l'ordre:")
    labelSensclassement.place(relx=0.4,rely=0,relwidth=0.3)
    cStringVar=StringVar(root,'sensclassement')

    #Bouton pour choisir Classement croissant
    classementC=Radiobutton(frameRadio, variable=cStringVar, value="C" )
    classementC.place(relx=0.42,rely=0.35,relwidth=0.2,relheight=0.2)
    labelclassementC=Label(frameRadio,text='croissant')
    labelclassementC.place(relx=0.5,rely=0.35,relheight=0.3)

    #Bouton pour choisir Classement décroissant
    classementD=Radiobutton(frameRadio,variable=cStringVar,value="D")
    classementD.place(relx=0.42,rely=0.75,relheight=0.2,relwidth=0.2)
    labelclassementD=Label(frameRadio,text='décroissant')
    labelclassementD.place(relx=0.5,rely=0.7,relheight=0.3)

    #Labels au-dessus du frame des checkbuttons
    ColonnesLabel=Label(root,text="Cocher pour filtrer la colonne, puis entrer une valeur-filtre\n"
                                  " et choisir une relation d'ordre")
    ColonnesLabel.place(relx=0.6,rely=0.05)


    #Check button pour choisir le ou les critères de filtre
    frameCheck = Frame(root,relief='raised',highlightbackground='red',borderwidth=2)
    frameCheck.place(relx=0.58,rely=0.1,relheight=0.35,relwidth=0.4)

    dicofiltres={} #Dictionnaire qui permet plus bas de savoir comment appliquer quels filtres

    class checkbutton : #classe de boutons cochables
            _registre = []
            def __init__(self,texte,a,b,zt,mdRO,checkbox):
                self.texte=texte
                self.a=a
                self.b=b
                self.zt=zt
                self.mdRO=mdRO
                self.checkbox=checkbox
                self._registre.append(self)


            def creerCheckbutton(self):  # on définit une fonction qui crée et place un bouton cochable et son entrée associée
                #Définition des variables du checkbutton
                self.cbVar = BooleanVar(frameCheck)
                self.ztVar= StringVar(frameCheck,value="")
                self.mdVar= StringVar(frameCheck,value=">")
                self.dico={self.texte:[self.cbVar.get(),self.ztVar.get(),self.mdVar.get()]} #on crée un item propre à chaque bouton, qui a pour key le nom du filtre et en value une liste avec l'etat et l'attribut de tri

                #création du Checkbutton
                self.checkbox = Checkbutton(frameCheck, variable=self.cbVar, text=str(self.texte))
                self.checkbox.place(relx=self.a, rely=self.b)

                #Création de l'Entry
                self.zt=Entry(frameCheck, textvariable=self.ztVar) #crée la zone de texte associée au bouton
                self.zt.place(relx=a+0.24,rely=b,relheight=0.08,relwidth=0.12)

                #Création du menu déroulant
                listeRelOrdre=["<",">","="]
                self.mdRO = ttk.Combobox(frameCheck, values=listeRelOrdre)
                self.mdRO.place(relx=a+0.35,rely=b,relheight=0.08,relwidth=0.1)

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

    #Création d'une fonction d'affichage du DF
    def clique_bouton():
        sdf = pokemon.copy()
        for i in checkbutton._registre: #On itère sur l'ensemble des boutons cochables
            i.dico={i.texte:[i.cbVar.get(),i.ztVar.get(),i.mdRO.get()]}
            dicofiltres.update(i.dico) #Lorsqu'on appuie sur le bouton, le dictionnaire des filtres est mis à jour avec les nouvelles entrées
        listeobjets = dicofiltres.items()
        for i in listeobjets: #Pour chaque critère de filtre possible, on vérifie s'il faut modifier le DF
            listeauxi = list(i)
            texte = listeauxi[0]
            stockinfo = listeauxi[1]
            if stockinfo[0] : #Si le bouton est coché
                if stockinfo[1]: #Si la zone de texte contient quelque-chose
                    if pd.api.types.is_numeric_dtype(sdf[texte]) and stockinfo[2] in ("<", ">", "="): #On vérifie la nature de la colonne
                        try:
                            valeur = float(stockinfo[1])
                        except ValueError:
                            print(
                                f"Erreur : Tentative de filtrer une colonne numérique avec une valeur non numérique ({stockinfo[1]}).")
                            continue
                    elif pd.api.types.is_string_dtype(sdf[texte]) and stockinfo[2] in ("<", ">", "="):
                        valeur = stockinfo[1]
                    else:
                        print(
                            f"Erreur : Tentative de filtrer une colonne avec un filtre alphabétique ou numérique non approprié.")
                        continue
                    if stockinfo[2] == "<":
                        sdf = filtreinf.filtre(sdf, texte, valeur)

                    elif stockinfo[2] == ">":
                        sdf = filtresup.filtre(sdf, texte, valeur)

                    elif stockinfo[2] == "=":
                        sdf = filtrec.filtre(sdf, texte, valeur)


        CC=str(choixClassement.get()) #On récupère la requête de classement ici
        Sens=cStringVar.get()
        if str(Sens)=="C":
            sdf=cc.classement(sdf,CC)
        if str(Sens)=="D":
            sdf=cd.classement(sdf,CC)
        else :
            sdf=sdf
        data_frame_viewer.update_dataframe(sdf) #Après application de toutes les requêtes, on utilise la méthode qui met à jour le DF affiché

    #Création du bouton afficheur
    boutonResultat = Button(root, text="Afficher DataFrame", command=clique_bouton)
    boutonResultat.place(relx=0.8, rely=0.4,relwidth=0.15,relheight=0.04)
    data_frame_viewer = DataFrameViewer(frameViewer, pokemon)

#################################
    #Création d'une frame pour abriter le graph radar

    frameGraph=Frame(root,relief='raised',highlightbackground='red',borderwidth=2)
    frameGraph.place(relx=0,rely=0.22,relwidth=0.52,relheight=0.48)
    ##Création de la fonction d'affichage du graph radar
    # Charger les données Pokémon depuis un fichier CSV
    df = pd.read_csv('pokemon.csv', index_col='Name')

    # Les attributs que nous voulons inclure dans le graphique radar
    attributs = ['Total', 'HP', 'Attack', 'Defense', 'Speed']

    # Normalisation des attributs
    df_normalisé = df.copy()
    for attribut in attributs:
        df_normalisé[attribut] = df_normalisé[attribut] / df_normalisé[attribut].max()

    # Fonction pour créer le graph radar
    def create_radar_plot(pokemons):
        variables = len(attributs)
        angles = np.linspace(0, 2 * np.pi, variables, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for pokemon, couleur in pokemons:
            valeurs = df_normalisé.loc[pokemon, attributs].tolist()
            valeurs += valeurs[:1]
            ax.plot(angles, valeurs, color=couleur, linewidth=1, label=pokemon)
            ax.fill(angles, valeurs, color=couleur, alpha=0.25)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        ax.set_thetagrids(np.degrees(angles[:-1]), attributs)

        for pokemon, angle in zip(ax.get_xticklabels(), angles[:-1]):
            if angle in (0, np.pi):
                pokemon.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                pokemon.set_horizontalalignment('left')
            else:
                pokemon.set_horizontalalignment('right')

        ax.set_ylim(0, 1)
        ax.set_rlabel_position(180 / variables)

        plt.legend(loc='upper right', bbox_to_anchor=(2.1, 1))
        return fig

    # Fonction pour afficher le graphique dans Tkinter
    def display_plot_tkinter(fig):
        canvas = FigureCanvasTkAgg(fig, master=frameGraph)
        canvas_widget = canvas.get_tk_widget()
        #canvas_widget.column(row=5, column=5, columnspan=3)
        canvas_widget.place(relx=0,rely=0.4,relwidth=1,relheight=0.6)

    # Fonction appelée quand on  clique sur le bouton
    def on_button_click():
        # Récupérer les noms des Pokémon depuis la saisie
        pokemon1 = entry_pokemon1.get()
        pokemon2 = entry_pokemon2.get()
        pokemon3 = entry_pokemon3.get()

        # Liste de Pokémon avec leur couleur associée
        pokemons = [(pokemon1, '#1aaf6c'), (pokemon2, '#429bf4'), (pokemon3, '#d42cea')]

        # Créer et afficher le graphique radar
        radar_plot = create_radar_plot(pokemons)
        display_plot_tkinter(radar_plot)

    # Saisie pour chaque pokémon
    ttk.Label(frameGraph, text="Nom Pokémon 1:").place(relx=0, rely=0,relwidth=0.3)
    entry_pokemon1 = ttk.Entry(frameGraph)
    entry_pokemon1.place(relx=0.3,rely=0,relwidth=0.25)

    ttk.Label(frameGraph, text="Nom Pokémon 2:").place(relx=0,rely=0.15,relwidth=0.3)
    entry_pokemon2 = ttk.Entry(frameGraph)
    entry_pokemon2.place(relx=0.3,rely=0.15,relwidth=0.25)

    ttk.Label(frameGraph, text="Nom Pokémon 3:").place(relx=0,rely=0.30,relwidth=0.3)
    entry_pokemon3 = ttk.Entry(frameGraph)
    entry_pokemon3.place(relx=0.3,rely=0.30,relwidth=0.25)

    #  bouton pour générer le graphique radar
    button_generate = ttk.Button(frameGraph, text="Générer le Graphique Radar", command=on_button_click)
    button_generate.place(relx=0.6,rely=0.30,relwidth=0.35)

    #Création du bouton d'affichage du graph radar


    #######################
    #Création du frame pour les combats pokémons
    frameBagarre=Frame(root,relief='raised',highlightbackground='red',borderwidth=2)
    frameBagarre.place(relx=0.68,rely=0.47,relheight=0.2,relwidth=0.3)
    LabelBagarre=Label(frameBagarre,text='Choisir les deux pokémons\n'
                                         'à faire combattre')
    LabelBagarre.grid(row=0,column=0,sticky='w',columnspan=3)

    #Création des entrées pour chaque pokémon :

    ztPokemon1=Entry(frameBagarre)
    ztPokemon1.place(relx=0,rely=0.4,relwidth=0.5)
    LabelPokemon1=Label(frameBagarre,text='Entrer Pokémon 1 :')
    LabelPokemon1.place(relx=0,rely=0.25)

    ztPokemon2=Entry(frameBagarre)
    ztPokemon2.place(relx=0,rely=0.75,relwidth=0.5)
    LabelPokemon2=Label(frameBagarre,text='Entrer Pokémon 2 :')
    LabelPokemon2.place(relx=0,rely=0.60)

    #Création du bouton pour afficher le résultat
    varResultat=StringVar()
    labelResultat=Label(frameBagarre,textvariable=varResultat,font=('Times New Roman',6,'bold'))
    labelResultat.place(relx=0.5,rely=0,relheight=0.75,relwidth=0.5)
    def commandBagarre():
        pokemon1=ztPokemon1.get()
        pokemon2=ztPokemon2.get()
        varResultat.set(combat_pokemon(pokemon1,pokemon2))

    boutonBagarre=Button(frameBagarre,text="Lancer combat",command=commandBagarre)
    boutonBagarre.place(relx=0.6,rely=0.8,relwidth=0.4,relheight=0.2)

############################
    #bouton pour fermer la fenêtre
    def fermer_fenetre():
        root.destroy()
    fermeture=Button(root,command=fermer_fenetre,text="X",bg='red')
    fermeture.place(relx=0,rely=0)




affichage(pokemon)
mainloop()






