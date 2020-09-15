#ifndef CMAP_H
#define CMAP_H

#include "CWall.h"
#include "CSpace.h"
#include "CEntrance.h"
#include "CTower.h"
#include "CEnemy.h"

#include <ctime>
#include <iostream>
#include <vector>
#include <list>
#include <deque>
#include <map>
#include <stack>
#include <cstring>
#include <set>
#include <algorithm>

using namespace std;
class CMap
{
    public:
                            CMap                ( int w, int l );
	/**< constructor with parameters weight and length                  */        
                            ~CMap               ( void );
	/**< destructor 						    */        
                            CMap                ( const CMap & src );

	/**< copy constructor 						    */        
        void                AddFence            ( void );
	/**< adds border fences and random fences (10% of map)              */
        void                SetEntrances        ( void );
	/**< randomly chooses entrance 					    */
        bool                AddTower            ( const CTower & t,
                                                  int x, int y, int & money );
 	/**< adds towers to map, returns if tower was added                 */
        bool                UpgradeTower        ( int x, int y, int & money );
        /**< upgrades existing tower, returns if tower was upgraded         */
        void                RenewDamage         ( const CTower & t );
        /**< increases/decreases damage around the tower                    */
        void                RenewHP             ( void );
        /**< return tower's HP to its maximum                               */

        void                PrintMap            ( void ) const;
        /**< prints map                                                     */
        void                PrintTowers         ( int money ) const;
        /**< prints info about existing towers                              */
        void                print_info_Towers   ( void ) const;
        /**< prints starting info about towers                              */
        void                print_coord_Towers  ( void ) const;
        /**< prints coordinates of existing towers                          */
        void                print_path          ( vector < CCoord > path ) const;
        /**< prints path for enemies                                        */

        bool                isFree              ( int x, int y ) const;
        /**< checks if there's a free place at this position                */
        bool                isInMap             ( int x, int y ) const;
        /**< checks if coordinates are valid                                */

        vector < CCoord >   CreatePath_BFS      ( bool print ) const;
        /**< creates path using BFS algorithm                               */
        vector < CCoord >   CreatePath_A        ( void ) const;
        /**< creates path using A* algorithm                                */

        vector < CCoord >   GetNeighbors        ( int x, int y ) const;
        /**< creates vector of north, south, west, east
                                            neighbors of given coordinates  */
        vector < CCoord >   GetNeighborsA       ( int x, int y ) const;
        /**< creates vector of north, south, west, east,
                               north-west, north-east, south-west, south-east
                                            neighbors of given coordinates  */
        vector < CCoord >   GetNeighborsB       ( int x ) const;
        /**< creates vector of all west and all east
                                            neighbors of given coordinates  */
        vector < CCoord >   GetNeighborsC       ( int x, int y ) const;
        /**< creates vector of all north, south, west, east
                                            neighbors of given coordinates  */

        inline int          GetX                ( int i ) const
                            { return m_towers[i].coord.x; }
        /**< returns coordinate x of tower at position i in m_towers        */
        inline int          GetY                ( int i ) const
                            { return m_towers[i].coord.y; }
        /**< returns coordinate y of tower at position i in m_towers        */
        inline int          GetType             ( int i ) const
                            { return m_towers[i].type; }
        /**< returns type of tower at position i in m_towers                */
        inline int          GetLevel            ( int i ) const
                            { return m_towers[i].level; }
        /**< returns level of tower at position i in m_towers               */
        inline int          TowerCnt            ( void ) const
                            { return m_towers.size();}
        /**< returns number of existing towers                              */
        int                 FindTower           ( int x, int y ) const;
        /**< returns position of tower with given coordinates,
                                    otherwise returns count of towers       */

friend  void                SaveInfo            ( const CMap & m );
friend  void                SaveGame            ( const CMap & m, int money, int win, int loss, int level );
friend  void                SaveWalls           ( const CMap & m );
friend  void                SaveTowers          ( const CMap & m );
friend  CMap                LoadGame            ( int & money, int & win, int & loss, int & level );
friend  bool                LoadWalls           ( CMap & m );
friend  bool                LoadEntrances       ( CMap & m );
friend  bool                LoadTowers          ( CMap & m, int t_cnt );
friend  int                 UnderAttack         ( CMap & m, vector < CEnemy > enemies,
                                                  vector < CCoord > path, int & brokenTowers );
friend  int                 damage              ( vector < CCoord > neib,
                                                  const CEnemy & e, CMap & m );
friend  int                 DamageTower         ( const CEnemy & e, CMap & m, int x, int y );

    protected:
        CObject ***                 m_map;
        vector < CTower >           m_towers;
        pair < CCoord, CCoord >     m_entrances;
        int                         m_weight;
        int                         m_length;

};

#endif // CMAP_H
