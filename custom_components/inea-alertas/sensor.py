import requests
from bs4 import BeautifulSoup
import logging

_LOGGER = logging.getLogger(__name__)

def fetch_station_data():
    url = "http://alertadecheias.inea.rj.gov.br/dados/piabanha.php"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"Erro ao acessar a URL: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    _LOGGER.info("HTML carregado com sucesso.")
    
    stations = []
    rows = soup.find_all('tr')
    
    _LOGGER.info(f"Número de linhas encontradas na tabela: {len(rows)}")
    
    for i, row in enumerate(rows):
        if 'fltrow' in row.get('class', []):
            continue

        cells = row.find_all('td')
        if len(cells) >= 6:
            img_tag = cells[3].find('img')
            # Mapeando o src da imagem para um status textual
            if img_tag and 'src' in img_tag.attrs:
                img_src = img_tag['src']
                if 'estavel' in img_src:
                    status_rio = 'Estável'
                elif 'subindo' in img_src:
                    status_rio = 'Subindo'
                elif 'descendo' in img_src:
                    status_rio = 'Descendo'
                else:
                    status_rio = 'Desconhecido'
            else:
                status_rio = 'N/A'
            
            station = {
                "municipio": cells[0].text.strip(),
                "curso_agua": cells[1].text.strip(),
                "nome_estacao": cells[2].text.strip(),
                "status_rio": status_rio,
                "ultima_leitura": cells[4].text.strip(),
                "status_monitoramento": cells[5].text.strip(),
                "chuva_ultimo": cells[6].text.strip() if len(cells) > 6 else 'N/A',
                "chuva_1h": cells[7].text.strip() if len(cells) > 7 else 'N/A',
                "chuva_24h": cells[9].text.strip() if len(cells) > 9 else 'N/A',
                "nivel_rio_ultimo": cells[12].get_text(strip=True) if len(cells) > 12 else 'N/A',
                "nivel_rio_45min": cells[15].get_text(strip=True) if len(cells) > 15 else 'N/A'
            }
            _LOGGER.info(f"Dados da estação encontrados: {station}")
            stations.append(station)
    
    if not stations:
        _LOGGER.warning("Nenhuma estação foi encontrada.")
    
    return stations
