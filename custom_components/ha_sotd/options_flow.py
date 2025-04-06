from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_NAME
from .const import DOMAIN

DEFAULT_LANG = "fr"
LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "es": "Español"
}

class SotdOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("language", default=self.config_entry.options.get("language", "fr")): vol.In(LANGUAGES)
            })
        )

class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Saint du jour"): str,
                vol.Required("language", default=DEFAULT_LANG): vol.In(LANGUAGES)
            })
        )

    async def async_get_options_flow(self, config_entry):
        return SotdOptionsFlowHandler(config_entry)
