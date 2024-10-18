import tkinter as tk
from tournoi import tournoi
import requests
import pygame
import threading
from PIL import Image, ImageTk
import random
import io

# Initialiser pygame pour gérer le son
pygame.mixer.init()

# Fonction pour jouer de la musique
def play_music():
    try:
        pygame.mixer.music.load('son/son.mp3')
        pygame.mixer.music.play(-1)  # Jouer en boucle
    except pygame.error as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")

def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def resume_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

# Télécharger l'image du Pokémon shiny, sinon prendre la version normale et traiter le fond
def get_pokemon_image(pokemon_num):
    shiny_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/shiny/{pokemon_num}.png'
    normal_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/{pokemon_num}.png'

    response = requests.get(shiny_url)
    if response.status_code != 200:
        response = requests.get(normal_url)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")

        # Rendre le fond blanc transparent
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[:3] == (255, 255, 255):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        return img
    else:
        print(f"Erreur lors du téléchargement de l'image pour le Pokémon {pokemon_num}")
        return None

# Charger les Pokémon depuis l'API PokéAPI
def load_pokemons(n):
    pokemons = {}
    plage_1 = list(range(1, 899))  # Restreindre à des IDs connus valides (générations 1 à 8)
    numeros_random = random.sample(plage_1, n)

    for index in range(n):
        if not numeros_random:
            print("Plus de numéros disponibles pour choisir un autre Pokémon.")
            break

        num = numeros_random.pop(0)
        url = f'https://pokeapi.co/api/v2/pokemon/{num}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            pokemons[f'pokemon_{index}'] = response.json()

            if get_pokemon_image(num) is None:
                print(f"Échec de l'image pour le Pokémon {num}, affichage de l'image par défaut.")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du Pokémon {num} : {e}")
    return pokemons, list(range(len(pokemons)))

# Mise à jour de l'arène (affichage des combats dans Tkinter)
def update_arena(text):
    arena_text.after(0, lambda: _update_arena_in_main_thread(text))

def _update_arena_in_main_thread(text):
    arena_text.config(state=tk.NORMAL)
    arena_text.insert(tk.END, text + "\n")
    arena_text.config(state=tk.DISABLED)
    arena_text.see(tk.END)  # Faire défiler vers le bas

# Afficher les 16 participants avant le tournoi pendant 8 secondes
def show_participants(arena_fenetre, pokemons, participants, img_labels, name_labels, callback):
    for i, participant in enumerate(participants):
        pokemon = pokemons.get(f'pokemon_{participant}')
        if pokemon:
            pokemon_img = get_pokemon_image(pokemon['id'])
            name = pokemon['name'].capitalize()

            if pokemon_img:
                img = pokemon_img.resize((100, 100), Image.Resampling.LANCZOS)
                img_photo = ImageTk.PhotoImage(img)
                img_labels[i].config(image=img_photo)
                img_labels[i].image = img_photo
            else:
                default_img = Image.open('image/no_image.png').resize((100, 100), Image.Resampling.LANCZOS)
                img_photo = ImageTk.PhotoImage(default_img)
                img_labels[i].config(image=img_photo)
                img_labels[i].image = img_photo

            name_labels[i].config(text=name)

    arena_fenetre.after(8000, callback)

# Afficher les Pokémon en combat avec leurs noms
def update_fight_images(pokemon1, pokemon2, img_label1, img_label2, name_label1, name_label2):
    img1 = get_pokemon_image(pokemon1["id"])
    img2 = get_pokemon_image(pokemon2["id"])

    name1 = pokemon1["name"].capitalize()
    name2 = pokemon2["name"].capitalize()

    if img1:
        img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
        img_photo1 = ImageTk.PhotoImage(img1)
        img_label1.config(image=img_photo1)
        img_label1.image = img_photo1
    else:
        img_label1.config(image="")

    if img2:
        img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
        img_photo2 = ImageTk.PhotoImage(img2)
        img_label2.config(image=img_photo2)
        img_label2.image = img_photo2
    else:
        img_label2.config(image="")

    name_label1.config(text=name1)
    name_label2.config(text=name2)

