from flask import Flask, render_template
import urllib.request
import json



app = Flask (__name__)

@app.route("/") # rota de  URL raiz
def get_list_characters_page():
    url = "https://rickandmortyapi.com/api/character";
    response = urllib.request.urlopen(url) # envia a req e recebe a res
    data = response.read(); # leitura dos dados vindos da api
    dict = json.loads(data); # transforma esses dados em json p/ python
    
    return render_template("personagens.html", characters = dict["results"])


@app.route("/profile/<id>") # obter um personagem
def get_profile(id):
    url = "https://rickandmortyapi.com/api/character/"+id;
    response = urllib.request.urlopen(url) 
    data = response.read(); 
    character_data = json.loads(data);

    list_info_episode = []

    # Iterar sobre as três páginas de episódios
    for page_number in range(1, 4):
        url = f"https://rickandmortyapi.com/api/episode?page={page_number}"
        response = urllib.request.urlopen(url) 
        data = response.read()
        episodes_dict = json.loads(data)
        episodes_results = episodes_dict["results"]
        
        # Iterar sobre os resultados e extrair as informações desejadas
        for episode_data in episodes_results:
            episode_info = {
                "id": episode_data["id"],
                "name": episode_data["name"],
                "episode": episode_data["episode"]
            }
            list_info_episode.append(episode_info)
            
    #Lista episodios que o personagem aparece
    list_episodes_profile = [episode.split("/")[-1] for episode in character_data['episode']]
    
  
    # Lista com episodios que o personagem aparece formatada 
    episodes_appeared = []
    
    # Filtrar os episódios em que o personagem aparece
    for episode_info in list_info_episode:
        if str (episode_info["id"]) in list_episodes_profile:
            episodes_appeared.append(episode_info)

  
    # pega o id da localização do personagem 
    location_id= character_data["location"]["url"].split("/")[-1]
    
    #validação caso personagem não aparecer em um epsodio
    if not episodes_appeared:
        error_message = "Não foram encontrados episódios para este personagem."
        return render_template("profile.html", profile=character_data, error_message=error_message, location_id=location_id)

    return render_template("profile.html", profile=character_data, location_id=location_id,episodes_appeared=episodes_appeared)


@app.route("/locations") # rota de locations
def get_list_locations_page():
    url = "https://rickandmortyapi.com/api/location";
    response = urllib.request.urlopen(url) # envia a req e recebe a res
    data = response.read(); # leitura dos dados vindos da api
    dict = json.loads(data); # transforma esses dados em json p/ python
    
    return render_template("locations.html", locations = dict["results"]);
   
     
@app.route("/listalocations") # rota da lista de localizações
def get_locations():
    url = "https://rickandmortyapi.com/api/location";
    response = urllib.request.urlopen(url) # envia a req e recebe a res
    data = response.read(); # leitura dos dados vindos da api
    dict = json.loads(data); # transforma esses dados em json p/ python
    
    locations = [];
    
    for location in dict["results"]:
        location = {
            "id":location["id"],
            "name":location["name"],
            "type":location["type"],
            "dimension":location["dimension"],
        }
        
        locations.append(location);
    
    return {"locations":locations}

@app.route("/location/<id>") # obter uma location
def get_location(id):
    url = f"https://rickandmortyapi.com/api/location/{id}"
    response = urllib.request.urlopen(url) 
    data = response.read(); 
    location_dict = json.loads(data);
    list_ids = [];
    character_names = [];
    
    for resident in location_dict["residents"]:
        resident_id = resident.split("/")[-1]
        list_ids.append(resident_id);
        
        # Consulta o nome do personagem pelo id e armazena na lista
        character_url = f"https://rickandmortyapi.com/api/character/{resident_id}"
        character_response = urllib.request.urlopen(character_url)
        character_data = character_response.read()
        character_dict = json.loads(character_data)
        character_names.append(character_dict["name"])
        
    residents_info = list(zip(list_ids, character_names))
        
    return render_template("location.html", location=location_dict, residents_info = residents_info);

# paginação de episodios
EPISODES_PER_PAGE = 20

@app.route('/episodes/page/<int:page_number>')
def episodes(page_number):
    try:
        url = f"https://rickandmortyapi.com/api/episode?page={page_number}"
        response = urllib.request.urlopen(url)
        data = response.read()
        episodes_data = json.loads(data)

        episodes = []
        for episode in episodes_data["results"]:
            episode_info = {
                "id": episode["id"],
                "name": episode["name"],
                "air_date": episode["air_date"],
                "episode": episode["episode"]
            }
            episodes.append(episode_info)

        total_episodes = len(episodes_data["results"])
        num_pages = total_episodes // EPISODES_PER_PAGE + 1 

        return render_template("episodes.html", episodes=episodes, num_pages=num_pages, current_page=page_number)

    except Exception as e:
        return f"Erro ao consultar dados: {str(e)}"

# Listar Episodios
@app.route("/episodes")
def get_list_episodes():
    try:
        url = "https://rickandmortyapi.com/api/episode";
        response = urllib.request.urlopen(url) 
        data = response.read();
        episodes_dict = json.loads(data); 
    
        episodes = [];
    
        for episode in episodes_dict["results"]:
            episode = {
                "id":episode["id"],
                "name":episode["name"],
                "air_date":episode["air_date"],
                "episode":episode["episode"]
            }
            episodes.append(episode);
        
        return render_template("episodes.html", episodes=episodes);
    
    except Exception as e:
        return f"Erro ao consultar dados: {str(e)}"
    
@app.route("/episode/<id>")
def get_episode(id):
    try:
        url = f"https://rickandmortyapi.com/api/episode/{id}"
        response = urllib.request.urlopen(url) 
        data = response.read(); 
        episode_dict = json.loads(data)
        list_ids_characters = []
        character_names = []

        for character in episode_dict["characters"]:
            character_id = character.split("/")[-1]
            list_ids_characters.append(character_id)

            # Consulta o nome do personagem pelo id e armazena na lista
            character_url = f"https://rickandmortyapi.com/api/character/{character_id}"
            character_response = urllib.request.urlopen(character_url)
            character_data = character_response.read()
            character_dict = json.loads(character_data)
            character_names.append(character_dict["name"])

        # Combine as duas listas em uma lista de tuplas
        character_info = list(zip(character_names, list_ids_characters))

        return render_template("episode.html", episode=episode_dict, character_info=character_info)
    except Exception as e:
        return f"Erro ao consultar dados: {str(e)}"