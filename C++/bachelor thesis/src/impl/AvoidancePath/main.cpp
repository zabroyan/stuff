#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <set>
#include <list>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include "Node.h"
#include "Agent.h"

using namespace std;

/**
 * create vector of nodes with random coordinates
 * @param size - number of nodes
 * @return vector of nodes
 */
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

/**
 * connect inner nodes inside one big node
 * @param nodes - vector of nodes
 * @return vector of nodes with connected inner nodes
 */
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

/**
 * calculate the whole path length
 * @param path - vector of nodes (path)
 * @return length
 */
double pathLength(const vector<Node> &path) {
    double len = 0;
    if (path.empty())
        return 0;
    Node last = path[0];
    for (auto &i : path) {
        len += i.distance(last);
        last = i;
    }
    return len;
}

/**
 * calculate the whole path length
 * @param path - vector of nodes (path)
 * @return length
 */
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

/**
 * check either given inner node is in the path
 * @param in - inner node to check
 * @param path
 * @return true if it isn't in the path, false otherwise
 */
bool notInPath(const InnerNode &in, const vector<Node> &path) {
    int size = path.size();
    for (int i = 0; i < size; i++)
        if (path[i].getIndex() == in.getNeighbor())
            return false;
    return true;
}

/**
 * check either given inner node is in the path
 * @param n - index of node to check
 * @param path
 * @return true if it isn't in the path, false otherwise
 */
bool notInPath(int n, const vector<pair<Schedule, Node> > &path) {
    int size = path.size();
    for (int i = 0; i < size; i++)
        if (path[i].second.getIndex() == n)
            return false;
    return true;
}

/**
 *
 * @param path_a
 * @param path_b
 * @param index_a
 * @param index_b
 * @return first different node if agents have same paths before indexes index_a/b
 */
int findDiffNode(const vector<pair<Schedule, Node> > &path_a, const vector<pair<Schedule, Node> > &path_b, int index_a,
                 int index_b) {
    for (int n = index_a; n >= 0; n--) {
        if (path_a[n].second.getIndex() != path_b[index_b].second.getIndex())
            return n;
        if (index_b == 0 && n != 0) return n - 1;
        if (index_b == 0) return -1;
        index_b--;
    }
    return -1;
}

/**
 * comparator for 2 paths
 * @param p1
 * @param p2
 * @return true if length of p1 is shorter than length of p2
 */
bool comparePath(const vector<Node> &p1, const vector<Node> &p2) {
    return (pathLength(p1) < pathLength(p2));
}

/**
 * find all paths from start node to finish node, ordered by its length asc
 * @param start - index of start node
 * @param finish - index of finish node
 * @param nodes - vector of nodes
 * @return all paths from start to finish
 */
vector<vector<Node> > getPaths(int start, int finish, const vector<Node> &nodes) {
    vector<vector<Node> > result;
    queue<vector<Node> > q;
    vector<Node> path;
    path.push_back(nodes[start]);
    q.push(path);
    while (!q.empty()) {
        path = q.front();
        q.pop();
        Node last = path[path.size() - 1];
        if (last == nodes[finish]) {
            result.push_back(path);
        }
        for (const InnerNode &in : last.innerNodes) {
            if (notInPath(in, path) && in.getNeighbor() != start) {
                vector<Node> new_path(path);
                new_path.push_back(nodes[in.getNeighbor()]);
                q.push(new_path);
            }
        }
    }
    sort(result.begin(), result.end(), comparePath);
    return result;
}

/**
 * reads map description from input
 * @return vector of nodes (map)
 */
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

bool edgeConflict(Agent &a, Agent &b, int index, const vector<Node> &nodes, int escape_node);

bool vertexConflict(Agent &a, Agent &b, int index, const vector<Node> &nodes);

bool atGoal(Agent &a, Agent &b, int index, int b_index, const vector<Node> &nodes);

