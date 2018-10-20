import csv
import sys
from pprint import pprint
from typing import Dict, Iterable, MutableMapping

import iso6709

from iana_tz_coord import Coordinates


ZONE_CSV_FIELDNAMES = ('codes', 'coordinates', 'TZ', 'comments')
ZoneCsvRow = MutableMapping[str, str]


def main() -> None:
    zone_csv_path = sys.argv[1]

    with open(zone_csv_path) as zone_csv:
        rows = csv.DictReader(
            without_comment_lines(zone_csv),
            fieldnames=ZONE_CSV_FIELDNAMES,
            delimiter='\t'
        )
        coordinate_pair_by_tz_name = pluck_coordinate_pair_by_tz_name(rows)

    pprint(coordinate_pair_by_tz_name)


def without_comment_lines(lines: Iterable[str]) -> Iterable[str]:
    return (line for line in lines if not line.startswith('#'))


def pluck_coordinate_pair_by_tz_name(zone_csv_rows: Iterable[ZoneCsvRow]) -> Dict[str, Coordinates]:
    return {zone_csv_row['TZ']: pluck_coordinate_pair(zone_csv_row['coordinates'])
            for zone_csv_row in zone_csv_rows}


def pluck_coordinate_pair(raw_coordinates: str) -> Coordinates:
    location = iso6709.Location(raw_coordinates)
    return Coordinates(
        latitude=float(location.lat.decimal),
        longitude=float(location.lng.decimal)
    )


if __name__ == '__main__':
    main()
