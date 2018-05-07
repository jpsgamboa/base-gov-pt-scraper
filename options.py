from objects import *

tipos_procedimento = {
    'Todos': 0,
    'Ajuste direto': 1,
    'Consulta Prévia': 8,
    'Concurso público': 2,
    'Concurso limitado por prévia qualificação': 3,
    'Procedimento de negociação': 4,
    'Diálogo concorrencial': 5,
    'Ao abrigo de acordo-quadro (art.º 258.º)': 6,
    'Ao abrigo de acordo-quadro (art.º 259.º)': 7,
    'Parceria para a inovação': 9,
    'Disponibilização de bens móveis': 10,
    'Serviços sociais e outros serviços específicos': 11,
}

def load_tipos_procedimento():
    tipos = []
    
    for k,v in tipos_procedimento.items():
        t = TipoProcedimento()
        t.id = v 
        t.nome = k
        tipos.append(t)

    return tipos

tipos_contrato = {
    'Todos': 0,
    'Aquisição de bens móveis': 1,
    'Aquisição de serviços': 2,
    'Concessão de obras públicas': 3,
    'Concessão de serviços públicos': 4,
    'Empreitadas de obras públicas': 5,
    'Locação de bens móveis': 6,
    'Sociedade': 7,
    'Outros': 8,
}

def load_tipos_contrato():
    tipos = []
    
    for k,v in tipos_contrato.items():
        t = TipoContrato()
        t.id = v 
        t.nome = k
        tipos.append(t)

    return tipos

