import tkinter as tk
from PIL import Image, ImageTk
import pygame
import requests
import random
import threading
from io import BytesIO
from tournament import tournoi  # Assurez-vous que tournament.py est correctement importé

# Initialiser pygame pour la musique
pygame.mixer.init()

# Fonction pour jouer automatiquement la musique à l'ouverture
def play_music():
    try:
        pygame.mixer.music.load('son/son.mp3')
        pygame.mixer.music.play(-1)  # Lecture en boucle
    except pygame.error as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")

# Fonction pour arrêter la musique
def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

# Télécharger et traiter les images des Pokémon
def get_pokemon_image(pokemon_num):
    shiny_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/shiny/{pokemon_num}.png'
    normal_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/{pokemon_num}.png'

    response = requests.get(shiny_url)
    if response.status_code != 200:
        response = requests.get(normal_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        datas = img.getdata()
        newData = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in datas]
        img.putdata(newData)
        return img
    else:
        print(f"Erreur lors du téléchargement de l'image pour le Pokémon {pokemon_num}")
        return None

# Charger les Pokémon depuis l'API
def load_pokemons(n):
    pokemons = {}
    numeros_random = random.sample(range(1, 899), n)  # Génère des ID aléatoires de Pokémon

    for index in range(n):
        num = numeros_random.pop(0)
        url = f'https://pokeapi.co/api/v2/pokemon/{num}'
        response = requests.get(url)
        if response.status_code == 200:
            pokemons[f'pokemon_{index}'] = response.json()
        else:
            print(f"Erreur lors de la récupération du Pokémon {num}")

    return pokemons, list(range(n))

# Mise à jour de l'arène (texte des combats)
def update_arena(text):
    arena_text.config(state=tk.NORMAL)
    arena_text.insert(tk.END, text + "\n")
    arena_text.config(state=tk.DISABLED)
    arena_text.see(tk.END)

