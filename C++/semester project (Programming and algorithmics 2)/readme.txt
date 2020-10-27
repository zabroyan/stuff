--- EN below---

# Zadani semestralni prace z Progtestu

Naprogramujte jendoduchou grafickou tower defense hru

Váš engine:

    ze souboru nahraje definici věží (cena, velikost, útok, dosah, ...)
    ze souboru nahraje možné mapy a typy nepřátel (životy, rychlost, odolnost na určitý typ věže ,...)
    implementuje jednoduchou interakci věž vs. útočníci (útok, proběhnutí, ...), počitadlo skore, detekci vítěztví (po nezabití x útočníků)
    implementuje alespoň 2 strategie průchodu hracím polem
    umožňuje ukládat a načítat rozehrané hry

Engine může fungovat real-time hra, či tahová hra.

Jak může vypadat mapa?

" " označuje možnou lokaci věže a prázdné místa, A, B označuje dva druhy věží, # označuje zeď, @ a % jsou různé druhy útočníků.

 
#################################################
#                        #       @@  #          #
#         #              #    %B  @  ###        #
#         #              #    %#  @    #    B   #
<=%%%     #              A    %#       #@@@@@@@<=
#         #              A    %#       @@   B   #
#                        A    %#                #
#                 %%%       %%%#                #
#################################################                      

Cesta kudy se budu útočníci ubírat bude vždy nejkratší možná vzhledem ke zdím a věžím

Kde lze využít polymorfismus? (doporučené)

    Parametry věží: znak, barva, dosah, zranění, ...
    Efekty útoku věží: zranění, zpomalení, ...
    Políčka mapy: volno, věž, útočník ...
    Strategie hledání cesty: předdefinovaná cesta, nejkratší (BFS, případně náhodná odchylka), A* prohledávání, vyhýbání se věžím
    Uživatelské rozhraní: konzole, ncurses, SDL, OpenGL (různé varianty), ...

Ukázky:

    https://en.wikipedia.org/wiki/Tower_defense
    https://en.wikipedia.org/wiki/GemCraft
    http://plantsvszombies.wikia.com/wiki/Main_Page


---EN---

# Assigned semester work

Program a simple graphic tower defense game

Your engine:

    uploads the definition of towers from the file (price, size, attack, range, ...)
    loads possible maps and types of enemies from the file (lives, speed, resistance to a certain type of tower, ...)
    implements a simple tower vs. attackers (attack, racing, ...), score counter, victory detection (after not killing x attackers)
    implements at least 2 strategies for passing through the playing field
    allows you to save and load played games

The engine can work real-time game or turn-based game.

What can a map look like?

" " indicates possible tower location and empty spaces, A, B indicates two types of towers, # indicates wall, @ and % are different types of attackers.

#################################################
#                        #       @@  #          #
#         #              #    %B  @  ###        #
#         #              #    %#  @    #    B   #
<=%%%     #              A    %#       #@@@@@@@<=
#         #              A    %#       @@   B   #
#                        A    %#                #
#                 %%%       %%%#                #
################################################# 

The path that the attackers will take will always be the shortest possible due to the walls and towers

Where can polymorphism be used? (recommended)

    Tower parameters: character, color, range, damage, ...
    Effects of tower attack: damage, slowdown, ...
    Map fields: free, tower, forward ...
    Path finding strategy: predefined path, shortest (BFS, or random deviation), A * search, avoiding towers
    User interface: console, ncurses, SDL, OpenGL (various variants), ...

Examples:

    https://en.wikipedia.org/wiki/Tower_defense
    https://en.wikipedia.org/wiki/GemCraft
    http://plantsvszombies.wikia.com/wiki/Main_Page