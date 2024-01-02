import requests
import fandom
def check_relic():
    valuted_relic=[]
    fandom.set_wiki('WARFRAME')
    page=fandom.page(title="Relic")
    valuted=page.section('Vaulted Relics')
    lines=valuted.split("\n")
    for line in lines:
        valuted_relic.append(line)


    vaulted_relic_updated=valuted_relic[13:]
    return vaulted_relic_updated







def get_relic_drop(relic_name):
    updated_relic_name=f"{relic_name} Relic"

    warframe_planets=[]
    item_loc=[]
    item_drop_details={}


    planets = requests.get('https://drops.warframestat.us/data/missionRewards.json').json()

    for Planets_rewards in planets['missionRewards']:
        warframe_planets.append(Planets_rewards)

    for i in warframe_planets:
       rewards = planets['missionRewards'][i]

       for r in rewards:

           itemToBeRecived=planets['missionRewards'][i][r]['rewards']
           gameMode=planets['missionRewards'][i][r]['gameMode']




           if type(itemToBeRecived) == dict:

               #print("Has rotations")
               a_rotation = itemToBeRecived["A"]
               b_rotation = itemToBeRecived["B"]
               c_rotation = itemToBeRecived["C"]
               #print(f"A: {a_rotation}\nB: {b_rotation}\nc: {c_rotation}")
               for a in a_rotation:
                   if updated_relic_name in a.values():
                       print(gameMode)

                       item_drop_details = {
                       "Planet-node": f"{i} {r}",
                       "Rotation": "A",
                       "rarity": a['rarity'],
                       "chance": a['chance'],
                        "GameMode": gameMode
                       }
                       item_loc.append(item_drop_details)


               for b in b_rotation:
                   if updated_relic_name in b.values():
                       item_drop_details = {
                           "Planet-node": f"{i} {r}",
                           "Rotation": "B",
                           "rarity": b['rarity'],
                           "chance": b['chance'],
                           "GameMode": gameMode }
                       item_loc.append(item_drop_details)

               for c in c_rotation:
                   if updated_relic_name in c.values():
                        item_drop_details = {
                            "Planet-node": f"{i} {r}",
                            "Rotation": "C",
                            "rarity": c['rarity'],
                            "chance": c['chance'],
                            "GameMode": gameMode}
                        item_loc.append(item_drop_details)
    return item_loc




def get_available_prime():
    current_prime_part=set()

    response_2 = requests.get('https://drops.warframestat.us/data/all.json').json()
    for i in response_2['relics']:
        for r in i['rewards']:
            item_name = r['itemName']
            current_prime_part.add(item_name)

    sorted_prime_list = sorted(current_prime_part)



    for prime in sorted_prime_list:
        if "Prime" not in prime:
            sorted_prime_list.remove(prime)

    return sorted_prime_list

def get_prime_part_relic(item_to_find):
    item_list = {}

    response_2=requests.get('https://drops.warframestat.us/data/all.json').json()

    for i in response_2['relics']:


        relic_info=f"{i['tier']}_{i['relicName']}_{i['state']}"


        for r in i['rewards']:
            item_name = r['itemName']

            rarity_of_getting_item = r['rarity']
            chance_of_getting_item = r['chance']



            if item_name == item_to_find:

                if relic_info in item_list:
                    item_list[relic_info].append((rarity_of_getting_item, chance_of_getting_item))
                else:
                    item_list[relic_info]=[(rarity_of_getting_item, chance_of_getting_item)]



    #for info in relic_info_return_list:

    return item_list




print



