import pandas as pd
from abc import ABC, abstractmethod
import tkinter as tk
pokemon = pd.read_csv("pokemon.csv") # il y aura peut-être besoin d'enlever les NaN plus tard

##########Model##########
class filtre(ABC) : #méthode de filtre générale

    @abstractmethod
    def filtre(self):
        pass

class filtrec(filtre): ##méthode pour chercher les pokémons avec un attribut = valeur
    def tri(self, attribut, valeur):
        return (self[self[attribut] == valeur])

class filtreinf(filtre): #méthode pour chercher les pokémons avec un attribut < valeur
    def filtre(self,attribut,valeur):
        return (self[self[attribut] < valeur])

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

#######Vue########
class vue(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.mainloop(self)













#def favori(cible):
    #créer sous dataframe


