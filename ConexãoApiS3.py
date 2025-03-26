import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound

# Função para obter dados de uma API
def get_jsonplaceholder_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_openweathermap():
    api_key = "bac9e9473dec7852929ad5e053ed258a"  # Substitua pela sua chave real
    city = "London"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter dados do OpenWeatherMap: {response.status_code}")
        return None  

def get_ibge_data():
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/7392/periodos/2014/variaveis/10484?localidades=N1[all]"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Função para salvar dados no arquivo JSON
def save_to_json_file(data, filename):
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    return False

# Função para fazer upload de um arquivo para o AWS S3 (com o caminho arquivos/)
def upload_to_s3(file_name, bucket_name, s3_path, profile_name="default"):
    try:
        session = boto3.Session(profile_name=profile_name)
        s3_client = session.client('s3')

        s3_client.upload_file(file_name, bucket_name, s3_path)
        print(f"Arquivo {file_name} enviado com sucesso para {s3_path} no S3.")
    except FileNotFoundError:
        print(f"Arquivo {file_name} não encontrado.")
    except NoCredentialsError:
        print("Credenciais da AWS não encontradas. Configure com 'aws configure'.")
    except ProfileNotFound:
        print(f"O perfil '{profile_name}' não foi encontrado. Verifique 'aws configure'.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Obter dados das APIs
users_data = get_jsonplaceholder_users()
weathermap_data = get_openweathermap()
ibge_data = get_ibge_data()

# Salvar dados localmente em arquivos JSON
if save_to_json_file(users_data, 'jsonplaceholder_users.json'):
    upload_to_s3('jsonplaceholder_users.json', 'dprsbucket', 'basesapi/jsonplaceholder_users.json', profile_name="dprs")

if save_to_json_file(weathermap_data, 'openweathermap.json'):
    upload_to_s3('openweathermap.json', 'dprsbucket', 'basesapi/openweathermap.json', profile_name="dprs")

if save_to_json_file(ibge_data, 'ibge_residente.json'):
    upload_to_s3('ibge_residente.json', 'dprsbucket', 'basesapi/ibge_residente.json', profile_name="dprs")

# Teste para validar/visualizar as base
# Visualizar os arquivos no S3: 
# ------- aws s3 ls s3://dprsbucket/basesapi/
# Visualizar o formato do arquivo: 
# ------- aws s3 cp s3://dprsbucket/basesapi/ibge_residente.json - | Select -First 20