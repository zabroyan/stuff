#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <list>
#include <algorithm>
#include <cmath>

#include "../AvoidancePath/Agent.h"
#include "../AvoidancePath/Node.h"
#include "../AvoidancePath/InnerNode.h"
#include "../AvoidancePath/Point.h"

#include "../AvoidancePath/Agent.cpp"
#include "../AvoidancePath/Node.cpp"
#include "../AvoidancePath/InnerNode.cpp"
#include "../AvoidancePath/Point.cpp"


vector<Node> createNodes(int size) {
    vector<Node> nodes;
    int max = 50;
    int min = -50;
    for (int i = 0; i < size; i++) {
        int x = int(random()) % max * 2 + 1 + min;
        int y = int(random()) % max + min;
        Node node = Node(i, x, y);
        nodes.push_back(node);
    }
    return nodes;
}

vector<Node> createInnerNodes(vector<Node> &nodes) {
    for (auto &it : nodes) {
        for (InnerNode &n : it.innerNodes) {
            for (InnerNode &n2 : it.innerNodes) {
                if (n.getNeighbor() == n2.getNeighbor())
                    continue;
                n.addNeighbor(n2);
                n2.addNeighbor(n);
            }
        }
    }
    return nodes;
}

vector<Node> createMap() {
    int nodes_cnt;
    cin >> nodes_cnt;
    vector<Node> nodes = createNodes(nodes_cnt);
    for (int n = 0; n < nodes_cnt; n++) {
        int x, y;
        cin >> x >> y;
        nodes[n].setCoordinates(x, y);
    }
    int edge_cnt;
    cin >> edge_cnt;
    for (int e = 0; e < edge_cnt; e++) {
        int n1, n2;
        cin >> n1 >> n2;
        InnerNode node1 = InnerNode(n1, n2, nodes[n1].getCoordinates(), nodes[n2].getCoordinates());
        InnerNode node2 = InnerNode(n2, n1, nodes[n2].getCoordinates(), nodes[n1].getCoordinates());
        node1.addNeighbor(node2);
        node2.addNeighbor(node1);
        nodes[n1].innerNodes.emplace_back(node1);
        nodes[n2].innerNodes.emplace_back(node2);
    }

    nodes = createInnerNodes(nodes);
    return nodes;
}

Agent readInput(const vector<Node> &nodes) {
    int vrt_cnt;
    vector<Vertex> vertices;
    cin >> vrt_cnt;
    for (int v = 0; v < vrt_cnt; v++) {
        double l, a;
        cin >> l >> a;
        vertices.emplace_back(Vertex(l, a));
    }
    int start, goal, index;
    double speed, rotation_speed;
    cin >> start >> goal >> speed >> rotation_speed >> index;

    return {nodes[start].innerNodes[0], nodes[goal].innerNodes[0], speed, rotation_speed, vertices, index};
}

double pathLength(const vector<pair<Schedule, Node> > &path) {
    double len = 0;
    if (path.empty())
        return 0;
    Node last = path[0].second;
    for (auto &i : path) {
        len += i.second.distance(last);
        last = i.second;
    }
    return len;
}

vector<pair<Schedule, Node> > adjustSchedule(const vector<Node> &path, const Agent &a) {
    vector<pair<Schedule, Node> > result = {};
    double t = 0;
    if (path.empty())
        return {};
    Node prev = path[0];
    double arr_angle = a.angle;
    for (int n = 0; n < path.size(); n++) {
        t += path[n].distance(prev) / a.getSpeed();
        double arrive = t;
        double depart = arrive;
        double dep_angle = arr_angle;
        if (n + 1 != path.size() && !(path[n] == path[n + 1])) {
            InnerNode in = path[n].getINbyNeighbor(path[n + 1].getIndex());
            depart += a.getRotationSpeed() *
                      (abs((in.getAngle() - arr_angle)) <= 180
                       ? abs((in.getAngle() - arr_angle))
                       : abs(abs((in.getAngle() - arr_angle)) - 360));
            dep_angle = in.getAngle();
        }
        result.emplace_back(Schedule(arrive, depart, arr_angle, dep_angle), path[n]);
        prev = path[n];
        arr_angle = dep_angle;
        t = depart;
    }
    return result;
}

