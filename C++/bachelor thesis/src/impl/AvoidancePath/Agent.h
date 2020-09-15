//
// Created by yana on 02.12.19.
//

#ifndef BAP_AGENT_H
#define BAP_AGENT_H

#include <set>
#include "InnerNode.h"
#include "Node.h"
#include "Schedule.h"
#include "Vertex.h"

using namespace std;

class Agent {
public:
    Agent() = delete;

    Agent(const InnerNode &s, const InnerNode &g, double v, double rs, vector<Vertex> &vrt, int i);

    InnerNode getStart() const;

    InnerNode getGoal() const;

    double getSpeed() const;

    double getRotationSpeed() const;

    bool isCircle();

    bool isRectangle();

    Point getCoord(double t);

    /**
     *
     * @param a_center - center of this agent
     * @param b_center - center of the second agent
     * @param dev - angle of this agent
     * @return coordination at this agent's edge which is an intersect of this edge and line from a_center to b_center
     */
    Point getCoordAtEdge(Point a_center, Point b_center, double dev, bool out = false);

    double calcWaitingTime(Point a_center, Point b_center, Agent b, double time, int vertex_conflict);

    /**
     * both agent are circles
     * @param a_center - center of this agent
     * @param b_center - center of the second agent
     * @param b_radius - second agent's radius
     * @param time - current time
     * @return time to wait for the second agent
     */
    double calcWaitingTime_circles(Point a_center, Point b_center, double b_radius, double time);

    /**
     * this agent is at node and second agent is moving
     * @param b_edge - second agent's closest coordination to this agent
     * @param b_center - center of the second agent
     * @param a_center - center of this agent
     * @param time - current time
     * @return time to wait for the second agent
     */
    double calcRotation(Point b_edge, Point b_center, Point a_center, double time);

    /**
     * both agent are polygons
     * @param a_center - center of this agent
     * @param b_center - center of the second agent
     * @param b - second agent
     * @param time - current time
	 * @param vertex_conflict - was it vertex conflict or not
     * @return time to wait for the second agent
     */
    double calcWaitingTime_polygons(Point a_center, Point b_center, Agent b, double time, int vertex_conflict);
	
	
    /**
     * both agent are rectangles
     * @param a_center - center of this agent
     * @param b_center - center of the second agent
     * @param b - second agent
     * @param time - current time
	 * @param vertex_conflict - was it vertex conflict or not
     * @return time to wait for the second agent
     */
    double calcWaitingTime_rectangles(Point a_center, Point b_center, Agent b, double time, int vertex_conflict);

    double getCurrentAngle(double time);

    /**
     *
     * @param t - current time
     * @return information about previous node and next node at time t
     */
    pair<pair<Schedule, Node>, pair<Schedule, Node> > atTime(double t);

    /**
     *
     * @param t
     * @return index of node if agent is at this node at time t or -1 if agent is moving
     */
    int getIndexByTime(double t);

    /**
     *
     * @param t
     * @return index of previous node if agent is moving or index of this node
     */
    int getPrevNode(double t);

    /**
     *
     * @param t
     * @param node
     * @return true if agent visits node with index n after time
     */
    bool goesThroughGoal(double t, int n);

    friend ostream &operator<<(ostream &out, const Agent &c);

    vector<pair<Schedule, Node> > path;
    vector<pair<Schedule, Node> > final_path;
    vector<Vertex> vertices;
    double angle;
    int index;
private:
    InnerNode start;
    InnerNode goal;
    double speed;
    double rotation_speed;

};


#endif //BAP_AGENT_H
