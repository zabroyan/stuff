#include "CAttack.h"

int     damage          ( vector < CCoord > neib, const CEnemy & e,
                          CMap & m )
{
        int cnt = 0;
        // going trough enemy's attack area an decreasing towers' HP
        for ( auto it : neib )
        {
            // position is valid
            if ( m . isInMap ( it . x, it . y ) )
            {
                int i = m . FindTower ( it . x, it . y );
                // tower is at this position
                if ( i != m . TowerCnt() )
                {
                    int hp = m . m_map [ it . x ] [ it . y ] -> GetHP();
                    m . m_map [ it . x ] [ it . y ] -> SetHP ( hp - e . GetDamage() );

                    // towers is destroyed
                    if ( m . m_map [ it . x ] [ it . y ] -> GetHP() <= 0 )
                    {
                        cnt++;
                        cout << "You lost one tower at position ("
                             << it . x << ", " << it . y <<")!" << endl;
                        // renewing map's damage
                        CTower t ( m . GetType ( i ), it . x, it . y );
                        int d = -1 * m . m_map [ it . x ] [ it . y ] -> GetDamage();
                        t . SetDamage ( d );
                        m . RenewDamage ( t );
                        delete m . m_map [ it . x ] [ it . y ];
                        m . m_map [ it . x ] [ it . y ] = new CSpace ( it . x, it . y );
                        m . m_towers . erase ( m . m_towers . begin() + i );
                    }
                }
            }
        }
        return cnt;
}

int     DamageTower     ( const CEnemy & e, CMap & m, int x, int y )
{
        if ( e . GetType() == 1 )
            return damage ( m . GetNeighborsA ( x, y ), e, m );
        else if ( e . GetType() == 2 )
            return damage ( m . GetNeighborsB ( x ), e, m );
        else
            return damage ( m . GetNeighborsC ( x, y ), e, m );
}

int     UnderAttack     ( CMap & m, vector < CEnemy > enemies,
                          vector < CCoord > path, int & brokenTowers )
{
        int deadEnemies = 0;
        // each enemy goes through all map or until it's dead
        for ( auto i : enemies )
        {
            for ( unsigned int j = 0; j < path . size(); j++ )
            {
                // updating enemies' HP
                int hp = i . GetHP();
                i . SetHP ( hp - m . m_map [ path [ j ] . x ] [ path [ j ] . y ] -> GetDamage() );
                brokenTowers += DamageTower ( i, m, path [ j ] . x, path [ j ] . y );

                // enemy is dead
                if ( i . GetHP() <= 0 )
                {
                    cout << "One enemy is dead at position " << path [ j ] << "!" << endl;
                    deadEnemies++;
                    j = path . size();
                }
            }
        }
        // returning towers' HP
        m . RenewHP();
        return deadEnemies;
}

vector < CEnemy >   CreateEnemies ( int n )
{
        vector < CEnemy > tmp;
        for ( int i = 0; i < n; i++ )
        {
            // enemy with random type and random level
            int t = rand() % 3 + 1;
            int l = rand() % 3 + 1;
            CEnemy e ( t, l );
            tmp . push_back ( e );
        }
        return tmp;
}

void    PrintEnemies    ( vector < CEnemy > e1, vector < CEnemy > e2,
                          int n, int e )
{
        // printing enemies
        cout << "Your towers are under attack!!!" << endl;
        cout << "There " << e << " enemies!" << endl;
        cout << n << " of them will use fast path and " << ( e - n ) << " will use safe path!" << endl;
        cout << "Be careful!" << endl << endl;
        cout << "Printing info about enemies:" << endl << endl;
        cout << "The fastest: " << endl;

        for ( auto i : e1 )
            cout << i << endl;
        cout << endl;
        if ( e - n > 0 )
        {
            cout << "The most careful: " << endl;
            for ( auto i : e2 )
                cout << i << endl;
            cout << endl << endl;
        }
}

bool    PrintScore      ( int deadEnemies, int e, int brokenTowers )
{
        cout << endl;
        // printing scores for attack
        if ( deadEnemies == e )
        {
            cout << "You killed all enemies! Wow!!" << endl;
            return 1;
        }
        else if ( deadEnemies > 0 )
        {
            cout << "You killed " << deadEnemies << " enemies! Wow!!" << endl;
            cout << "Escaped " << ( e - deadEnemies ) << " enemies" << endl;
            return 0;
        }
        else
        {
            cout << "Everyone escaped :(" << endl;
            cout << "Be a better defender next time" << endl;
            return 0;
        }
        cout << endl;
        cout << "You lost " << brokenTowers << " towers" << endl;
}

void    _Attack ( CMap & m, int & money, int & win, int & loss)
{
        int t_cnt = m . TowerCnt ();
        srand ( time ( NULL ) );

        // creating paths for enemies
        vector < CCoord > fast_path = m . CreatePath_BFS ( true );
        vector < CCoord > safe_path = m . CreatePath_A();

        // number of enemies
        int e = rand() % 5 + 5;
        // number of enemies that will use fast path (e-n will use safe path)
        int n = rand() % e + 1;

        vector < CEnemy > fast_enemy = CreateEnemies ( n );
        vector < CEnemy > careful_enemy = CreateEnemies ( e - n );
        PrintEnemies ( fast_enemy, careful_enemy, n, e );

        cout << "Fastest path: " << endl;
        m . print_path ( fast_path );
        cout << "Safest path: " << endl;
        m . print_path ( safe_path );

        int deadEnemies = 0, brokenTowers = 0;
        deadEnemies += UnderAttack ( m, fast_enemy, fast_path, brokenTowers );
        deadEnemies += UnderAttack ( m, careful_enemy, safe_path, brokenTowers );

        win += PrintScore ( deadEnemies, e, brokenTowers );
        money += deadEnemies * 50;

        if ( brokenTowers == t_cnt && t_cnt )
            loss += 1;

}
