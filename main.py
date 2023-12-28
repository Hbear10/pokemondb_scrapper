from bs4 import BeautifulSoup
import requests
import os

page_to_scrape = requests.get("https://pokemondb.net/pokedex/national")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
names = soup.findAll("a", attrs={"class": "ent-name"})
pokemon = [name.text for name in names]
for i in pokemon:
    new = i.replace("♀", "-f").replace("♂", "-m")
    ind = pokemon.index(i)
    pokemon[ind] = new


def scrap_pokemon(start, end):
    x = ""
    for i in range(start, end):
        name = pokemon[i]
        apostraphe = "\'"
        page_to_scrape = requests.get(f"https://pokemondb.net/pokedex/{name.lower().replace('. ', '-').replace('.', '').replace(' ', '-').replace('é', 'e').replace(':', '').replace(apostraphe, '')}")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        pokename = name
        numbers = soup.find("strong")
        generation = soup.find("abbr")
        types = soup.findAll("a", {"class": "type-icon"})
        species = soup.findAll("td")
        height = soup.findAll("td")
        length_to_get_height = height[3].text.index(".") + 2
        weight = soup.findAll("td")
        length_to_get_weight = weight[4].text.index(".") + 2
        abilitiey1 = str(soup.findAll("span", {"class": "text-muted"})[0])[
                     46:str(soup.findAll("span", {"class": "text-muted"})[0])[46:].index("\"") + 46]

        two_ab = False
        text = str(soup.findAll("small"))
        if text.find("ability") != -1:
            hidden_ab = True
            if len((soup.findAll("span", {"class": "text-muted"}))) > 1:
                if "ability" in soup.findAll("span", {"class": "text-muted"}):
                    two_ab = True
                else:
                    two_ab = False
            else:
                two_ab = False
        else:
            hidden_ab = False

        if two_ab:
            abilitiey1 += ("~" + (str(soup.findAll("span", {"class": "text-muted"})[1])[
                                  46:str(soup.findAll("span", {"class": "text-muted"})[1])[46:].index("\"") + 46]))

        if hidden_ab:
            hdabtext = str(soup.findAll("small")[0])[44:str(soup.findAll("small")[0])[44:].index("\"") + 44]
        else:
            hdabtext = ""

        stats = soup.findAll("td", {"class": "cell-num"})
        hp = stats[0].text
        attack = stats[3].text
        defence = stats[6].text
        spattack = stats[9].text
        spdefence = stats[12].text
        speed = stats[15].text

        x += f"{pokename},{numbers.text},{generation.text[-1]},{types[0].text},{types[1].text if types[1].text != 'Nor' else ''}\
,{species[2].text},{height[3].text[:length_to_get_height]},{weight[4].text[:length_to_get_weight]},{abilitiey1},\
{hdabtext},{hp},{attack},{defence},{spattack},{spdefence},{speed}\n"

    return x


#kanto = scrap_pokemon(0, 151)

#with open("pokemon.txt", "w", encoding="windows-1252") as file:
 #   file.write(kanto)


def img_scrape(start,end):
    for i in range(start,end):
        name = pokemon[i]
        apostraphe = "'"
        page = requests.get(f"https://img.pokemondb.net/sprites/home/normal/{name.lower().replace('. ', '-').replace('.', '').replace(' ', '-').replace('é', 'e').replace(':', '').replace(apostraphe, '')}.png")

        soup=BeautifulSoup(page.text,"html.parser")

        images = soup.find("img")
        print(images)

        name = name.lower()
        link = f"https://img.pokemondb.net/sprites/home/normal/{name.lower().replace('. ', '-').replace('.', '').replace(' ', '-').replace('é', 'e').replace(':', '').replace(apostraphe, '')}"
        print(name,link)
        with open(name+".png","wb") as file:
            im = requests.get(link)
            file.write(link.content)
#img_scrape(0,1)
