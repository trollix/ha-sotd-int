
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
    vol.Optional("show_dicton", default=True): bool,
    vol.Optional("show_proverbe", default=True): bool
})

class SotdConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_NAME: user_input[CONF_NAME],
                    "language": user_input["language"],
                    "show_dicton": user_input.get("show_dicton", True),
                    "show_proverbe": user_input.get("show_proverbe", True)
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return SotdOptionsFlow(config_entry)


class SotdOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_NAME,
                    default=self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)
                ): str,
                vol.Required(
                    "language",
                    default=self.config_entry.options.get("language", DEFAULT_LANG)
                ): vol.In(LANGUAGES),
                vol.Optional(
                    "show_dicton",
                    default=self.config_entry.options.get("show_dicton", True)
                ): bool,
                vol.Optional(
                    "show_proverbe",
                    default=self.config_entry.options.get("show_proverbe", True)
                ): bool
            })
        )
