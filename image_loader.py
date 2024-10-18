import requests
from PIL import Image
import io

# Fonction pour télécharger et traiter les images des Pokémon
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
        newData = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in datas]
        img.putdata(newData)
        return img
    else:
        print(f"Erreur lors du téléchargement de l'image pour le Pokémon {pokemon_num}")
        return None
