import copy
import time
from Solution import *

stats = {'m_edges_vars': [], 'm_edges_constrs': [], 'm_times_vars': [], 'm_times_constrs': []}


def find_edges(map, root_node, a):
    """
    Linear program for finding edges
    :param map: map structure
    :param root_node: node from constraint tree
    :param a: agent to find path for
    :return: unoptimized model, unevaluated variables
    """
    m_edges = Model('m_edges')
    m_edges.Params.LogToConsole = 0
    edges = m_edges.addVars(map.links, name="flow")
    distance = m_edges.addVars(map.links, name='dist')
    m_edges.setObjective(quicksum(distance), GRB.MINIMIZE)

    m_edges.addConstrs(
        (quicksum(edges[i, j] for i, j in map.links.select('*', j)) ==
         quicksum(edges[j, k] for j, k in map.links.select(j, '*'))
         for j in map.nodes if not ((j == a.start) or (j == a.end))), "node")

    m_edges.addConstrs(
        (quicksum(edges[i, j] for i, j in map.links.select('*', j)) -
         quicksum(edges[j, k] for j, k in map.links.select(j, '*')) == -1
         for j in map.nodes if (j == a.start)), "start_node")

    m_edges.addConstrs(
        (quicksum(edges[i, j] for i, j in map.links.select('*', j)) -
         quicksum(edges[j, k] for j, k in map.links.select(j, '*')) == 1
         for j in map.nodes if (j == a.end)), "end_node")

    if len(root_node.constraints[a.id]) != 0:
        for conflict in root_node.constraints[a.id]:
            if conflict.type == Conflict.EDGE:
                escape_conflict_nodes = tuplelist()
                for _, j in map.links.select(conflict.vertex, '*'):  # find all nodes to escape the conflict
                    if conflict.vertex_prev != j and j != conflict.vertex_next:
                        escape_conflict_nodes.extend([(conflict.vertex, j)])
                if len(escape_conflict_nodes) == 0:  # nowhere to escape
                    m_edges.addConstr(edges[conflict.vertex, conflict.vertex_next] == 0,
                                      f"no_visit_node-{conflict.vertex, conflict.vertex_next}")
                    break
                m_edges.addConstrs(
                    (quicksum(edges[i, j] for i, j in escape_conflict_nodes.select(i, '*')) == 1
                     for i in map.nodes if (i == conflict.vertex)), "edge_node")

    m_edges.addConstrs((distance[i, j] == edges[i, j] * map.nodes[i].distance(map.nodes[j]) for i, j in map.links),
                       "distance")

    return m_edges, edges


