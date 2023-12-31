import streamlit as st
from getting_data import get_available_prime,get_prime_part_relic,check_relic,get_relic_drop
import pandas as pd
from time import sleep
from stqdm import stqdm
from ordered_set import OrderedSet
from datetime import date

counter=0
# Initialize session_state
if "i" not in st.session_state:
    st.session_state.i = None


def set_style_for_chance(x:str):
    if x=="Uncommon":
        return 'background-color : grey'
    if x=='Rare':
        return 'background-color: #B8860B'
    if x=='Common':
        return 'background-color : #C0C0C0'





def set_data():
    relic_list=[]
    chance_info=[]
    number_list=[]
    valuted=[]




    choice=st.session_state.get("-i-")
    relics=get_prime_part_relic(choice)

    for relic in relics.keys():

        name=relic.split("_")[0]+" "+relic.split("_")[1]


        relic_list.append(relic)
        chance_info.append(relics[relic][0][0])
        number_list.append(int(relics[relic][0][1]))

    valuted_relic = check_relic()
    t=[]
    for name in relic_list:
        updated_name=name.split("_")[0]+" "+name.split("_")[1]
        t.append(updated_name)

    relic_set=OrderedSet(t)
    for relic in relic_set:
        if relic in valuted_relic:
            for i in range(4):
                valuted.append(True)

        else:
            for c in range(4):
                valuted.append(False)



    relic_info=pd.DataFrame({
        "Relic name": relic_list,
        "Rarity of getting item": chance_info,
        "Chance of getting item": number_list,
        "Valuted": valuted
    })
    return  relic_info,relic_set




def set_relic_graphs(relic_name):
    p=[]
    n=[]
    R=[]
    RGI=[]
    CGI=[]
    G=[]
    info=get_relic_drop(relic_name)
    for loc in info:
        if len(loc)!=0:
            planet = loc['Planet']
            Node=loc["Node"]
            Rotation = loc['Rotation']
            rarity_of_getting_item = loc['rarity']
            chance_of_getting_item = loc['chance']
            gamemode = loc['GameMode']
            p.append(planet)
            n.append(Node)
            R.append(Rotation)
            RGI.append(rarity_of_getting_item)
            CGI.append(chance_of_getting_item)
            G.append(gamemode)
    drop_sources=pd.DataFrame({
        "Planet": p,
        "Node": n,
        "Rotation": R,
        "Rarity of getting item": RGI,
        "Chance of getting item": CGI,
        "GameMode": G
    })
    return drop_sources




primes = get_available_prime()

st.title("WarframeFinder")
st.text("You can select the item you want from the box below or type in the item")
prime_part = st.selectbox(label="Choose the prime part you want to get", options=primes, key="-i-")
get_item=st.button(label="Click here to get relics for your prime part")

if get_item:

    table, relics_to_farm = set_data()
    for _ in stqdm(range(100),desc=f"Getting relics for {prime_part}"):
        sleep(0.1)

    new_dataframe=(table.style
                   .map(set_style_for_chance,subset=['Rarity of getting item'])
                   .bar(subset=['Chance of getting item'],color='#C0C0C0'))



    table['Chance of getting item']=table['Chance of getting item']/100

    max_prime_chance=table['Chance of getting item'].max()
    min_prime_chance=table["Chance of getting item"].min()
    st.dataframe(new_dataframe,column_config={
        "Chance of getting item" : st.column_config.ProgressColumn(
            label="Chance of getting item(%)",
            min_value=min_prime_chance-0.01,
            max_value=max_prime_chance+0.01




        )

    },hide_index=True)

    relics=[r for r in relics_to_farm]
    for r in relics:
        relic_data=set_relic_graphs(r)
        if relic_data.empty==False:
            st.subheader("Relics to farm that are not valuted")
            st.write(f'Drop location for {r}')
            max_chance=relic_data['Chance of getting item'].max()
            min_chance=relic_data['Chance of getting item'].min()
            updated_relic_data=((relic_data.style.map(set_style_for_chance,subset=['Rarity of getting item']).
                                format({'Chance of getting item': '{:,.2f}'}))
                                .bar(subset=['Chance of getting item'],color='#C0C0C0'))
            st.dataframe(updated_relic_data,column_config={
                'Chance of getting item':st.column_config.ProgressColumn(
                    "Chance of getting item(%)",
                    min_value=min_chance-1,
                    max_value=max_chance+1,
                    format="%.0f%%"




                )
            },
            hide_index=True
                         )

        if relic_data.empty==True:
            st.text(f"Relic {r} is valuted so there is no chance of farming it")

            counter+=1

    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    if counter==len(relics):

        st.text(f"{prime_part} is not currently available to get as of {year}-{month}-{day}")

    if len(relics)>=1:
        st.text(f"{prime_part} is currently available to get as of {year}-{month}-{day}")




