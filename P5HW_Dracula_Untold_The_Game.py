# Avery Delpit
# 2025-04-09
# P5HW Dracula Untold Game: You will destroy your enemies and conquer the world.

import random
import time

# Initialize global variables
global player_name, player_health, player_gold, player_level, player_experience
global player_max_health, player_attack, player_defense, player_inventory
global player_skills, player_quests, player_location
global player_quests_failed_list, player_quests_completed_list
global player_quests_available_list, player_quests_in_progress_list

player_name = ""
player_health = 100
player_gold = 0
player_level = 1
player_experience = 0
player_max_health = 100
player_attack = 10
player_defense = 5
player_inventory = []
player_skills = []
player_quests = []
player_location = "Castle Dracula"
player_quests_failed_list = []
player_quests_completed_list = []
player_quests_available_list = []
player_quests_in_progress_list = []

def initialize_game():
    """Initialize or reset game variables"""
    global player_name, player_health, player_gold, player_level, player_experience
    global player_max_health, player_attack, player_defense, player_inventory
    global player_skills, player_quests, player_location
    global player_quests_failed_list, player_quests_completed_list
    global player_quests_available_list, player_quests_in_progress_list
    
    player_health = 100
    player_gold = 0
    player_level = 1
    player_experience = 0
    player_max_health = 100
    player_attack = 10
    player_defense = 5
    player_inventory = []
    player_skills = []
    player_quests = ['Get Bitten by your master']
    player_location = "Castle Dracula"
    player_quests_failed_list = []
    player_quests_completed_list = []
    player_quests_available_list = []
    player_quests_in_progress_list = []

def get_bitten():
    global player_health, player_experience, player_skills, player_attack, player_defense
    global player_quests, player_inventory, player_location, player_name
    global player_quests_completed_list, player_max_health
    
    print("\nYour master approaches you in the dark castle...")
    time.sleep(3)
    print("The shadows seem to dance around him as he draws near...")
    time.sleep(2)
    print("He offers you the gift of immortality.")
    time.sleep(2)
    print("\nWhat will you do?")
    print("1. Accept the gift willingly")
    print("2. Try to resist")
    print("3. Attempt to flee")
    choice = input("Enter your choice (1-3): ")
    time.sleep(2)
    
    if choice == "1":
        print("\nYou accept your master's gift with open arms...")
        time.sleep(2)
        print("He seems pleased with your eagerness...")
        time.sleep(2)
        print("The bite is swift and almost painless...")
        time.sleep(2)
        player_health -= 5
        player_experience += 30
        player_max_health += 20
        print(f"Your willingness has made the transformation easier.")
        print(f"Maximum health increased to {player_max_health}!")
        print(f"You gained 30 experience points!")
        player_inventory.extend(['Master\'s Signet Ring', 'Enchanted Blood Vial'])
    elif choice == "2":
        print("\nYou try to resist the dark gift...")
        time.sleep(2)
        print("But your master is far too powerful...")
        time.sleep(2)
        print("The transformation is painful and traumatic!")
        time.sleep(2)
        player_health -= 20
        player_experience += 40
        player_attack += 8
        print("Your struggle has made you stronger, but at a cost.")
        print(f"You gained 40 experience points!")
        player_inventory.extend(['Warrior\'s Spirit', 'Pain Essence'])
    else:
        print("\nYou attempt to flee into the darkness...")
        time.sleep(2)
        print("But your master appears before you instantly!")
        time.sleep(2)
        print("The bite is savage and merciless!")
        time.sleep(2)
        player_health -= 30
        player_experience += 50
        player_defense += 8
        print("Your survival instinct has enhanced your defensive capabilities.")
        print(f"You gained 50 experience points!")
        player_inventory.extend(['Swift Shadows', 'Survival Instinct'])
    
    print("You feel a surge of power coursing through your veins.")
    player_skills.extend(['Blood Magic', 'Shadow Step', 'Vampire Transformation'])
    player_attack += 5
    player_defense += 5
    
    print(f"Your attack is now {player_attack}.")
    print(f"Your defense is now {player_defense}.")
    print(f"Your skills are now: {player_skills}")
    
    player_inventory.extend(['Fang of the Vampire', 'Bloodstone', 'Vampire Amulet'])
    print(f"Your inventory is now: {player_inventory}")
    
    player_quests.extend(['Explore Your Newfound Skills', 'Prepare for Battle', 
                         'Fight The Sultan\'s Army', 'Conquer Your Enemies'])
    print(f"Your quests are now: {player_quests}")
    
    player_quests_completed_list.append('You\'ve Been Bitten by your master')
    time.sleep(2)