def find_path(map, root_node, a):
    """
    Linear program for finding continuous path
    :param map: map structure
    :param root_node: node from constraint tree
    :param a: agent to find path for
    :return: path with continuous time without collisions for a given agent
    """
    try:
        m_edges, edges = find_edges(map, root_node, a)
        m_edges.optimize()
        global stats
        stats['m_edges_vars'].append(len(m_edges.getVars()))
        stats['m_edges_constrs'].append(len(m_edges.getConstrs()))
        m_times = Model('m_times')
        m_times.Params.LogToConsole = 0

        extended_links = tuplelist()
        for i, j in map.links:
            if edges[i, j].x > 0.5:
                for x in range(round(edges[i, j].x)):  # for repeated edges
                    extended_links.append((i, j, x))

        times = m_times.addVars(extended_links, name="time")
        m_times.setObjective(quicksum(times), GRB.MINIMIZE)

        for i, j, l in extended_links:
            k_in = []
            for k, _, n in extended_links.select('*', i):
                k_in.append((k, n))
            if len(k_in) > 1 or i == a.start or i == a.end:
                # number of *->i > 1: repeated visit to i (or i is start/end)
                k_out = []
                for _, k, n in extended_links.select(i, '*'):
                    k_out.append((k, n))
                if i == a.start:  # constraints for start node
                    y = m_times.addVars(math.factorial(len(k_in)) * len(k_out), vtype=GRB.BINARY, name="y")
                    for start in range(len(k_out)):
                        k_out_new = [x for x in k_out if x != k_out[start]]
                        possibilities = [list(zip(x, range(len(k_out_new)))) for x in
                                         itertools.permutations(range(len(k_in)), len(k_out_new))]
                        for possibility in range(len(possibilities)):
                            m_times.addConstr((y[len(k_out) * possibility + start] == 1) >>
                                              (times[i, k_out[start][0], k_out[start][1]] >=
                                               map.nodes[i].distance(
                                                   map.nodes[k_out[start][0]]) / a.speed),
                                              name=f'time_start-{i, k_out[start][0], k_out[start][1]}')
                            for p in possibilities[possibility]:
                                m_times.addConstr((y[len(k_out) * possibility + start] == 1) >>
                                                  (times[i, k_out_new[p[1]][0], k_out_new[p[1]][1]] >=
                                                   times[k_in[p[0]][0], i, k_in[p[0]][1]] + map.nodes[i]
                                                   .distance(map.nodes[k_out_new[p[1]][0]]) / a.speed),
                                                  name=f'k_{i}_{p}')
                    m_times.addConstr(quicksum(y) == 1, name=f'sum_y_start-{i}')
                elif i == a.end:  # constraints for end node
                    y = m_times.addVars(math.factorial(len(k_out)) * len(k_in), vtype=GRB.BINARY, name="y")
                    for end in range(len(k_in)):
                        k_in_new = [x for x in k_in if x != k_in[end]]
                        possibilities = [list(zip(x, range(len(k_out)))) for x in
                                         itertools.permutations(range(len(k_in_new)), len(k_out))]
                        for possibility in range(len(possibilities)):
                            for p in possibilities[possibility]:
                                m_times.addConstr((y[len(k_in) * possibility + end] == 1) >>
                                                  (times[k_in[end][0], i, k_in[end][1]] >=
                                                   times[i, k_out[p[1]][0], k_out[p[1]][1]] + map.nodes[i]
                                                   .distance(map.nodes[k_in[end][0]]) / a.speed),
                                                  name=f'time_end-{i}')
                                m_times.addConstr((y[len(k_in) * possibility + end] == 1) >>
                                                  (times[i, k_out[p[1]][0], k_out[p[1]][1]] >=
                                                   times[k_in_new[p[0]][0], i, k_in_new[p[0]][1]] + map.nodes[i]
                                                   .distance(map.nodes[k_out[p[1]][0]]) / a.speed),
                                                  name=f'k_{i}_{p}')
                    m_times.addConstr(quicksum(y) == 1, name=f'sum_y_end-{i}')
                else:  # repeated visits to i node
                    possibilities = [list(zip(x, range(len(k_out)))) for x in
                                     itertools.permutations(range(len(k_in)), len(k_out))]
                    y = m_times.addVars(len(possibilities), vtype=GRB.BINARY, name="y")

                    for possibility in range(len(possibilities)):
                        for p in possibilities[possibility]:
                            m_times.addConstr(
                                (y[possibility] == 1) >> (times[i, k_out[p[1]][0], k_out[p[1]][1]] >=
                                                          times[k_in[p[0]][0], i, k_in[p[0]][1]] + map.nodes[i]
                                                          .distance(map.nodes[k_out[p[1]][0]]) / a.speed),
                                name=f'k_{i}_{p}')
                    m_times.addConstr(quicksum(y) == 1, name=f'sum_y_node-{i}')

            elif len(k_in) == 1:  # i node was visited only once
                m_times.addLConstr(
                    times[i, j, l] >= times[k_in[0][0], i, k_in[0][1]] + map.nodes[i].distance(map.nodes[j]) / a.speed,
                    name=f'time_node-{i, j, l}')

        if len(root_node.constraints[a.id]) != 0:  # constraints for vertex and overlap conflicts
            for conflict in root_node.constraints[a.id]:
                if conflict.type != Conflict.EDGE:
                    for _, _, l in extended_links.select(conflict.vertex_prev, conflict.vertex):
                        if edges[conflict.vertex_prev, conflict.vertex].x > 0.5 \
                                and conflict.vertex_prev != conflict.vertex:
                            if conflict.type == Conflict.VERTEX:
                                waiting_time = (root_node.agents[conflict.ai].radius
                                                + root_node.agents[conflict.aj].radius) \
                                               / root_node.agents[conflict.aj].speed
                            else:  # overlap conflict
                                waiting_time = conflict.overlap_time
                            if waiting_time < 0.01:
                                waiting_time = 0.01
                            constr = m_times.addLConstr(
                                times[conflict.vertex_prev, conflict.vertex, l] >= conflict.time
                                + waiting_time,
                                name=f'time_conflict_vertex-{conflict.vertex_prev, conflict.vertex, l}')
                            constr.Lazy = 1

        m_times.optimize()
        stats['m_times_vars'].append(len(m_times.getVars()))
        stats['m_times_constrs'].append(len(m_times.getConstrs()))

        return construct_path(times, map, a.start, a.speed, extended_links)

    except (AttributeError, GurobiError):
        # print('>>>ERROR<<<')
        return list()


