
import random
from homeassistant.components.sensor import SensorEntity
import datetime
import csv
import os
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.debug("🔧 async_setup_entry() called")
    try:
    show_proverbe = entry.options.get("show_proverbe", entry.data.get("show_proverbe", True))
    name = entry.data.get("name")
    language = entry.options.get("language", entry.data.get("language", "fr"))
    show_dicton = entry.options.get("show_dicton", entry.data.get("show_dicton", True))
    entry_id = entry.entry_id

        sensors = [SaintOfTheDaySensor(name, language, entry_id)]
        if show_dicton:
        sensors.append(DictonOfTheDaySensor(language, entry_id))
            if show_proverbe:
        sensors.append(ProverbeOfTheDaySensor(language, entry_id))
            _LOGGER.debug(f"🔧 Adding sensors: {[s.name for s in sensors]}")
                async_add_entities(sensors, True)

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
        return f"{self._domain}_{self._entry_id}_saint"

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

class DictonOfTheDaySensor(SensorEntity):
    def __init__(self, language, entry_id):
        self._language = language
        self._entry_id = entry_id
        self._state = None
        self._attr_icon = "mdi:comment-quote"
        self._attr_should_poll = True
        self._domain = DOMAIN

    @property
    def name(self):
        return "Dicton du jour"

    @property
    def native_value(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._domain}_{self._entry_id}_dicton"

    @property
    def extra_state_attributes(self):
        return {
            "date": datetime.date.today().isoformat(),
            "language": self._language
        }

    async def async_update(self):
        today = datetime.date.today()
        date_key = today.strftime("%d/%m")
        base_path = os.path.dirname(__file__)
        dictons_file = os.path.join(base_path, "data", f"dictons_{self._language}.csv")

        try:
            with open(dictons_file, encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == date_key:
                        dictons = row[1:]  # toutes les colonnes après la date
                        dictons = [d.strip() for d in dictons if d.strip()]
                        if dictons:
                            self._state = random.choice(dictons)
                        else:
                            self._state = "Aucun dicton trouvé."
                        break
                else:
                    self._state = "Aucun dicton pour aujourd'hui."
        except Exception as e:
            self._state = f"Erreur: {e}"
            _LOGGER.warning(f"Erreur chargement dictons : {e}")


class ProverbeOfTheDaySensor(SensorEntity):
    def __init__(self, language, entry_id):
        self._language = language
        self._entry_id = entry_id
        self._state = None
        self._attr_icon = "mdi:format-quote-close"
        self._attr_should_poll = True
        self._domain = DOMAIN

    @property
    def name(self):
        return "Proverbe du jour"

    @property
    def native_value(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._domain}_{self._entry_id}_proverbe"

    @property
    def extra_state_attributes(self):
        return {
            "date": datetime.date.today().isoformat(),
            "language": self._language
        }

    async def async_update(self):
        today = datetime.date.today()
        date_key = today.strftime("%d/%m")
        base_path = os.path.dirname(__file__)
        proverbes_file = os.path.join(base_path, "data", f"proverbes_{self._language}.csv")

        try:
            with open(proverbes_file, encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == date_key:
                        proverbes = row[1:]
                        proverbes = [p.strip() for p in proverbes if p.strip()]
                        if proverbes:
                            self._state = random.choice(proverbes)
                        else:
                            self._state = "Aucun proverbe trouvé."
                        break
                else:
                    self._state = "Aucun proverbe pour aujourd'hui."
        except Exception as e:
            self._state = f"Erreur: {e}"
            _LOGGER.warning(f"Erreur chargement proverbes : {e}")
