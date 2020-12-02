#include "CMap.h"

     CMap:: CMap            ( int w, int l )
                            : m_weight ( w ), m_length ( l )
{
        m_map = new CObject ** [l];
        for (int i = 0; i < l; i++)
            m_map[i] = new CObject * [w];
        AddFence();
}
     CMap:: ~CMap           ( void )
{
        for (int i = 0; i < m_length; i++)
        {
            for (int j = 0; j < m_weight; j++)
                delete m_map[i][j];
            delete [] m_map[i];
        }
        delete [] m_map;
}
     CMap:: CMap            ( const CMap & src )
                            : m_weight ( src . m_weight ), m_length ( src . m_length )
{
        m_map = new CObject ** [ m_length ];
        for ( int i = 0; i < m_length; i++ )
            m_map [ i ] = new CObject * [ m_weight ];

        for ( int i = 0; i < m_length; i++ )
            for ( int j = 0; j < m_weight; j++ )
                m_map [ i ] [ j ] = src . m_map [ i] [ j ] -> clone();

        for ( int i = 0; i < src . TowerCnt(); i++ )
            m_towers . push_back ( src . m_towers [ i ] );

        m_entrances . first  . x = src . m_entrances . first  . x;
        m_entrances . first  . y = src . m_entrances . first  . y;
        m_entrances . second . x = src . m_entrances . second . x;
        m_entrances . second . y = src . m_entrances . second . y;
}

void CMap:: AddFence        ( void )
{
        // border fences
        for ( int i = 0; i < m_length; i++ )
        {
            for ( int j = 0; j < m_weight; j++ )
            {
                if ( ! i || ! j || i + 1 == m_length || j + 1 == m_weight )
                    m_map [ i ] [ j ] = new CWall  ( i, j );
                else
                    m_map [ i ] [ j ] = new CSpace ( i, j );
            }
        }

        srand ( time ( NULL ) );
        SetEntrances();

        // random fences
        int walls = m_length * m_weight * 0.1; //10% of the map are walls
        for ( int i = 1; i <= walls; i++ )
        {
            int x = rand() % ( m_length - 2 ) + 1;
            int y = rand() % ( m_weight - 2 ) + 1;

            if ( isInMap ( x, y ) && isFree ( x, y ) )
            {
                delete m_map [ x ] [ y ];
                m_map [ x ] [ y ] = new CWall ( x, y );
                if ( ! CreatePath_BFS ( false ) . size() )
                {
                delete m_map [ x ] [ y ];
                m_map [ x ] [ y ] = new CSpace ( x, y );
                }
            }
        }
}
void CMap:: SetEntrances    ( void )
{
        int NorthOrWest = rand() % 2 + 1;
        int where;
        if ( NorthOrWest == 1 )  // entrance is in the north and exit is on south
        {
            where = rand() % ( m_weight - 2 ) + 1;
            delete m_map [ 0 ] [ where ];
            m_map [ 0 ] [ where ] = new CEntrance ( 0, where );
            delete m_map [ m_length - 1 ] [ m_weight - 1 - where ];
            m_map [ m_length - 1 ] [ m_weight - 1 - where ]
                        = new CEntrance ( m_length - 1, m_weight - 1 - where );
            m_entrances . first  . x = 0;
            m_entrances . first  . y = where;
            m_entrances . second . x = m_length - 1;
            m_entrances . second . y = m_weight - 1 - where;
        }
        else                    // entrance is in the west and exit is in the east
        {
            where = rand() % ( m_length - 2 ) + 1;
            delete m_map [ where ] [ 0 ];
            m_map [ where ] [ 0 ] = new CEntrance ( where, 0 );
            delete m_map [ m_length - 1 - where ] [ m_weight - 1 ];
            m_map [ m_length - 1 - where ] [ m_weight - 1 ]
                        = new CEntrance ( m_length - 1 - where, m_weight - 1 );
            m_entrances . first  . x = where;
            m_entrances . first  . y = 0;
            m_entrances . second . x = m_length - 1 - where;
            m_entrances . second . y = m_weight - 1;
        }
}

