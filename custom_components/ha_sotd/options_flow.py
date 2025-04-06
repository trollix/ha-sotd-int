from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN
import logging

DEFAULT_LANG = "fr"
LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "es": "Español"
}

_LOGGER = logging.getLogger(__name__)

class SotdOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        _LOGGER.warning("✅ Options flow déclenché !")

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            _LOGGER.warning(f"📨 Données soumises : {user_input}")
            return self.async_create_entry(title="", data=user_input)

        _LOGGER.warning("📋 Affichage du formulaire d’options")
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("language", default=self.config_entry.options.get("language", DEFAULT_LANG)): vol.In(LANGUAGES),
                vol.Optional("dummy_option", default=self.config_entry.options.get("dummy_option", "visible")): str
            })
        )