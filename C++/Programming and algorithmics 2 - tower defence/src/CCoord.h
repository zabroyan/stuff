#ifndef CCOORD_H
#define CCOORD_H
#include <iostream>

/**< CCoord stores coordinates for every object in game */
class CCoord
{
    public:
                CCoord          ( int X, int Y ) : x ( X ), y ( Y )     {}
                CCoord          ( void )                                {}
        bool    operator ==     ( const std::pair < int, int > other ) const
            {
                return x == other . first && y == other . second;
            }
        bool    operator ==     ( const CCoord & other ) const
            {
                return x == other . x && y == other . y;
            }
        bool    operator !=     ( const CCoord & other ) const
            {
                return x != other . x || y != other . y;
            }
        bool    operator <      ( const CCoord & other ) const
            {
                if ( x < other . x)
                    return true;
                else if (x == other . x && y > other . y)
                    return true;
                return false;
            }
friend std::ostream & operator << ( std::ostream & os, const CCoord & c )
            {
                os << "(" << c . x << ", " << c . y << ")";
                return os;
            }
   int x;
   int y;
};

#endif // CCOORD_H
