## Bakalářská práce

# Řešení kolizí mezi geometrickými roboty ve spojitém prostoru

## Yana Zabrodskaya

## V rámci práce byl navržen algoritmus AvoidancePath, který hledá nejkratší cestu pro dva roboty libovolného geometrického tvaru a řeší konflikty, když během jejich cesty dochází ke srážkám.

Spouštění programu:

cat mapa agent | ./algoritmus

- Mapa se nachází ve složce inputs/map$i/map_$i, kde $i je číslo 1-4
- Agent se nachází ve složce inputs/map$i/agents/$agent, kde $i je již zvolené číslo mapy a $agent je soubor ve tvaru 'circles/rectangles/squares/triangles_$n', $n je číslo agenta tohoto tvaru pro tuto mapu

Příklad:

cat inputs/map1/map_1 inputs/map1/agents/rectangles_1 | ./AvoidancePath