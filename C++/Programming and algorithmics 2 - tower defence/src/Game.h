#ifndef GAME_H
#define GAME_H
#include <cstring>
#include <cstdlib>
#include <stdlib.h>
#include <time.h>
#include <cstdio>
#include <cctype>
#include <ctime>
#include <climits>
#include <cmath>
#include <cassert>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <list>
#include <algorithm>
#include <functional>
#include <memory>
#include "CInit.h"
#include "CAttack.h"
using namespace std;
/** that's the map
# - walls
A,B,C - towers
% - enemies
##############################
#                            #
#        #     #      B      #
#           ####             #
#   #                     #  #
%%%%%%%%%%%%%%%%%%%%%%%%###  #
#               #      %%%%%%#
#          A   #            %#
#              #            %#
#                   #       %%
#                            #
#  #      #     #            #
#                    CB      #
#            #       ##      #
##############################
**/

void BeautifullyPrint_level ( int i );
/**< Beautifully prints number of level 		*/
void BeautifullyPrint_score ( int win, int loss );
/**< Beautifully prints score 				*/
void PrintWelcome           ( void );
/**< prints rules 					*/
void Game                   ( CMap m, int money, int win, int loss, int level );
/**< starts a new game or continues saved 		*/
void Play                   ( void );
/**<  before the game 					*/

#endif // GAME_H
