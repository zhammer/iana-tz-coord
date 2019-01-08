import csv
import os.path
import sys
from pprint import pprint
from typing import Dict, Iterable, MutableMapping

import iso6709

from iana_tz_coord import Coordinates


ZONE_CSV_FIELDNAMES = ('codes', 'coordinates', 'TZ', 'comments')
CsvRow = MutableMapping[str, str]

BACKWARD_CSV_FIELDNAMES = ('link', 'target', 'link_name')

# i miss messy files

def main() -> None:
    iana_tz_dir = sys.argv[1]
    zone_file_path = os.path.join(iana_tz_dir, 'zone1970.tab')
    backward_file_path = os.path.join(iana_tz_dir, 'backward')

    with open(zone_file_path) as zone_file:
        zone_file_rows = list(csv.DictReader(
            without_comment_lines(zone_file),
            fieldnames=ZONE_CSV_FIELDNAMES,
            delimiter='\t'
        ))
        coordinate_pair_by_tz_name = pluck_coordinate_pair_by_tz_name(zone_file_rows)

    with open(backward_file_path) as backward_file:
        lines = (line.split() for line in backward_file
                 if not line == '\n' and not line.startswith('#'))
        current_name_with_backwards_name = [(current, backwards) for the_word_link, current, backwards in lines]

    for current, backwards in current_name_with_backwards_name:
        if current in coordinate_pair_by_tz_name:
            coordinate_pair_by_tz_name[backwards] = coordinate_pair_by_tz_name[current]

    pprint(coordinate_pair_by_tz_name)


def without_comment_lines(lines: Iterable[str]) -> Iterable[str]:
    return (line for line in lines if not line.startswith('#'))


def pluck_coordinate_pair_by_tz_name(zone_csv_rows: Iterable[CsvRow]) -> Dict[str, Coordinates]:
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
