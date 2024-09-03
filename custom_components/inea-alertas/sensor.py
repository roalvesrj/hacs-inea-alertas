import logging
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

def fetch_station_data():
    url = "http://alertadecheias.inea.rj.gov.br/dados/piabanha.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    stations = []
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 6:
            station = {
                "name": cells[0].text.strip(),
                "status_river": cells[1].find('img')['alt'],  # Capturando o texto da imagem
                "last_reading": cells[2].text.strip(),
                "monitoring_status": cells[3].text.strip(),
                "rain_1h": cells[4].text.strip(),
                "rain_24h": cells[5].text.strip()
            }
            _LOGGER.debug(f"Fetched data for station: {station}")
            stations.append(station)
    
    if not stations:
        _LOGGER.warning("No stations data found on INEA page.")
    
    return stations

async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info("Setting up INEA Alertas de Cheias integration...")
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="INEA data",
        update_method=fetch_station_data,
        update_interval=timedelta(minutes=30),
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    if coordinator.data is None:
        _LOGGER.warning("No data fetched from INEA, no sensors will be added.")
        return

    sensors = []
    for station in coordinator.data:
        sensors.append(INEASensor(coordinator, station))
        _LOGGER.info(f"Sensor added for station: {station['name']}")
    
    async_add_entities(sensors)
