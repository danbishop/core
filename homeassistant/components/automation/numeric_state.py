"""
homeassistant.components.automation.state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Offers state listening automation rules.
"""
import logging

from homeassistant.helpers.event import track_state_change


CONF_ENTITY_ID = "state_entity_id"
CONF_BELOW = "state_below"
CONF_ABOVE = "state_above"

_LOGGER = logging.getLogger(__name__)

def register(hass, config, action):
    """ Listen for state changes based on `config`. """
    entity_id = config.get(CONF_ENTITY_ID)

    if entity_id is None:
        _LOGGER.error("Missing configuration key %s", CONF_ENTITY_ID)
        return False

    below = config.get(CONF_BELOW)
    above = config.get(CONF_ABOVE)

    if below is None and above is None:
        _LOGGER.error("Missing configuration key %s or %s", CONF_BELOW, CONF_ABOVE)

    def numeric_in_range(value, range_start, range_end):
        """ Checks if value is inside the range
        :param value:
        :param range_start:
        :param range_end:
        :return:
        """

        if value is None:
            _LOGGER.warn("Missing value in numeric check")
            return False

        value = float(value)

        if range_start is not None and range_end is not None:
            return float(range_start) < value < float(range_end)
        elif range_end is not None:
            return value < float(range_end)
        else:
            return value > float(range_start)

    def state_automation_listener(entity, from_s, to_s):
        """ Listens for state changes and calls action. """

        # Fire action if we go from outside range into range
        if numeric_in_range(to_s.state, above, below) and \
           from_s is None or not numeric_in_range(from_s.state, above, below):
            action()

    track_state_change(
        hass, entity_id, state_automation_listener)

    return True
