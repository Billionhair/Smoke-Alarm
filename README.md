Smoke Alarm Compliance Monorepo
===============================

This repository contains the Python agent, Google Sheets scripts and supporting
assets for managing smoke alarm inspections.

Routing
-------
Use the agent's ``route`` command to optimise visits. Addresses may be
provided directly or loaded from the Sheet using ``--date``.

```
PYTHONPATH=agent/src python -m agent.cli route [ADDRESS...]
                             [--date YYYY-MM-DD|today]
                             [--days N]
                             [--responses-file FILE]
```

- ``--date`` loads properties due on the given day instead of supplying
  addresses on the command line.
- ``--days`` splits confirmed stops across multiple days.
- ``--responses-file`` points to a JSON mapping of address to
  confirmation (``true`` or ``false``) used when planning multi-day
  routes.

Routing relies on the public OSRM demo server and OpenStreetMap's
Nominatim geocoder. Internet access is required, and heavy usage should
provide self-hosted services.

Example single-day output:

```
1. 10 Downing St, London
2. Buckingham Palace, London
3. St Paul's Cathedral, London
Total distance: 5.5 km
Total duration: 15.1 min
https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London%7CBuckingham+Palace%2C+London
```

Example multi-day output:

```
Day 1:
  1. 10 Downing St, London
  2. St Paul's Cathedral, London
  Distance: 2.9 km
  Duration: 8.0 min
  Map: https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London
Day 2:
  1. Buckingham Palace, London
  2. London Eye, London
  Distance: 2.4 km
  Duration: 6.6 min
  Map: https://www.google.com/maps/dir/?api=1&destination=London+Eye%2C+London&waypoints=Buckingham+Palace%2C+London
```

Testing
-------
Run the unit tests from the repository root:

```
PYTHONPATH=agent/src python -m unittest discover agent/tests -v
```

See [docs/README.md](docs/README.md) for additional setup instructions and
project details.