def explore_new_skills():
    global player_experience, player_attack, player_defense, player_health
    global player_inventory, player_skills, player_quests, player_quests_completed_list
    
    print("\nYou feel the dark powers within you...")
    time.sleep(3)
    print("Your blood burns with supernatural energy...")
    time.sleep(2)
    print("How will you explore your newfound abilities?")
    print("1. Practice Blood Magic")
    print("2. Master Shadow Movement")
    print("3. Embrace the Beast Within")
    choice = input("Enter your choice (1-3): ")
    
    print("\nYou focus your concentration...")
    time.sleep(2)
    
    if choice == "1":
        print("\nYou attempt to control the blood around you...")
        time.sleep(2)
        print("1. Try to heal your wounds")
        print("2. Form weapons from blood")
        print("3. Attempt blood domination")
        subchoice = input("Choose your technique (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("You successfully heal your wounds!")
            player_health += 30
            player_attack += 5
            player_skills.append('Blood Healing')
        elif subchoice == "2":
            print("You form deadly weapons from your own blood!")
            player_attack += 15
            player_health -= 10
            player_skills.append('Blood Weapons')
        else:
            print("You attempt to dominate others through blood magic!")
            player_attack += 10
            player_defense += 10
            player_skills.append('Blood Domination')
            
    elif choice == "2":
        print("\nYou practice moving through shadows...")
        time.sleep(2)
        print("1. Learn to teleport")
        print("2. Master stealth")
        print("3. Become one with darkness")
        subchoice = input("Choose your technique (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("You master the art of shadow teleportation!")
            player_attack += 10
            player_defense += 5
            player_skills.append('Shadow Step')
        elif subchoice == "2":
            print("You become invisible in darkness!")
            player_defense += 15
            player_skills.append('Shadow Cloak')
        else:
            print("You merge with the shadows themselves!")
            player_attack += 5
            player_defense += 10
            player_max_health += 20
            player_skills.append('Shadow Form')
            
    else:
        print("\nYou embrace your inner beast...")
        time.sleep(2)
        print("1. Focus on strength")
        print("2. Enhance speed")
        print("3. Maximize ferocity")
        subchoice = input("Choose your aspect (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("Your strength becomes supernatural!")
            player_attack += 20
            player_health -= 10
            player_skills.append('Supernatural Strength')
        elif subchoice == "2":
            print("Your speed becomes lightning-fast!")
            player_attack += 10
            player_defense += 10
            player_skills.append('Supernatural Speed')
        else:
            print("Your ferocity becomes terrifying!")
            player_attack += 15
            player_defense += 5
            player_max_health += 10
            player_skills.append('Supernatural Ferocity')
    
    player_experience += 50
    print(f"\nYou gained 50 experience points!")
    print(f"Your attack is now {player_attack}.")
    print(f"Your defense is now {player_defense}.")
    time.sleep(2)
    
    print("\nYou get hungry for blood!")
    player_health -= 10
    print(f"Your health is now {player_health}.")
    
    print("\nYou have found an unsuspecting victim!")
    print("You have the option to attack or spare them.")
    choice = input("Enter 'attack' or 'spare': ")
    
    if choice.lower() == 'attack':
        player_health += 20
        player_experience += 50
        player_inventory.extend(['Bloodstone', 'Vampire Amulet'])
        print(f"You gained 50 experience points!")
        print(f"Your health is now {player_health}.")
        print("You have gained new items!")
        print(f"Your inventory is now: {player_inventory}")
    else:
        player_health -= 10
        player_experience -= 20
        print(f"Your health is now {player_health}.")
        print("You have lost experience points!")
        print(f"You lost 20 experience points!")
    
    if 'Explore Your Newfound Skills' in player_quests:
        player_quests.remove('Explore Your Newfound Skills')
        player_quests_completed_list.append('Explore Your Newfound Skills')

def prepare_for_battle():
    global player_experience, player_attack, player_defense, player_skills, player_health
    global player_inventory, player_location, player_quests, player_quests_completed_list, player_level
    global player_max_health
    
    print("\nThe time has come to prepare for the great battle ahead...")
    time.sleep(3)
    print("How will you ready yourself for the coming war?")
    time.sleep(2)
    print("1. Train with Ancient Weapons")
    print("2. Study Battle Tactics")
    print("3. Enhance Your Vampire Powers")
    choice = input("Enter your choice (1-3): ")
    
    print("\nYou begin your preparation...")
    time.sleep(2)
    
    if choice == "1":
        print("\nYou seek out the ancient armory...")
        time.sleep(2)
        print("1. Master the Sword of the First Vampire")
        print("2. Learn the Arts of the Shadow Bow")
        print("3. Wield the Cursed Warhammer")
        subchoice = input("Choose your weapon (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("The legendary blade accepts you as its master!")
            player_attack += 15
            player_defense += 5
            player_inventory.extend(['First Vampire\'s Sword', 'Blood-Forged Armor'])
        elif subchoice == "2":
            print("You become one with the shadows and the bow!")
            player_attack += 12
            player_defense += 8
            player_inventory.extend(['Shadow Bow', 'Quiver of Night'])
        else:
            print("The cursed warhammer fills you with power!")
            player_attack += 20
            player_health -= 10
            player_inventory.extend(['Cursed Warhammer', 'Berserker\'s Plate'])
            
    elif choice == "2":
        print("\nYou delve into ancient military texts...")
        time.sleep(2)
        print("1. Study Defensive Formations")
        print("2. Learn Offensive Strategies")
        print("3. Master Guerrilla Tactics")
        subchoice = input("Choose your focus (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("You master the art of defense!")
            player_defense += 15
            player_max_health += 20
            player_inventory.extend(['Commander\'s Shield', 'Strategic Maps'])
        elif subchoice == "2":
            print("You learn the perfect time to strike!")
            player_attack += 15
            player_defense += 5
            player_inventory.extend(['Commander\'s Sword', 'Battle Plans'])
        else:
            print("You become a master of surprise attacks!")
            player_attack += 10
            player_defense += 10
            player_inventory.extend(['Stealth Armor', 'Tactical Scrolls'])
            
    else:
        print("\nYou focus on your vampiric nature...")
        time.sleep(2)
        print("1. Enhance Blood Magic")
        print("2. Strengthen Your Transformation")
        print("3. Master Mind Control")
        subchoice = input("Choose your power (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("Your blood magic reaches new heights!")
            player_attack += 12
            player_max_health += 15
            player_inventory.extend(['Blood Chalice', 'Crimson Robes'])
        elif subchoice == "2":
            print("Your beast form becomes more powerful!")
            player_attack += 15
            player_defense += 10
            player_inventory.extend(['Beast Form Talisman', 'Primal Armor'])
        else:
            print("Your mental powers become overwhelming!")
            player_attack += 8
            player_defense += 12
            player_max_health += 10
            player_inventory.extend(['Mind Control Crown', 'Psychic Focus'])
    
    player_experience += 50
    
    print(f"You gained 50 experience points!")
    print(f"Your attack is now {player_attack}.")
    print(f"Your defense is now {player_defense}.")
    
    player_skills.extend(['Vampire Lord Transformation', 'Blood Sacrifice', 'Shadow Cloak'])
    print("You have unlocked new skills!")
    print(f"Your skills are now: {player_skills}")
    
    player_inventory.extend(['Vlad the Impaler\'s Sword', 'Vlad the Impaler\'s Shield',
                           'Vlad the Impaler\'s Armor'])
    print("You have gained new items!")
    print(f"Your inventory is now: {player_inventory}")
    
    player_location = "Ottoman Empire"
    print(f"Your location is now: {player_location}")
    
    if 'Prepare for Battle' in player_quests:
        player_quests.remove('Prepare for Battle')
        player_quests_completed_list.append('Prepare for Battle')

def fight_sultans_army():
    global player_experience, player_attack, player_defense, player_health
    global player_inventory, player_location, player_quests, player_quests_completed_list, player_level
    
    print("\nThe Sultan's mighty army appears on the horizon...")
    time.sleep(3)
    print("Thousands of soldiers stretch as far as the eye can see...")
    time.sleep(2)
    print("How will you approach this battle?")
    time.sleep(2)
    print("1. Launch a Frontal Assault")
    print("2. Attack from the Shadows")
    print("3. Use Your Vampire Powers")
    choice = input("Enter your choice (1-3): ")
    
    print("\nThe battle begins...")
    time.sleep(2)
    
    if choice == "1":
        print("\nYou prepare for a direct confrontation...")
        time.sleep(2)
        print("1. Lead the Charge")
        print("2. Command from the Rear")
        print("3. Fight Alongside Your Troops")
        subchoice = input("Choose your approach (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("You lead a devastating charge!")
            battle_bonus = 25
            player_attack += 5
        elif subchoice == "2":
            print("You coordinate a masterful battle plan!")
            battle_bonus = 20
            player_defense += 5
        else:
            print("Your presence inspires your soldiers!")
            battle_bonus = 15
            player_max_health += 10
            
    elif choice == "2":
        print("\nYou move under cover of darkness...")
        time.sleep(2)
        print("1. Assassinate the Leaders")
        print("2. Sabotage Their Supplies")
        print("3. Spread Terror in Their Ranks")
        subchoice = input("Choose your strategy (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("The enemy leadership falls to your blade!")
            battle_bonus = 30
            player_attack += 8
        elif subchoice == "2":
            print("Their army crumbles without supplies!")
            battle_bonus = 25
            player_experience += 50
        else:
            print("Fear destroys their morale!")
            battle_bonus = 20
            player_defense += 8
            
    else:
        print("\nYou call upon your dark powers...")
        time.sleep(2)
        print("1. Summon a Blood Storm")
        print("2. Transform into a Monstrous Beast")
        print("3. Raise an Army of the Dead")
        subchoice = input("Choose your power (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("A rain of blood decimates their forces!")
            battle_bonus = 35
            player_health -= 20
        elif subchoice == "2":
            print("Your monstrous form tears through their ranks!")
            battle_bonus = 30
            player_attack += 10
        else:
            print("The dead rise to fight for you!")
            battle_bonus = 25
            player_max_health += 15
    
    time.sleep(2)
    battle_result = random.randint(1, 100) + battle_bonus
    
    if battle_result > 40:  # 60% chance of victory
        print("Victory! You have defeated the Sultan's army!")
        player_experience += 100
        player_attack += 10
        player_defense += 10
        player_inventory.extend(['Sultan\'s Sword', 'Sultan\'s Shield', 'Sultan\'s Armor'])
        
        print(f"You gained 100 experience points!")
        print(f"Your attack is now {player_attack}.")
        print(f"Your defense is now {player_defense}.")
        print("You have gained new items!")
        print(f"Your inventory is now: {player_inventory}")
        
        player_location = "Rome"
        print(f"Your location is now: {player_location}")
        
        if 'Fight The Sultan\'s Army' in player_quests:
            player_quests.remove('Fight The Sultan\'s Army')
            player_quests_completed_list.append('Fight The Sultan\'s Army')
    else:
        print("The battle was fierce! You were wounded but managed to escape...")
        player_health -= 30
        print(f"Your health is now {player_health}")

def conquer_enemies():
    global player_experience, player_attack, player_defense, player_health, player_level
    global player_inventory, player_quests, player_quests_completed_list, player_max_health
    
    print("\nThe time has come for your final conquest...")
    time.sleep(3)
    print("The world trembles before your power...")
    time.sleep(2)
    print("How will you claim your ultimate victory?")
    time.sleep(2)
    print("1. Military Domination")
    print("2. Political Manipulation")
    print("3. Supernatural Terror")
    choice = input("Enter your choice (1-3): ")
    
    print("\nYou begin your conquest...")
    time.sleep(2)
    
    if choice == "1":
        print("\nYou gather your armies for the final campaign...")
        time.sleep(2)
        print("1. Lead a Global Invasion")
        print("2. Siege Their Capitals")
        print("3. Crush Their Armies")
        subchoice = input("Choose your military strategy (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("Your armies march across the world!")
            conquest_bonus = 35
            player_attack += 15
            player_inventory.extend(['World Map', 'General\'s Regalia'])
        elif subchoice == "2":
            print("Their greatest cities fall before you!")
            conquest_bonus = 30
            player_defense += 15
            player_inventory.extend(['City Keys', 'Siege Master\'s Crown'])
        else:
            print("You destroy all who oppose you!")
            conquest_bonus = 25
            player_max_health += 30
            player_inventory.extend(['Victory Banner', 'Conqueror\'s Plate'])
            
    elif choice == "2":
        print("\nYou weave a web of political intrigue...")
        time.sleep(2)
        print("1. Corrupt Their Leaders")
        print("2. Incite Civil Wars")
        print("3. Form Dark Alliances")
        subchoice = input("Choose your political approach (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("The world's leaders bow to your will!")
            conquest_bonus = 40
            player_experience += 100
            player_inventory.extend(['Crown of Dominion', 'Royal Seals'])
        elif subchoice == "2":
            print("Nations tear themselves apart!")
            conquest_bonus = 35
            player_attack += 10
            player_inventory.extend(['Chaos Orb', 'Discord Scepter'])
        else:
            print("Dark powers pledge their loyalty!")
            conquest_bonus = 30
            player_defense += 20
            player_inventory.extend(['Dark Pact Scrolls', 'Alliance Rings'])
            
    else:
        print("\nYou unleash your full supernatural might...")
        time.sleep(2)
        print("1. Eclipse the Sun")
        print("2. Unleash the Vampire Plague")
        print("3. Command Nature Itself")
        subchoice = input("Choose your supernatural power (1-3): ")
        time.sleep(2)
        
        if subchoice == "1":
            print("Eternal darkness covers the world!")
            conquest_bonus = 45
            player_max_health += 50
            player_inventory.extend(['Sun\'s Heart', 'Night Crown'])
        elif subchoice == "2":
            print("Your curse spreads across humanity!")
            conquest_bonus = 40
            player_attack += 25
            player_inventory.extend(['Plague Chalice', 'First Blood'])
        else:
            print("The elements themselves obey you!")
            conquest_bonus = 35
            player_defense += 25
            player_inventory.extend(['Nature\'s Crown', 'Elemental Orbs'])
    
    time.sleep(2)
    conquest_result = random.randint(1, 100) + conquest_bonus
    
    if conquest_result > 50:  # 50% chance of victory
        print("Victory! You have conquered your enemies!")
        player_experience += 200
        player_level += 1
        player_attack += 20
        player_defense += 20
        player_inventory.extend(['Crown of the Vampire Lord', 'Scepter of Power'])
        
        print(f"You gained 200 experience points!")
        print(f"You are now level {player_level}!")
        print(f"Your attack is now {player_attack}.")
        print(f"Your defense is now {player_defense}.")
        print("You have gained new items!")
        print(f"Your inventory is now: {player_inventory}")
        
        if 'Conquer Your Enemies' in player_quests:
            player_quests.remove('Conquer Your Enemies')
            player_quests_completed_list.append('Conquer Your Enemies')
            print("\nCongratulations! You have completed all quests!")
            print("You are now the supreme ruler of the night!")
    else:
        print("The conquest was challenging! You must retreat and grow stronger...")
        player_health -= 40
        print(f"Your health is now {player_health}")

def display_player_info():
    print("\n=== Player Status ===")
    print(f"Name: {player_name}")
    print(f"Health: {player_health}/{player_max_health}")
    print(f"Gold: {player_gold}")
    print(f"Level: {player_level}")
    print(f"Experience: {player_experience}")
    print(f"Attack: {player_attack}")
    print(f"Defense: {player_defense}")
    print(f"Location: {player_location}")
    print("\nInventory:")
    for item in player_inventory:
        print(f"- {item}")
    print("\nSkills:")
    for skill in player_skills:
        print(f"- {skill}")
    print("\nActive Quests:")
    for quest in player_quests:
        print(f"- {quest}")
    print("\nCompleted Quests:")
    for quest in player_quests_completed_list:
        print(f"- {quest}")
    time.sleep(2)

def main():
    print("Welcome to Dracula Untold: The Game!")
    global player_name, player_health, player_gold, player_level, player_experience
    global player_max_health, player_attack, player_defense, player_inventory
    global player_skills, player_quests, player_location
    global player_quests_failed_list, player_quests_completed_list
    global player_quests_available_list, player_quests_in_progress_list
    
    player_name = input("Enter your name, future vampire lord: ")
    initialize_game()
    
    while True:
        if player_health <= 0:
            print("\nYour health has fallen to zero...")
            print("Game Over!")
            break
            
        print("\n=== Game Menu ===")
        print("1. Get Bitten")
        print("2. Explore New Skills")
        print("3. Prepare for Battle")
        print("4. Fight The Sultan's Army")
        print("5. Conquer Your Enemies")
        print("6. Display Player Info")
        print("7. Exit Game")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            if 'Get Bitten by your master' in player_quests:
                get_bitten()
            else:
                print("You have already been bitten!")
        elif choice == "2":
            if 'Explore Your Newfound Skills' in player_quests:
                explore_new_skills()
            else:
                print("You must be bitten first!" if not player_skills else "You have already mastered your skills!")
        elif choice == "3":
            if 'Prepare for Battle' in player_quests:
                prepare_for_battle()
            else:
                print("You must explore your skills first!" if not player_skills else "You are already prepared for battle!")
        elif choice == "4":
            if 'Fight The Sultan\'s Army' in player_quests:
                fight_sultans_army()
            else:
                print("You must prepare for battle first!" if not 'Prepare for Battle' in player_quests_completed_list else "You have already defeated the Sultan's army!")
        elif choice == "5":
            if 'Conquer Your Enemies' in player_quests:
                conquer_enemies()
            else:
                print("You must defeat the Sultan's army first!" if not 'Fight The Sultan\'s Army' in player_quests_completed_list else "You have already conquered your enemies!")
        elif choice == "6":
            display_player_info()
        elif choice == "7":
            print("\nThanks for playing!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        # Level up check
        if player_experience >= 100 * player_level:
            player_level += 1
            player_max_health += 20
            player_health = player_max_health
            player_attack += 5
            player_defense += 5
            print(f"\nLevel Up! You are now level {player_level}!")
            print(f"Your stats have increased!")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