def calculate_waiting_time(N, i, j, t, nodes):
    """
    Calculates time to wait for agent i
    :param N: node from constraint tree
    :param i: agent who waits
    :param j: agent who moves
    :param t: collision time
    :param nodes: nodes from map
    :return: time to wait or 0
    """
    intersect = N.time_to_wait(i, j, t, nodes)
    if intersect != -1:
        return intersect / N.agents[j].speed
    return 0


def construct_path(times, map, start, speed, extended_links):
    """
    Constructs a continuous path
    :param times: variables from continuous time model
    :param map: map structure
    :param start: start node
    :param speed: agent's speed
    :param extended_links: links from continuous time model
    :return: continuous path
    """
    result = [(start, (0, 0))]
    for i, j, l in extended_links:
        if times[i, j, l].x >= 0.1:
            result.append((j, (times[i, j, l].x, times[i, j, l].x)))
    result.sort(key=lambda x: x[1][1])  # sort by depart time
    for i in range(len(result)):  # depart = arrive + wait
        if i != len(result) - 1:
            j = i + 1
            if map.nodes[result[i][0]].distance(map.nodes[result[j][0]]) / speed \
                    - (result[j][1][1] - result[i][1][0]) < -0.001:
                result[i] = (result[i][0], (result[i][1][0],
                                            result[j][1][0] - map.nodes[result[i][0]]
                                            .distance(map.nodes[result[j][0]]) / speed))
    result.sort(key=lambda x: x[1][1])  # sort by depart time
    return result


def vertex_conflict(i, j):
    """
    Checks if there's a vertex conflict
    :param i: vertex from agent i path
    :param j: vertex from agent j path
    :return: True if collision was detected, False otherwise
    """
    a0, d0 = i[1]
    a1, d1 = j[1]
    if i[0] == j[0] and ((abs(a1 - a0) < 0.01 and abs(d1 - d0) < 0.01)
                         or (a1 <= a0 <= d0 <= d1)
                         or (a0 <= a1 <= d1 <= d0)
                         or (a1 <= a0 <= d1 <= d0)
                         or (a0 <= a1 <= d0 <= d1)):
        return True
    return False


