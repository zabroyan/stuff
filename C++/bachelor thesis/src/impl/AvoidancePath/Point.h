//
// Created by yana on 16.11.19.
//

#ifndef BAP_POINT_H
#define BAP_POINT_H

#define PI 3.1415
#define EPS 1e-2

#include <cmath>
#include <iostream>

/**
 * class Point represents a point in 2D space.
 */
class Point {
public:
    Point() = default;

    Point(double new_x, double new_y);

    double GetX() const;

    double GetY() const;

    friend bool operator==(const Point &a, const Point &b);

    double distance(Point b) const;

    double setAngle(const Point &neighbor_coord);

    /**
     *  checks if point is between start and end
     * @param start
     * @param end
     * @return true if point is at interval from start to end
     */
    bool atInterval(Point start, Point end);

    /**
     * checks if point is lying at line given by start and end
     * @param start
     * @param end
     * @return true if point is at line
     */
    bool atLine(Point start, Point end);

    /**
     *
     * @param length
     * @param angle
     * @return coordination of point with given distance and angle from this point
     */
    Point getVertex(double length, double angle);

    /**
     *
     * @param length
     * @param angle
     * @return center coordination from a given vertex
     */
    Point getCenter(double length, double angle);

    /**
     * this - start point of the first interval
     * @param end  - end point of the first interval
     * @param start2 - start point of the second interval
     * @param end2 - end point of the second interval
     * @return intersect of two intervals
     */
    Point getIntersect(Point end, Point start2, Point end2);

private:
    double xCOORD, yCOORD;
};


#endif //BAP_POINT_H
