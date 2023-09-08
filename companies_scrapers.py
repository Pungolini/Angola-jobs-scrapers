#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

AVAILABLE_COMPANIES = {

    "AZULE ENERGY": {
        "url": "https://careers.azule-energy.com/search"
    }
}

# URLs of the webpages containing the jobs table
AZULE_URL = 'https://careers.azule-energy.com/search/'
SBA_URL = "https://www.standardbank.com/sbg/standard-bank-group/careers/apply/jobs/view-all-jobs"


def get_jobs_Azule(url = AZULE_URL,verbose = False):

    resposta = requests.get(url)

    # Enviar um pedido HTTP GET para o endereço URL da página

    if resposta.status_code != 200:
        print('[HTTP GET] Erro ao fazer o pedido para a página')
        exit()

    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(resposta.content, 'html.parser')
    

    try:
        # Encontrar primeiro a tabela com ID definido
        tabela_div = soup.find('table', id='searchresults')

        # Encontrar o corpo da tabela
        tabela_body = tabela_div.find('tbody')
    except AttributeError:
        vaga = {
            'Título': None,
            'Localização': None,
            'Departamento': None,
            'Link': None
        }
        return pd.DataFrame.from_dict(dict())

    # Inicializar uma lista para armazenar os detalhes das vagas
    detalhes_vagas = []

    # Percorrer cada linha no corpo da tabela
    for row in tabela_body.find_all('tr', class_='data-row'):
        # Encontrar o link e título da vaga
        titulo = row.find('a', class_='jobTitle-link')
        link_vaga = f"https://careers.azule-energy.com{titulo['href']}"
        titulo_vaga = titulo.text.strip()

        
        # Encontrar a localização da vaga
        localizacao_vaga = row.find('span', class_='jobLocation').text.strip()
        
        # Encontrar o departamento da vaga
        departamento_vaga = row.find('span', class_='jobDepartment').text.strip()
        
        # Criar um dicionário para os detalhes da vaga
        vaga = {
            'Título': titulo_vaga,
            'Localização': localizacao_vaga,
            'Departamento': departamento_vaga,
            'Link': link_vaga
        }
        
        # Adicionar os detalhes da vaga à lista
        detalhes_vagas.append(vaga)

    # Converter dicionario em DataFrame
    vagas_df = pd.DataFrame.from_dict(detalhes_vagas)

    # Mostrar os detalhes das vagas, caso o usuario queira

    if verbose:
        for idx, vaga in enumerate(detalhes_vagas, start=1):
            print(f"Vaga {idx}:")
            print(f"Título: {vaga['Título']}")
            print(f"Localização: {vaga['Localização']}")
            print(f"Departamento: {vaga['Departamento']}")
            print("=" * 40)

    return vagas_df

# ==================== STANDARD BANK ANGOLA ========================
# Extract job details
def extract_job_details(job_card):
    job_details = {}
    
    # # Extract posting_date
    # posting_date_element = job_card.find('span', class_='career-search-component__item--date')
    # job_details['posting_date'] = posting_date_element.get_text(strip=True) if posting_date_element else None
    
    # # Extract title
    # title_element = job_card.find('h4', class_='title')
    # job_details['title'] = title_element.get_text(strip=True) if title_element else None
    
    # Extract meta segments
    meta_segments = job_card.find_all('span', class_='career-search-component__item--meta__segment')
    for segment in meta_segments:
        key_element = segment.find('strong')
        key = key_element.get_text(strip=True).rstrip(':') if key_element else None
        value = segment.get_text(strip=True).replace(f"{key}:", '').strip() if key else None
        if key:
            job_details[key] = value
    
    # Extract link
    job_details['link'] = job_card['href']
    
    return job_details

    
def scrape_job_postings():
    # Fetch the web page
    response = requests.get(SBA_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract job listings
    job_listings_div = soup.find('div', class_='career-search-component__content--items')
    job_cards = [child for child in job_listings_div.children if child.name]

    print(f"{len(job_cards)} job cards")

    extracted_jobs = [extract_job_details(job_card) for job_card in job_cards if job_card.name == 'a']
    return extracted_jobs