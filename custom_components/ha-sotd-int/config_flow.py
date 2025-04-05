import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_NAME

class HaSotdIntConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Saint of the Day integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", default=DEFAULT_NAME): str
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HaSotdIntOptionsFlowHandler(config_entry)

class HaSotdIntOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("name", default=self.config_entry.data.get("name", DEFAULT_NAME)): str
            })
        )
