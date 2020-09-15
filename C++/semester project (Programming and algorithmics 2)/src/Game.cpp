#include "Game.h"
#include <chrono>
#include <thread>

void    BeautifullyPrint_level  ( int i )
{
        cout << "     ***********" << endl;
        cout << "     * LEVEL " << i+1 << " *" << endl;
        cout << "     ***********" << endl;
}

void    BeautifullyPrint_score  ( int win, int loss )
{
        cout << "     ***************" << endl;
        cout << "     *    SCORE    *" << endl;
        cout << "     *    YOU:   " << win  << " *" << endl;
        cout << "     *    ENEMY: " << loss << " *" << endl;
        cout << "     ***************" << endl;
}

void    PrintWelcome            ( void )
{
    cout << "Welcome to the greatest Tower defense game you've ever seen!!!" << endl;
    cout << "Just short rules below:" << endl << endl;
    cout << "***** TO SKIP PRESS ANY BUTTON *****" << endl << endl;
    this_thread::sleep_for(chrono::seconds(1));
    cout << "The main goal is to kill as many enemies as you can and to defend your towers" << endl;
    cout << "You will have 5 chances to win" << endl;
    cout << "You'll get +1 score for killing ALL enemies before they reach the exit" << endl;
    cout << "And enemies will get +1 if they destroy ALL your towers" << endl << endl;
    cout << "There're 3 types of towers:" << endl;
    cout << "Tower A: the cheapest and the weakest" << endl;
    cout << "Damage area: " << endl;
    cout << "_______" << endl;
    cout << "|_|_|_|" << endl;
    cout << "|_|A|_|" << endl;
    cout << "|_|_|_|" << endl << endl;

    cout << "Tower B: more expensive and stronger" << endl;
    cout << "Damage area: " << endl;
    cout << "    _______________" << endl;
    cout << "#...|_|_|_|B|_|_|_|...#" << endl << endl;

    cout << "Tower C: is the best" << endl;
    cout << "Damage area: " << endl;
    cout << "           #" << endl;
    cout << "          ..." << endl;
    cout << "          |_|" << endl;
    cout << "          |_|" << endl;
    cout << "#...|_|_|_|C|_|_|_|...#" << endl;
    cout << "          |_|" << endl;
    cout << "          |_|" << endl;
    cout << "          ..." << endl;
    cout << "           #" << endl << endl;

    cout << "Also you'll defeat 3 types of enemies X, Y, Z with damage area like towers' A, B, C" << endl << endl;

    cout << "And that's all!" << endl;
    cout << "Good luck!!!" << endl << endl;
    cout << "***** TO CONTINUE PRESS ANY BUTTON *****" << endl << endl;

    char line[255];
    cin.getline(line, sizeof(line));
    return;
}
void    Game                    ( CMap m, int money,
                                  int win, int loss, int level )
{
        // 5 levels at all
        for ( int i = level; i < 5; i++ )
        {
            BeautifullyPrint_level( i );
            _Init( m, money, win, loss, i );
            _Attack( m, money, win, loss );
        }
        BeautifullyPrint_score( win, loss );
}

void    Play                    ( void ) {
        ClearHistory ();
        PrintWelcome ();
        string choice;
        cout << "To start new game press 42" << endl;
        cout << "To continue saved game press 2" << endl;

        while ( true )
        {
            cout << "Your choice: ";
            cin >> choice;
            cout << endl;
            if ( choice == "42" )
            {
                cout << "New game! Wow! So exciting!!" << endl << endl;
                CMap m ( 30, 15 );
                int money = 500;
                int win = 0, loss = 0, level = 0;
                Game ( m, money, win, loss, level );
                break;
            }
            else if ( choice == "2" )
            {
                cout << "Saved game! Wow! So exciting!!" << endl << endl;
                int money, win, loss, level;
                CMap m = LoadGame ( money, win, loss, level );
                Game ( m, money, win, loss, level );
                break;
            }
            else if ( cin . eof() )
                break;
            cout << "Oh no :( " << endl
                 << "Something wrong. Please choose 42 or 2" << endl << endl;
        }

}
