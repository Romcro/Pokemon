import random
from combat import combat

def tournoi(participants, pokemons, arena_callback=None, fight_callback=None, end_callback=None):
    if not participants or len(participants) < 2:
        print("Erreur : La liste des participants est vide ou trop petite pour un tournoi.")
        return

    while len(participants) > 1:
        winners = []

        while len(participants) >= 2:
            fighter_1 = participants.pop(0)
            fighter_2 = participants.pop(0)

            pokemon1 = pokemons.get(f'pokemon_{fighter_1}')
            pokemon2 = pokemons.get(f'pokemon_{fighter_2}')
            if not pokemon1 or not pokemon2:
                print(f"Erreur : Pokémon non trouvé pour {fighter_1} ou {fighter_2}")
                continue

            name_f1 = pokemon1["name"].capitalize()
            name_f2 = pokemon2["name"].capitalize()

            if fight_callback:
                fight_callback(pokemon1, pokemon2)

            print(f"Combat entre {name_f1} et {name_f2} commence !")

            try:
                gagnant = combat(pokemon1, pokemon2, arena_callback)
            except Exception as e:
                print(f"Erreur pendant le combat entre {name_f1} et {name_f2}: {e}")
                continue

            if gagnant["name"].capitalize() == name_f1:
                winner = fighter_1
            elif gagnant["name"].capitalize() == name_f2:
                winner = fighter_2
            else:
                print(f"Erreur : Le gagnant n'est ni {name_f1} ni {name_f2}")
                continue

            if arena_callback:
                arena_callback(f"Combat : {name_f1} vs {name_f2} -> Gagnant : {gagnant['name'].capitalize()}")
            print(f"Le gagnant du combat est {gagnant['name'].capitalize()}")

            winners.append(winner)

        if len(participants) == 1:
            lone_participant = participants.pop(0)
            winners.append(lone_participant)
            if arena_callback:
                arena_callback(f"{lone_participant} passe automatiquement au tour suivant.")
            print(f"{lone_participant} passe automatiquement au tour suivant.")

        participants = winners
        if arena_callback:
            arena_callback("NOUVEAU TOUR\n")
        print("Nouveau tour du tournoi commence\n")

    final_winner = participants[0]
    pokemon_final = pokemons.get(f'pokemon_{final_winner}')
    if pokemon_final:
        name_final = pokemon_final["name"].capitalize()
        if arena_callback:
            arena_callback(f"Le grand gagnant est : {name_final}")
        print(f"Le grand gagnant du tournoi est : {name_final}")
        
        # Appeler le callback de fin avec le gagnant
        if end_callback:
            end_callback(pokemon_final)
    else:
        print(f"Erreur : Pokémon final non trouvé pour {final_winner}")
