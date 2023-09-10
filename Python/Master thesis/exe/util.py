from Solution import *
import matplotlib.pyplot as plt
import random
import os.path


def read_input(input_=None):
    """
    Takes user input and parses it into arguments
    :param input_: input from command line or None
    :return: list of agents, map
    """
    try:
        if input_ is None:
            input_ = input('Enter map_name k_number scenario_name (or random keyword and agents count):')
        while len(input_.split()) < 3:
            input_ = input('Please enter a valid input:')
        input_ = input_.split()
        filename = input_[0]
        while True:
            if os.path.exists(filename) is False:
                print(f'{filename} does not exist')
                filename = input('Please enter a valid map name:')
            else:
                break
        k = input_[1]
        while True:
            if not k.isdigit() or int(k) not in (2, 3, 4):
                k = input('Please enter a valid k (2, 3 or 4):')
            else:
                k = int(k)
                break
        scenario = input_[2]
        random_pos = False
        agents_cnt = 0
        while True:
            if scenario == 'random':
                random_pos = True
                break
            elif os.path.exists(scenario) is False:
                scenario = input('Please enter a valid scenario name or random keyword:')
            else:
                break
        if random_pos:
            if len(input_) != 4:
                while True:
                    agents_cnt = input('You chose a random placement. Please enter an agents count:')
                    if agents_cnt.isdigit() and int(agents_cnt) > 0:
                        agents_cnt = int(agents_cnt)
                        break
            else:
                agents_cnt = input_[3]
                while True:
                    if agents_cnt.isdigit() and int(agents_cnt) > 0:
                        agents_cnt = int(agents_cnt)
                        break
                    else:
                        agents_cnt = input('Please enter a valid agents count:')

        if random_pos:
            return read_map(map_name=filename, k=k, random_pos=random_pos, agents_cnt=agents_cnt)
        else:
            return read_map(map_name=filename, k=k, scenario=scenario)
    except:
        print('Something went wrong. Please try again.')
        return None, None


def read_map(map_name, k=3, scenario=None, random_pos=False, agents_cnt=1, map=None):
    """
    Creates agents list and map structure
    :param map_name: map filename
    :param k: k from 2^k neighbors method, default is 3
    :param scenario: scenario name or None, default is None
    :param random_pos: True if random placement is chosen, False otherwise, default is False
    :param agents_cnt: agents count for random placement, default is 1
    :return: agents list, map structure
    """
    try:
        if map is not None:
            m = map
            node = node = len(m.nodes)
        else:
            f = open(map_name, "r")
            lines = f.readlines()
            m = Map()
            h = len(lines)
            w = len(lines[0].strip())
            node = 0
            for i in range(0, h):
                for j in range(0, w):
                    if lines[i][j] == '.':
                        m.add_node(node, i, j)
                        node += 1
            for n in m.nodes:
                x, y = m.nodes[n]
                for i in range(min(x - 1, x - k + 2), max(x + 2, x + k - 1)):
                    for j in range(min(y - 1, y - k + 2), max(y + 2, y + k - 1)):
                        if -1 < i < h and -1 < j < w and lines[i][j] == '.' and m.points[(i, j)] != n \
                                and (abs(i - x) + abs(j - y) <= k - 1):

                            if (i == x and abs(j - y) > 1) or (j == y and abs(i - x) > 1):
                                continue
                            m.add_link(n, m.points[(i, j)])
        agents = []
        starts = []
        ends = []
        speeds = []
        radii = []
        if not random_pos and scenario is None:
            print('Changing random placement to True')
            random_pos = True
        if random_pos:
            for _ in range(agents_cnt):
                start = random.randint(0, node - 1)
                while start in starts:
                    start = random.randint(0, node - 1)
                starts.append(start)
                end = random.randint(0, node - 1)
                while end in ends:
                    end = random.randint(0, node - 1)
                ends.append(end)
                radii.append(random.randint(10, 20) / 10.)
                speeds.append(random.randint(1, 4))
        else:
            scenario = open(scenario, 'r').readlines()
            for i in range(0, len(scenario)):
                starts.append(scenario[i].split()[0])
                ends.append(scenario[i].split()[1])
                speeds.append(scenario[i].split()[2])
                radii.append(float(scenario[i].split()[3]))
        for i in range(0, len(starts)):
            if starts[i] == ends[i]:
                return None, None
            agents.append(Agent(id=i, start=int(starts[i]), end=int(ends[i]), speed=int(speeds[i]),
                                radius=radii[i]))
            print(agents[-1])
        return agents, m
    except:
        print('error while reading a map', map_name)
        return None, None


