//
// Created by yana on 16.11.19.
//

#ifndef BAP_NODE_H
#define BAP_NODE_H

#include <vector>
#include "Point.h"
#include "InnerNode.h"

using namespace std;

class Node {
public:
    Node() { index = -1; }

    explicit Node(int index, int x, int y);

    void setCoordinates(int x, int y);

    Point getCoordinates() const;

    int getIndex() const;

    friend bool operator<(const Node &a, const Node &b);

    friend bool operator==(const Node &a, const Node &b);

    double distance(const Node &b) const;

    /**
     *
     * @param n - index of neighbor
     * @return inner node from InnerNodes vector connected to node with index n
     */
    InnerNode getINbyNeighbor(int n) const;

    vector<InnerNode> innerNodes;

private:
    int index;
    Point coordinates;
};


#endif //BAP_NODE_H
