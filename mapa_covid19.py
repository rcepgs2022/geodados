# Importando bibliotecas necessárias
import pandas as pd

# Importando o conjunto de dados
covid = pd.read_csv(
    filepath_or_buffer = 'https://raw.githubusercontent.com/jonates/opendata/master/covid19_brasil/cases-brazil-cities-20220811.csv',
    sep=',',
    decimal='.'
)

# Fazendo download do conjunto de dados
!wget --verbose --show-progress --no-check-certificate https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/geojs-100-mun.json

# Importando biblioteca necessária
import json

# Abrindo o JSON e guardando em um objeto Python
objeto_geo_cidades = open('/content/geojs-100-mun.json',)

# Lendo o arquivo georreferenciado no formato JSON
geo_uf = json.load(objeto_geo_cidades)

# Verificar a estrutura do json
# geo_uf['features'][1]

# Renomeando o ibgeID para id igual ao do arquivo geoespacial
covid = covid.rename(columns={'ibgeID':'id'})

# transformando o 'id' para tipo object, o mesmo do geoespacial
covid['id'] = covid['id'].astype('str')

# Mostrando o resultado da estrutura
# covid.info()

# Importando biblioteca necessaria
import plotly.express as px

# Criando o mapa
mapa_mortalidade_covid = px.choropleth_mapbox(
    data_frame = covid,
    geojson = geo_uf,
    locations='id',
    featureidkey='properties.id',
    color='deaths_per_100k_inhabitants',
    color_continuous_scale= 'reds',
    range_color=(150, 450),
    mapbox_style='open-street-map',
    zoom=2.5,
    center = {"lat": -17.14, "lon": -57.33},
    opacity=1,
    labels={'deaths_per_100k_inhabitants':'Tx. Mortalidade (/ 100 mil hab.)',
            'id' : 'Código do município'
    },
    width = 1000,
    height = 800,
    title = 'Taxa de Mortalidade por Covid-19, por municípios, 11/08/2022'
)

# Ajustando as margens
mapa_mortalidade_covid.update_layout(margin={'r':0,'t':0,'l':0, 'b':0})

# Reduzindo a largura das bordas dos municípios
mapa_mortalidade_covid.update_traces(marker_line_width=0.01)

# Exibindo o mapa
mapa_mortalidade_covid.show()
