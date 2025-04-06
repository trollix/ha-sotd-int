from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import voluptuous as vol
from .const import DOMAIN

DEFAULT_NAME = "Saint du jour"
DEFAULT_LANG = "fr"
LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "es": "Español"
}

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Required("language", default=DEFAULT_LANG): vol.In(LANGUAGES),
})

class SotdConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

    async def async_step_options(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="options", data_schema=CONFIG_SCHEMA)

    def async_get_options_flow(self):
        return self