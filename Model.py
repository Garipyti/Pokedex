import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd

# Charger les données Pokémon depuis un fichier CSV
df = pd.read_csv('pokemon.csv', index_col='Name')

# Les attributs que nous voulons inclure dans le graphique radar
attributs = ['Total', 'HP', 'Attack', 'Defense', 'Speed']

# Normalisation des attributs
df_normalisé = df.copy()
for attribut in attributs:
    df_normalisé[attribut] = df_normalisé[attribut] / df_normalisé[attribut].max()

# Fonction pour créer le graph radar
# détails à commenter
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

    plt.legend(loc='upper right')
    return fig

# Fonction pour afficher le graphique dans Tkinter
def display_plot_tkinter(fig):
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=5, columnspan=3)

# Fonction appelée quan il y le  clic sur le bouton
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

root = tk.Tk()

# Saisi pour chaque pokémon
ttk.Label(root, text="Nom Pokémon 1:").grid(row=1, column=0, pady=10)
entry_pokemon1 = ttk.Entry(root)
entry_pokemon1.grid(row=1, column=1, pady=10)

ttk.Label(root, text="Nom Pokémon 2:").grid(row=2, column=0, pady=10)
entry_pokemon2 = ttk.Entry(root)
entry_pokemon2.grid(row=2, column=1, pady=10)

ttk.Label(root, text="Nom Pokémon 3:").grid(row=3, column=0, pady=10)
entry_pokemon3 = ttk.Entry(root)
entry_pokemon3.grid(row=3, column=1, pady=10)

#  bouton pour générer le graphique radar
button_generate = ttk.Button(root, text="Générer le Graphique Radar", command=on_button_click)
button_generate.grid(row=4, column=16, pady=10)

root.mainloop()


import tkinter as tk
from tkinter import ttk
import pandas as pd

# Fonction appelée lorsque le bouton est coché ou décoché
def on_checkbox_click():
    value = checkbox_var.get()  # Obtenir la valeur du bouton (1 si coché, 0 sinon)
    print("La valeur du bouton est :", value)

# Créer une fenêtre principale
app = tk.Tk()
app.title("Bouton Cochable")

# Créer une variable Tkinter pour stocker l'état du bouton
checkbox_var = tk.IntVar()

# Créer un bouton cochable
checkbox = ttk.Checkbutton(app, text="Cocher pour 1, Décocher pour 0", variable=checkbox_var, command=on_checkbox_click)
checkbox.grid(column=0, row=0, padx=10, pady=10)

# Lancer la boucle principale
app.mainloop()



