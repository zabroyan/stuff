#ifndef CIMMOBILE_H
#define CIMMOBILE_H

#include "CObject.h"

/**< CImmobile contains objects that can't be moved: walls, entrances and spaces */
class CImmobile : public CObject
{
    public:
                CImmobile       ( int x, int y ) : CObject ( x, y ) {}
        bool    CanIBuildHere   ( void ) const   { return false; }
};

#endif // CIMMOBILE_H
