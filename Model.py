import pandas as pd
from abc import ABC, abstractmethod
pokemon = pd.read_csv("/Users/clementbarcaroli/PycharmProjects/Pokedex/pokemon.csv")


#Définition des méthodes de classement des Pokémons

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


#Définition des méthodes de tri des Pokémons
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






