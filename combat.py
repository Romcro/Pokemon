import random
import time

def combat(f1, f2, arena_callback=None):
    fighter1 = {
        'name': f1["name"],
        'hp': f1["stats"][0]["base_stat"],  # HP
        'attack': f1["stats"][1]["base_stat"],  # Attaque
        'defense': f1["stats"][2]["base_stat"],  # Défense
        'speed': f1["stats"][5]["base_stat"]  # Vitesse
    }
    
    fighter2 = {
        'name': f2["name"],
        'hp': f2["stats"][0]["base_stat"],
        'attack': f2["stats"][1]["base_stat"],
        'defense': f2["stats"][2]["base_stat"],
        'speed': f2["stats"][5]["base_stat"]
    }

    # Déterminer qui attaque en premier
    if fighter1['speed'] > fighter2['speed']:
        attaquant, defenseur = fighter1, fighter2
    else:
        attaquant, defenseur = fighter2, fighter1

    if arena_callback:
        arena_callback(f"Le combat commence ! {attaquant['name']} attaque en premier !")

    # Combat loop
    while defenseur['hp'] > 0:
        damage = attaquant['attack'] - defenseur['defense']
        damage = max(1, damage)  # Le minimum de dégâts est 1
        defenseur['hp'] -= damage

        if arena_callback:
            arena_callback(f"{attaquant['name']} attaque {defenseur['name']} et inflige {damage} dégâts.")
            arena_callback(f"{defenseur['name']} a maintenant {defenseur['hp']} HP.")

        if defenseur['hp'] <= 0:
            if arena_callback:
                arena_callback(f"{defenseur['name']} est vaincu ! {attaquant['name']} gagne le combat.")
            return attaquant

        # Inverser les rôles pour le prochain tour
        attaquant, defenseur = defenseur, attaquant

        # Pause pour visualisation du combat
        time.sleep(1)
