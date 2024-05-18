CC = gcc
CFLAGS = -Wall -g

# Targets
TARGET = test_rational
SOURCES = rational.c test_rational.c
HEADERS = rational.h

# Default target
all: $(TARGET)

# Build the test executable
$(TARGET): $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)

# Clean up build files
clean:
	rm -f $(TARGET)
	rm -fr $(TARGET).dSYM
	rm -f *.o
