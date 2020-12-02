#ifndef CATTACK_H
#define CATTACK_H

#include "CMap.h"

void                _Attack         ( CMap & m, int & money, int & win, int & loss );
/**< random number of enemies attack towers 						*/
vector < CEnemy >   CreateEnemies   ( int n );
/**< creates random number of random enemies, returns vector of enemies 		*/
int                 UnderAttack     ( CMap & m, vector < CEnemy > enemies,
                                      vector < CCoord > path, int & brokenTowers );
/**< provides attack for each enemy, returns number of killed enemies 			*/
int                 DamageTower     ( const CEnemy & e, CMap & m, int x, int y );
/**< decides which enemy attack to use, returns number of destroyed towers 		*/
int                 damage          ( vector < CCoord > neib, const CEnemy & e, CMap & m );
/**< decreases towers' HP, returns number of destroyed towers 				*/
void                PrintEnemies    ( vector < CEnemy > e1, vector < CEnemy > e2,
                                      int n, int e );
/**< prints information about enemies 							*/
bool                PrintScore      ( int deadEnemies, int e, int brokenTowers );
/**< prints score, returns true for win  						*/
#endif // CATTACK_H
