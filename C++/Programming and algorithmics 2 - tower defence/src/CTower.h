#ifndef CTOWER_H
#define CTOWER_H

#include "CMobile.h"
#include "CMap.h"

/**< CTower defines towers in game. Place which can be added, updated and destroyed */
class CTower : public CMobile
{
    public:
                CTower      ( int t, int x, int y ) : CMobile (x, y, t)
                {   coast = damage = HP = ( t + 1 ) * 25;
                    upgradeCoast = 1.5 * coast;
                }
        void    print       ( std::ostream & os )   const
                { os << ( char ( type + 64 ) ); }
        int     GetCoast    ( void )                const
                { return coast; }
        CTower* clone       ( void )                const
                { return new CTower ( *this ); }

friend  class   CMap;
friend  class   CInit;
};

#endif // CTOWER_H