def change_format(map, filename):
    """
    Changes map format for SMT-CBS algorithm
    :param map: map to change format for
    :param filename: output filename
    """
    out = open(filename, 'a')
    print(f'Locations: {len(map.nodes)}', file=out)
    for n in map.nodes:
        print(f'{n}: {map.nodes[n].x}.000, {map.nodes[n].y}.000', file=out)
    print(f'Vertices: {len(map.nodes)}', file=out)
    print(f'Edges: {int(len(map.links) / 2)}', file=out)
    added = []
    for e in map.links:
        if e not in added and (e[1], e[0]) not in added:
            added.append(e)
            print('{' + f'{e[0]},{e[1]}' + '}', file=out)


def draw_map(map, paths=None, filename='img', ask_input=False):
    """
    Draws map with or without given paths, saves to filename.png
    :param map: map to draw
    :param paths: paths to draw if given, default is None
    :param filename: output filename, default if img
    :param ask_input: True to ask user for the input, False otherwise, default is False
    """
    if ask_input:
        draw = input('\nDo you want to draw a map? Press NO for No, press anything else for Yes:')
        if draw.upper() == 'NO':
            return
        draw = input('Do you want to draw paths? Press NO for No, press anything else for Yes:')
        if draw.upper() == 'NO':
            paths = None
        filename = input('Enter an output filename:')
        if len(filename) == 0:
            filename = 'img'
    x = [map.nodes[n].x for n in map.nodes]
    y = [map.nodes[n].y for n in map.nodes]

    if len(x) <= 100:
        plt.plot(y, x, 'co')
        for n in map.nodes:
            plt.annotate(n, (map.nodes[n].y, map.nodes[n].x), xytext=(map.nodes[n].y + 0.2, map.nodes[n].x + 0.1))

    edges = []
    if paths is not None:
        markers = ['#00ff00', '#0000ff', '#ff0000', '#ffff00', '#006400', '#00ffff', '#ff00ff', '#6495ed', '#b03060',
                   '#ffe4b5']
        markers_cnt = len(paths) - len(markers)
        if markers_cnt > 0:
            for _ in range(markers_cnt):
                markers.append("#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)]))
        for path in range(len(paths)):
            padding = path / 50
            for p in range(1, len(paths[path])):
                x1, y1 = map.nodes[paths[path][p - 1][0]]
                x2, y2 = map.nodes[paths[path][p][0]]
                edges.append((paths[path][p - 1][0], paths[path][p][0]))
                edges.append((paths[path][p][0], paths[path][p - 1][0]))
                if p == 1:
                    plt.plot([y1 + 0, y2 + 0], [x1 + padding, x2 + padding], markers[path], label=f'agent {path}',
                             zorder=10)
                else:
                    plt.plot([y1 + 0, y2 + 0], [x1 + padding, x2 + padding], markers[path], zorder=10)

    for n1, n2 in map.links:
        if (n1, n2) not in edges and (n2, n1) not in edges:
            x1, y1 = map.nodes[n1]
            x2, y2 = map.nodes[n2]
            plt.plot([y1, y2], [x1, x2], 'grey', alpha=0.1, zorder=0)

    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.gca().invert_yaxis()
    if paths is not None:
        plt.legend()
    plt.savefig(f'{filename}.png', dpi=300)
    print(f'Picture is saved as {filename}.png')


def print_stats(S, map, start, end, calls, stats):
    """
    Prints statistics for the solution
    :param S: solution
    :param map: map structure
    :param start: start time
    :param end: end time
    :param calls: number of calls
    :param stats: list of statistics
    """
    nodes_in_paths = [len(x) for x in S.paths]
    conflicts = {Conflict.EDGE: 0, Conflict.VERTEX: 0, Conflict.OVERLAP: 0}
    for constraint in S.constraints:
        for c in S.constraints[constraint]:
            conflicts[c.type] += 1
    print('\nTime:', round(end - start, 3), 's')
    print("Calls:", calls + len(S.agents))
    print(conflicts)
    print(f'№ of nodes: {len(map.nodes)}, № of edges: {len(map.links)}')
    print('Average № of nodes in paths:', sum(nodes_in_paths) / len(nodes_in_paths))
    print('Total № of nodes in paths:', sum(nodes_in_paths))
    print('Average № of vars in edge model:',
          round(sum(stats['m_edges_vars']) / len(stats['m_edges_vars']), 2))
    print('Average № of constrs in edge model:',
          round(sum(stats['m_edges_constrs']) / len(stats['m_edges_constrs']), 2))
    print('Average № of vars in time model:',
          round(sum(stats['m_times_vars']) / len(stats['m_times_vars']), 2))
    print('Average № of constrs in time model:',
          round(sum(stats['m_times_constrs']) / len(stats['m_times_constrs']), 2))
