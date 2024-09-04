from homeassistant.helpers.entity import Entity

def setup_platform(hass, config, add_entities, discovery_info=None):
    # Chame a função que busca os dados
    stations = fetch_station_data()
    
    # Crie uma lista de entidades com base nos dados das estações
    entities = []
    for station in stations:
        entity = INEACheiasSensor(
            station["municipio"],
            station["curso_agua"],
            station["nome_estacao"],
            station["status_rio"],
            station["ultima_leitura"],
            station["status_monitoramento"],
            station["chuva_ultimo"],
            station["chuva_1h"],
            station["chuva_24h"],
            station["nivel_rio_ultimo"],
            station["nivel_rio_45min"],
        )
        entities.append(entity)
    
    # Adiciona as entidades ao Home Assistant
    add_entities(entities, True)

class INEACheiasSensor(Entity):
    def __init__(self, municipio, curso_agua, nome_estacao, status_rio, ultima_leitura, status_monitoramento, chuva_ultimo, chuva_1h, chuva_24h, nivel_rio_ultimo, nivel_rio_45min):
        self._municipio = municipio
        self._curso_agua = curso_agua
        self._nome_estacao = nome_estacao
        self._status_rio = status_rio
        self._ultima_leitura = ultima_leitura
        self._status_monitoramento = status_monitoramento
        self._chuva_ultimo = chuva_ultimo
        self._chuva_1h = chuva_1h
        self._chuva_24h = chuva_24h
        self._nivel_rio_ultimo = nivel_rio_ultimo
        self._nivel_rio_45min
