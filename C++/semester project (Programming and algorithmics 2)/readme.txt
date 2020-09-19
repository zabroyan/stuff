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
