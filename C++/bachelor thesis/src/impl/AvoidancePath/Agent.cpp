//
// Created by yana on 27.03.20.
//
#include "Agent.h"

Agent::Agent(const InnerNode &s, const InnerNode &g, double v, double rs, vector<Vertex> &vrt, int i) {
    start = s;
    goal = g;
    angle = s.getAngle();
    speed = v;
    rotation_speed = rs;
    vertices = vrt;
    index = i;
}

InnerNode Agent::getStart() const {
    return start;
}

InnerNode Agent::getGoal() const {
    return goal;
}

double Agent::getSpeed() const {
    return speed;
}

double Agent::getRotationSpeed() const {
    return rotation_speed;
}

bool Agent::isCircle() {
    return vertices.size() == 1;
}

bool Agent::isRectangle() {
    if (vertices.size() != 4) return false;
    double a = vertices[0].angle;
    return vertices[1].angle == 180 - a && vertices[2].angle == 180 + a && vertices[3].angle == 360 - a;
}

Point Agent::getCoord(double t) {
    pair<Schedule, Node> prev = path[getPrevNode(t)];
    double alpha = prev.first.dep_angle;
    double x = prev.second.getCoordinates().GetX();
    double y = prev.second.getCoordinates().GetY();
    double d = (t - prev.first.depart) * speed;
    if (d < 0 || getIndexByTime(t) == path.size() - 1)
        return prev.second.getCoordinates();
    return Point(x, y).getVertex(d, alpha);
}

Point Agent::getCoordAtEdge(Point a_center, Point b_center, double dev, bool out) {
    Point v1 = Point(0, 0);
    Point v2 = Point(0, 0);
    double d = a_center.setAngle(b_center);
    if (isCircle()) {
        return a_center.getVertex(vertices[0].length, d);
    }

    //find the closest edge to the second agent
    for (int v = 0; v < vertices.size(); v++) {
        int v_next = v == vertices.size() - 1 ? 0 : v + 1;
        if ((fmod(vertices[v].angle + dev, 360) <= d && fmod(vertices[v_next].angle + dev, 360) >= d)
            || (fmod(vertices[v].angle + dev, 360) > fmod(vertices[v_next].angle + dev, 360)) &&
               (fmod(vertices[v].angle + dev, 360) <= d || fmod(vertices[v_next].angle + dev, 360) >= d)) {
            v1 = a_center.getVertex(vertices[v].length, fmod(vertices[v].angle + dev, 360));
            v2 = a_center.getVertex(vertices[v_next].length,
                                    fmod(vertices[v_next].angle + dev, 360));
        }
    }
    Point res = a_center.getIntersect(b_center, v1, v2);
    return res;
}

double Agent::calcWaitingTime (Point a_center, Point b_center, Agent b, double time, int vertex_conflict) {
    if (isCircle()) return calcWaitingTime_circles(a_center, b_center, b.vertices[0].length, time);
    else if (isRectangle()) return calcWaitingTime_rectangles(a_center, b_center, b, time, vertex_conflict);
    else return calcWaitingTime_polygons(a_center, b_center, b, time, vertex_conflict);
}

double Agent::calcWaitingTime_circles(Point a_center, Point b_center, double b_radius, double time) {
    double t = -1;
    Point nextNode = path[getPrevNode(time) + 1].second.getCoordinates();
    if (b_center.atInterval(a_center, nextNode)) return t;
    double alpha = getIndexByTime(time) == -1
                   ? getCurrentAngle(time) //moving
                   : path[getPrevNode(time)].first.dep_angle; //at node

    double b = -2 * cos(alpha * PI / 180) * (a_center.GetX() - b_center.GetX()) -
               2 * sin(alpha * PI / 180) * (a_center.GetY() - b_center.GetY());
    double c = (a_center.GetX() - b_center.GetX()) * (a_center.GetX() - b_center.GetX()) +
               (a_center.GetY() - b_center.GetY()) * (a_center.GetY() - b_center.GetY()) -
               (vertices[0].length + b_radius) * (vertices[0].length + b_radius);
    t = (-b + sqrt(b * b - 4 * c)) / 2 / speed;
    if (t < 0)
        t = (-b - sqrt(b * b - 4 * c)) / 2 / speed;
    return t;
}

