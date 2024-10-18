import tkinter as tk
from tkinter import filedialog, PhotoImage, messagebox, Scrollbar, Canvas
import threading
import requests
import random
import pygame
import subprocess
import os
from PIL import Image, ImageTk

# Initialiser le mixer de pygame pour la musique
pygame.mixer.init()

# Fonction principale qui gère toutes les interactions
def main_function(action):
    global fichier_audio

    if action == "play_music":
        fichier_audio = 'son.mp3'
        if fichier_audio:
            try:
                pygame.mixer.music.load(fichier_audio)
                pygame.mixer.music.play()
            except pygame.mixer.Error as e:
                print(f"Erreur lors de la lecture du fichier audio : {e}")

    elif action == "pause_music":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    elif action == "resume_music":
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()

    elif action == "stop_music":
        pygame.mixer.music.stop()

    elif action == "destroy_window":
        fenetre.destroy()
        nouvelle_fenetre = tk.Tk()
        nouvelle_fenetre.geometry('1200x800')


        # Ajouter une image de fond dans la nouvelle fenêtre avec PIL
        try:
            image_fond = Image.open('bgpoke.png').resize((1200, 800), Image.Resampling.LANCZOS)
            image_fond = ImageTk.PhotoImage(image_fond)
            label_image_fond = tk.Label(nouvelle_fenetre, image=image_fond)
            label_image_fond.place(relwidth=1, relheight=1)
            label_image_fond.image = image_fond  # Garder une référence à l'image
        except Exception as e:
            print(f"Erreur de chargement de l'image de fond : {e}")
            nouvelle_fenetre.configure(bg='yellow') 

        # Fonction pour lancer le tournoi via le fichier main.py et récupérer les résultats
        def lancer_tournoi():
            try:
                # Exécuter le script main.py et capturer la sortie
                result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
                output = result.stdout

                # Créer un cadre pour le contenu défilant
                frame_resultat = tk.Frame(nouvelle_fenetre)
                frame_resultat.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                # Créer un canevas pour pouvoir scroller le contenu
                canvas_resultat = tk.Canvas(frame_resultat)
                scrollbar = Scrollbar(frame_resultat, orient=tk.VERTICAL, command=canvas_resultat.yview)
                scrollable_frame = tk.Frame(canvas_resultat)

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas_resultat.configure(
                        scrollregion=canvas_resultat.bbox("all")
                    )
                )

                canvas_resultat.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas_resultat.configure(yscrollcommand=scrollbar.set)

                # Ajouter les résultats dans le cadre défilant
                label_resultat = tk.Label(scrollable_frame, text=output, font=("Arial", 14), fg='blue', bg='yellow', justify='left')
                label_resultat.pack(pady=10, padx=10)

                # Pack canvas and scrollbar
                canvas_resultat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'exécution du tournoi : {e}")

        # Bouton pour lancer le tournoi
        bouton_lancer = tk.Button(nouvelle_fenetre, text="Lancer le Tournoi", command=lancer_tournoi, font=("Arial", 16), bg='yellow', fg='blue')
        bouton_lancer.pack(pady=50)

        nouvelle_fenetre.mainloop()

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry('1200x800')
fenetre.configure(bg='yellow')

# Charger les images et créer l'interface
try:
    image_logo = PhotoImage(file='logo.png').subsample(3, 3)
    label_image_logo = tk.Label(fenetre, image=image_logo, bg='yellow')
    label_image_logo.pack(pady=20)
except Exception as e:
    print(f"Erreur de chargement de l'image 'logo.png' : {e}")

titre_1 = tk.Label(fenetre, text="Attrapez les Tous", font=("Arial", 30, "bold"), fg='blue', bg='yellow')
titre_1.pack(pady=20)

titre_2 = tk.Label(fenetre, text="Bienvenue dans l'arène", font=("Arial", 24, "bold"), fg='blue', bg='yellow')
titre_2.pack(pady=10)

# Créer les boutons de contrôle pour la musique et un bouton pour détruire la fenêtre
bouton_play = tk.Button(fenetre, text="Jouer Musique", command=lambda: main_function("play_music"))
bouton_play.pack(pady=5)

bouton_pause = tk.Button(fenetre, text="Pause", command=lambda: main_function("pause_music"))
bouton_pause.pack(pady=5)

bouton_resume = tk.Button(fenetre, text="Reprendre", command=lambda: main_function("resume_music"))
bouton_resume.pack(pady=5)

bouton_stop = tk.Button(fenetre, text="Arrêter", command=lambda: main_function("stop_music"))
bouton_stop.pack(pady=5)

# Bouton pour détruire la fenêtre principale et ouvrir une nouvelle avec un fond personnalisé
bouton_destroy = tk.Button(fenetre, text="Accéder à l'aréne", command=lambda: main_function("destroy_window"), font=("Arial", 16), bg='#000', fg='white')
bouton_destroy.pack(pady=50)

# Charger la deuxième image PNG
try:
    image_poke = PhotoImage(file='poke.png').subsample(4, 4)
    label_image_poke = tk.Label(fenetre, image=image_poke, bg='yellow')
    label_image_poke.pack(pady=20)
except Exception as e:
    print(f"Erreur de chargement de l'image 'poke.png' : {e}")

# Lancer la boucle principale
fenetre.mainloop()