# Afficher le gagnant en grand
def show_winner(fenetre, winner_pokemon):
    fenetre.destroy()
    winner_fenetre = tk.Tk()
    winner_fenetre.geometry('1200x900')
    winner_fenetre.configure(bg='white')

    winner_name = winner_pokemon["name"].capitalize()

    winner_label = tk.Label(winner_fenetre, text=f"Le grand gagnant est {winner_name} !", font=("Arial", 24), bg="white")
    winner_label.pack(pady=20)

    winner_img = get_pokemon_image(winner_pokemon["id"])
    if winner_img:
        winner_img = winner_img.resize((400, 400), Image.Resampling.LANCZOS)
        winner_photo = ImageTk.PhotoImage(winner_img)
        winner_image_label = tk.Label(winner_fenetre, image=winner_photo, bg='white')
        winner_image_label.pack(pady=20)
        winner_image_label.image = winner_photo

    winner_fenetre.mainloop()

# Lancer l'arène
def launch_arena(fenetre, pokemons, participants):
    fenetre.destroy()

    arena_fenetre = tk.Tk()
    arena_fenetre.geometry('1200x900')

    # Ajouter une image de fond pour l'arène
    bg_image = Image.open('image/vs.png')
    bg_image = bg_image.resize((1200, 900), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(arena_fenetre, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    global arena_text
    arena_text = tk.Text(arena_fenetre, height=10, width=80, bg='white', fg='black', wrap=tk.WORD)
    
    # Masquer la zone de texte au début, elle n'apparaitra que lorsque les combats commencent
    arena_text.place_forget()

    img_labels = []
    name_labels = []
    for i in range(16):
        img_label = tk.Label(arena_fenetre, bg='white')
        img_label.place(x=50 + (i % 8) * 150, y=100 + (i // 8) * 150)
        img_labels.append(img_label)

        name_label = tk.Label(arena_fenetre, text="", bg='white')
        name_label.place(x=50 + (i % 8) * 150, y=200 + (i // 8) * 150)
        name_labels.append(name_label)

    def start_tournament():
        for label in img_labels + name_labels:
            label.place_forget()

        # Afficher la zone de texte après la présentation des participants
        arena_text.place(x=350, y=600)

        img_label1 = tk.Label(arena_fenetre, bg='white')
        img_label1.place(x=100, y=300)

        img_label2 = tk.Label(arena_fenetre, bg='white')
        img_label2.place(x=900, y=300)

        name_label1 = tk.Label(arena_fenetre, text="", font=("Arial", 14), bg="white")
        name_label1.place(x=100, y=250)

        name_label2 = tk.Label(arena_fenetre, text="", font=("Arial", 14), bg="white")
        name_label2.place(x=900, y=250)

        def tournoi_callback(pokemon1, pokemon2):
            update_fight_images(pokemon1, pokemon2, img_label1, img_label2, name_label1, name_label2)

        def end_callback(winner_pokemon):
            show_winner(arena_fenetre, winner_pokemon)

        threading.Thread(target=tournoi, args=(participants, pokemons, update_arena, tournoi_callback, end_callback)).start()

    show_participants(arena_fenetre, pokemons, participants, img_labels, name_labels, start_tournament)

    arena_fenetre.mainloop()

# Interface principale
fenetre = tk.Tk()
fenetre.geometry('1200x900')
fenetre.title("Jeu Pokemon")
fenetre.configure(bg='yellow')

logo_img = Image.open('image/logo.png')
logo_img = logo_img.resize((400, 200), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(fenetre, image=logo_photo, bg='yellow')
logo_label.pack(pady=20)

poke_img = Image.open('image/poke.png')
poke_img = poke_img.resize((400, 200), Image.Resampling.LANCZOS)
poke_photo = ImageTk.PhotoImage(poke_img)
poke_label = tk.Label(fenetre, image=poke_photo, bg='yellow')
poke_label.pack(side="bottom", pady=20)

pokemons, participants = load_pokemons(16)

if len(participants) == 0:
    print("Erreur : la liste des participants est vide !")
else:
    print(f"{len(participants)} participants chargés.")

btn_start_tournoi = tk.Button(fenetre, text="Lancer le Tournoi", command=lambda: launch_arena(fenetre, pokemons, participants))
btn_start_tournoi.pack(pady=10)

btn_play_music = tk.Button(fenetre, text="Jouer Musique", command=play_music)
btn_play_music.pack(pady=5)

btn_pause_music = tk.Button(fenetre, text="Pause Musique", command=pause_music)
btn_pause_music.pack(pady=5)

btn_resume_music = tk.Button(fenetre, text="Reprendre Musique", command=resume_music)
btn_resume_music.pack(pady=5)

btn_stop_music = tk.Button(fenetre, text="Arrêter Musique", command=stop_music)
btn_stop_music.pack(pady=5)

fenetre.mainloop()
