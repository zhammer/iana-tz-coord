import pytest

from iana_tz_coord import Coordinates, get_coordinates


class TestGetCoordinates(object):

    def test_returns_coordinates_for_america_new_york(self) -> None:
        coordinates = get_coordinates('America/New_York')
        expected_coordinates = Coordinates(
            latitude=40.714166666666664,
            longitude=-74.00638888888889
        )
        assert coordinates == expected_coordinates

    def test_raises_lookup_error_on_invalid_timezone(self) -> None:
        with pytest.raises(LookupError):
            get_coordinates('Aqua_Magna/Mata_Nui')
