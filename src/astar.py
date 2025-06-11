import main as cj
import heapq as heap
import time
from typing import Tuple, Dict, List, Set, Any


def format_coord(coord: Tuple[float, float]) -> Tuple[float, float]:
    """Round coordinates to 7 decimal places for consistent comparison."""
    return tuple(round(x, 7) for x in coord)


def initialize_search(source: Tuple[float, float], destination: Tuple[float, float]) -> Tuple[
    str, str, Dict[str, float]]:
    """Initialize the A* search parameters and data structures."""
    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])

    print(f"Source coordinates: {source}")
    print(f"Destination coordinates: {destination}")
    print(f"Source ID: {sourceID}")
    print(f"Destination ID: {destID}")

    # Initialize g_values with source cost
    g_values = {sourceID: 0.0}

    return sourceID, destID, g_values


def process_neighbor(
        neighbor_data: Dict[str, List],
        curr_state: str,
        g_values: Dict[str, float],
        closed_list: Set[str],
        path: Dict[str, Dict[str, Any]]
) -> Tuple[str, float, float]:
    """Process a neighbor node and update path information."""
    neighborId, neighborHeuristic, neighborCost, neighborLatLon = cj.getNeighbourInfo(neighbor_data)

    if neighborId in closed_list:
        return neighborId, 0, float('inf')  # Return infinite f_value to skip this neighbor

    # Calculate new cost
    current_inherited_cost = g_values[curr_state] + neighborCost
    g_values[neighborId] = current_inherited_cost
    f_value = neighborHeuristic + current_inherited_cost

    # Update path dictionary
    curr_latlon = format_coord(cj.getLatLon(curr_state))
    neighbor_latlon = format_coord(neighborLatLon)
    path[str(neighbor_latlon)] = {"parent": str(curr_latlon), "cost": neighborCost}
    print(f"Added to path - Key: {str(neighbor_latlon)}, Parent: {str(curr_latlon)}")

    return neighborId, f_value, current_inherited_cost


def aStar(source: Tuple[float, float], destination: Tuple[float, float]) -> Dict[str, Dict[str, Any]]:
    """
    Implementation of A* pathfinding algorithm.

    Args:
        source: Starting coordinates (lat, lon)
        destination: Target coordinates (lat, lon)

    Returns:
        Dictionary containing the path information
    """
    # Initialize data structures
    open_list: List[Tuple[float, str]] = []  # Priority queue of (f_value, node_id)
    closed_list: Set[str] = set()  # Set of visited nodes
    path: Dict[str, Dict[str, Any]] = {}  # Store path information

    # Initialize search parameters
    sourceID, destID, g_values = initialize_search(source, destination)

    # Add start node to open list
    h_source = cj.calculateHeuristic(source, destination)
    heap.heappush(open_list, (h_source, sourceID))

    # Start timing
    start_time = time.time()

    # Main search loop
    while open_list:
        # Get node with lowest f_value
        _, curr_state = heap.heappop(open_list)

        # Skip if already processed
        if curr_state in closed_list:
            continue

        # Mark as visited
        closed_list.add(curr_state)

        # Check if we reached the goal
        if curr_state == destID:
            print("We have reached the goal")
            break

        # Process neighbors
        neighbors = cj.getNeighbours(curr_state, destination)
        for neighbor in neighbors[curr_state]:
            neighborId, f_value, _ = process_neighbor(
                neighbor,
                curr_state,
                g_values,
                closed_list,
                path
            )

            if f_value != float('inf'):
                heap.heappush(open_list, (f_value, neighborId))

    # Print final path information
    print("\nFinal path dictionary:")
    for key, value in path.items():
        print(f"Key: {key}, Value: {value}")

    print(f"Time taken to find path(in seconds): {time.time() - start_time}")
    return path