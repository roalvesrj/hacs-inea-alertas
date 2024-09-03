import requests
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

def fetch_station_data():
    url = "http://alertadecheias.inea.rj.gov.br/dados/piabanha.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    stations = []
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 6:  # Ajuste baseado na estrutura da tabela
            station = {
                "name": cells[0].text.strip(),
                "status_river": cells[1].find('img')['alt'],  # Imagem para texto
                "last_reading": cells[2].text.strip(),
                "monitoring_status": cells[3].text.strip(),
                "rain_1h": cells[4].text.strip(),
                "rain_24h": cells[5].text.strip()
            }
            stations.append(station)
    return stations

class INEASensor(SensorEntity):
    def __init__(self, coordinator, station):
        self.coordinator = coordinator
        self.station = station

    @property
    def name(self):
        return f"INEA {self.station['name']}"

    @property
    def state(self):
        return self.station['status_river']

    @property
    def extra_state_attributes(self):
        return {
            "last_reading": self.station['last_reading'],
            "monitoring_status": self.station['monitoring_status'],
            "rain_1h": self.station['rain_1h'],
            "rain_24h": self.station['rain_24h'],
        }

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="INEA data",
        update_method=fetch_station_data,
        update_interval=timedelta(minutes=30)
    )
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for station in coordinator.data:
        sensors.append(INEASensor(coordinator, station))

    async_add_entities(sensors)
