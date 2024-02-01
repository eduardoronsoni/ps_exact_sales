import sqlite3
import random
from datetime import datetime, timedelta, time
import pandas as pd

# Definir uma semente fixa para o gerador de números aleatórios - Fazer com que as pessoas obtenham o mesmo resultado ao rodar este código.
random.seed(1234) 


# Conectar ao banco de dados
conn = sqlite3.connect('./locacoes.db')
cursor = conn.cursor()

# Puxar datas de criação dos filmes
cursor.execute('SELECT ID, DtCriacao FROM FILME')
filmes = cursor.fetchall()

# Puxar IDs dos usuários
cursor.execute('SELECT ID FROM USUARIO')
usuarios = [row[0] for row in cursor.fetchall()]


#Inicialização de uma lista para colocar todas as locações a serem geradas
locacoes = [] 

#Inicializando variável de id para locação
id_locacao = 1 

# Define a data atual
hoje = datetime.now()


#Se são usados todos os filmes, automaticamente são usados todos os gêneros
for filme in filmes: #loop em todos os filmes

    usuario_id = random.choice(usuarios) #fazer distribuição aleatória de usuários para os filmes

    dt_criacao_filme = datetime.strptime(filme[1], '%Y-%m-%d %H:%M:%S') #Coloca a dt_criacao_filme no formato desejado

    # Calcula a diferença máxima (em dias) entre a data de criação do filme e o dia atual
    diferenca_dias_max = (hoje - dt_criacao_filme).days
    # Escolhe um número aleatório de dias, limitado pela diferença máxima
    dias_para_adicionar = random.randint(0, diferenca_dias_max)
    # Calcula a data de locação
    data_locacao = hoje - timedelta(days=dias_para_adicionar)
    # Garantir que a data de locação não seja anterior à data de criação do filme
    data_locacao = max(data_locacao, dt_criacao_filme)

    locacoes.append((id_locacao,usuario_id, filme[0], data_locacao)) #estou colocando filme[0] porque no meu caso o id do filme é igual ao filmelocacaoid

    id_locacao += 1

#Query para inserção de dados no banco
sql_insert = '''
    INSERT INTO LOCACAO (ID,UsuarioID, FilmeLocacaoID, DtLocacao)
    VALUES (?, ?, ?, ?)
'''

#fazendo loop sobre a lista e inserindo os dados
for locacao in locacoes:

    # Rodando a query de insert na tabela locacao
    cursor.execute(sql_insert, locacao)

    #commitando para o banco
    conn.commit()

#Fechando a conexão
cursor.close()
conn.close()