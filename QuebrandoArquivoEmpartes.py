import pandas as pd
import math
import os

# Nome do arquivo CSV original (ajuste conforme seu nome real)
nome_arquivo = 'seu_arquivo.csv'

# Pega o caminho da área de trabalho do usuário
area_de_trabalho = os.path.join(os.path.expanduser("~"), 'Desktop')

# Define o caminho da pasta base do projeto
base_dir = os.path.join(area_de_trabalho, 'ProjetosPython')

# Define os caminhos das subpastas
pasta_origem = os.path.join(base_dir, 'Arquivos_Original')
pasta_destino = os.path.join(base_dir, 'Arquivos_Resultado')

# Cria as pastas, se ainda não existirem
os.makedirs(pasta_origem, exist_ok=True)
os.makedirs(pasta_destino, exist_ok=True)

# Caminho completo do arquivo original
caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)

# Verifica se o arquivo existe
if not os.path.exists(caminho_arquivo):
    print(f'⚠️ Arquivo CSV não encontrado em: {caminho_arquivo}')
    print('➡️ Coloque seu arquivo CSV dentro da pasta "Arquivos_Original" na Área de Trabalho e execute novamente.')
    exit()

# Tenta ler o arquivo
try:
    df = pd.read_csv(caminho_arquivo)
except Exception as e:
    print(f'❌ Erro ao ler o arquivo: {e}')
    exit()

# Divide em blocos de 1000 linhas (mantendo o cabeçalho)
linhas_por_arquivo = 1000
total_arquivos = math.ceil(len(df) / linhas_por_arquivo)

for i in range(total_arquivos):
    inicio = i * linhas_por_arquivo
    fim = inicio + linhas_por_arquivo
    df_parte = df.iloc[inicio:fim]

    nome_saida = f'parte_{i+1}.csv'
    caminho_saida = os.path.join(pasta_destino, nome_saida)

    df_parte.to_csv(caminho_saida, index=False, header=True)
    print(f'✅ Arquivo salvo: {nome_saida}')

print(f'\n🎉 Total de {total_arquivos} arquivos criados com sucesso em:\n{pasta_destino}')
