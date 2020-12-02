#ifndef CENTRANCE_H
#define CENTRANCE_H

#include "CImmobile.h"

/**< CEntrance defines entrance and exit in game */
class CEntrance : public CImmobile
{
    public:
                    CEntrance   ( int x, int y )        : CImmobile ( x, y )
                    { CObject::damage = 0; }
        void        print       ( std::ostream & os )   const
                    { os << ' '; }
        CEntrance*  clone       ( void )                const
                    { return new CEntrance ( *this ); }
};

#endif // CENTRANCE_H
