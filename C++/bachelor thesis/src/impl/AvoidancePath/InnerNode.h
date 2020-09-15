//
// Created by yana on 20.11.19.
//

#ifndef BAP_INNERNODE_H
#define BAP_INNERNODE_H

#include "Point.h"
#include <set>
using namespace std;

/**
 * class InnerNode represents an inner node in node, used for agent's rotation.
 */
class InnerNode {
public:
    InnerNode();

    explicit InnerNode(int, int, Point, Point);
    friend bool operator < (const InnerNode & a, const InnerNode & b);
    friend bool operator == (const InnerNode & a, const InnerNode & b);

    void addNeighbor(const InnerNode &);

    double getAngle() const;

    int getNeighbor () const;
    int getParent() const;

    set <InnerNode> neighbors;
private:
    int neighbor;
    int parent;
    double angle;
};


#endif //BAP_INNERNODE_H
