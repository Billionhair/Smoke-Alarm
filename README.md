 codex/update-readme.md-with-documentation-and-examples-ldgzgw
# Smoke Alarm Compliance Monorepo

Effortless compliance and routing for property smoke alarm inspections.

## Overview

This repository contains the Python agent, Google Sheets scripts and supporting assets for managing smoke alarm inspections.

## Features

- AI-assisted routing and scheduling
- Google Sheets automations for reports, invoices and SMS reminders
- Document templates and CI workflows for seamless deployments

## Routing
Use the agent's `route` command to optimise visits. Addresses may be provided directly or loaded from the Sheet using `--date`.

Smoke Alarm Compliance Monorepo


This repository contains the Python agent, Google Sheets scripts and supporting
assets for managing smoke alarm inspections.

Routing

Use the agent's ``route`` command to optimise visits. Addresses may be
provided directly or loaded from the Sheet using ``--date``.
 main

```
PYTHONPATH=agent/src python -m agent.cli route [ADDRESS...]
                             [--date YYYY-MM-DD|today]
                             [--days N]
                             [--responses-file FILE]
```

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
- `--date` loads properties due on the given day instead of supplying addresses on the command line.
- `--days` splits confirmed stops across multiple days.
- `--responses-file` points to a JSON mapping of address to confirmation (`true` or `false`) used when planning multi-day routes.

Routing relies on the public OSRM demo server and OpenStreetMap's Nominatim geocoder. Internet access is required, and heavy usage should provide self-hosted services.

- ``--date`` loads properties due on the given day instead of supplying
  addresses on the command line.
- ``--days`` splits confirmed stops across multiple days.
- ``--responses-file`` points to a JSON mapping of address to
  confirmation (``true`` or ``false``) used when planning multi-day
  routes.

Routing relies on the public OSRM demo server and OpenStreetMap's
Nominatim geocoder. Internet access is required, and heavy usage should
provide self-hosted services.
 main

Example single-day output:

```
1. 10 Downing St, London
2. Buckingham Palace, London
3. St Paul's Cathedral, London
Total distance: 5.5 km
Total duration: 15.1 min
 codex/update-readme.md-with-documentation-and-examples-ldgzgw
Map: https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London%7CBuckingham+Palace%2C+London

https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London%7CBuckingham+Palace%2C+London
 main
```

Example multi-day output:

```
Day 1:
  1. 10 Downing St, London
  2. St Paul's Cathedral, London
  Distance: 2.9 km
  Duration: 8.0 min
  Map: https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London
 codex/update-readme.md-with-documentation-and-examples-ldgzgw


 main
Day 2:
  1. Buckingham Palace, London
  2. London Eye, London
  Distance: 2.4 km
  Duration: 6.6 min
  Map: https://www.google.com/maps/dir/?api=1&destination=London+Eye%2C+London&waypoints=Buckingham+Palace%2C+London
```

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
## Testing

Testing

 main
Run the unit tests from the repository root:

```
PYTHONPATH=agent/src python -m unittest discover agent/tests -v
```

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
### GUI

A React-based operator console lives in [`gui/`](gui). Start the development server with:

```
cd gui
npm install
npm run dev
```

Run the component tests with:

```
npm test
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and [docs/README.md](docs/README.md) for additional setup instructions.
Pull requests are welcome; please include tests for any new features.

## Security

Review [SECURITY.md](SECURITY.md) for guidance on reporting vulnerabilities.

See [docs/README.md](docs/README.md) for additional setup instructions and
project details.
 main
