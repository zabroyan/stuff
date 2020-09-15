#ifndef CMOBILE_H
#define CMOBILE_H

#include "CObject.h"

/**< CMobile contains objects that can be moved: towers and enemies */
class CMobile : public CObject
{
    public:
             CMobile        ( int x, int y, int t ) :CObject ( x, y )
        {
             CObject::type = t;
        }
        bool CanIBuildHere  ( void ) const
             { return false; }
friend class CMap;
friend class CInit;
};

#endif // CMOBILE_H
