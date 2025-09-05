"""Vehicle routing with time windows using OR-Tools."""

from __future__ import annotations

from typing import List, Tuple

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from ..services import osrm


def optimize(
    coords: List[Tuple[float, float]],
    time_windows: List[Tuple[int, int]] | None = None,
    demands: List[int] | None = None,
    vehicle_capacities: List[int] | None = None,
    depot: int = 0,
) -> dict:
    """Solve a VRP with optional time windows and capacity constraints."""
    n = len(coords)
    if n == 0:
        return {"routes": []}
    matrix = osrm.table(coords)
    vehicles = len(vehicle_capacities) if vehicle_capacities else 1

    manager = pywrapcp.RoutingIndexManager(n, vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def transit_callback(from_index: int, to_index: int) -> int:
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(matrix[from_node][to_node])

    transit_cb_idx = routing.RegisterTransitCallback(transit_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_idx)

    if demands and vehicle_capacities:

        def demand_callback(from_index: int) -> int:
            return demands[manager.IndexToNode(from_index)]

        demand_cb_idx = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_cb_idx, 0, vehicle_capacities, True, "Capacity"
        )

    if time_windows:
        routing.AddDimension(transit_cb_idx, 30, 24 * 3600, False, "Time")
        time_dim = routing.GetDimensionOrDie("Time")
        for i, window in enumerate(time_windows):
            if not window:
                continue
            index = manager.NodeToIndex(i)
            time_dim.CumulVar(index).SetRange(window[0], window[1])

    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    solution = routing.SolveWithParameters(search)
    routes: List[List[int]] = []
    if solution:
        for v in range(vehicles):
            idx = routing.Start(v)
            route: List[int] = []
            while not routing.IsEnd(idx):
                route.append(manager.IndexToNode(idx))
                idx = solution.Value(routing.NextVar(idx))
            route.append(manager.IndexToNode(idx))
            routes.append(route)
    return {"routes": routes}