bool CMap:: AddTower        ( const CTower & t, int x, int y,
                              int & money )
{
        if ( isFree ( x, y ) )
        {
            int tmp = m_map [ x ] [ y ] -> GetDamage();
            delete m_map [ x ] [ y ];
            m_map [ x ][ y ] = new CTower ( t . type,
                                            t . coord . x, t . coord . y );

            // checks if tower doesn't block the way
            if ( ! CreatePath_BFS ( false ) . size() )
            {
                delete m_map [ x ] [ y ];
                m_map [ x ] [ y ] = new CSpace ( x, y );
                m_map [ x ] [ y ] -> SetDamage ( tmp );
                return false;
            }

            money = money - t . coast;
            RenewDamage ( t );
            m_towers . push_back ( t );
            return true;
        }

        return false;
}

bool CMap:: UpgradeTower    ( int x, int y, int & money )
{
        int ind = FindTower ( x, y );
        if ( ind == TowerCnt() )
        {
            cout << "Wrong coordinates" << endl;
            return false;
        }
        if ( m_map [ x ] [ y ] -> level == 3 )
        {
            cout << "Last level" << endl;
            return false;
        }
        if ( money - m_map [ x ] [ y ] -> upgradeCoast < 0 )
        {
            cout << "No money" << endl;
            return false;
        }

        // updating tower's info
        int d = m_map [ x ] [ y ] -> damage;
        m_map [ x ] [ y ] -> coast        = m_map [ x ] [ y ] -> upgradeCoast;
        m_map [ x ] [ y ] -> level++;
        m_map [ x ] [ y ] -> damage       = m_map [ x ] [ y ] -> damage * 1.3;
        m_map [ x ] [ y ] -> HP           = m_map [ x ] [ y ] -> HP * 1.3;
        m_map [ x ] [ y ] -> upgradeCoast = m_map [ x ] [ y ] -> coast * 1.5;

        m_towers [ ind ] . level++;
        m_towers [ ind ] . coast        = m_towers [ ind ] . upgradeCoast;
        m_towers [ ind ] . damage       = m_towers [ ind ] . damage * 1.3;
        m_towers [ ind ] . HP           = m_towers [ ind ] . HP * 1.3;
        m_towers [ ind ] . upgradeCoast = m_towers [ ind ] . coast * 1.5;

        money = money - m_map [ x ] [ y ] -> coast;

        // adding bigger damage to map
        int newD = m_map [ x ] [ y ] -> damage - d;
        CTower t ( GetType ( ind ), GetX ( ind ), GetY ( ind ) );
        t . SetDamage ( newD );
        RenewDamage ( t );

        return true;
}

void CMap:: RenewDamage     ( const CTower & t )
{
        vector < CCoord > neib;
        if ( t . type == 1 )
            neib = GetNeighborsA ( t . coord . x, t . coord . y );
        else if ( t . type == 2 )
            neib = GetNeighborsB ( t . coord . x);
        else
            neib = GetNeighborsC ( t . coord . x, t . coord . y);

        for ( auto i : neib )
            if ( isFree ( i . x, i . y ) )
                m_map [ i . x ] [ i . y ] -> damage += t . damage;
}

void CMap:: RenewHP         ( void )
{
        for ( int i = 0; i  < TowerCnt(); i++ )
            m_map [ GetX ( i ) ] [ GetY ( i ) ] ->
                                   SetHP ( m_towers [ i ] . GetHP() );
}

void CMap:: PrintMap        ( void ) const
{
        for ( int i = 0; i < m_length; i++ )
        {
            for ( int j = 0; j < m_weight; j++ )
                cout << * m_map [ i ][ j ];
            cout << endl;
        }
        cout << endl;
}

