

# Orbitr: Resident Space Object Almanac

Orbitr is a combined Python/Flask + AngularJS application that tracks Resident Space Objects (RSOs) and visualizes them in either a 2D map or a 3D Cesium globe. The backend provides a CRUD API for spacecraft, while the frontend offers an explorer interface for analysts.

## Getting Started

```bash
# Install dependencies
uv sync

# Run the Flask + Angular application
uv run python main.py
```

The server starts on `http://localhost:5000`. The Cesium/Angular interface lives under `/app`, so navigate to `http://localhost:5000/app` to use the UI. The root URL redirects there automatically.

Flask uses its standard `instance/` directory to persist RSO data in `instance/rso_store.json`. The file is automatically seeded from the built‑in catalog the first time you run the app. You can safely delete it to reload the original data set.

## API Overview

All endpoints are under the `/api` prefix and return JSON.

| Method & Path | Description |
| --- | --- |
| `GET /api/health` | Basic health probe plus total object count. |
| `GET /api/rso` | List all stored RSOs. |
| `POST /api/rso` | Create a new spacecraft entry. |
| `GET /api/rso/<satcat>` | Retrieve one spacecraft by SatCat number. |
| `PUT /api/rso/<satcat>` | Replace a spacecraft (all fields required). |
| `PATCH /api/rso/<satcat>` | Update a spacecraft (partial fields). |
| `DELETE /api/rso/<satcat>` | Remove a spacecraft. |
| `GET /api/rso/almanac/catalog` | Return the seeded catalog derived from public GPS, NOAA, GOES, WSF‑M, WindSat/Coriolis, ISS, Hubble, and JWST listings. |

### Payload Schema

Every spacecraft tracks the following fields:

```jsonc
{
  "display_name": "GPS III SV05 (USA-334)",
  "satcat_number": "48274",
  "international_designator": "2021-041A",
  "tle": "1 48274U ...",          // multi-line string
  "aliases": ["GPS III-5", "PRN 18"],
  "tags": ["gps", "navigation"]
}
```

Aliases and tags are always arrays of strings. The server enforces deduplication, and the SatCat number acts as the identifier for CRUD operations.

## Frontend Features

The AngularJS/Cesium application (served from `/app`) provides:

- A **View** menu that flips between a Cesium 3D globe and a 2D map of Earth.
- Search & filtering across display names, SatCat numbers, aliases, and tags.
- A Cesium visualization layer that plots each spacecraft with pseudo‑positions (derived from SatCat numbers) so analysts can browse the catalog in both 2D and 3D.
- Detail panels that expose metadata, aliases, tags, and TLE text for the currently selected RSO.

AngularJS consumes the same `/api/rso` endpoints described above, so any CRUD changes made via the API will be reflected in the visualization after a refresh.

## Extending the Catalog

The static catalog lives in `orbitr/catalog.py`. Each entry includes representative TLE strings sourced from public element sets and can be expanded with additional RSOs (e.g., full historical GPS fleets). After editing the catalog you can delete `instance/rso_store.json` to reseed the persistent store with your updates.
