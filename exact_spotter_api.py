import requests
import json
import pandas as pd
import numpy as np
from pandas import json_normalize

url_base = 'https://api.exactspotter.com/v3'
token = 'e4b1da77-06aa-4777-a594-cc5bb6e549c4'


headers = {
  'Content-Type': 'application/json',
  'token_exact': token
}

#Fazendo a consulta no endpoint Histórico de Qualificações - Listagem
response = requests.get(f'{url_base}/QualificationHistories', headers=headers)

#Jogando a response recebida em um dataframe para melhor visualização
df =  pd.DataFrame(response.json()['value'])

#Desaninhando a coluna user action, que mostra o funcionário responsável pela ação de qualificação, e separando em um df auxiliar. Depois, concateno esse df com o original
df_aux = pd.concat([json_normalize(x) for x in df['userAction']], ignore_index=True)
df  = pd.concat([df.drop('userAction', axis=1), df_aux], axis=1) 

#Tratando algumas colunas - unindo nome e sobrenome de usuário, tratando meetingDate nulo
df['user_full_name'] = df['name'] + ' ' + df['lastName']
df.rename(columns={
    'id': 'user_id', 
    'name': 'user_name', 
    'email': 'user_email'
}, inplace=True)

df['meetingDate'] = df['meetingDate'].replace("0001-01-01T00:00:00Z", np.nan)


#Dropando colunas não necessárias
colunas_de_interresse = ['leadId',
                    'stageId',
                    'stage',
                    'funnelId',
                    'score',
                    'qualificationDate',
                    'meetingDate',
                    'user_id',
                    'user_full_name',
                    'user_email',
]

df = df[colunas_de_interresse]
#Mudando tipos de dados para não precisar mudar no Power BI

#IDs são categorias, não números
df['leadId'] = df['leadId'].astype(str)
df['stageId'] = df['stageId'].astype(str)
df['funnelId'] = df['funnelId'].astype(str)

df['qualificationDate'] = pd.to_datetime(df['qualificationDate'], utc=True)
df['meetingDate'] = pd.to_datetime(df['meetingDate'], utc=True)


#Jogando para um csv (sem coluna de índice) que será importado via PowerBI
df.to_csv('dados_api.csv', index=False)