void CMap:: PrintTowers     ( int money ) const
{
        if ( ! TowerCnt() )
            cout <<  "You don't have any tower :( " << endl
                 <<  "Be a good defender! Buy one!" << endl;
        else
        {
            cout <<  "Your tower(s): " << endl;
            cout <<  "TYPE:    "
                 <<  "LEVEL:    "
                 <<  "HP:    "
                 <<  "DAMAGE:    "
                 <<  "Upgrade coast:   "
                 <<  "Coordinates:   "
                 <<  "Can you upgrade it?    " <<  endl;

            for ( int i = 0; i < TowerCnt(); i++ )
            {
                cout << char(m_towers[i].type+64) << "         "
                     << m_towers[i].level << "        "
                     << m_towers[i].HP << "     "
                     << m_towers[i].damage << "         "
                     << m_towers[i].upgradeCoast << "             "
                     << m_towers[i].coord << "          ";
                if ( m_towers [ i ] . upgradeCoast <= money && m_towers [ i ] . level < 3 )
                    cout << "Yes!! Do it!!!" << endl;
                else
                    cout << "No... " << endl;
            }
        }
}

void CMap:: print_info_Towers ( void ) const
{
        cout << "Towers: " << endl;
        for ( int i = 2; i < 5; i++ )
            cout << char ( i + 63 ) <<": coast = " << i * 25
                                    << ", damage = " << i * 25
                                    << ", HP = "  << i * 25 << endl;
}

void CMap:: print_coord_Towers ( void ) const
{
        for ( int i = 0; i < TowerCnt(); i++ )
            cout << char ( m_towers [ i ] . type + 64 ) << " is at "
                 << m_towers [ i ] . coord
                 << ". Coasts "
                 << m_towers [ i ] . upgradeCoast << endl;
}

void CMap:: print_path      ( vector < CCoord > path ) const
{
        // creating char map
        char ** attack = new char * [ m_length ];
        for ( int i = 0; i < m_length; i++ )
            attack [ i ] = new char [ m_weight ];

        // adding walls
        for ( int i = 0; i < m_length; i++ )
            for ( int j = 0; j < m_weight; j++ )
            {
                if ( ! isFree ( i, j ) )
                    attack [ i ] [ j ] = '#';
                else
                    attack [ i ] [ j ] = ' ';
            }
        // adding towers
        for ( auto i : m_towers )
            attack [ i . coord . x ] [ i . coord . y ] = char ( i . type + 64 );

        // adding enemies
        for ( auto i : path )
            attack [ i . x ] [ i . y ] = '%';

        // printing
        for ( int i = 0; i < m_length; i++ )
        {
            for ( int j = 0; j < m_weight; j++ )
                cout << attack [ i ] [ j ];
            cout << endl;
        }
        cout << endl;

        // deleting char map
        for ( int i = 0; i < m_length; i++ )
            delete [] attack [ i ];
        delete [] attack;
}

int  CMap:: FindTower       ( int x, int y ) const
{
        for ( int i = 0; i < TowerCnt(); i++ )
            if ( m_towers [ i ] . coord == make_pair ( x, y ) )
                return i;
        return TowerCnt();
}
bool CMap:: isFree          ( int x, int y ) const
{
        return isInMap ( x, y )
            && m_map [ x ] [ y ] -> CanIBuildHere();
}
bool CMap:: isInMap         ( int x, int y ) const
{
        return x >= 0 && x < m_length &&
               y >= 0 && y < m_weight;
}

vector < CCoord > CMap:: GetNeighbors   ( int x, int y ) const
{
        vector < CCoord > tmp;
        if ( isFree ( x - 1, y )
        || ( m_entrances . second == make_pair ( x - 1, y ) ) )
            tmp . push_back ( CCoord ( x - 1, y ) );
        if ( isFree ( x, y - 1 )
        || ( m_entrances . second == make_pair ( x, y - 1 ) ) )
            tmp . push_back ( CCoord ( x, y - 1 ) );
        if ( isFree ( x, y + 1 )
        || ( m_entrances . second == make_pair ( x, y + 1 ) ) )
            tmp . push_back ( CCoord ( x, y + 1 ) );
        if ( isFree ( x + 1, y )
        || ( m_entrances . second == make_pair ( x + 1, y ) ) )
            tmp . push_back ( CCoord ( x + 1, y ) );

        return tmp;
}

vector < CCoord > CMap:: GetNeighborsA  ( int x, int y ) const
{
        vector < CCoord > neib =
        {
            CCoord ( x - 1, y - 1 ), CCoord ( x - 1, y ), CCoord ( x - 1, y + 1 ),
            CCoord ( x, y - 1 ),  /* CCoord ( x, y )  */  CCoord ( x, y + 1 ),
            CCoord ( x + 1, y - 1 ), CCoord ( x + 1, y ), CCoord ( x + 1, y + 1 )
        };
        return neib;
}

