CC = clang
CXX = clang++

TARGET = target/main
OBJECTS = target/output.o target/print.o target/input.o

$(TARGET): $(OBJECTS)
	$(CC) -o $@ $^

target/output.o: main.bk
	python shell.py

target/print.o: 
	python shell.py

target/input.o: 
	python shell.py

run: 
	make; $(TARGET)