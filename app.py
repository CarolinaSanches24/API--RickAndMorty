from flask import Flask, render_template
import urllib.request, json

app = Flask (__name__)

@app.route("/") # rota de  URL raiz
def get_list_characters_page():
    url = "https://rickandmortyapi.com/api/character";
    response = urllib.request.urlopen(url) # envia a req e recebe a res
    data = response.read(); # leitura dos dados vindos da api
    dict = json.loads(data); # transforma esses dados em json p/ python
    
    return render_template("personagens.html", characters = dict["results"])

@app.route("/lista")

def get_list_characters():
    url = "https://rickandmortyapi.com/api/character";
    response = urllib.request.urlopen(url)
    characters = response.read();
    dict = json.loads(characters);
    
    characters = []
    
    for character in dict["results"]:
        character = {
            "name":character["name"],
            "status":character["status"]
        }
        
        characters.append(character);
    return {"characters":characters}
    