double Agent::calcWaitingTime_rectangles(Point a_center, Point b_center, Agent b, double time, int vertex_conflict) {
    double waitingTime = -1;
    if (getPrevNode(time) == path.size() - 1) return waitingTime;
    Point nextNode = path[getPrevNode(time) + 1].second.getCoordinates();

    if (!vertex_conflict && b_center.atInterval(a_center, nextNode)) return waitingTime;
    double a_angle = getIndexByTime(time) == -1
                     ? getCurrentAngle(time) //moving
                     : path[getPrevNode(time)].first.dep_angle; //at node
    double b_angle = b.getIndexByTime(time) == -1
                     ? b.getCurrentAngle(time) //moving
                     : b.path[b.getPrevNode(time)].first.dep_angle; //at node

    vector<pair<Point, Point> > new_vrt;
    //getting intersect for every pair of this agent's vertex and second agent's edge
    for (auto & vertex : vertices) {
        Point vrt = a_center.getVertex(vertex.length, fmod(vertex.angle + a_angle, 360));
        Point nextNode_vrt = nextNode.getVertex(vertex.length, fmod(vertex.angle + a_angle, 360));

        vector<Point> vrt_intersects;
        for (int e = 0; e < b.vertices.size(); e++) {
            Point edge_start = b_center.getVertex(b.vertices[e].length, fmod(b.vertices[e].angle + b_angle, 360));
            Point edge_end{};

            if (e + 1 == b.vertices.size()) //last vertex connected to first
                edge_end = b_center.getVertex(b.vertices[0].length, fmod(b.vertices[0].angle + b_angle, 360));
            else
                edge_end = b_center.getVertex(b.vertices[e + 1].length,
                                              fmod(b.vertices[e + 1].angle + b_angle, 360));
            Point intersect = vrt.getIntersect(nextNode_vrt, edge_start, edge_end);
            if (intersect.atLine(edge_start, edge_end) &&
                intersect.atInterval(vrt, nextNode_vrt)) { //intersect is at edge and is at future path

                Point b_edge = b.getCoordAtEdge(b_center, a_center, fmod(b_angle, 360));
                Point a_center_new = intersect.getCenter(vertex.length, fmod(vertex.angle + a_angle, 360));
                Point a_edge = getCoordAtEdge(a_center_new, b_center, a_angle);

                if (b_edge.atInterval(a_center_new, a_edge) || a_edge.atInterval(b_center, b_edge) ||
                    b_center.atInterval(a_center_new, a_edge) || a_center_new.atInterval(b_center, b_edge)) {
                    continue;
                }

                if (a_center.distance(b_center) >
                    intersect.getCenter(vertex.length, fmod(vertex.angle + a_angle, 360)).distance(
                            b_center)) {
                    continue;
                }
                vrt_intersects.emplace_back(intersect);
            }
        }

        if (vrt_intersects.empty()) continue;
        Point next_vrt = vrt_intersects[0]; //closest intersect to the next node
        for (auto &i : vrt_intersects) {
            if (i.distance(nextNode_vrt) < next_vrt.distance(nextNode_vrt))
                next_vrt = i;
        }
        new_vrt.emplace_back(make_pair(vrt, next_vrt));
    }
    if (new_vrt.empty()) return waitingTime;
    waitingTime = new_vrt[0].second.distance(
            new_vrt[0].first); //finally choosing 1 intersect with the longest distance from starting vertex
    for (auto &v : new_vrt) {
        if (v.first.distance(v.second) > waitingTime) {
            waitingTime = v.first.distance(v.second);
        }
    }
    return waitingTime / speed + fabs(a_angle - getCurrentAngle(time)) * rotation_speed;
}

double Agent::calcWaitingTime_polygons(Point a_center, Point b_center, Agent b, double time, int vertex_conflict) {
    double waitingTime = -1;
    if (getPrevNode(time) == path.size() - 1) return waitingTime;
    Point prevNode = b.path[getPrevNode(time)].second.getCoordinates();

    if (!vertex_conflict && a_center.atInterval(b_center, prevNode)) return waitingTime;
    double a_angle = getIndexByTime(time) == -1
                     ? getCurrentAngle(time) //moving
                     : path[getPrevNode(time)].first.dep_angle; //at node
    double b_angle = b.getIndexByTime(time) == -1
                     ? b.getCurrentAngle(time) //moving
                     : b.path[b.getPrevNode(time)].first.dep_angle; //at node

    vector<pair<Point, Point> > new_vrt;
    //getting intersect for every pair of this agent's vertex and second agent's edge
    for (int v = 0; v < b.vertices.size(); v++) {
        Point vrt = b_center.getVertex(b.vertices[v].length, fmod(b.vertices[v].angle + b_angle, 360));
        Point prevNode_vrt = prevNode.getVertex(b.vertices[v].length, fmod(b.vertices[v].angle + b_angle, 360));

        vector<Point> vrt_intersects;
        for (int e = 0; e < vertices.size(); e++) {
            Point edge_start = a_center.getVertex(vertices[e].length, fmod(vertices[e].angle + a_angle, 360));
            Point edge_end{};

            if (e + 1 == vertices.size()) //last vertex connected to first
                edge_end = a_center.getVertex(vertices[0].length, fmod(vertices[0].angle + a_angle, 360));
            else
                edge_end = a_center.getVertex(vertices[e + 1].length,
                                              fmod(vertices[e + 1].angle + a_angle, 360));

            Point intersect = vrt.getIntersect(prevNode_vrt, edge_start, edge_end);
            if (intersect.atLine(edge_start, edge_end) &&
                intersect.atInterval(vrt, prevNode_vrt)) { //intersect is at edge and is at future path

                Point a_edge = getCoordAtEdge(a_center, b_center, fmod(a_angle, 360));
                Point b_center_new = intersect.getCenter(b.vertices[v].length, fmod(b.vertices[v].angle + b_angle, 360));
                Point b_edge = b.getCoordAtEdge(b_center_new, a_center, b_angle);

                if (a_edge.atInterval(b_center_new, b_edge) || b_edge.atInterval(a_center, a_edge) ||
                    a_center.atInterval(b_center_new, b_edge) || b_center_new.atInterval(a_center, a_edge)) {
                    continue;
                }

                if (a_center.distance(b_center) >
                    intersect.getCenter(b.vertices[v].length, fmod(b.vertices[v].angle + b_angle, 360)).distance(
                            a_center)) {
                    continue;
                }

                vrt_intersects.emplace_back(intersect);
            }
        }

        if (vrt_intersects.empty()) continue;
        Point next_vrt = vrt_intersects[0]; //closest intersect to the next node
        for (auto &i : vrt_intersects) {
            if (i.distance(prevNode_vrt) < next_vrt.distance(prevNode_vrt))
                next_vrt = i;
        }
        new_vrt.emplace_back(make_pair(vrt, next_vrt));
    }
    if (new_vrt.empty()) return waitingTime;
    waitingTime = new_vrt[0].second.distance(
            new_vrt[0].first); //finally choosing 1 intersect with the longest distance from starting vertex

    for (auto &v : new_vrt) {
        if (v.first.distance(v.second) > waitingTime) {
            waitingTime = v.first.distance(v.second);
        }
    }
    return waitingTime / speed + fabs(a_angle - getCurrentAngle(time)) * rotation_speed;
}

