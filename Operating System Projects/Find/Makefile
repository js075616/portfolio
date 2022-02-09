CFLAGS = -g -Wall -Werror -O3
CC = gcc

find: find.o
	g++ ${CFLAGS} find.o -o find

find.o: find.cpp
	g++ ${CFLAGS} -c find.cpp

clean:
	/bin/rm -f *.o find 