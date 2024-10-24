import random

# Classes for Guns, Bows, and Melee Weapons
class Gun:
    def __init__(self, name, magazine_size, rate_of_fire, damage, automatic=False, durability=100, attachments=None):
        self.name = name
        self.magazine_size = magazine_size
        self.rate_of_fire = rate_of_fire
        self.damage = damage
        self.automatic = automatic
        self.durability = durability
        self.attachments = attachments if attachments else []
        self.current_ammo = magazine_size  # Start with full ammo

    def shoot(self, target, player):
        if self.current_ammo > 0:
            self.current_ammo -= 1
            actual_damage = self.damage - (random.uniform(0.1, 0.5) * self.damage * (self.durability / 100))
            for attachment in self.attachments:
                actual_damage += attachment.bonus_damage
            target.hp -= actual_damage
            self.durability -= 0.1
            print(f"{player.name} shoots {target.target_type} with {self.name} for {actual_damage:.2f} damage.")
            if target.hp <= 0:
                print(f"{target.target_type} has been eliminated!")
        else:
            print("Out of ammo! Please reload.")

    def reload(self):
        self.current_ammo = self.magazine_size
        print(f"{self.name} reloaded. Ammo: {self.current_ammo}/{self.magazine_size}")

    def add_attachment(self, attachment):
        self.attachments.append(attachment)
        print(f"{attachment.name} added to {self.name}. Current attachments: {[a.name for a in self.attachments]}.")

class Bow:
    def __init__(self, name, damage, durability=100):
        self.name = name
        self.damage = damage
        self.durability = durability

    def shoot(self, target, player):
        actual_damage = self.damage
        target.hp -= actual_damage
        print(f"{player.name} shoots {target.target_type} with {self.name} for {actual_damage:.2f} damage.")
        if target.hp <= 0:
            print(f"{target.target_type} has been eliminated!")

class MeleeWeapon:
    def __init__(self, name, damage, durability=100):
        self.name = name
        self.damage = damage
        self.durability = durability

    def attack(self, target, player):
        actual_damage = self.damage
        target.hp -= actual_damage
        self.durability -= 0.1
        print(f"{player.name} attacks {target.target_type} with {self.name} for {actual_damage:.2f} damage.")
        if target.hp <= 0:
            print(f"{target.target_type} has been eliminated!")

# Attachments Class
class Attachment:
    def __init__(self, name, bonus_damage):
        self.name = name
        self.bonus_damage = bonus_damage

# Target Class
class Target:
    def __init__(self, hp, damage, target_type):
        self.hp = hp
        self.damage = damage
        self.target_type = target_type

# Player Class
class Player:
    def __init__(self, hp, name, money=0):
        self.hp = hp
        self.name = name
        self.inventory = []
        self.achievements = []
        self.money = money
        self.kills = 0
        self.deaths = 0
        self.total_money = 0
        self.total_cases_earned = 0

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def earn_money(self, amount):
        self.money += amount
        self.total_money += amount

    def show_achievements(self):
        print("Achievements:")
        for achievement in self.achievements:
            print(f"- {achievement}")

    def show_stats(self):
        print(f"\n--- Player Stats for {self.name} ---")
        print(f"Money: ${self.money}")
        print(f"Kills: {self.kills}")
        print(f"Deaths: {self.deaths}")
        print(f"Total Money Earned: ${self.total_money}")
        print(f"Total Cases Earned/Open: {self.total_cases_earned}")

# Shop Class
class Shop:
    def __init__(self):
        self.inventory = [
            Gun(name="Pistol", magazine_size=15, rate_of_fire=0.5, damage=15, durability=100),
            Gun(name="Submachine Gun", magazine_size=20, rate_of_fire=0.15, damage=18, automatic=True, durability=60),
            Gun(name="Light Machine Gun", magazine_size=100, rate_of_fire=0.5, damage=20, automatic=True, durability=90),
            Gun(name="Crossbow", magazine_size=1, rate_of_fire=2, damage=40, automatic=False, durability=40),
            Gun(name="Grenade Launcher", magazine_size=5, rate_of_fire=2.5, damage=30, automatic=False, durability=30),
            Gun(name="Desert Eagle", magazine_size=7, rate_of_fire=1.2, damage=40, durability=100),
            Gun(name="M4 Carbine", magazine_size=30, rate_of_fire=0.09, damage=25, automatic=True, durability=85),
            Gun(name="AK-47", magazine_size=30, rate_of_fire=0.1, damage=30, automatic=True, durability=70),
            Gun(name="MP5", magazine_size=30, rate_of_fire=0.08, damage=20, automatic=True, durability=75),
            Gun(name="Barrett .50 cal", magazine_size=10, rate_of_fire=1.5, damage=80, automatic=False, durability=50),
            Gun(name="UMP45", magazine_size=25, rate_of_fire=0.1, damage=28, automatic=True, durability=65)
        ]

        # Rare Guns
        self.rare_inventory = [
            Gun(name="Golden Gun", magazine_size=6, rate_of_fire=0.8, damage=100, durability=50),
            Gun(name="Platinum SMG", magazine_size=30, rate_of_fire=0.05, damage=50, automatic=True, durability=40)
        ]

        # Attachments (examples)
        self.attachments = [
            Attachment(name="Scope", bonus_damage=5),
            Attachment(name="Extended Magazine", bonus_damage=0),
            Attachment(name="Silencer", bonus_damage=2)
        ]

    def get_price(self, gun):
        return 50 * gun.durability // 100

    def display_inventory(self):
        print("\n--- Shop Inventory ---")
        for idx, gun in enumerate(self.inventory):
            print(f"{idx + 1}. {gun.name} (Damage: {gun.damage}, Durability: {gun.durability}) - ${self.get_price(gun)}")

    def display_rare_inventory(self):
        print("\n--- Rare Guns Inventory ---")
        for idx, gun in enumerate(self.rare_inventory):
            print(f"{idx + 1}. {gun.name} (Damage: {gun.damage}, Durability: {gun.durability}) - ${self.get_price(gun)}")

    def sell_gun(self, player, gun_index):
        if 0 <= gun_index < len(self.inventory):
            gun = self.inventory[gun_index]
            price = self.get_price(gun)
            if player.spend_money(price):
                player.inventory.append(gun)
                print(f"{player.name} bought {gun.name} for ${price}.")
            else:
                print("Not enough money!")
        elif 0 <= gun_index < len(self.rare_inventory):
            gun = self.rare_inventory[gun_index]
            price = self.get_price(gun)
            if player.spend_money(price):
                player.inventory.append(gun)
                print(f"{player.name} bought {gun.name} for ${price}.")
            else:
                print("Not enough money!")

    def sell_attachment(self, player, attachment_index):
        if 0 <= attachment_index < len(self.attachments):
            attachment = self.attachments[attachment_index]
            if player.spend_money(20):  # Flat price for attachments
                player.inventory[0].add_attachment(attachment)  # Add attachment to currently equipped weapon
                print(f"{attachment.name} added to {player.inventory[0].name}.")
            else:
                print("Not enough money!")