# Afficher les 16 participants avant le tournoi pendant 8 secondes avec un fond `bgpoke.png`
def show_participants(arena_fenetre, pokemons, participants, canvas, callback):
    # Charger et placer le fond bgpoke.png
    bg_image = Image.open('image/bgpoke.png')
    bg_image = bg_image.resize((1200, 900), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo  # Garder une référence pour éviter la suppression

    # Placer les images des Pokémon et leurs noms sur le Canvas
    for i, participant in enumerate(participants):
        pokemon = pokemons.get(f'pokemon_{participant}')
        pokemon_img = get_pokemon_image(pokemon['id'])
        name = pokemon['name'].capitalize()

        if pokemon_img:
            img_photo = ImageTk.PhotoImage(pokemon_img.resize((150, 150), Image.Resampling.LANCZOS))
            canvas.create_image(50 + (i % 4) * 300, 100 + (i // 4) * 300, image=img_photo, anchor="nw")
            # Conserver les images en mémoire pour éviter qu'elles disparaissent
            canvas.img_photos = canvas.img_photos if hasattr(canvas, 'img_photos') else []
            canvas.img_photos.append(img_photo)

        canvas.create_text(50 + (i % 4) * 300, 250 + (i // 4) * 300, text=name, font=("Arial", 16), fill="black")

    # Masquer les 16 Pokémon et passer à la phase de tournoi après 8 secondes
    arena_fenetre.after(8000, lambda: (canvas.delete("all"), callback()))

# Afficher les Pokémon en combat avec leurs noms
def update_fight_images(pokemon1, pokemon2, img_label1, img_label2, name_label1, name_label2):
    img1 = get_pokemon_image(pokemon1["id"]).resize((300, 300), Image.Resampling.LANCZOS)
    img2 = get_pokemon_image(pokemon2["id"]).resize((300, 300), Image.Resampling.LANCZOS)

    img_photo1 = ImageTk.PhotoImage(img1)
    img_photo2 = ImageTk.PhotoImage(img2)

    img_label1.config(image=img_photo1)
    img_label1.image = img_photo1  # Assurer que l'image soit conservée en mémoire
    img_label2.config(image=img_photo2)
    img_label2.image = img_photo2

    name_label1.config(text=pokemon1["name"].capitalize(), font=("Arial", 24), fg='black')
    name_label2.config(text=pokemon2["name"].capitalize(), font=("Arial", 24), fg='black')

# Afficher le gagnant en grand
def show_winner(fenetre, winner_pokemon):
    fenetre.destroy()
    winner_fenetre = tk.Tk()
    winner_fenetre.geometry('1200x900')
    winner_fenetre.title("Gagnant du Tournoi")
    winner_fenetre.configure(bg='white')

    winner_name = winner_pokemon["name"].capitalize()
    tk.Label(winner_fenetre, text=f"Le grand gagnant est {winner_name} !", font=("Arial", 24), bg="white").pack(pady=20)

    winner_img = get_pokemon_image(winner_pokemon["id"]).resize((400, 400), Image.Resampling.LANCZOS)
    winner_photo = ImageTk.PhotoImage(winner_img)
    tk.Label(winner_fenetre, image=winner_photo, bg='white').pack(pady=20)

    winner_fenetre.mainloop()

# Lancer l'arène avec un Canvas pour afficher les éléments au-dessus de l'image de fond
def launch_arena(fenetre, pokemons, participants):
    fenetre.destroy()
    arena_fenetre = tk.Tk()
    arena_fenetre.geometry('1200x900')
    arena_fenetre.title("Tournoi_Pokemon")

    # Utiliser un Canvas pour gérer les éléments sur différents calques
    canvas = tk.Canvas(arena_fenetre, width=1200, height=900)
    canvas.pack(fill="both", expand=True)

    # Charger et placer l'image de fond "vs.png" une fois les combats lancés
    bg_image = Image.open('image/vs.png')
    bg_image = bg_image.resize((1200, 900), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Masquer vs.png et la zone de texte pendant la présentation des 16 Pokémon
    def start_tournament():
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")  # Placer l'image de fond des combats
        arena_text.place(x=350, y=600)  # Montrer la zone de texte des combats

        threading.Thread(target=tournoi, args=(participants, pokemons, update_arena, update_fight_images, img_label1, img_label2, name_label1, name_label2, lambda winner: show_winner(arena_fenetre, winner))).start()

    global arena_text
    arena_text = tk.Text(canvas, height=10, width=80, bg='white', fg='black', wrap=tk.WORD, font=("Arial", 14))
    arena_text.place_forget()  # Masquer au départ

    # Labels pour afficher les images et noms des Pokémon pendant les combats
    img_label1 = tk.Label(canvas, bg='white')
    img_label2 = tk.Label(canvas, bg='white')
    img_label1.place(x=100, y=300)
    img_label2.place(x=900, y=300)

    name_label1 = tk.Label(canvas, font=("Arial", 24), bg="white", fg='black')
    name_label2 = tk.Label(canvas, font=("Arial", 24), bg="white", fg='black')
    name_label1.place(x=100, y=250)
    name_label2.place(x=900, y=250)

    show_participants(arena_fenetre, pokemons, participants, canvas, start_tournament)
    arena_fenetre.mainloop()

# Interface principale
fenetre = tk.Tk()
fenetre.geometry('1300x900')
fenetre.title("Tournoi_Pokemon")
fenetre.configure(bg='yellow')

# Lancer automatiquement la musique
play_music()

# Ajouter logo et image d'accueil
logo_img = Image.open('image/logo.png').resize((400, 200), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
tk.Label(fenetre, image=logo_photo, bg='yellow').pack(pady=20)

poke_img = Image.open('image/poke.png').resize((400, 200), Image.Resampling.LANCZOS)
poke_photo = ImageTk.PhotoImage(poke_img)
tk.Label(fenetre, image=poke_photo, bg='yellow').pack(side="bottom", pady=20)

# Charger les Pokémon
pokemons, participants = load_pokemons(16)

# Bouton de lancement du tournoi
tk.Button(fenetre, text="Lancer le Tournoi", command=lambda: launch_arena(fenetre, pokemons, participants)).pack(pady=10)

# Bouton pour arrêter la musique
tk.Button(fenetre, text="Arrêter la Musique", command=stop_music).pack(pady=5)

fenetre.mainloop()
