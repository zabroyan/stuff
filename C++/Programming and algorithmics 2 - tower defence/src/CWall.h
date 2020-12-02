#ifndef CWALL_H
#define CWALL_H

#include "CImmobile.h"

/**< CWall defines walls in game. Places where you can't build anything */
class CWall : public CImmobile
{
    public:
                CWall ( int x, int y )      : CImmobile ( x, y ) {}
        void    print ( std::ostream & os ) const
                { os << '#'; }
        CWall * clone ( void )              const
                { return new CWall(*this); }
};

#endif // CWALL_H
