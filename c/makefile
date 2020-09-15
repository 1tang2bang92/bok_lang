CC = clang
CXX = clang++

TARGET = main
OBJECTS = main.o output.o

$(TARGET): $(OBJECTS)
	$(CC) -o $@ $^

output.o: main.bk
	python main2.py

run: 
	make; ./$(TARGET)