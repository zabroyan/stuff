#ifndef COBJECT_H
#define COBJECT_H
#include <iostream>
#include "CMap.h"
#include "CCoord.h"

/**< CObject contains all objects in map */
class CObject
{
    public:
                    
                    CObject         ( int x, int y ) : level ( 1 ), coord ( x,y ) { }
		    /**< creates an object with coordinates ( x, y ) 			*/
virtual             ~CObject        ( void ) = default;
                    CObject         ( const CObject & other ) = default;
virtual void        print           ( std::ostream & os ) const = 0;

                   
virtual bool        CanIBuildHere   ( void ) const = 0;
 		    /**< detects if it's a free place 					*/
virtual CObject*    clone           ( void ) const = 0;
                    /**<  creates a clone of object 					*/

        int         GetHP           ( void  ) const { return HP; }
        int         GetX            ( void  ) const { return coord.x; }
        int         GetY            ( void  ) const { return coord.y; }
        void        SetHP           ( int x )       { HP = x; }
        void        SetDamage       ( int x )       { damage = x; }
        int         GetDamage       ( void  ) const { return damage; }
        int         GetType         ( void  ) const { return type; }

friend std::ostream& operator << ( std::ostream & os,
                                   const CObject & o )
                    { o . print ( os ); return os; }
friend class CMap;

    protected:
        int level;
        int type;
        int damage;
        int HP;
        int coast;
        int upgradeCoast;
        CCoord coord;
};

#endif // COBJECT_H
