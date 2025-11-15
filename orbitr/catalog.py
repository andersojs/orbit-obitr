from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

RsoRecord = Dict[str, Any]


def load_catalog() -> List[RsoRecord]:
    """Return a deep copy of the static catalog."""
    return deepcopy(CATALOG_RSOS)


def _tle_template(satcat: str, inclination: float, mean_motion: float) -> str:
    sat_num = int("".join(filter(str.isdigit, satcat)) or 0)
    line1 = (
        f"1 {sat_num:05d}U 24001A   24123.00000000  .00000000  00000-0  00000-0 0  9991"
    )
    line2 = (
        f"2 {sat_num:05d} {inclination:8.4f} 123.4567 0001000 120.1234 240.5678 {mean_motion:11.8f}    05"
    )
    return f"{line1}\n{line2}"


CATALOG_RSOS: List[RsoRecord] = [
    {
        "display_name": "GPS III SV01 (USA-289)",
        "satcat_number": "43073",
        "international_designator": "2018-079A",
        "tle": _tle_template("43073", 55.0, 2.0056),
        "aliases": ["GPS III-1", "Navstar 74", "PRN 04"],
        "tags": ["gps", "navigation", "m-code"],
    },
    {
        "display_name": "GPS III SV02 (USA-293)",
        "satcat_number": "44402",
        "international_designator": "2019-029A",
        "tle": _tle_template("44402", 55.0, 2.0056),
        "aliases": ["GPS III-2", "Navstar 75", "PRN 05"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS III SV03 (USA-304)",
        "satcat_number": "44873",
        "international_designator": "2019-079A",
        "tle": _tle_template("44873", 55.0, 2.0056),
        "aliases": ["GPS III-3", "Navstar 76", "PRN 07"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS III SV04 (USA-309)",
        "satcat_number": "46450",
        "international_designator": "2020-067A",
        "tle": _tle_template("46450", 55.0, 2.0056),
        "aliases": ["GPS III-4", "Navstar 77", "PRN 13"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS III SV05 (USA-334)",
        "satcat_number": "48274",
        "international_designator": "2021-041A",
        "tle": _tle_template("48274", 55.0, 2.0056),
        "aliases": ["GPS III-5", "Navstar 78", "PRN 18"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS III SV06 (USA-345)",
        "satcat_number": "49678",
        "international_designator": "2023-006A",
        "tle": _tle_template("49678", 55.0, 2.0056),
        "aliases": ["GPS III-6", "Navstar 80", "PRN 16"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-1 (USA-232)",
        "satcat_number": "36585",
        "international_designator": "2010-019A",
        "tle": _tle_template("36585", 55.0, 2.0056),
        "aliases": ["GPS IIF-1", "Navstar 66", "PRN 25"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-3 (USA-239)",
        "satcat_number": "38833",
        "international_designator": "2012-053A",
        "tle": _tle_template("38833", 55.0, 2.0056),
        "aliases": ["GPS IIF-3", "Navstar 68", "PRN 24"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-5 (USA-248)",
        "satcat_number": "40105",
        "international_designator": "2014-068A",
        "tle": _tle_template("40105", 55.0, 2.0056),
        "aliases": ["GPS IIF-5", "Navstar 70", "PRN 30"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-7 (USA-261)",
        "satcat_number": "40730",
        "international_designator": "2015-013A",
        "tle": _tle_template("40730", 55.0, 2.0056),
        "aliases": ["GPS IIF-7", "Navstar 72", "PRN 09"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-9 (USA-265)",
        "satcat_number": "41024",
        "international_designator": "2015-024A",
        "tle": _tle_template("41024", 55.0, 2.0056),
        "aliases": ["GPS IIF-9", "Navstar 73", "PRN 01"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "GPS IIF SV-10 (USA-266)",
        "satcat_number": "41328",
        "international_designator": "2015-062A",
        "tle": _tle_template("41328", 55.0, 2.0056),
        "aliases": ["GPS IIF-10", "Navstar 71", "PRN 27"],
        "tags": ["gps", "navigation"],
    },
    {
        "display_name": "NOAA-15",
        "satcat_number": "25338",
        "international_designator": "1998-030A",
        "tle": _tle_template("25338", 98.7, 14.2500),
        "aliases": ["NOAA-K"],
        "tags": ["noaa", "weather", "polar-orbiting"],
    },
    {
        "display_name": "NOAA-18",
        "satcat_number": "28654",
        "international_designator": "2005-018A",
        "tle": _tle_template("28654", 99.0, 14.1200),
        "aliases": ["NOAA-N"],
        "tags": ["noaa", "weather"],
    },
    {
        "display_name": "NOAA-19",
        "satcat_number": "33591",
        "international_designator": "2009-005A",
        "tle": _tle_template("33591", 99.1, 14.1200),
        "aliases": ["NOAA-N Prime"],
        "tags": ["noaa", "weather"],
    },
    {
        "display_name": "NOAA-20 (JPSS-1)",
        "satcat_number": "43013",
        "international_designator": "2017-071A",
        "tle": _tle_template("43013", 98.7, 14.2300),
        "aliases": ["JPSS-1", "NOAA/NASA Joint Polar Satellite System-1"],
        "tags": ["noaa", "weather", "jp"],
    },
    {
        "display_name": "NOAA-21 (JPSS-2)",
        "satcat_number": "54240",
        "international_designator": "2022-146A",
        "tle": _tle_template("54240", 98.7, 14.2300),
        "aliases": ["JPSS-2"],
        "tags": ["noaa", "weather"],
    },
    {
        "display_name": "GOES-15",
        "satcat_number": "36411",
        "international_designator": "2010-008A",
        "tle": _tle_template("36411", 0.1, 1.0027),
        "aliases": ["GOES-P"],
        "tags": ["goes", "geostationary", "weather"],
    },
    {
        "display_name": "GOES-16 (GOES-R)",
        "satcat_number": "41866",
        "international_designator": "2016-071A",
        "tle": _tle_template("41866", 0.0, 1.0027),
        "aliases": ["GOES-East"],
        "tags": ["goes", "geostationary", "weather"],
    },
    {
        "display_name": "GOES-17 (GOES-S)",
        "satcat_number": "43226",
        "international_designator": "2018-022A",
        "tle": _tle_template("43226", 0.0, 1.0027),
        "aliases": ["GOES-West"],
        "tags": ["goes", "geostationary", "weather"],
    },
    {
        "display_name": "GOES-18 (GOES-T)",
        "satcat_number": "49384",
        "international_designator": "2022-057A",
        "tle": _tle_template("49384", 0.0, 1.0027),
        "aliases": ["GOES-West prime"],
        "tags": ["goes", "geostationary", "weather"],
    },
    {
        "display_name": "GOES-U (GOES-19)",
        "satcat_number": "59000",
        "international_designator": "2024-900A",
        "tle": _tle_template("59000", 0.0, 1.0027),
        "aliases": ["GOES-U", "GOES-19"],
        "tags": ["goes", "geostationary", "weather"],
    },
    {
        "display_name": "WSF-M",
        "satcat_number": "59500",
        "international_designator": "2024-901A",
        "tle": _tle_template("59500", 98.7, 14.2000),
        "aliases": ["Weather System Follow-on Microwave"],
        "tags": ["wsf-m", "weather", "us-space-force"],
    },
    {
        "display_name": "WindSat / Coriolis",
        "satcat_number": "27640",
        "international_designator": "2003-006A",
        "tle": _tle_template("27640", 98.7, 14.2000),
        "aliases": ["Coriolis", "WindSat"],
        "tags": ["windsat", "weather"],
    },
    {
        "display_name": "International Space Station",
        "satcat_number": "25544",
        "international_designator": "1998-067A",
        "tle": _tle_template("25544", 51.64, 15.495),
        "aliases": ["ISS", "Zarya"],
        "tags": ["iss", "human-spaceflight"],
    },
    {
        "display_name": "Hubble Space Telescope",
        "satcat_number": "20580",
        "international_designator": "1990-037B",
        "tle": _tle_template("20580", 28.47, 15.091),
        "aliases": ["HST"],
        "tags": ["science", "observatory"],
    },
    {
        "display_name": "James Webb Space Telescope",
        "satcat_number": "50463",
        "international_designator": "2021-130A",
        "tle": _tle_template("50463", 0.0, 1.0027),
        "aliases": ["JWST", "Webb"],
        "tags": ["science", "observatory", "l2"],
    },
]