vector < CCoord > CMap:: GetNeighborsB  ( int x ) const
{
        vector < CCoord > neib;
        for ( int y = 0; y < m_weight; y++ )
            neib . push_back ( CCoord ( x, y ) );
        return neib;
}

vector < CCoord > CMap:: GetNeighborsC  ( int x, int y ) const
{
        vector < CCoord > neib;
        for ( int u = 0; u < m_weight; u++ )
            neib . push_back ( CCoord ( x, u ) );

        for ( int u = 0; u < m_length; u++ )
            neib . push_back ( CCoord ( u, y ) );

        return neib;
}

vector < CCoord >        BuildPath      ( CCoord start, CCoord target,
                                          map < CCoord, CCoord > prev )
{
        vector < CCoord > path;
        path . push_back ( target );
        while ( start != target )
        {
            auto it = prev . find ( target );
            target = it -> second;
            path . push_back ( target );
        }
        return path;
}

vector < CCoord > CMap:: CreatePath_BFS ( bool print ) const
{
        deque   < CCoord >          opened;
        list    < CCoord >          closed;
        CCoord                      current;
        map     < CCoord, CCoord >  prev;
        vector < CCoord >           res;

        opened . push_back ( m_entrances . first );
        while ( ! opened . empty() )
        {
            current = opened . front();
            opened . pop_front();
            if ( current == m_entrances . second)
            {
                if ( print ) // prints path
                    return BuildPath ( m_entrances . first,
                                       m_entrances . second, prev );
                else // only returns that path is found
                {
                    res . push_back ( CCoord ( 1, 1 ) );
                    return res;
                }
            }
            vector < CCoord > neib = GetNeighbors ( current . x, current . y );
            for ( auto i : neib )
            {
                if ( find ( opened . begin(), opened . end(), i ) == opened . end()
                  && find ( closed . begin(), closed . end(), i) == closed . end() )
                {
                    opened . push_back ( i );
                    prev . insert ( make_pair ( i, current ) );
                }

            }
            closed . push_back ( current );
        }
        return res;
}

double      distance        ( CCoord src, CCoord dst )
/**< calculates Euclidean distance between two points */
{
        // sqrt ( ( x1 - x2 )^2 + ( y1 - y2 )^2 )
        return ( ( double ) sqrt (
            ( src . x - dst . x ) * ( src . x - dst . x )
          + ( src . y - dst . y ) * ( src . y - dst . y ) ) );
}
vector < CCoord > CMap:: CreatePath_A   ( void ) const
{
        map < CCoord, CCoord >                          prev;
        set < pair < pair < double, int >, CCoord > >   opened;
        set < CCoord >                                  closed;

        opened . insert ( make_pair ( make_pair ( 0.0, 0 ), m_entrances . first ) );

        while ( ! opened . empty() )
        {
            pair < pair < double, int >, CCoord > current = * opened . begin();
            opened . erase ( opened . begin() );

            double f, g, h;
            vector < CCoord > neib = GetNeighbors ( current . second . x,
                                                    current . second . y );
            for ( auto it : neib )
            {
                if ( m_entrances . second == it )
                {
                    prev [ it ] = current . second;
                    return BuildPath ( m_entrances . first,
                                       m_entrances . second, prev );
                }
                else if ( closed . find ( it ) == closed . end() )
                {
                    // calculates new g, h, f
                    g = current . first . second + m_map [ it . x ] [ it . y ] -> damage;
                    h = distance ( it, m_entrances . second );
                    f = g + h;

                    auto i = opened . end();
                    for ( auto j = opened . begin();
                               j != opened . end(); ++j )
                    {
                        if ( j -> second == it )
                            i = j;
                    }

                    if ( i == opened . end() || i -> first . first > f )
                    {
                        opened . insert ( make_pair ( make_pair ( f, g ), it ) );
                        prev [ it ] = current . second;
                    }
                }
            }
            closed . insert ( current . second );
        }
        vector < CCoord > res;
        return res;
 }
