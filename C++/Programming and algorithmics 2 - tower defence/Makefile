CXX=g++
LD=g++
CXXFLAGS=-Wall -pedantic -Wno-long-long -o0 -ggdb -std=c++11
RM=rm -rf
OBJECTS=src/Game.o src/CMap.o src/CInit.o src/CAttack.o src/CHistory.o src/main.o
BIN=zabroyan
DOXY=Doxyfile
DOCDIR=doc
#------------------------------------------------------------

all: compile doc

compile: $(BIN)

doc: src/main.cpp src/Game.cpp src/CMap.cpp src/CInit.cpp src/CAttack.cpp src/CHistory.cpp\
		  src/Game.h   src/CMap.h   src/CInit.h   src/CAttack.h   src/CHistory.h\
		  src/CCoord.h src/CEnemy.h src/CEntrance.h src/CImmobile.h src/CMobile.h\
		  src/CObject.h src/CSpace.h src/CTower.h src/CWall.h
	$(RM) $(DOCDIR); mkdir $(DOCDIR);\
	cd src; \
	doxygen $(DOXY); \
	mv html/ latex/ ../$(DOCDIR)/;\
	cd ../$(DOCDIR);\
	mv html/* .;\
	$(RM) html/ latex/
	
clean:
	$(RM) $(BIN) $(OBJECTS) $(DOCDIR)

run: 
	./$(BIN)

#-------------------------------------------------------------

$(BIN): $(OBJECTS)
	$(LD) -o $@ $^
%o: %cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

src/Game.o: src/Game.cpp src/Game.h src/CInit.h src/CAttack.h

src/CMap.o: src/CMap.cpp src/CMap.h src/CWall.h src/CSpace.h src/CEntrance.h src/CTower.h src/CEnemy.h

src/CInit.o: src/CInit.cpp src/CInit.h src/CMap.h src/CHistory.h

src/CAttack.o: src/CAttack.cpp src/CAttack.h src/CMap.h

src/CHistory.o: src/CHistory.cpp src/CHistory.h src/CMap.h 

src/main.o: src/main.cpp src/Game.h


