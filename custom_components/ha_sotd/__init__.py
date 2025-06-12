from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

# ---------- SETUP ---------- #
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ha_sotd from a config entry."""
    # Nouvelle API (HA >= 2025.06)
    if hasattr(hass.config_entries, "async_forward_entry_setups"):
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    # Ancienne API (jusqu’à 2025.05)
    else:  # pragma: no cover
        await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    return True

# ---------- UNLOAD ---------- #
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload ha_sotd config entry."""
    if hasattr(hass.config_entries, "async_forward_entry_unloads"):
        return await hass.config_entries.async_forward_entry_unloads(entry, ["sensor"])
    # Ancienne API
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")  # pragma: no cover
