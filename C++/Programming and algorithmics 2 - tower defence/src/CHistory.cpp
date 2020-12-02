#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include "CHistory.h"

void    ClearHistory    ( void )
{
        ofstream history ( "examples/history.txt" , ios::out | ios::trunc );
        history . close();
}

void    SaveInfo        ( const CMap & m ) {
        ofstream history ( "examples/history.txt" , ios::app );

        for ( int i = 0; i < m . m_length; i++ )
        {
            for ( int j = 0; j < m . m_weight; j++ )
                history << * m . m_map [ i ] [ j ];
                history << endl;
        }
        history << endl;
        history . close();
}

//<-------- SAVING ----------------------------------------------->
void    SaveMainInfo    ( int money, int win, int loss, int level,
                          int l, int w, int t_cnt )
{
        ofstream lastgame ( "examples/main_info.txt" );

        if ( ! lastgame )
            return;
        // saving money, win, loss and level
        lastgame << money << endl;
        lastgame << win << endl;
        lastgame << loss << endl;
        lastgame << level << endl;

        // saving length, weight and number of towers
        lastgame << l << endl << w << endl;
        lastgame << t_cnt << endl;
        lastgame . close();
}

void    SaveWalls       ( const CMap & m )
{
        ofstream lastgame ( "examples/walls.txt" );
        if ( ! lastgame )
            return;
        // saving number of walls and walls
        int cnt = 0;
        for ( int i = 0; i < m . m_length; i++ ) {
            for ( int j = 0; j < m . m_weight; j++ )
                if ( ! m . isFree ( i, j ) &&
                     ! ( ! i || ! j || i + 1 == m . m_length || j + 1 == m . m_weight) )
                    cnt++;
        }
        lastgame << cnt << endl;
        for ( int i = 0; i < m . m_length; i++ ) {
            for ( int j = 0; j < m . m_weight; j++ )
                if ( ! m . isFree ( i, j ) &&
                     ! ( ! i || ! j || i + 1 == m . m_length || j + 1 == m . m_weight) )
                    lastgame << i << endl << j << endl;
        }
        lastgame . close();
}

void    SaveEntrances   ( int x1, int y1, int x2, int y2 )
{
        ofstream lastgame ( "examples/entrances.txt" );
        if ( ! lastgame )
            return;
        // saving entrances
        lastgame << x1 << endl;
        lastgame << y1 << endl;
        lastgame << x2 << endl;
        lastgame << y2 << endl;
        lastgame . close();
}

void    SaveTowers      ( const CMap & m )
{
        ofstream lastgame ( "examples/towers.txt" );

        if ( ! lastgame )
            return;
        // saving towers
        for ( int i = 0; i < m . TowerCnt(); i++ )
        {
            lastgame << m . GetX     ( i ) << endl;
            lastgame << m . GetY     ( i ) << endl;
            lastgame << m . GetType  ( i ) << endl;
            lastgame << m . GetLevel ( i ) << endl;
        }
        lastgame . close();
}

void    SaveGame        ( const CMap & m, int money, int win, int loss, int level)
{

        SaveMainInfo    ( money, win, loss, level,
                          m . m_length, m . m_weight, m . TowerCnt() );

        SaveWalls       ( m );

        SaveEntrances   ( m . m_entrances . first  . x, m . m_entrances . first  . y,
                          m . m_entrances . second . x, m . m_entrances . second . y );

        SaveTowers      ( m );
}

//<-------- LOADING ----------------------------------------------------->
bool    LoadMainInfo    ( int & money, int & win, int & loss, int & level,
                          int & l, int & w, int & t_cnt )
{
        ifstream lastgame ( "examples/main_info.txt" );
        if ( ! lastgame || lastgame . peek() == EOF )
            return false;
        // reading money, win, loss and level
        lastgame >> money;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> win;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> loss;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> level;
        if ( lastgame . peek() == EOF ) { return false; }

        // reading length, weight and number of towers
        lastgame >> l;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> w;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> t_cnt;
        lastgame . close();
        return true;
}

bool    LoadWalls       ( CMap & m )
{
        ifstream lastgame ( "examples/walls.txt" );
        if ( ! lastgame || lastgame . peek() == EOF )
            return false;

        // filling map with spaces
        for ( int i = 0; i < m . m_length; i++ )
            for ( int j = 0; j < m . m_weight; j++ )
            {
                delete m . m_map [ i ] [ j ];
                m . m_map [ i ] [ j ] = new CSpace ( i, j );
            }
        int w_cnt;

        // reading walls
        lastgame >> w_cnt;

        for ( int i = 0; i < w_cnt; i++ )
        {
            int x, y;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> x;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> y;
            delete m . m_map [ x ] [ y ];
            m . m_map [ x ] [ y ] = new CWall ( x, y );
        }

        // border walls
        for ( int i = 0; i < m . m_length; i++ )
        {
            for ( int j = 0; j < m . m_weight; j++ )
            {
                if ( ! i || ! j
                    || i + 1 == m . m_length || j + 1 == m . m_weight )
                {
                    delete m . m_map [ i ] [ j ];
                    m . m_map [ i ] [ j ] = new CWall ( i, j );
                }
            }
        }

        lastgame . close();

        return true;
}

bool    LoadEntrances   ( CMap & m )
{
        ifstream lastgame ( "examples/entrances.txt" );
        if ( ! lastgame || lastgame . peek() == EOF )
            return false;
        // reading entrances
        int x, y;

        // entrance
        lastgame >> x;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> y;
        delete m . m_map [ x ] [ y ];
        m . m_map [ x ] [ y ] = new CEntrance ( x, y );
        m . m_entrances . first . x = x;
        m . m_entrances . first . y = y;

        // exit
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> x;
        if ( lastgame . peek() == EOF ) { return false; }
        lastgame >> y;
        delete m.m_map [ x ] [ y ];
        m . m_map [ x ] [ y ] = new CEntrance ( x, y );
        m . m_entrances . second . x = x;
        m . m_entrances . second . y = y;
        lastgame . close();

        return true;
}

bool    LoadTowers      ( CMap & m, int t_cnt )
{
        ifstream lastgame ( "examples/towers.txt" );
        if ( ( ! lastgame || lastgame . peek() == EOF ) && t_cnt > 0 )
            return false;
        // reading towers
        for ( int i = 0; i < t_cnt; i++ )
        {
            int x, y, type, lvl, mn = 50000;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> x;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> y;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> type;
            if ( lastgame . peek() == EOF ) { return false; }
            lastgame >> lvl;
            delete m . m_map [ x ] [ y ];
            m . m_map [ x ] [ y ] = new CSpace ( x, y );
            CTower t ( type, x, y );
            m . AddTower ( t, x, y, mn );
            while ( m . GetLevel ( i ) != lvl )
                m . UpgradeTower ( x, y, mn );
        }
        lastgame . close();

        return true;
}

CMap    LoadGame        ( int & money, int & win, int & loss, int & level ) {

        int l, w, t_cnt;

        if ( ! LoadMainInfo    ( money, win, loss, level, l, w, t_cnt ) )
            return DefaultGame ( money, win, loss, level );

        CMap m ( w, l ) ;

        if ( ! LoadWalls  ( m ) || ! LoadEntrances   ( m )
            || ! LoadTowers ( m, t_cnt ) )
            return DefaultGame ( money, win, loss, level );

        return m;
}

CMap    DefaultGame     ( int & money, int & win, int & loss, int & level )
{
        cout << "No saved game (" << endl << endl;
        money = 500;
        win = loss = level = 0;
        CMap m ( 30, 15 );
        return m;
}
