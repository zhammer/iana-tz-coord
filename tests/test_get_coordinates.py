import re
from typing import List

import pytest

from iana_tz_coord import Coordinates, get_coordinates


IANA_TZS_WITH_EXTRA_PREFIX: List[str] = [
    'America/Argentina/Buenos_Aires',
    'America/Argentina/Catamarca',
    'America/Argentina/Cordoba',
    'America/Argentina/Jujuy',
    'America/Argentina/La_Rioja',
    'America/Argentina/Mendoza',
    'America/Argentina/Rio_Gallegos',
    'America/Argentina/Salta',
    'America/Argentina/San_Juan',
    'America/Argentina/San_Luis',
    'America/Argentina/Tucuman',
    'America/Argentina/Ushuaia',
    'America/Indiana/Indianapolis',
    'America/Indiana/Knox',
    'America/Indiana/Marengo',
    'America/Indiana/Petersburg',
    'America/Indiana/Tell_City',
    'America/Indiana/Vevay',
    'America/Indiana/Vincennes',
    'America/Indiana/Winamac',
    'America/Kentucky/Louisville',
    'America/Kentucky/Monticello',
    'America/North_Dakota/Beulah',
    'America/North_Dakota/Center',
    'America/North_Dakota/New_Salem'
]


class TestGetCoordinates(object):

    def test_returns_coordinates_for_america_new_york(self) -> None:
        coordinates = get_coordinates('America/New_York')
        expected_coordinates = Coordinates(
            latitude=40.714166666666664,
            longitude=-74.00638888888889
        )
        assert coordinates == expected_coordinates

    @pytest.mark.parametrize('iana_tz_name_with_prefix', IANA_TZS_WITH_EXTRA_PREFIX)  # type: ignore
    def test_can_ignore_special_iana_prefix(self, iana_tz_name_with_prefix: str) -> None:
        iana_tz_name_without_prefix = _remove_extra_iana_prefix(iana_tz_name_with_prefix)
        assert get_coordinates(iana_tz_name_with_prefix) == get_coordinates(iana_tz_name_without_prefix)

    def test_raises_lookup_error_on_invalid_timezone(self) -> None:
        with pytest.raises(LookupError):
            get_coordinates('Aqua_Magna/Mata_Nui')


def _remove_extra_iana_prefix(iana_tz_with_prefix: str) -> str:
    """
    >>> _remove_extra_iana_prefix('America/North_Dakota/Beulah')
    'America/Beulah'
    """
    return re.sub(r'(?<=America/)\w+/', '', iana_tz_with_prefix)
