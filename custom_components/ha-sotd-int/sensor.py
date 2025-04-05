from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME
from .const import DOMAIN
import datetime
import json
import os

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data.get(CONF_NAME)
    async_add_entities([SaintOfTheDaySensor(hass, name)], True)

class SaintOfTheDaySensor(SensorEntity):
    def __init__(self, hass, name):
        self._name = name
        self._state = None
        self._attr_icon = "mdi:church"
        self.hass = hass

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    async def async_update(self):
        today = datetime.date.today()
        date_key = today.strftime("%m-%d")
        #saints_file = os.path.join(self.hass.config.path("custom_components/ha-sotd-int/data/saints_fr.json"))
        saints_file =  os.path.join(base_path, "custom_components", "ha-sotd-int", "data", "saints_fr.json")

        try:
            with open(saints_file, encoding="utf-8") as f:
                data = json.load(f)
            self._state = data.get(date_key, "Inconnu")
        except Exception as e:
            self._state = f"Erreur: {e}"
