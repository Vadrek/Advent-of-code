from collections import defaultdict
from os.path import join, dirname
import re
import networkx as nx
import time
from heapq import heappush, heappop

def get_places_and_tunnels(data):
    rates = {}
    tunnels = set()
    for line in data:
        infos = re.findall(r'[A-Z]{2}|\d+', line)
        place_name = infos[0]
        rate = int(infos[1])
        directions = tuple(infos[2:])
        if rate > 0:
            rates[place_name] = rate
        for dir in directions:
            tunnels.add(tuple(sorted((place_name, dir))))
    return rates, tunnels

def get_shortest_path_length(places, tunnels):
    G = nx.Graph()
    G.add_nodes_from(places)
    G.add_edges_from(tunnels)
    # sp = dict(nx.all_pairs_shortest_path(G))
    dist = dict(nx.all_pairs_shortest_path_length(G))
    return dist

def create_hash(infos):
    (time, pressure, destination, valves) = infos
    hash = '_' + destination + '_' + '-'.join(sorted(valves))
    hash_time = 'P' + str(pressure) + hash
    hash_pressure = 'T' + str(time) + hash
    return hash_time, hash_pressure


def solve(rates, dist, valves_to_open, total_time, start = 'AA', elephant = False):
    states_by_pressure = defaultdict(lambda: -1)
    states_by_time = defaultdict(lambda: total_time + 1)
    best_pressure = 0

    stack = [(total_time, 0, start, valves_to_open, [start])]
    while stack:
        print('len(stack)', len(stack))
        time, pressure, current, valves_to_open, path = heappop(stack)
        # print('time, pressure, current, path', time, pressure, current, path)
        hash_time, hash_pressure = create_hash((time, pressure, current, valves_to_open))
        if states_by_pressure[hash_pressure] >= pressure:
            continue
        else:
            states_by_pressure[hash_pressure] = pressure
        if states_by_time[hash_time] <= time:
            continue
        else:
            states_by_time[hash_time] = time

        for destination in valves_to_open:
            # print('desti', destination, 'time', time, 'rates[destination]', rates[destination])
            new_time = time - dist[current][destination] - 1
            new_pressure = pressure + new_time * rates[destination]
            if new_time > 0:
                heappush(stack, (new_time, new_pressure, destination, valves_to_open-{destination}, path+[destination]))
            
            best_pressure = max(best_pressure, new_pressure)

    return best_pressure

with open(join(dirname(__file__), 'data.txt')) as f:
    data = f.read().splitlines()

rates, tunnels = get_places_and_tunnels(data)
dist = get_shortest_path_length(rates.keys(), tunnels)

start = time.time()
print('PART_1', solve(rates, dist, set(rates.keys()), 30))
end = time.time()
print('seconds :', end - start)

print('PART_2', solve(rates, dist, set(rates.keys()), 26, elephant = True))
