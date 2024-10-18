import random
import time

# Fonction de combat Pokémon
def combat(pokemon1, pokemon2, update_arena):
    fighter1 = {
        'name': pokemon1["name"],
        'hp': pokemon1["stats"][0]["base_stat"],
        'attack': pokemon1["stats"][1]["base_stat"],
        'defense': pokemon1["stats"][2]["base_stat"],
        'speed': pokemon1["stats"][5]["base_stat"]
    }

    fighter2 = {
        'name': pokemon2["name"],
        'hp': pokemon2["stats"][0]["base_stat"],
        'attack': pokemon2["stats"][1]["base_stat"],
        'defense': pokemon2["stats"][2]["base_stat"],
        'speed': pokemon2["stats"][5]["base_stat"]
    }

    # Déterminer qui attaque en premier
    if fighter1['speed'] > fighter2['speed']:
        attaquant, defenseur = fighter1, fighter2
    else:
        attaquant, defenseur = fighter2, fighter1

    update_arena(f"{attaquant['name']} attaque en premier !")

    while defenseur['hp'] > 0:
        damage = max(1, attaquant['attack'] - defenseur['defense'])
        defenseur['hp'] -= damage
        update_arena(f"{attaquant['name']} inflige {damage} dégâts à {defenseur['name']}")

        if defenseur['hp'] <= 0:
            update_arena(f"{defenseur['name']} est vaincu ! {attaquant['name']} gagne le combat !")
            return attaquant

        # Inverser les rôles
        attaquant, defenseur = defenseur, attaquant

        time.sleep(1)  # Pause pour simuler le déroulement du combat

