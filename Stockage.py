import pandas as pd
pokemon = pd.read_csv("K:\Documents\pokemon.csv",index_col="Name")
pd.DataFrame.info(pokemon)
premiers =  pd.DataFrame.head(pokemon, n=10)
Type2 = pokemon["Type 2"]
pokemoncorrigé = pd.DataFrame.fillna(pokemon, "")
pokemonmodif = pd.DataFrame.drop(pokemon,columns=["#","Sp. Atk","Sp. Def"])
Bulbizarre = pokemon.loc["Bulbasaur",["Type 1","Type 2"]]
Cinqdeux = pd.DataFrame.tail(pokemon.iloc[:,[0,1]])
Legendairesplante = pokemon[(pokemon["Legendary"]==True) & (pokemon["Type 1"]=="Grass")]
quatrecolonnes=pokemon.iloc[:,0:6].describe()
TopPv=pokemon[pokemon["HP"]==255]
Top3vitesse=pd.DataFrame.tail((pd.DataFrame.sort_values(pokemon,"Speed")),n=3)
Pokemonslegendaires=pokemon[pokemon["Legendary"]==True]
print(Pokemonslegendaires)

