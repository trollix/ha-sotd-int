from homeassistant.components.sensor import SensorEntity
import datetime
import csv
import os
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data.get("name")
    language = entry.options.get("language", entry.data.get("language", "fr"))
    entry_id = entry.entry_id
    async_add_entities([SaintOfTheDaySensor(name, language, entry_id)], True)

class SaintOfTheDaySensor(SensorEntity):
    def __init__(self, name, language, entry_id):
        self._name = name
        self._language = language
        self._entry_id = entry_id
        self._state = None
        self._attr_icon = "mdi:calendar"
        self._attr_should_poll = True
        self._domain = DOMAIN

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._domain}_{self._entry_id}"

    @property
    def extra_state_attributes(self):
        return {
            "date": datetime.date.today().isoformat(),
            "language": self._language
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(self._domain, self._name)},
            "name": "Saint of the Day",
            "manufacturer": "Ha-SOTD Project",
            "model": "Saint CSV Calendar",
            "entry_type": "service"
        }

    async def async_update(self):
        today = datetime.date.today()
        date_key = today.strftime("%d/%m")
        base_path = os.path.dirname(__file__)
        saints_file = os.path.join(base_path, "data", f"saints_{self._language}.csv")

        try:
            with open(saints_file, encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == date_key:
                        self._state = row[1]
                        break
                else:
                    self._state = "Inconnu"
        except Exception as e:
            self._state = f"Erreur: {e}"
            _LOGGER.error(f"Erreur lors du chargement du fichier CSV : {e}")
