#include "CInit.h"

void    PrintInfo       ( const CMap & m, int money )
{
        cout << "Your map looks like this: " << endl << endl;
        m . PrintMap();
        if ( money > 0 )
            cout << "Wow!! You have money: " << money << endl;
        else
            cout << "You don't have money" << endl;
        m . PrintTowers ( money );
        cout << endl;
}

int     getCoords          ( void )
{
        string str;
        cin >> str;
        int x = 0;
        for ( char c : str )
        {
            if ( isdigit ( c ) )
                x = x * 10 + ( c - '0' );
            else
            {
                cout << "Only numbers please!" << endl;
                return -1;
            }
        }
    return x;
}

bool    BuyTower        ( CMap & m,int & money )
{
        // getting type
        int t;
        string type;
        cout << "Choose a type of your new and wonderful tower (A, B or C)" << endl;
        cin >> type;
        if (type == "A")
            t = 1;
        else if (type == "B")
            t = 2;
        else if (type == "C")
            t = 3;
        else
        {
            cout << "Wrong type" << endl;
            return false;
        }

        if ( money - CTower ( t, 0, 0 ) . GetCoast() < 0 )
        {
            cout << "You don't have money" << endl;
            return false;
        }
        cout << "Now I need coordinates (just write x y. No commas, no parentheses)" << endl;

        int x = getCoords();
        int y = getCoords();

        if ( x == -1 || y == -1 )
            return false;
        // adding tower
        CTower tower ( t, x, y );
        if ( m . AddTower ( tower, x, y, money ) )
        {
            cout << "Tower: " << type << " added. Congratulations!" << endl;
            return true;
        }
        else
        {
            cout << "Most likely that coordinates were taken :(" << endl;
            return false;
        }

}

bool    UpgradeTower    ( CMap &m, int & money )
{
        cout << "Choose a tower to upgrade (i need coordinates :) )" << endl;

        int x = getCoords();
        int y = getCoords();

        if ( x == -1 || y == -1 )
            return false;

        if ( m . UpgradeTower ( x, y, money ) )
        {
            cout << "Tower is updated" << endl;
            return true;
        }
        else
        {
            return false;
        }
}

void    buy_upgrade     ( CMap & m, int & money,
                          function < bool ( CMap &, int & ) > f )
{
        // endless cycle until success or exit
        while ( true ){
            if ( f ( m, money ) )
                break;
            string x;
            cout << "Press 1 to try again, 0 to exit" << endl;
            cin >> x;
            if (x == "0" || cin . eof() )
                break;
        }
}

void    _Init           ( CMap & m, int & money, int win, int loss, int level )
{
        PrintInfo ( m, money );
        while ( true )
        {
            string x;
            cout << "To buy a new tower press 1" << endl
                 << "To upgrade existing press 2" << endl
                 << "To exit press 0" << endl
                 << "To save the game press 3 (!!! it will overwrite your last saved game !!!)" << endl;
            cin >> x;
            cout << endl;

            if ( x == "1" )
            {
                m . PrintMap();
                m . print_info_Towers();
                buy_upgrade ( m, money, BuyTower );
            }

            else if ( x == "2" )
            {
                if ( m . TowerCnt() == 0 )
                    cout << "You don't have any tower" << endl;
                else
                {
                    m . print_coord_Towers();
                    buy_upgrade ( m, money, UpgradeTower );
                }
            }

            else if ( x == "3" )
	    {
		cout << "Game is saved!" << endl;
                SaveGame ( m, money, win, loss, level );
	    }

            else if ( x == "0" || cin . eof() )
                break;
        }

        PrintInfo ( m, money );
        SaveInfo ( m );
}

