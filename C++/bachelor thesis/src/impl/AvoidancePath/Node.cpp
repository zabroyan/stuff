//
// Created by yana on 16.11.19.
//

#include "Node.h"

using namespace std;

Node::Node(int index, int x, int y) : index(index) {
    setCoordinates(x, y);
}

void Node::setCoordinates(int x, int y) {
    coordinates = Point(x, y);
}

Point Node::getCoordinates() const {
    return coordinates;
}

int Node::getIndex() const {
    return index;
}

bool operator<(const Node &a, const Node &b) {
    return a.getIndex() < b.getIndex();
}

bool operator==(const Node &a, const Node &b) {
    return a.getIndex() == b.getIndex();
}

double Node::distance(const Node &b) const {
    return sqrt((coordinates.GetX() - b.coordinates.GetX()) * (coordinates.GetX() - b.coordinates.GetX())
                + (coordinates.GetY() - b.coordinates.GetY()) * (coordinates.GetY() - b.coordinates.GetY()));
}

InnerNode Node::getINbyNeighbor(int n) const {
    for (auto &i : innerNodes) {
        if (i.getNeighbor() == n)
            return i;
    }
    return InnerNode(); //there is always an inner node because given node follows this node in agent's path
}
