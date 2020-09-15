#ifndef CSPACE_H
#define CSPACE_H

#include "CImmobile.h"

/**< CSpace defines free places in game. You can put here a tower */
class CSpace : public CImmobile
{
    public:
                CSpace          ( int x, int y )        : CImmobile ( x, y )
                { damage = 0; }
        bool    CanIBuildHere   ( void )                const override
                { return true; }
        void    print           ( std::ostream & os )   const
                { os << ' '; }
        void    SetDamage       ( int x )
                { damage = x; }
        CSpace* clone           ( void )                const
                { return new CSpace ( *this ); }
};

#endif // CSPACE_H