vector<Node> buildPath(const Node &start, Node target, map<Node, Node> prev, vector<Node> nodes) {
    vector<Node> path;
    vector<Node> result;
    path.push_back(target);

    while (!(start == target)) {
        target = prev[target];
        path.push_back(target);
    }

    reverse(path.begin(), path.end());

    for (const Node &n : path) {
        if (!result.empty() && result[result.size() - 1] == n)
            continue;
        result.push_back(n);
    }
    return result;
}

vector<Node> BFS(int start, int finish, vector<Node> nodes, int b_start, int b_finish) {
    list<Node> opened;
    list<Node> closed;
    map<Node, Node> prev;
    vector<Node> path;
    path.push_back(nodes[start]);
    opened.push_back(nodes[start]);
    while (!opened.empty()) {
        Node current = opened.front();
        opened.pop_front();
        if (current == nodes[finish]) {
            return buildPath(nodes[start], current, prev, nodes);
        }
        for (const InnerNode &y : current.innerNodes) {
            if (find(opened.begin(), opened.end(), nodes[y.getNeighbor()]) == opened.end()
                && find(closed.begin(), closed.end(), nodes[y.getNeighbor()]) == closed.end()
                && y.getNeighbor() != b_start && y.getNeighbor() != b_finish) {
                opened.push_back(nodes[y.getNeighbor()]);
                prev[nodes[y.getNeighbor()]] = current;
            }
        }
        closed.push_back(current);
    }
    return {};
}

bool notInPath(const InnerNode &in, const vector<Node> &path) {
    int size = path.size();
    for (int i = 0; i < size; i++)
        if (path[i].getIndex() == in.getNeighbor())
            return false;
    return true;
}

vector<Node>
BFS_2(int start, int finish, const vector<Node> &nodes, const vector<Node> &a_path, int a_start, int a_finish) {
    list<Node> opened;
    list<Node> closed;
    map<Node, Node> prev;
    vector<Node> path;
    path.push_back(nodes[start]);
    opened.push_back(nodes[start]);
    while (!opened.empty()) {
        Node current = opened.front();
        opened.pop_front();
        if (current == nodes[finish]) {
            return buildPath(nodes[start], current, prev, nodes);
        }
        for (const InnerNode &y : current.innerNodes) {
            if (find(opened.begin(), opened.end(), nodes[y.getNeighbor()]) == opened.end()
                && find(closed.begin(), closed.end(), nodes[y.getNeighbor()]) == closed.end()
                && notInPath(y, a_path)
                && y.getNeighbor() != a_start && y.getNeighbor() != a_finish) {
                opened.push_back(nodes[y.getNeighbor()]);
                prev[nodes[y.getNeighbor()]] = current;
            }
        }
        closed.push_back(current);
    }
    return {};
}


int main() {
    vector<Node> nodes = createMap();
    Agent a = readInput(nodes);
    Agent b = readInput(nodes);
    vector<Node> a_path = BFS(a.getStart().getParent(), a.getGoal().getParent(), nodes, b.getStart().getParent(),
                              b.getGoal().getParent());
    b.final_path = adjustSchedule(
            BFS_2(b.getStart().getParent(), b.getGoal().getParent(), nodes, a_path, a.getStart().getParent(),
                  a.getGoal().getParent()), b);
    a.final_path = adjustSchedule(a_path, a);
    a.path = a.final_path;
    b.path = b.final_path;
    cout << "....................................................." << endl << endl;
    cout << "\t\t\t\tRESULT:\n\n";
    if (a.final_path.empty()) cout << "A: NO PATH\n";
    else {
        cout << "path length = " << pathLength(a.final_path) << endl;
        cout << "time = " << a.final_path[a.final_path.size() - 1].first.depart << endl;
        cout << a;
    }
    if (b.final_path.empty()) cout << "B: NO PATH\n";
    else {
        cout << "path length = " << pathLength(b.final_path) << endl;
        cout << "time = " << b.final_path[b.final_path.size() - 1].first.depart << endl;
        cout << b;
    }


    return 0;
}
