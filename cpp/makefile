CC = clang
CXX = clang++
# CFLAGS = 
# CPPFLAGS = 

TARGET = main
OBJECTS = main.o

$(TARGET): $(OBJECTS)
	$(CXX) -o $@ $^

run: 
	make && echo "" && ./$(TARGET)