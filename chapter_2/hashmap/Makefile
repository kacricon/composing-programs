CC = gcc
CFLAGS = -Wall -g

# Targets
TARGET = test_hashmap
SOURCES = djb2.c hashmap.c test_hashmap.c
HEADERS = djb2.h hashmap.h

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
