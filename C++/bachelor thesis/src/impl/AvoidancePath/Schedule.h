//
// Created by yana on 09.02.20.
//

#ifndef BAP_SCHEDULE_H
#define BAP_SCHEDULE_H

/**
 * class Schedule represents information about arriving and departing.
 */
class Schedule {
public:
    Schedule() {
        arrive = depart = 0;
        arr_angle = dep_angle = -1;
    }

    Schedule(double a, double d, double a_angle, double d_angle) {
        arrive = a;
        depart = d;
        arr_angle = a_angle;
        dep_angle = d_angle;
    }

    friend bool operator==(const Schedule &a, const Schedule &b) {
        return a.arrive == b.arrive && a.depart == b.depart;
    }

    double arrive;
    double depart;

    double arr_angle;
    double dep_angle;
};


#endif //BAP_SCHEDULE_H
