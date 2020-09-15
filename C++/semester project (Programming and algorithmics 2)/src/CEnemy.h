#ifndef CENEMY_H
#define CENEMY_H

#include "CMobile.h"

/**< CEnemy defines enemies in game */
class CEnemy : public CMobile
{
    public:
                CEnemy  ( int t, int l ) : CMobile ( 0, 0, t )
            {
                CObject::level = l;
                switch(t)
                {
                case 1:
                    HP = 100;
                    damage = 3*level;
                    break;
                case 2:
                    HP = 200;
                    damage = 5*level;
                    break;
                case 3:
                    HP = 300;
                    damage = 10*level;
                    break;
                }
            }
        void    print   ( std::ostream & os ) const
            {     os << "type: " << char (type + 87)
                     << ", HP: " << HP << ", damage: " << damage
                     << ", level: " << level;
            }
        CEnemy* clone ( void ) const
                { return new CEnemy ( *this ); }
};

#endif // CENEMY_H
