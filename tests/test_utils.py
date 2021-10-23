# switchbot-mqtt - MQTT client controlling SwitchBot button & curtain automators,
# compatible with home-assistant.io's MQTT Switch & Cover platform
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

from switchbot_mqtt._utils import (
    _mac_address_valid,
    _MQTTTopicPlaceholder,
    _parse_mqtt_topic,
)


@pytest.mark.parametrize(
    ("mac_address", "valid"),
    [
        ("aa:bb:cc:dd:ee:ff", True),
        ("AA:BB:CC:DD:EE:FF", True),
        ("AA:12:34:45:67:89", True),
        ("aabbccddeeff", False),  # not supported by PySwitchbot
        ("aa:bb:cc:dd:ee:gg", False),
    ],
)
def test__mac_address_valid(mac_address, valid):
    # pylint: disable=protected-access
    assert _mac_address_valid(mac_address) == valid


@pytest.mark.parametrize(
    ("expected_levels", "topic", "expected_attrs"),
    [
        (
            ["switchbot", _MQTTTopicPlaceholder.MAC_ADDRESS, "set"],
            "switchbot/aa:bb:cc:dd:ee:ff/set",
            {_MQTTTopicPlaceholder.MAC_ADDRESS: "aa:bb:cc:dd:ee:ff"},
        ),
        (
            ["switchbot", _MQTTTopicPlaceholder.MAC_ADDRESS, "set"],
            "switchbot//set",
            {_MQTTTopicPlaceholder.MAC_ADDRESS: ""},
        ),
        (
            ["prefix", _MQTTTopicPlaceholder.MAC_ADDRESS],
            "prefix/aa:bb:cc:dd:ee:ff",
            {_MQTTTopicPlaceholder.MAC_ADDRESS: "aa:bb:cc:dd:ee:ff"},
        ),
        (
            [_MQTTTopicPlaceholder.MAC_ADDRESS],
            "00:11:22:33:44:55",
            {_MQTTTopicPlaceholder.MAC_ADDRESS: "00:11:22:33:44:55"},
        ),
    ],
)
def test__parse_mqtt_topic(expected_levels, topic, expected_attrs):
    assert (
        _parse_mqtt_topic(topic=topic, expected_levels=expected_levels)
        == expected_attrs
    )


@pytest.mark.parametrize(
    ("expected_levels", "topic"),
    [
        (
            ["switchbot", _MQTTTopicPlaceholder.MAC_ADDRESS, "set"],
            "switchbot/aa:bb:cc:dd:ee:ff",
        ),
        (
            ["switchbot", _MQTTTopicPlaceholder.MAC_ADDRESS, "set"],
            "switchbot/aa:bb:cc:dd:ee:ff/change",
        ),
        (
            ["switchbot", _MQTTTopicPlaceholder.MAC_ADDRESS, "set"],
            "switchbot/aa:bb:cc:dd:ee:ff/set/suffix",
        ),
    ],
)
def test__parse_mqtt_topic_fail(expected_levels, topic):
    with pytest.raises(ValueError):
        _parse_mqtt_topic(topic=topic, expected_levels=expected_levels)