paises = {
    'Todos': 0,
    'Afeganistão': 1,
    'África do Sul': 2,
    'Albânia': 3,
    'Alemanha': 4,
    'Andorra': 5,
    'Angola': 6,
    'Anguila': 7,
    'Antárctica': 8,
    'Antígua e Barbuda': 9,
    'Antilhas Holandesas': 10,
    'Arábia Saudita': 11,
    'Argélia': 12,
    'Argentina': 13,
    'Arménia': 14,
    'Aruba': 15,
    'Ascensão': 16,
    'Austrália': 17,
    'Áustria': 18,
    'Azerbaijão': 19,
    'Bahamas': 20,
    'Bangladesh': 21,
    'Barbados': 22,
    'Barém': 23,
    'Bélgica': 24,
    'Belize': 25,
    'Benim': 26,
    'Bermudas': 27,
    'Bielorrússia': 28,
    'Bolívia': 29,
    'Bósnia-Herzegovina': 30,
    'Botswana': 31,
    'Brasil': 32,
    'Brunei Darussalam': 33,
    'Bulgária': 34,
    'Burkina Faso': 35,
    'Burundi': 36,
    'Butão': 37,
    'Cabo Verde': 38,
    'Camarões': 39,
    'Camboja': 40,
    'Canadá': 41,
    'Catar': 42,
    'Cazaquistão': 43,
    'Centro-Africana (República)': 44,
    'Chade': 45,
    'Chile': 46,
    'China': 47,
    'Chipre': 48,
    'Colômbia': 49,
    'Comores': 50,
    'Congo': 51,
    'Congo (República Democrática do)': 52,
    'Coreia (República da)': 53,
    'Coreia (República Popular Democrática da)': 54,
    'Costa do Marfim': 55,
    'Costa Rica': 56,
    'Croácia': 57,
    'Cuba': 58,
    'Dinamarca': 59,
    'Domínica': 60,
    'Egipto': 61,
    'El Salvador': 62,
    'Emiratos Árabes Unidos': 63,
    'Equador': 64,
    'Eritreia': 65,
    'Eslováquia': 66,
    'Eslovénia': 67,
    'Espanha': 68,
    'Estados Unidos': 69,
    'Estónia': 70,
    'Etiópia': 71,
    'Filipinas': 72,
    'Finlândia': 73,
    'França': 74,
    'Gabão': 75,
    'Gâmbia': 76,
    'Gana': 77,
    'Geórgia': 78,
    'Geórgia do Sul e Ilhas Sandwich': 79,
    'Gibraltar': 80,
    'Granada': 81,
    'Grécia': 82,
    'Gronelândia': 83,
    'Guadalupe': 84,
    'Guam': 85,
    'Guatemala': 86,
    'Guernsey': 87,
    'Guiana': 88,
    'Guiana Francesa': 89,
    'Guiné': 90,
    'Guiné Equatorial': 91,
    'Guiné-Bissau': 92,
    'Haiti': 93,
    'Honduras': 94,
    'Hong Kong': 95,
    'Hungria': 96,
    'Iémen': 97,
    'Ilha Bouvet': 98,
    'Ilha Christmas': 99,
    'Ilha de Man': 100,
    'Ilha Heard e Ilhas Mcdonald': 101,
    'Ilha Norfolk': 102,
    'Ilhas Aland': 103,
    'Ilhas Caimão': 104,
    'Ilhas Cocos (Keeling)': 105,
    'Ilhas Cook': 106,
    'Ilhas Falkland (Malvinas)': 107,
    'Ilhas Faroé': 108,
    'Ilhas Fiji': 109,
    'Ilhas Marianas do Norte': 110,
    'Ilhas Marshall': 111,
    'Ilhas Menores Distantes dos Estados Unidos': 112,
    'Ilhas Salomão': 113,
    'Ilhas Turcas e Caicos': 114,
    'Ilhas Virgens (Britânicas)': 115,
    'Ilhas Virgens (Estados Unidos)': 116,
    'Índia': 117,
    'Indonésia': 118,
    'Irão (República Islâmica)': 119,
    'Iraque': 120,
    'Irlanda': 121,
    'Islândia': 122,
    'Israel': 123,
    'Itália': 124,
    'Jamaica': 125,
    'Japão': 126,
    'Jersey': 127,
    'Jibuti': 128,
    'Jordânia': 129,
    'Jugoslávia': 130,
    'Kiribati': 131,
    'Kosovo': 132,
    'Kuwait': 133,
    'Laos (República Popular Democrática do)': 134,
    'Lesoto': 135,
    'Letónia': 136,
    'Líbano': 137,
    'Libéria': 138,
    'Líbia (Jamahiriya Árabe da)': 139,
    'Liechtenstein': 140,
    'Lituânia': 141,
    'Luxemburgo': 142,
    'Macau': 143,
    'Macedónia (Antiga República Jugoslava da)': 144,
    'Madagáscar': 145,
    'Malásia': 146,
    'Malawi': 147,
    'Maldivas': 148,
    'Mali': 149,
    'Malta': 150,
    'Marrocos': 151,
    'Martinica': 152,
    'Maurícias': 153,
    'Mauritânia': 154,
    'Mayotte': 155,
    'México': 156,
    'Micronésia (Estados Federados da)': 157,
    'Moçambique': 158,
    'Moldova': 159,
    'Mónaco': 160,
    'Mongólia': 161,
    'Monserrate': 162,
    'Montenegro': 163,
    'Myanmar': 164,
    'Namíbia': 165,
    'Nauru': 166,
    'Nepal': 167,
    'Nicarágua': 168,
    'Niger': 169,
    'Nigéria': 170,
    'Niue': 171,
    'Noruega': 172,
    'Nova Caledónia': 173,
    'Nova Zelândia': 174,
    'Omã': 175,
    'Países Baixos': 176,
    'Palau': 177,
    'Panamá': 178,
    'Papuásia-Nova Guiné': 179,
    'Paquistão': 180,
    'Paraguai': 181,
    'Peru': 182,
    'Pitcairn': 183,
    'Polinésia Francesa': 184,
    'Polónia': 185,
    'Porto Rico': 186,
    'Portugal': 187,
    'Quénia': 188,
    'Quirguizistão': 189,
    'Reino Unido': 190,
    'República Checa': 191,
    'República Dominicana': 192,
    'Reunião': 193,
    'Roménia': 194,
    'Ruanda': 195,
    'Rússia (Federação da)': 196,
    'Samoa': 197,
    'Samoa Americana': 198,
    'Santa Helena': 199,
    'Santa Helena': 200,
    'Santa Lúcia': 201,
    'Santa Sé (Cidade Estado do Vaticano)': 202,
    'São Bartolomeu': 203,
    'São Cristóvão e Nevis': 204,
    'São Marino': 205,
    'São Martinho (parte francesa)': 206,
    'São Pedro e Miquelon': 207,
    'São Tomé e Príncipe': 208,
    'São Vicente e Granadinas': 209,
    'Sara Ocidental': 210,
    'Sem nacionalid.': 211,
    'Senegal': 212,
    'Serra Leoa': 213,
    'Sérvia': 214,
    'Servia Monteneg': 215,
    'Seychelles': 216,
    'Singapura': 217,
    'Síria (República Árabe da)': 218,
    'Somália': 219,
    'Sri Lanka': 220,
    'Suazilândia': 221,
    'Sudão': 222,
    'Suécia': 223,
    'Suiça': 224,
    'Suriname': 225,
    'Svalbard e a Ilha de Jan Mayen': 226,
    'Tailândia': 227,
    'Taiwan (Província da China)': 228,
    'Tajiquistão': 229,
    'Tanzânia': 230,
    'Território Britânico do Oceano Índico': 231,
    'Território Palestiniano Ocupado': 232,
    'Territórios Franceses do Sul': 233,
    'Timor Leste': 234,
    'Timor': 235,
    'Togo': 236,
    'Tokelau': 237,
    'Tonga': 238,
    'Trindade e Tobago': 239,
    'Tristão Cunha': 240,
    'Tunísia': 241,
    'Turquemenistão': 242,
    'Turquia': 243,
    'Tuvalu': 244,
    'Ucrânia': 245,
    'Uganda': 246,
    'Uruguai': 247,
    'Usbequistão': 248,
    'Vanuatu': 249,
    'Venezuela': 250,
    'Vietname': 251,
    'Wallis e Futuna (Ilhas)': 252,
    'Zaire': 253,
    'Zâmbia': 254,
    'Zimbabwe': 255
}

distritos = {
    'Todos': 0,
    'Aveiro': 2,
    'Beja': 3,
    'Braga': 4,
    'Braganca': 5,
    'Castelo Branco': 6,
    'Coimbra': 7,
    'Évora': 8,
    'Faro': 9,
    'Guarda': 10,
    'Leiria': 11,
    'Lisboa': 12,
    'Portalegre': 13,
    'Porto': 14,
    'Santarém': 15,
    'Setúbal': 16,
    'Viana do Castelo': 17,
    'Vila Real': 18,
    'Viseu': 19,
    'Região Autónoma dos Açores': 20,
    'Região Autónoma da Madeira': 21,
    'Portugal Continental': 22,
    'Distrito não determinado': 23,
    'Consulado situados no estrangeiro': 24
}
