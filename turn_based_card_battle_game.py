import random

player_health = 50
enemy_health = 150
player_block = 0

#List of cards that are drawn during the game
draw_pile = [
  "Slash", "Slash",
  "Hew",
  "Fighting Spirit",
  "Source of Water", "Source of Water",
  "Water Barrier",
  "Shelter Kick",
  "Shelter Defense",
  "Shelter Hold"
]

hew_level = 0
hand = []

#Determines effects of a card when played
def use_card(card_name, hew_level):
  damage = 0
  heal = 0
  block = 0
  ap_gain = 0
  hew_used = False

  if card_name == "Slash":
    damage = 6

  elif card_name.startswith("Hew"):
    hew_used = True
    damage = 8 + (hew_level * 4)

  elif card_name == "Source of Water":
    heal = 3
    ap_gain = 1

  elif card_name == "Water Barrier":
    heal = 8

  elif card_name == "Shelter Kick":
    damage = 4

  elif card_name == "Shelter Defense":
    block = 7

  elif card_name == "Shelter Hold":
    block = 12

  return damage, heal, block, ap_gain, hew_used

#Draw 5 random cards to create the player's starting hand
for i in range(5):
  hand.append(random.choice(draw_pile))

#Main
while player_health > 0 and enemy_health > 0:
  ap = 3
  player_block = 0

  print("\n--- NEW TURN ---")

  while ap > 0:
    print(f"\nHP: {player_health} | Enemy: {enemy_health} | AP: {ap}")

    #Displays every card in player's hand
    for i in range(len(hand)):
      card = hand[i]

    #Display Hew's current level of upgrade
      if card.startswith("Hew"):
        card_display = (f"Hew lvl.{hew_level}")
      else:
        card_display = card
        
    #Print description of cards
      if card.startswith("Hew"):
        if hew_level == 5:
          desc = "Cost: 2 AP | Highest damage"
        else:
          desc = "Cost: 3 AP | Scaling damage"

      elif card == "Slash":
        desc = "Cost: 1 AP | Deal 6 damage"

      elif card == "Fighting Spirit":
        desc = "Cost: 1 AP | Use highest AP card for only 1 AP"

      elif card == "Source of Water":
        desc = "Cost: 0 AP | Heal 3 + Gain 1 AP"

      elif card == "Water Barrier":
        desc = "Cost: 1 AP | Heal 8"

      elif card == "Shelter Kick":
        desc = "Cost: 1 AP | Deal 4 damage"

      elif card == "Shelter Defense":
        desc = "Cost: 1 AP | Gain 7 block"

      elif card == "Shelter Hold":
        desc = "Cost: 2 AP | Gain 12 block"

      print(f"{i}: {card_display} -> {desc}")

    choice = input("Choose a card index or 'end': ")

    #End player's current turn early
    if choice == "end":
      break

    if choice.isdigit():
      choice = int(choice)
    
    #Makes sure that the index exists in hand
      if 0 <= choice < len(hand):
        card_name = hand[choice]

        #Determines AP cost of selected card
        if card_name.startswith("Hew"):
          if hew_level == 5:
            cost = 2
          else:
            cost = 3

        elif card_name == "Source of Water":
          cost = 0

        elif card_name == "Shelter Hold":
          cost = 2

        elif card_name == "Fighting Spirit":
          cost = 1

        else:
          cost = 1

        if ap >= cost:

          if card_name == "Fighting Spirit":
            highest_card = None
            highest_cost = -1

            #Searches player's hand for the card with highest AP cost
            for c in hand:

              if c.startswith("Hew"):
                if hew_level == 5:
                  c_cost = 2
                else:
                  c_cost = 3

              elif c == "Shelter Hold":
                c_cost = 2

              elif c == "Source of Water":
                c_cost = 0

              else:
                c_cost = 1

            #Ignores the Fighting Spirit card when searching for highest cost card
              if c_cost > highest_cost and c != "Fighting Spirit":
                highest_cost = c_cost
                highest_card = c

            ap -= 1
            hand.pop(choice)
            #Applies effects of highest cost card without paying its AP cost
            if highest_card:
              damage, heal, block, ap_gain, hew_used = use_card(highest_card, hew_level)

              enemy_health -= damage
              player_health += heal
              player_block += block
              ap += ap_gain
              
              if hew_used and hew_level < 5:
                hew_level += 1

              if enemy_health <= 0:
                break

          else:
            ap -= cost

            #Get the effects of the selected card
            damage, heal, block, ap_gain, hew_used = use_card(card_name, hew_level)

            #Applies card's effects to player and enemy
            enemy_health -= damage
            player_health += heal
            player_block += block
            ap += ap_gain

            if hew_used and hew_level < 5:
              hew_level += 1

            if not card_name.startswith("Hew"):
              hand.pop(choice)

            if enemy_health <= 0:
              break

        else:
          print("Not enough AP!")

      else:
        print("Invalid index.")

    else:
      print("Invalid input.")

#Creates new hand for next turn
  new_hand = []

#Keeps Hew cards instead of removing them between turns
  for card in hand:
    if card.startswith("Hew"):
      new_hand.append(card)

  while len(new_hand) < 5:
    new_card = random.choice(draw_pile)
    can_add = True

    if new_card == "Hew":
      for card in new_hand:
        if card.startswith("Hew"):
          can_add = False

    if can_add:
      new_hand.append(new_card)

#Replaces old hand with newly created hand
  hand = new_hand

#Hew automatically levels up every turn until lvl. 5
  if hew_level > 0 and hew_level < 5:
    hew_level += 1

  if enemy_health > 0:
    damage = random.randint(5, 10)
    damage_taken = max(0, damage - player_block)
    player_health -= damage_taken

    print(f"\nEnemy attacks for {damage} damage!")
    print(f"You blocked {player_block}, took {damage_taken}")


if player_health <= 0:
  print("\nYou lost!")
else:
  print("\nYou won!")