double Agent::calcRotation(Point b_edge, Point b_center, Point a_center, double time) {
    double startDeviation = getCurrentAngle(time);
    for (int i = 0; i < 360; i++) {
        Point a_edge = getCoordAtEdge(a_center, b_center, fmod(startDeviation + i, 360));
        if (!a_edge.atInterval(b_center, b_edge) && !b_edge.atInterval(a_center, a_edge) &&
            !a_center.atInterval(b_center, b_edge) && !b_center.atInterval(a_center, a_edge)) {
            return i * rotation_speed;
        }
    }
    return -1;
}

double Agent::getCurrentAngle(double time) {
    Schedule sch = path[getPrevNode(time)].first;

    double wait = sch.depart - sch.arrive - (abs(sch.dep_angle - sch.arr_angle) - 180 < EPS
                                             ? abs(sch.dep_angle - sch.arr_angle)
                                             : abs(abs(sch.dep_angle - sch.arr_angle) - 360)) * rotation_speed;
    sch.arrive += wait;
    if (sch.arr_angle == sch.dep_angle) return sch.arr_angle;
    if (time >= sch.depart) return sch.dep_angle;
    else {
        if ((sch.arr_angle - 180 < EPS && sch.dep_angle - 180 < EPS) ||
            (sch.arr_angle - 180 > EPS && sch.dep_angle - 180 > EPS)) {
            if (sch.arr_angle <= sch.dep_angle) {
                double a = sch.dep_angle - (sch.depart - time) / rotation_speed;
                return a;
            } else {
                double a = sch.arr_angle - (time - sch.arrive) / rotation_speed;
                return a;
            }
        } else {
            if (sch.arr_angle <= sch.dep_angle) {
                double a = sch.dep_angle + (sch.depart - time) / rotation_speed;
                return a;
            } else {
                double a = sch.arr_angle + (time - sch.arrive) / rotation_speed;
                return a;
            }
        }
    }
}

pair<pair<Schedule, Node>, pair<Schedule, Node> > Agent::atTime(double t) {
    for (int i = 0; i < path.size(); i++) {
        if (path[i].first.arrive >= t) {
            if (i > 0)
                return make_pair(path[i - 1], path[i]);
            else
                return make_pair(path[i], path[i]);
        }
    }
    return make_pair(path[path.size() - 2], //t is bigger than last node's arrive
                     make_pair(Schedule(0, 0, -1, -1), path[path.size() - 1].second));
}

int Agent::getIndexByTime(double t) {
    for (int i = 0; i < path.size(); i++) {
        if (path[i].first.arrive <= t && path[i].first.depart >= t)
            return i;
        if (i == path.size() - 1 && t > path[i].first.depart) return i;
    }
    return -1;
}

int Agent::getPrevNode(double t) {
    for (int i = 0; i < path.size(); i++) {
        if (path[i].first.arrive == t) return i;
        if (path[i].first.arrive > t) {
            return i - 1;
        }
    }
    return int(path.size() - 1);
}

bool Agent::goesThroughGoal(double t, int node) {
    for (auto &n : path) {
        if (n.second.getIndex() == node && n.first.arrive >= t)
            return true;
    }
    return false;
}

ostream &operator<<(ostream &out, const Agent &c) {
    out << "Agent #" << c.index << ": "
        << c.getStart().getParent() << " -> " << c.getGoal().getParent();
    out << " | PATH: \n";
    for (auto &i : c.path)
        out << "(arrive " << round(i.first.arrive * 10) / 10 << "/" << round(i.first.arr_angle) << ", depart "
            << round(i.first.depart * 10) / 10 << "/" << round(i.first.dep_angle)
            << ") at node "
            << i.second.getIndex() << "\n";
    out << endl;
}
