//
// Created by yana on 20.11.19.
//

#include "InnerNode.h"

using namespace std;

InnerNode::InnerNode() {
    parent = neighbor = -1;
    angle = -1;
}

bool operator<(const InnerNode &a, const InnerNode &b) {
    if (a.getParent() == b.getParent())
        return a.getNeighbor() < b.getNeighbor();
    return a.getParent() < b.getParent();
}

bool operator==(const InnerNode &a, const InnerNode &b) {
    return a.getNeighbor() == b.getNeighbor() && a.parent == b.parent;
}

InnerNode::InnerNode(int parent, int neighbor, Point parent_coord, Point neighbor_coord) : parent(parent),
                                                                                           neighbor(neighbor) {
    angle = parent_coord.setAngle(neighbor_coord);
}

void InnerNode::addNeighbor(const InnerNode &n) {
    neighbors.insert(n);
}

double InnerNode::getAngle() const {
    return angle;
}

int InnerNode::getNeighbor() const {
    return neighbor;
}

int InnerNode::getParent() const {
    return parent;
}