def edge_conflict_no_swap(i, j, path0, path1, i_id, j_id):
    """
    Checks for edge conflict with same direction
    :param i: vertex from agent i path
    :param j: vertex from agent j path
    :param path0: agent i path
    :param path1: agents j path
    :param i_id: agent i id
    :param j_id: agent j id
    :return: agent to wait, vertex of conflict, time to wait or -1,-1,0 if there's no collision
    """
    a0, d0 = path0[i][1]
    a1, d1 = path0[i + 1][1]
    a2, d2 = path1[j][1]
    a3, d3 = path1[j + 1][1]
    if path0[i][0] == path1[j][0] and path0[i + 1][0] == path1[j + 1][0]:
        if d0 <= d2 <= d3 <= d1:
            time = d1 - d3 + d2 - d0
            return i_id, i, time
        elif d2 <= d0 <= d1 <= d3:
            time = d3 - d1 + d0 - d2
            return j_id, j, time
    return -1, -1, 0


def edge_conflict(i, j, path0, path1):
    """
    Checks for edge conflicts with different directions
    :param i: vertex from agent i path
    :param j: vertex from agent j path
    :param path0: agent i path
    :param path1: agent j path
    :return: conflict time or -1 if there's no collision
    """
    a0, d0 = path0[i][1]
    a1, d1 = path0[i + 1][1]
    a2, d2 = path1[j][1]
    a3, d3 = path1[j + 1][1]
    if path0[i][0] == path1[j + 1][0] and path0[i + 1][0] == path1[j][0]:
        if d0 <= d2 < d1 <= d3 \
                or d0 <= d2 <= d3 <= d1 \
                or d2 <= d0 < d3 <= d1 \
                or d2 <= d0 <= d1 <= d3:
            return min(d0, d1, d2, d3)
    return -1


