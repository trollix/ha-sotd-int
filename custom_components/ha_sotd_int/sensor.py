from homeassistant.components.sensor import SensorEntity
import datetime
import json
import os
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data.get("name")
    language = entry.data.get("language", "fr")
    async_add_entities([SaintOfTheDaySensor(name, language)], True)

class SaintOfTheDaySensor(SensorEntity):
    def __init__(self, name, language):
        self._name = name
        self._language = language
        self._state = None
        self._attr_icon = "mdi:church"
        self._attr_should_poll = True

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "date": datetime.date.today().isoformat()
        }

    async def async_update(self):
        today = datetime.date.today()
        date_key = today.strftime("%m-%d")
        base_path = os.path.dirname(__file__)
        saints_file = os.path.join(base_path, "data", f"saints_{self._language}.json")

        try:
            with open(saints_file, encoding="utf-8") as f:
                data = json.load(f)
            self._state = data.get(date_key, "Inconnu")
            _LOGGER.debug(f"Saint du {date_key} : {self._state}")
        except Exception as e:
            self._state = f"Erreur: {e}"
            _LOGGER.error(f"Erreur lors du chargement des saints : {e}")
