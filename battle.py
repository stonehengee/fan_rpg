import sqlalchemy as alchemy
from models import Player, Enemy, SkillOwnership, Skill
from sqlalchemy.ext.declarative import declarative_base
import random, sys
from termcolor import colored, cprint

engine = alchemy.create_engine("sqlite:///app.db")
# Base = declarative_base()
Session = alchemy.orm.sessionmaker(bind=engine)
session = Session()

# player = Player()
metadata = alchemy.MetaData()
metadata.bind = alchemy.engine


player = session.query(Player).filter_by(id=1).all()[0]
enemy = session.query(Enemy).filter_by(name="Rat").all()[0]
skills = [session.query(Skill).filter_by(id = each.skill_id).all()[0] for each in session.query(SkillOwnership).filter_by(player_id = player.id).all()]
skills_dict = {}
player_max_hp = player.hp
for each in skills:
    skills_dict[each.name] = each
skills_list = sorted(list(skills_dict.keys()))
#player = alchemy.engine.execute(
   #     player_table.select().where(player_table.c.id == 1)
#)

# forrest = Player()

# print(player[0].name)
# print(enemy[0].name)
def escape_battle():
    F = random.randint(0, 255)
    if ((player.agility*128/enemy.agility)+30)%256 > F:
        print ("You successfully escaped!")
        return True
    else:
        print ("Can't escape!")
        return False

def enemy_attack():
    dodge = input("Enemy {} is about to attack!\nDodge:\n[L]eft\n[R]right\n[U]p\n[D]own\n".format(enemy.name))
    if dodge.lower() == random.choice(['l', 'r', 'u', 'd']):
        print("You narrowly dodged {}'s attack!".format(enemy.name))
    else:
        player.hp -= enemy.strength
        print("You were hit for {} points! {} hp remaining.".format(enemy.strength, player.hp))

def player_attack():
    while True:
        choice = input("What would you like to do?\n[A]ttack\n[I]tem\n[R]un\n")
        if choice.lower() == 'a':
            choice = input("How would you like to attack?\n[A]ttack\n[S]kills\n")
            if choice.lower() == 'a':
                damage = player.strength/enemy.fortitude
            elif choice.lower() == 's':
                for index, skill in enumerate(skills_list, start=1):
                    cost = skills_dict[skill].use_cost
                    output = index, skill, cost
                    if player.mp >= cost:
                        cprint(output, "green")
                    else:
                        cprint(output, "red")
                attack = int(input())
                if skills_list[attack-1]:
                    damage = skills_dict[skills_list[attack-1]].damage_heal
    ###Damage calculation
            if damage > 0:
                enemy.hp -= damage
                print("You hit for {} points! Enemy has {} hp remaining.".format(damage, enemy.hp))
            else:
                player.hp -= damage
                if player.hp > player_max_hp:
                    player.hp = player_max_hp
                print("You healed for {} points! {} hp remaining".format(-damage, player.hp))
            break
        elif choice.lower() == 'i':
            pass
        elif choice.lower() == 'r':
            if escape_battle() == True:
                return "escaped"

def random_encounter():
    print("An enemy {} has appeared!".format(enemy.name))
    # speed check
    if enemy.agility > player.agility:
        while enemy.hp > 0 and player.hp > 0:
            enemy_attack()
            if player.hp > 0:
                if player_attack() == "escaped":
                    break
        if player.hp <= 0:
            print("You were defeated!")
        elif enemy.hp <= 0:
            print("You defeated {}! {} gold!".format(enemy.name, enemy.gold))
            player.gold += enemy.gold
    
    elif player.agility >= enemy.agility:
        while enemy.hp > 0 and player.hp > 0:
            if player_attack() == "escaped":
                break
            if enemy.hp > 0:
                enemy_attack()
        if player.hp <= 0:
            print("You were defeated!")
        elif enemy.hp <= 0:
            print("You defeated {}! You gained {} gold!".format(enemy.name, enemy.gold))
            player.gold += enemy.gold
            
if __name__ == "__main__":
    random_encounter()
    
##TODO
# implement cast costs
# add in items
#Skills are too weak - damage should be adjusted based on player level