# Main Game Loop
def main():
    print("Welcome to the Gun Simulation Game!")
    player_name = input("Enter your player name: ")
    player = Player(hp=100, name=player_name, money=100)

    # Starter kit: choice of pistol, crossbow, or melee weapon
    print("Choose a starter kit:")
    print("1. Pistol (Comes with 3 mags of ammo)")
    print("2. Crossbow (+ $100)")
    print("3. Melee weapon (No range, high durability)")
    starter_choice = input("Enter choice: ")
    if starter_choice == '1':
        starter_gun = Gun(name="Pistol", magazine_size=15, rate_of_fire=0.5, damage=10, durability=100)
        player.inventory.append(starter_gun)
    elif starter_choice == '2':
        starter_bow = Bow(name="Crossbow", damage=40, durability=100)
        player.inventory.append(starter_bow)
        player.earn_money(100)
    elif starter_choice == '3':
        starter_melee = MeleeWeapon(name="Knife", damage=30, durability=200)
        player.inventory.append(starter_melee)
    else:
        print("Invalid choice, starting with Pistol.")
        starter_gun = Gun(name="Pistol", magazine_size=15, rate_of_fire=0.5, damage=10, durability=100)
        player.inventory.append(starter_gun)

    shop = Shop()

    while True:
        print("\n--- Main Menu ---")
        print("1. Start Fight")
        print("2. Go to Shop")
        print("3. View Rare Guns")
        print("4. Show Achievements")
        print("5. Check Inventory")
        print("6. View Stats")
        print("7. Quit Game")

        choice = input("Enter your choice: ")

        if choice == '1':
            target = Target(hp=100, damage=10, target_type="Target")
            while target.hp > 0 and player.hp > 0:
                action = input(f"Using {player.inventory[0].name}. Enter 'shoot', 'switch' to change weapon, or 'leave' to exit the fight: ").lower()
                if action == "shoot":
                    if isinstance(player.inventory[0], Gun):
                        player.inventory[0].shoot(target, player)
                    elif isinstance(player.inventory[0], Bow):
                        player.inventory[0].shoot(target, player)
                    elif isinstance(player.inventory[0], MeleeWeapon):
                        player.inventory[0].attack(target, player)
                elif action == "switch":
                    for idx, weapon in enumerate(player.inventory):
                        print(f"{idx + 1}. {weapon.name}")
                    weapon_choice = int(input("Choose a weapon (enter number): ")) - 1
                    if 0 <= weapon_choice < len(player.inventory):
                        print(f"Switched to {player.inventory[weapon_choice].name}.")
                        player.inventory[0], player.inventory[weapon_choice] = player.inventory[weapon_choice], player.inventory[0]
                    else:
                        print("Invalid choice.")
                elif action == "leave":
                    print(f"{player.name} has left the fight.")
                    break
                else:
                    print("Invalid action.")

        elif choice == '2':
            shop.display_inventory()
            gun_choice = int(input("Enter the number of the gun you want to buy: ")) - 1
            shop.sell_gun(player, gun_choice)
        elif choice == '3':
            shop.display_rare_inventory()
            gun_choice = int(input("Enter the number of the rare gun you want to buy: ")) - 1
            shop.sell_gun(player, gun_choice)
        elif choice == '4':
            player.show_achievements()
        elif choice == '5':
            print("\n--- Inventory ---")
            for idx, item in enumerate(player.inventory):
                print(f"{idx + 1}. {item.name} (Durability: {item.durability})")
            print(f"Money: ${player.money}")
        elif choice == '6':
            player.show_stats()
        elif choice == '7':
            print("Exiting the game. Thanks for playing!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
