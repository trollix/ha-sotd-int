from datetime import datetime
import logging
import json
import os

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Saint of the Day"
CONF_NAME = "name"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})


SAINTS = {}

def load_saints():
    """Charge les saints depuis le fichier JSON."""
    global SAINTS
    try:
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "data", "saints_fr.json")
        with open(file_path, encoding='utf-8') as f:
            SAINTS = json.load(f)
            _LOGGER.debug("Fichier des saints chargé avec succès (%d entrées).", len(SAINTS))
    except Exception as e:
        _LOGGER.error("Erreur lors du chargement du fichier saints_fr.json : %s", e)
        SAINTS = {}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Configure le capteur."""
    load_saints()
    name = config.get(CONF_NAME)
    add_entities([SaintOfTheDaySensor(name)], True)

class SaintOfTheDaySensor(SensorEntity):
    """Représente le capteur saint du jour."""

    def __init__(self, name):
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        """Met à jour l’état du capteur avec le saint du jour."""
        today = datetime.now().strftime("%m-%d")
        self._state = SAINTS.get(today, "Inconnu")
