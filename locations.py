import os
import jsonpickle
from objects import *

base_path = os.path.dirname(os.path.abspath(__file__)) 

def download_locations():
    import options
    import requests

    paises = []
    for p,pv, in options.paises.items():
        print(p)

        pais = Pais()
        pais.id = pv
        pais.nome = p
        
        distritos = []

        if p == "Portugal":
            for d, dv in options.distritos.items():

                distrito = Distrito()
                distrito.id = dv
                distrito.nome = d
                
                r = requests.post("http://www.base.gov.pt/templates/main_base/objects/ajax.php", data={'query': "/lista/concelhos?distrito=" + str(dv)})
                data = r.json()

                concelhos = []

                for c in data['items']:
                    concelho = Concelho()
                    concelho.id = c['id']
                    concelho.nome = c['description']
                    concelhos.append(concelho)

                distrito.concelhos = concelhos
                distritos.append(distrito)

        else:
            distrito = Distrito()
            distrito.id = 0
            distrito.nome = "Todos"
            concelho = Concelho()
            concelho.id = 0
            concelho.nome = "Todos"
            distrito.concelhos = [concelho]
            distritos.append(distrito)

        pais.distritos = distritos
        paises.append(pais)

    locations = Locations()
    locations.paises = paises

    with open(os.path.join(base_path, "locations.json"), 'w') as outf:
        outf.write(jsonpickle.encode(locations))


def load_locations():
    with open(os.path.join(base_path, "locations.json"), 'r') as inf:
        json = inf.read()
        return jsonpickle.decode(json)