def collision(N, nodes):
    """
    Constructs collisions list
    :param N: node from constraint tree
    :param nodes: nodes from map
    :return: list of fopund collisions
    """
    tuple_agents = list(itertools.combinations(N.agents, 2))
    collisions = []

    for (i, j) in tuple_agents:
        path0 = N.paths[i.id]
        path1 = N.paths[j.id]
        collision = False

        ai = i.get_center_at_time(path0, 0, nodes)
        aj = j.get_center_at_time(path1, 0, nodes)
        d = ai.distance(aj)
        if d <= i.radius + j.radius:  # start nodes are too close
            return None

        for p0 in path0:
            for p1 in path1:
                p0_idx = path0.index(p0)
                p1_idx = path1.index(p1)

                if vertex_conflict(p0, p1):  # vertex conflict
                    collision = True
                    collisions.append(
                        Constraint(i.id, j.id, p0[0], p0[1][0], Conflict.VERTEX,
                                   v_prev=get_prev_node(path0, p0[1][0], True)[0]))
                    collisions.append(
                        Constraint(j.id, i.id, p1[0], p1[1][0], Conflict.VERTEX,
                                   v_prev=get_prev_node(path1, p1[1][0], True)[0]))

                if p0_idx != len(path0) - 1 and p1_idx != len(path1) - 1:
                    edge_conflict_time = edge_conflict(p0_idx, p1_idx, path0, path1)
                    agent_to_wait, edge_no_swap_vertex, edge_no_swap_time \
                        = edge_conflict_no_swap(p0_idx, p1_idx, path0, path1, i.id, j.id)
                    if edge_conflict_time != -1:  # edge conflict
                        collision = True
                        collisions.append(
                            Constraint(i.id, j.id, p0[0], edge_conflict_time, Conflict.EDGE,
                                       v_prev=path0[p0_idx - 1][0], v_next=path0[p0_idx + 1][0]))
                        collisions.append(
                            Constraint(j.id, i.id, p1[0], edge_conflict_time, Conflict.EDGE,
                                       v_prev=path1[p1_idx - 1][0], v_next=path1[p1_idx + 1][0]))
                    if edge_no_swap_vertex != - 1:  # edge conflict
                        collision = True
                        if agent_to_wait == i.id:
                            collisions.append(
                                Constraint(i.id, j.id, path0[edge_no_swap_vertex][0],
                                           path0[edge_no_swap_vertex][1][0], Conflict.OVERLAP, edge_no_swap_time,
                                           v_prev=path0[edge_no_swap_vertex - 1][0]))
                        else:
                            collisions.append(
                                Constraint(j.id, i.id, path1[edge_no_swap_vertex][0],
                                           path1[edge_no_swap_vertex][1][0], Conflict.OVERLAP, edge_no_swap_time,
                                           v_prev=path1[edge_no_swap_vertex - 1][0]))

        if collision:  # find all vertex and edge conflicts first
            continue

        t = 0
        t_stop = max(path0[-1][1][1], path1[-1][1][1])
        t_increment = min(i.speed, j.speed) / 2
        i_vertex = -1
        j_vertex = -1
        i_time = 0
        j_time = 0
        while t < t_stop:  # check for overlap conflict
            ai = i.get_center_at_time(path0, t, nodes)
            aj = j.get_center_at_time(path1, t, nodes)
            d = ai.distance(aj)
            if d <= i.radius + j.radius:
                if ai == nodes[path0[0][0]] and aj == nodes[path1[0][0]]:  # start nodes are too close
                    return None
                prev_i = get_prev_node(path0, t, True)
                prev_j = get_prev_node(path1, t, True)
                next_i = get_next_node(path0, prev_i)
                next_j = get_next_node(path1, prev_j)
                ci = Constraint(i.id, j.id, next_i[0], next_i[1][0], Conflict.OVERLAP)
                cj = Constraint(j.id, i.id, next_j[0], next_j[1][0], Conflict.OVERLAP)

                if ci not in collisions and cj not in collisions and prev_i[0] != prev_j[0]:  # new collision
                    if prev_j[0] != next_i[0]:
                        j_time += calculate_waiting_time(N, j.id, i.id, t, nodes)
                        # sum up all wait time to the first vertex
                        if j_vertex == -1:
                            j_vertex = prev_j
                    if prev_i[0] != next_j[0]:
                        i_time += calculate_waiting_time(N, i.id, j.id, t, nodes)
                        # sum up all wait time to the first vertex
                        if i_vertex == -1:
                            i_vertex = prev_i
            t += t_increment
        if i_vertex != -1:  # overlap conflict
            next_i = get_next_node(path0, i_vertex)
            collisions.append(
                Constraint(i.id, j.id, next_i[0], next_i[1][0], Conflict.OVERLAP, i_time, v_prev=i_vertex[0]))
        if j_vertex != -1:  # overlap conflict
            next_j = get_next_node(path1, j_vertex)
            collisions.append(
                Constraint(j.id, i.id, next_j[0], next_j[1][0], Conflict.OVERLAP, j_time, v_prev=j_vertex[0]))
    return collisions


def find_solution(N, map, start_time):
    """
    Main method to find the solution
    :param N: root node of constraint tree
    :param map: map structure
    :param start_time: start time
    :return: solution if exists or None, calls count, statistics
    """
    global stats
    calls = 0
    all_solutions = [N]
    open = [N]
    while open:

        if time.time() - start_time >= 300:
            print('timeout')
            return None, calls, stats

        open.sort(key=lambda x: x.cost)
        N = open.pop(0)
        collisions = collision(N, map.nodes)

        if collisions is None:
            print('\nStarting points are too close')
            return None, calls, stats

        if len(collisions) == 0:  # solution is found
            print('\nSolution:')
            return N, calls, stats

        for c in collisions:
            N_ = Solution()
            N_.agents = copy.deepcopy(N.agents)
            N_.paths = copy.deepcopy(N.paths)
            N_.constraints = copy.deepcopy(N.constraints.copy())

            N_.constraints[c.ai].append(c)
            result = find_path(map=map, root_node=N_, a=N.agents[c.ai])
            calls += 1
            if len(result) == 0:  # path for current collisions does not exist
                continue
            N_.paths[c.ai] = result
            N_.calculate_cost()
            if N_ not in all_solutions:
                open.append(N_)
                all_solutions.append(N_)

    return None, calls, stats