bool findPath(const vector<Node> &nodes, Agent &a, Agent &b);

/**
 * check if there's already path exists
 * @param a
 * @param b
 * @return true if it exists, false otherwise
 */
bool pathExists(Agent &a, Agent &b) {
    return !a.final_path.empty() && !b.final_path.empty();
}

/**
 *calculate arrive and depart time for each node
 * @param path
 * @param a - agent
 * @return vector of pair time-node
 */
vector<pair<Schedule, Node> > adjustSchedule(const vector<Node> &path, const Agent &a) {
    vector<pair<Schedule, Node>> result = {};
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

/**
 *calculate arrive and depart time for each node
 * @param path
 * @param a - agent
 * @param startNode - start adjusting from this node
 * @param index - wait at this node
 * @param waitTime - time to wait
 * @param angle - angle to rotate
 * @return vector of pair time-node
 */
void adjustSchedule(vector<pair<Schedule, Node> > &path,
                    const Agent &a, int startNode, int index = -1, double waitTime = 0, double angle = -1) {
    if (path.empty())
        return;

    double t;
    if (startNode == index && waitTime != 0 && angle == -1) { //adding waiting
        path[startNode].first.depart += waitTime;
        startNode++;
    }
    t = startNode > 0 ? path[startNode - 1].first.depart : path[startNode].first.arrive;
    Node prev = startNode > 0 ? path[startNode - 1].second : path[startNode].second;
    for (int i = startNode; i < path.size(); i++) {

        t += path[i].second.distance(prev) / a.getSpeed(); //adding distance
        double arrive = t;
        double depart = arrive;
        double arr_angle = i == 0 ? a.angle : path[i - 1].first.dep_angle;
        double dep_angle = i == path.size() - 1 ? arr_angle : path[i + 1].first.arr_angle;
        if (angle != -1) {
            cout << "--------------------------ROTATION--------------------\n";
            depart += a.getRotationSpeed() * angle + waitTime;
            dep_angle = fmod(arr_angle + angle, 360);
            path[i].first.arrive = arrive;
            path[i].first.depart = depart;
            path[i].first.arr_angle = arr_angle;
            path[i].first.dep_angle = dep_angle;
            return;
        } else if (i + 1 != path.size() && !(path[i].second == path[i + 1].second)) { //adding rotation
            InnerNode in = path[i].second.getINbyNeighbor(path[i + 1].second.getIndex());
            depart += a.getRotationSpeed() *
                      (abs((in.getAngle() - arr_angle)) <= 180
                       ? abs((in.getAngle() - arr_angle))
                       : abs(abs((in.getAngle() - arr_angle)) - 360));
            dep_angle = in.getAngle();
        }
        path[i].first.arrive = arrive;
        path[i].first.depart = depart;
        path[i].first.arr_angle = arr_angle;
        path[i].first.dep_angle = dep_angle;

        prev = path[i].second;
        t = depart;
    }
}

/**
 *
 * @param a - agent
 * @param b - agent
 * @param i - a's position
 * @param b_now - b's position
 * @param nodes
 * @return true if there's a vertex conflict when agent a is at node i and agent b is at node b_now.first/second
 */
bool checkVertexConflict1(Agent &a, Agent &b, int i,
                          pair<pair<Schedule, Node>, pair<Schedule, Node> > &b_now,
                          const vector<Node> &nodes) {
    if (a.path[i] == b_now.second
        || (a.path[i].first.arrive <= b_now.second.first.depart
            && a.path[i].first.depart >= b_now.second.first.arrive
            && a.path[i].second == b_now.second.second)
        || (a.path[i].first.arrive >= b_now.second.first.depart
            && a.path[i].first.depart <= b_now.second.first.arrive
            && a.path[i].second == b_now.second.second)
        || (a.path[i].first.arrive <= b_now.first.first.depart
            && a.path[i].first.depart >= b_now.first.first.arrive
            && a.path[i].second == b_now.first.second)
        || (a.path[i].first.arrive >= b_now.first.first.depart
            && a.path[i].first.depart <= b_now.first.first.arrive
            && a.path[i].second == b_now.first.second)) { //at vertex
        cout << "(1) VERTEX CONFLICT AT AGENT #" << a.index << " NODE #" << a.path[i].second.getIndex() << endl << endl;
        return vertexConflict(a, b, i, nodes);
    }
    return false;
}

/**
 *
 * @param a - agent
 * @param b - agent
 * @param i - a's position
 * @param nodes
 * @return true if one agent finished its path but another has to use this node
 */
bool checkVertexConflict2(Agent &a, Agent &b, int i, const vector<Node> &nodes) {
    int b_prev = b.getPrevNode(a.path[i].first.depart);
    if (b_prev == b.path.size() - 1 //b is at goal
        && b.path[b_prev].second.getIndex() == a.path[i].second.getIndex()) //a is at b's goal
    {
        cout << "(2) VERTEX CONFLICT AT AGENT #" << a.index << " NODE #" << a.path[i].second.getIndex() << endl << endl;
        cout << "_____________________________________________________\n";
        if (atGoal(b, a, b_prev, i, nodes)) return true;
    } else if (i == a.path.size() - 1 //a is at goal
               && b.goesThroughGoal(a.path[i].first.depart,
                                    a.getGoal().getParent())) { //b goes through a's goal after a finished its move
        cout << "(2) VERTEX CONFLICT AT AGENT #" << a.index << " NODE #" << a.path[i].second.getIndex() << endl << endl;
        cout << "_____________________________________________________\n";
        if (atGoal(a, b, i, b_prev == b.path.size() - 1
                            ? b_prev : b.getPrevNode(a.path[i].first.depart), nodes))
            return true;
    }
    return false;
}

/**
 *
 * @param a - agent
 * @param b - agent
 * @param i - a's position
 * @param nodes
 * @return true is there's an edge conflict
 */
bool checkEdgeConflict1(Agent &a, Agent &b, int i, const vector<Node> &nodes) {
    /** same edge       y-------x
    *                       x-----y
    */
    int b_prev = b.getPrevNode(a.path[i].first.depart);
    if (i > 0
        && b.path[b_prev].second == a.path[i].second
        &&
        (b_prev == b.path.size() - 1 ? b.path[b_prev].second : b.path[b_prev + 1].second) == a.path[i - 1].second) {
        cout << "(1) EDGE CONFLICT BETWEEN AGENT #" << a.index << " NODE #" << a.path[i - 1].second.getIndex()
             << " --- NODE #" << a.path[i].second.getIndex() << endl
             << endl;
        cout << "_____________________________________________________\n";
        edgeConflict(a, b, i - 1, nodes, -1);
        edgeConflict(b, a, b.path[b_prev].second.getIndex(), nodes, -1);
        return true;
    }
    return false;
}

/**
 *
 * @param a - agent
 * @param b - agent
 * @param i - a's position
 * @param nodes
 * @return true if there's an edge conflict
 */
bool checkEdgeConflict2(Agent &a, Agent &b, int i, const vector<Node> &nodes) {
    /**same edge          x------y
    *                 y-----x
    */
    int b_prev = b.getPrevNode(a.path[i].first.depart);
    if (i < a.path.size() - 1
        && b.path[b_prev].second == a.path[i + 1].second
        && (b_prev == b.path.size() - 1 ? b.path[b_prev].second : b.path[b_prev + 1].second) == a.path[i].second) {
        cout << "(2) EDGE CONFLICT BETWEEN AGENT #" << a.index << " NODE #" << a.path[i].second.getIndex()
             << " --- NODE #" << a.path[i + 1].second.getIndex() << endl
             << endl;
        cout << "_____________________________________________________\n";
        edgeConflict(a, b, i, nodes, -1);
        edgeConflict(b, a, b.path[b_prev].second.getIndex(), nodes, -1);
        return true;
    }
    return false;
}

/**
 *
 * @param waitingTime - time to wait
 * @param a - moving agent
 * @param b - waiting agent
 * @param t - time of conflict
 * @param a_coord - a's center
 * @param b_coord - b's center
 * @param nodes
 * @param vertex_conflict - was it vertex conflict or another one
 * @return true conflict was resolved
 */
bool moving(double waitingTime, Agent &a, Agent &b, double t, Point a_coord, Point b_coord, const vector<Node> &nodes,
            int vertex_conflict = 0) {
    if (pathExists(a, b)) return false;
    if (waitingTime < EPS) return false;
    if (a.getPrevNode(t) == a.path.size() - 1) return false;
    if (b.getPrevNode(t) == b.path.size() - 1) return false;
    Point new_a_coord = a_coord.getVertex(waitingTime * a.getSpeed(), a.getCurrentAngle(t));
    if (new_a_coord.atInterval(b_coord, nodes[a.getPrevNode(t) + 1].getCoordinates())) return false;
    cout << "DISTANCE CONFLICT AT t" << t << endl;
    cout << "AGENT #" << b.index << " WAITS FOR " << waitingTime << " AT NODE #"
            << b.path[b.getPrevNode(t) - vertex_conflict].second.getIndex()
            << endl << endl;
    cout << "_____________________________________________________\n";
    adjustSchedule(b.path, b, b.getPrevNode(t) - vertex_conflict, b.getPrevNode(t) - vertex_conflict, waitingTime);
    findPath(nodes, a, b);
    return true;
}

/**
 *
 * @param a - rotating agent
 * @param b - another agent
 * @param a_coord - a's center
 * @param b_coord - b's center
 * @param b_edge - b's closest point to a
 * @param t - time of conflict
 * @param nodes
 * @return true if conflict was resolved
 */
bool rotation(Agent &a, Agent &b, Point a_coord, Point b_coord, Point b_edge, double t, const vector<Node> &nodes) {
    if (pathExists(a, b)) return false;
    double rotation = a.calcRotation(b_edge, b_coord, a_coord, t);

    if (rotation > EPS) { //agent a is rotating
        double waitingTime = b.calcWaitingTime(b_coord, a_coord, a, t, 0);
        if (waitingTime < EPS) return false;
        Point new_b_coord = b_coord.getVertex(waitingTime * b.getSpeed(), b.getCurrentAngle(t));
        if (new_b_coord.atInterval(a_coord, nodes[b.getPrevNode(t) + 1].getCoordinates())) return false;

        adjustSchedule(b.path, b, b.getPrevNode(t), b.getPrevNode(t), rotation);
        cout << "DISTANCE CONFLICT AT t" << t << endl;
        if (a.getIndexByTime(t) != a.path.size() - 1) { //agent a after rotation continues moving
            adjustSchedule(a.path, a, a.getPrevNode(t), a.getPrevNode(t),
                           waitingTime, rotation / a.getRotationSpeed());
            int a_prev = a.getPrevNode(t);
            double a_next_arrive = a.path[a_prev].first.depart;
            double a_next_arr_angle = a.path[a_prev].first.dep_angle;
            double a_next_dep_angle = a.path[a_prev + 1].first.arr_angle;
            double a_next_depart = a_next_arrive + a.getRotationSpeed() * abs(a_next_arr_angle - a_next_dep_angle);
            Schedule a_next_sch = Schedule(a_next_arrive, a_next_depart, a_next_arr_angle, a_next_dep_angle);
            pair<Schedule, Node> tmp = make_pair(a_next_sch, a.path[a_prev].second);
            a.path.insert(a.path.begin() + a_prev + 1, tmp);
            adjustSchedule(a.path, a, a_prev + 2);
            cout << "AGENT #" << a.index << " ROTATES " << rotation / a.getRotationSpeed() << " THEN WAITS FOR "
                 << waitingTime << " AT NODE #"
                 << a.path[a_prev].second.getIndex() << endl;
        } else { //agent a is at its goal
            a.path[a.getIndexByTime(t)].first.dep_angle += rotation / a.getRotationSpeed();
            a.path[a.getIndexByTime(t)].first.depart += rotation;
            cout << "AGENT #" << a.index << " ROTATES " << rotation / a.getRotationSpeed() << " AT NODE #"
                 << a.path[a.getIndexByTime(t)].second.getIndex() << endl;
        }
        cout << "AGENT #" << b.index << " WAITS FOR " << rotation << " AT NODE #"
             << b.path[b.getPrevNode(t)].second.getIndex()
             << endl << endl << "_____________________________________________________\n";
        findPath(nodes, a, b);
        return true;
    }
    vector<pair<Schedule, Node> > a_old_path = a.index == 0 ? a.path : b.path;
    vector<pair<Schedule, Node> > b_old_path = b.index == 1 ? b.path : a.path;

    //rotation wasn't successful, so someone has to move
    bool moving_a = moving(a.calcWaitingTime(a_coord, b_coord, b, t, 0),
            a, b, t, a_coord, b_coord, nodes, 0);
    if (moving_a) {
        a.path = a.index == 0 ? a_old_path : b_old_path;
        b.path = b.index == 1 ? b_old_path : a_old_path;
    }
    bool moving_b = moving(b.calcWaitingTime(b_coord, a_coord, a, t, 0),
            b, a, t, b_coord, a_coord, nodes, 0);
    if (moving_b) {
        a.path = a.index == 0 ? a_old_path : b_old_path;
        b.path = b.index == 1 ? b_old_path : a_old_path;
    }
    return moving_a || moving_b;
}

/**
 * @param a - agent
 * @param b - agent
 * @param i - checking distance between a.path[i] and a.path[i+1] 
 * @param nodes 
 * @return true if conflict was detected  
 */
bool checkDistance(Agent &a, Agent &b, int i,
                   const vector<Node> &nodes) {
    if (i + 1 == a.path.size()) return false;
    double t = a.path[i].first.arrive;
    while (t < a.path[i + 1].first.arrive) {
        if (pathExists(a, b)) return false;
        Point b_coord = b.getCoord(t);
        Point a_coord = a.getCoord(t);
        Point a_edge = a.getCoordAtEdge(a_coord, b_coord, a.getCurrentAngle(t));
        Point b_edge = b.getCoordAtEdge(b_coord, a_coord, b.getCurrentAngle(t));

        if (a_edge.atInterval(b_coord, b_edge) || b_edge.atInterval(a_coord, a_edge)
            || (a_coord.atInterval(b_coord, b_edge)) || (b_coord.atInterval(a_coord, a_edge))) { //conflict
            vector<pair<Schedule, Node> > a_old_path = a.index == 0 ? a.path : b.path;
            vector<pair<Schedule, Node> > b_old_path = b.index == 1 ? b.path : a.path;

            if (a.getIndexByTime(t) == -1 && b.getIndexByTime(t) == -1) { //both are moving
                bool moving_a = moving(a.calcWaitingTime(a_coord, b_coord, b, t, 0),
                                       a, b, t, a_coord, b_coord, nodes);
                if (moving_a) {
                    a.path = a.index == 0 ? a_old_path : b_old_path;
                    b.path = b.index == 1 ? b_old_path : a_old_path;
                }
                bool moving_b = moving(b.calcWaitingTime(b_coord, a_coord, a, t, 0),
                                       b, a, t, b_coord, a_coord, nodes);
                if (moving_b) {
                    a.path = a.index == 0 ? a_old_path : b_old_path;
                    b.path = b.index == 1 ? b_old_path : a_old_path;
                }
                if (moving_a || moving_b)
                    return true;
            } else if (a.getIndexByTime(t) != -1 && b.getIndexByTime(t) == -1) { //a is at node, b is moving
                if (rotation(a, b, a_coord, b_coord, b_edge, t, nodes)) return true;
                a.path = a.index == 0 ? a_old_path : b_old_path;
                b.path = b.index == 1 ? b_old_path : a_old_path;
            } else if (a.getIndexByTime(t) == -1 && b.getIndexByTime(t) != -1) { //a is moving, b is at node
                if (rotation(b, a, b_coord, a_coord, a_edge, t, nodes)) return true;
                a.path = a.index == 0 ? a_old_path : b_old_path;
                b.path = b.index == 1 ? b_old_path : a_old_path;
            }
        }
        t += 0.1; //step
    }

    return false;
}

/**
 *
 * @param nodes - vector of nodes
 * @param a - agent
 * @param b - agent
 * @return true if path was found
 */
bool findPath(const vector<Node> &nodes, Agent &a, Agent &b) {
    bool final_path = true;
    if (pathExists(a, b)) {
        return true;
    }

    cout << a << b;

    if (pathLength(b.path) > pathLength(a.path)) {
        swap(a, b);
    }
    for (int i = 0; i < a.path.size(); i++) { //checking for vertex/edge conflicts
        pair<pair<Schedule, Node>, pair<Schedule, Node> > b_now = b.atTime(a.path[i].first.depart);
        if (checkVertexConflict1(a, b, i, b_now, nodes)
            || checkVertexConflict2(a, b, i, nodes)
            || checkEdgeConflict1(a, b, i, nodes)
            || checkEdgeConflict2(a, b, i, nodes)) {
            final_path = false;
        }
    }
    if (final_path) {
        for (int i = 0; i < a.path.size(); i++) { //checking for overlap conflict
            if (checkDistance(a, b, i, nodes)) {
                final_path = false;
            }
        }

    }
    if (final_path && !pathExists(a, b)) { //no conflicts

        a.final_path = a.path;
        b.final_path = b.path;
        a.path = a.final_path;
        b.path = b.final_path;
    }

    return final_path;
}

/**
 * initialisation of paths searching
 * @param nodes
 * @param a
 * @param b
 */
void init(const vector<Node> &nodes, Agent &a, Agent &b) {
    a.path = adjustSchedule(getPaths(a.getStart().getParent(), a.getGoal().getParent(), nodes).front(), a);
    b.path = adjustSchedule(getPaths(b.getStart().getParent(), b.getGoal().getParent(), nodes).front(), b);
    a.final_path = {};
    b.final_path = {};

    findPath(nodes, a, b);
}

/**
 * create a new path when there's an edge conflict
 * @param a - agent
 * @param b - agent
 * @param index - index of conflict
 * @param nodes - vector of nodes
 * @return true if conflict was resolved
 */
bool edgeConflict(Agent &a, Agent &b, int index, const vector<Node> &nodes, int escape_node) {
    vector<pair<Schedule, Node> > a_old_path = a.index == 0 ? a.path : b.path;
    vector<pair<Schedule, Node> > b_old_path = b.index == 1 ? b.path : a.path;
    if (a.path[index].second.innerNodes.size() > 1) {

        for (const InnerNode &in : a.path[index].second.innerNodes) {
            if (in.getNeighbor() != a.path[index + 1].second.getIndex()
                && in.getNeighbor() != a.path[index].second.getIndex()
                && (index == 0
                    || (index > 0 && in.getNeighbor() != a.path[index - 1].second.getIndex()))) {
                vector<vector<Node> > tmp = getPaths(in.getNeighbor(), a.getGoal().getParent(), nodes);
                for (auto &i : tmp) {
                    vector<pair<Schedule, Node> > i_t = adjustSchedule(i, a);
                    if (!notInPath(escape_node, i_t) || !notInPath(a.path[index].second.getIndex(), i_t)) continue;
                    a.path.erase(a.path.begin() + index + 1, a.path.end());
                    a.path.insert(a.path.begin() + index + 1, i_t.begin(), i_t.end());
                    adjustSchedule(a.path, a, index);
                    if (findPath(nodes, a, b)) {
                        a.path = a.index == 0 ? a_old_path : b_old_path;
                        b.path = b.index == 1 ? b_old_path : a_old_path;
                        return true;
                    }
                    a.path = a.index == 0 ? a_old_path : b_old_path;
                    b.path = b.index == 1 ? b_old_path : a_old_path;
                }
            }
        }
    }
    if (index != 0)
        if (edgeConflict(a, b, index - 1, nodes, escape_node)) return true;
    return false;
}

/**
 *
 * @param tmp - vector of paths
 * @param path
 * @return true if there's no edge conflicts between path and all paths in tmp
 */
bool checkPaths(const vector<vector<Node> > &tmp, const vector<pair<Schedule, Node> > &path) {
    for (auto &i : tmp) {
        for (int j = 0; j < i.size(); j++) {
            if (j != path.size() - 1 && i[j].getIndex() == path[j + 1].second.getIndex()
                                        && j != i.size() - 1 && i[j + 1].getIndex() == path[j].second.getIndex())
                return false;
        }
    }
    return true;
}

/**
 * create another path when agent a is at its goal but agent b has to go through this node
 * @param a - agent
 * @param b - agent
 * @param index - index of a's goal
 * @param b_index - b's position
 * @param nodes - vector of nodes
 * @return true if conflict was resolved
 */
bool atGoal(Agent &a, Agent &b, int index, int b_index, const vector<Node> &nodes) {
    int diffNode = findDiffNode(a.path, b.path, index, b_index);
    if (diffNode != -1) { //agent a waits before same part of their paths
        vector<vector<Node> > tmp = getPaths(b.path[diffNode].second.getIndex(), b.getGoal().getParent(), nodes);
        if (((b.path[b_index].first.depart - a.path[index].first.arrive) > EPS && tmp.size() == 1)
            || !checkPaths(tmp, a.path)) {
            cout << "AGENT# " << a.index << " WAITS FOR "
                 << (b.path[b_index].first.depart - a.path[index].first.arrive) +
                    a.getCoord(a.path[index].first.depart).distance(
                            a.getCoord(a.path[index].first.depart).getVertex(
                                    a.vertices[0].length, a.vertices[0].angle))
                 << " AT NODE# " << a.path[diffNode].second.getIndex() << endl;
            cout << "__________________________________________________________\n";
            adjustSchedule(a.path, a, diffNode, diffNode, (b.path[b_index].first.depart - a.path[index].first.arrive) +
                                                          a.getCoord(a.path[index].first.depart).distance(
                                                                  a.getCoord(a.path[index].first.depart).getVertex(
                                                                          a.vertices[0].length, a.vertices[0].angle)));

            findPath(nodes, a, b);
            return true;
        }
    }
    if (a.path[index].second.innerNodes.size() > 2) { //a steps aside to let b go through conflict node
        for (const InnerNode &in : a.path[index].second.innerNodes) {
            if (in.getNeighbor() != a.path[index].second.getIndex()
                && in.getNeighbor() != a.path[index - 1].second.getIndex()
                && in.getNeighbor() != b.getGoal().getParent()) {
                vector<pair<Schedule, Node> > a_old_path = a.index == 0 ? a.path : b.path;
                vector<pair<Schedule, Node> > b_old_path = b.index == 1 ? b.path : a.path;
                a.path.emplace_back(Schedule(0, 0, -1, -1), nodes[in.getNeighbor()]);
                a.path.emplace_back(Schedule(0, 0, -1, -1), nodes[in.getParent()]);
                adjustSchedule(a.path, a, index);
                if (findPath(nodes, a, b)) {
                    return true;
                }
                a.path = a.index == 0 ? a_old_path : b_old_path;
                b.path = b.index == 1 ? b_old_path : a_old_path;
            }
        }
    }
    for (int i = b_index - 2; i >= 0; i--) { //if there was a rotation, looking for a first node before rotation
        if (b.path[i].second.getIndex() == b.path[b_index - 1].second.getIndex()) b_index--;
    }
    return edgeConflict(b, a, b_index - 1, nodes, a.getGoal().getParent()); //alternative path

}

/**
 * create a new path when there's a vertex conflict
 * @param a - agent
 * @param b - agent
 * @param index - index of a's conflict
 * @param nodes - vector of nodes
 * @return true if conflict was resolved
 */
bool vertexConflict(Agent &a, Agent &b, int index, const vector<Node> &nodes) {
    double t = a.path[index].first.depart;
    Point a_coord = a.getCoord(t);
    Point b_coord = b.getCoord(t);
    Point a_edge = a.getCoordAtEdge(a_coord, a_coord, a.getCurrentAngle(t));
    Point b_edge = b.getCoordAtEdge(b_coord, a_coord, b.getCurrentAngle(t));
    vector<pair<Schedule, Node> > a_old_path = a.index == 0 ? a.path : b.path;
    vector<pair<Schedule, Node> > b_old_path = b.index == 1 ? b.path : a.path;
    if (a.getSpeed() < b.getSpeed()) {
        double waitingTime_a = a.calcWaitingTime(a_coord, b_coord, b, t, 1);
        if (moving(waitingTime_a, a, b, t, a_coord, b_coord, nodes, 1)) return true;
        a.path = a.index == 0 ? a_old_path : b_old_path;
        b.path = b.index == 1 ? b_old_path : a_old_path;
    } else if (a.getSpeed() > b.getSpeed()) {
        double waitingTime_b = b.calcWaitingTime(b_coord, a_coord, a, t, 1);
        if (moving(waitingTime_b, b, a, t, b_coord, a_coord, nodes, 1)) return true;
        a.path = a.index == 0 ? a_old_path : b_old_path;
        b.path = b.index == 1 ? b_old_path : a_old_path;
    } else {
        double waitingTime_a = a.calcWaitingTime(a_coord, b_coord, b, t, 1);
        double waitingTime_b = b.calcWaitingTime(b_coord, a_coord, a, t, 1);
        if (waitingTime_a >= waitingTime_b) {
            if (moving(waitingTime_a, a, b, t, a_coord, b_coord, nodes, 1)) return true;
            a.path = a.index == 0 ? a_old_path : b_old_path;
            b.path = b.index == 1 ? b_old_path : a_old_path;
        } else {
            if (moving(waitingTime_b, b, a, t, b_coord, a_coord, nodes, 1)) return true;
            a.path = a.index == 0 ? a_old_path : b_old_path;
            b.path = b.index == 1 ? b_old_path : a_old_path;
        }
    }
    return false;
}

/**
 * reads agent description from input
 * @param nodes
 * @return agent
 */
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

int main() {
    srand(time(nullptr));

    vector<Node> nodes = createMap();

    Agent a = readInput(nodes);
    Agent b = readInput(nodes);

    vector<Agent> agents = {a, b};
    init(nodes, a, b);
    a.path = a.final_path;
    b.path = b.final_path;

    cout << "....................................................." << endl << endl;
    cout << "\t\t\t\tRESULT:\n\n";
    cout << "path length = " << pathLength(a.final_path) << endl;
    cout << "time = " << a.final_path[a.final_path.size() - 1].first.depart << endl;
    cout << a;
    cout << "path length = " << pathLength(b.final_path) << endl;
    cout << "time = " << b.final_path[b.final_path.size() - 1].first.depart << endl;
    cout << b;
    return 0;
}
