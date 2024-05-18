CC = gcc
CFLAGS = -Wall -g

# Targets
TARGET = test_list
SOURCES = list.c test_list.c
HEADERS = list.h

# Default target
all: $(TARGET)

# Build the test executable
$(TARGET): $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)

# Clean up build files
clean:
	rm -f $(TARGET)
	rm -rf $(TARGET).dSYM
	rm -f *.o
