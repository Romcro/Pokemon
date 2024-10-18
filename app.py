import tkinter as tk
import threading
from PIL import ImageTk
from image_loader import get_pokemon_image
from tournament import tournoi

# Mise à jour de l'arène (texte)
def update_arena(text):
    arena_text.after(0, lambda: _update_arena_in_main_thread(text))

def _update_arena_in_main_thread(text):
    if arena_text.winfo_exists():
        arena_text.config(state=tk.NORMAL)
        arena_text.insert(tk.END, text + "\n")
        arena_text.config(state=tk.DISABLED)
        arena_text.see(tk.END)

# Afficher les Pokémon en combat
def update_fight_images(pokemon1, pokemon2, img_label1, img_label2, name_label1, name_label2):
    img1 = ImageTk.PhotoImage(get_pokemon_image(pokemon1["id"]).resize((300, 300)))
    img2 = ImageTk.PhotoImage(get_pokemon_image(pokemon2["id"]).resize((300, 300)))
    
    img_label1.config(image=img1)
    img_label1.image = img1
    img_label2.config(image=img2)
    img_label2.image = img2

    name_label1.config(text=pokemon1["name"].capitalize())
    name_label2.config(text=pokemon2["name"].capitalize())

# Afficher le gagnant final
def show_winner(winner):
    winner_fenetre = tk.Tk()
    winner_fenetre.geometry('1200x900')
    winner_fenetre.configure(bg='white')

    winner_name = winner["name"].capitalize()
    winner_label = tk.Label(winner_fenetre, text=f"Le grand gagnant est {winner_name} !", font=("Arial", 24), bg="white")
    winner_label.pack(pady=20)

    winner_img = ImageTk.PhotoImage(get_pokemon_image(winner['id']).resize((400, 400)))
    winner_image_label = tk.Label(winner_fenetre, image=winner_img, bg='white')
    winner_image_label.pack(pady=20)

    winner_fenetre.mainloop()

# Lancer l'arène et gérer les combats
def launch_arena(fenetre, pokemons, participants):
    fenetre.destroy()
    arena_fenetre = tk.Tk()
    arena_fenetre.geometry('1200x900')

    global arena_text
    arena_text = tk.Text(arena_fenetre, height=10, width=80, bg='red', fg='black', wrap=tk.WORD)
    arena_text.place(x=350, y=600)

    img_label1 = tk.Label(arena_fenetre, bg='white')
    img_label2 = tk.Label(arena_fenetre, bg='white')
    img_label1.place(x=100, y=300)
    img_label2.place(x=900, y=300)

    name_label1 = tk.Label(arena_fenetre, font=("Arial", 24), bg="white", fg='black')
    name_label2 = tk.Label(arena_fenetre, font=("Arial", 24), bg="white", fg='black')
    name_label1.place(x=100, y=250)
    name_label2.place(x=900, y=250)

    # Lancer le tournoi
    def start_tournament():
        winner_index = tournoi(participants, pokemons, update_arena, lambda p1, p2: update_fight_images(p1, p2, img_label1, img_label2, name_label1, name_label2))
        show_winner(pokemons[f'pokemon_{winner_index}'])

    threading.Thread(target=start_tournament).start()

# Interface principale
fenetre = tk.Tk()
fenetre.geometry('1200x900')
fenetre.configure(bg='yellow')

# Bouton de lancement du tournoi
pokemons = { # Exemple d'une liste simplifiée de Pokémon, tu dois charger les vrais Pokémon ici
    'pokemon_0': {'id': 1, 'name': 'Bulbasaur', 'stats': [{'base_stat': 45}, {'base_stat': 49}, {'base_stat': 49}, {}, {}, {'base_stat': 45}]},
    'pokemon_1': {'id': 4, 'name': 'Charmander', 'stats': [{'base_stat': 39}, {'base_stat': 52}, {'base_stat': 43}, {}, {}, {'base_stat': 65}]}
}
participants = [0, 1]  # Exemple de participants

tk.Button(fenetre, text="Lancer le Tournoi", command=lambda: launch_arena(fenetre, pokemons, participants)).pack(pady=10)

fenetre.mainloop()
