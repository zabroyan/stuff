#ifndef CHISTORY_H
#define CHISTORY_H
#include "CMap.h"

void ClearHistory   ( void );
/**< clears file history.txt */
void SaveInfo       ( const CMap & m );
/**< saves history of your last game */
void SaveGame       ( const CMap & m, int money, int win, int loss, int level );
/**< saves game */
CMap LoadGame       ( int & money, int & win, int & loss, int & level );
/**< loads saved game */

void    SaveMainInfo    ( int money, int win, int loss, int level,
                          int l, int w, int t_cnt );
/**< saves money, wins, losses, level, length and weight of map and count of towers */
void    SaveWalls       ( const CMap & m );
/**< saves walls */
void    SaveEntrances   ( int x1, int y1, int x2, int y2 );
/**< saves entrance and exit */
void    SaveTowers      ( const CMap & m );
/**< saves towers */

bool    LoadMainInfo    ( int & money, int & win, int & loss, int & level,
                          int & l, int & w, int & t_cnt );
/**< loads money, wins, losses, level, length and weight of map and count of towers */
bool    LoadWalls       ( CMap & m );
/**< loads walls */
bool    LoadEntrances   ( CMap & m );
/**< loads entrance and exit */
bool    LoadTowers      ( CMap & m, int t_cnt );
/**< loads towers */
CMap    DefaultGame     ( int & money, int & win, int & loss, int & level );
/**< creates game with default settings */

#endif // CHISTORY_H
