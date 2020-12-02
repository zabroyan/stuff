#ifndef CINIT_H
#define CINIT_H
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <functional>
#include "CMap.h"
#include "CHistory.h"

void PrintInfo      ( const CMap & m, int money );
/**< prints map and money 						*/
int  getCoords      ( void );
/**< takes string and converts to int 					*/
bool BuyTower       ( CMap &m,int & money );
/**< adds new tower to map 						*/
bool UpgradeTower   ( CMap &m, int & money );
/**< upgrades existing tower 						*/
void buy_upgrade    ( CMap & m, int & money, function<bool(CMap&, int&)> );
/**< just endless cycle until success 					*/
void _Init          ( CMap &m, int & money, int win, int loss, int level );
/**< asks player to choose (buy tower, upgrade, save game or continue) 	*/


#endif // CINIT_H
