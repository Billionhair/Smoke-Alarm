AGENTS.md (optimizer)

Scope: VRP and time window optimization.

Inputs

Jobs with lat lon service time and optional time window

Vehicles with shift start, shift end, and capacity

Depot coordinate

Travel time matrix in seconds from OSRM /table

Rules

Use OR-Tools RoutingModel and time window constraints

Deterministic seed

Respect vehicle shift windows

Allow hard or soft time windows configurable

If solver fails, return a clear error and a fallback nearest neighbor plan

Performance targets

Up to 200 jobs and 10 vehicles on a laptop within a few seconds to a minute

Matrix build is the main cost so cache by day and depot

Tests

Unit test for cost functions and constraints

Golden tests for small synthetic days

Property tests for trivial cases such as one job per vehicle

Outputs

Ordered stops per vehicle with arrival and departure times

Total drive time and service time

Google Maps share links for each vehicle path
