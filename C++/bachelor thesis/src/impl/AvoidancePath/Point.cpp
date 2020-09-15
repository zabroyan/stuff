//
// Created by yana on 27.03.20.
//
#include <regex>
#include "Point.h"

Point::Point(double new_x, double new_y) {
    xCOORD = new_x;
    yCOORD = new_y;
}

double Point::GetX() const {
    return xCOORD;
}

double Point::GetY() const {
    return yCOORD;
}

bool operator==(const Point &a, const Point &b) {
    return fabs(a.GetX() - b.GetX()) < EPS && fabs(a.GetY() - b.GetY()) < EPS;
}

double Point::distance(const Point b) const {
    return sqrt((xCOORD - b.GetX()) * (xCOORD - b.GetX())
                + (yCOORD - b.GetY()) * (yCOORD - b.GetY()));
}

double Point::setAngle(const Point &neighbor_coord) {
    double d = atan2(neighbor_coord.GetY() - GetY(),
                     neighbor_coord.GetX() - GetX()) * 180 / PI;
    return d >= 0 ? d : 360 + d;
}

bool Point::atInterval(Point start, Point end) {
    if (*this == start) return true; //same point

    if (start.GetX() > end.GetX()) {
        Point tmp = start;
        start = end;
        end = tmp;
    }
    return fabs((xCOORD - start.GetX()) * (end.GetY() - start.GetY()) -
                (yCOORD - start.GetY()) * (end.GetX() - start.GetX())) < EPS &&
           (distance(start) <= start.distance(end)) && (distance(end) <= start.distance(end));
}

bool Point::atLine(Point start, Point end) {
    if (*this == start) return true; //same point

    if (start.GetX() > end.GetX()) {
        Point tmp = start;
        start = end;
        end = tmp;
    }
    return fabs((xCOORD - start.GetX()) * (end.GetY() - start.GetY()) -
                (yCOORD - start.GetY()) * (end.GetX() - start.GetX())) < EPS;
}

Point Point::getVertex(double length, double angle) {
    return {(GetX() + length * cos(angle * PI / 180)),
            (GetY() + length * sin(angle * PI / 180))};
}

Point Point::getCenter(double length, double angle) {
    return {(GetX() - length * cos(angle * PI / 180)),
            (GetY() - length * sin(angle * PI / 180))};
}

Point Point::getIntersect(Point end, Point start2, Point end2) {
    //getting coefficients of linear equations
    double A1 = GetY() - end.GetY();
    double B1 = end.GetX() - GetX();
    double C1 = GetX() * end.GetY() - end.GetX() * GetY();

    double A2 = start2.GetY() - end2.GetY();
    double B2 = end2.GetX() - start2.GetX();
    double C2 = start2.GetX() * end2.GetY() - end2.GetX() * start2.GetY();

    if (fabs(A1 * B2 - B1 * A2) < EPS) { //parallel lines
        if (fabs(A2) < EPS) {//line2 is parallel to Ox
            return {GetX(), fabs(GetY() + C2 / B2)};
        } else if (fabs(B2) < EPS) { //line2 is parallel to Oy
            return {fabs(GetX() + C2 / A2), GetY()};
        } else {
            double new_y = (B2 * C2 - A2 * (A2 * GetY() - B2 * GetX())) / (B2 * B2 - A2 * A2);
            double new_x = (-B2 * new_y - C2) / A2;
            return {new_x, new_y};
        }
    }
    return {(B2 * C1 - B1 * C2) / (A2 * B1 - A1 * B2), (A2 * C1 - A1 * C2) / (A1 * B2 - A2 * B1)};
}
