//
// Created by yana on 25.02.20.
//

#ifndef BAP_VERTEX_H
#define BAP_VERTEX_H

/**
 * class represents 1 vertex in a figure. Vertex has a distance and angle from a given point (centre)
 */
class Vertex {
public:
    Vertex() {
        length = 0;
        angle = 0;
    }

    Vertex(double l, double a) {
        length = l;
        angle = a;
    }

    Vertex &operator=(const Vertex &v2) = default;

    double length;
    double angle;
};


#endif //BAP_VERTEX_H
