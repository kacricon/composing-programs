#ifndef HASHMAP_H
#define HASHMAP_H

#include <stdlib.h>

typedef struct Entry entry_t;

struct Entry {
    char *key;
    float value;
    entry_t *next; // chaining in case of collision
};

typedef struct {
    entry_t **buckets; // array of pointers to buckets of entries
    size_t capacity;   // number of positions in buckets
    size_t size;       // number of entries
} hashmap_t;

hashmap_t *hashmap_create(size_t capacity);

void hashmap_set(hashmap_t *hashmap, char *key, size_t value);

float hashmap_get(hashmap_t *hashmap, char *key);

#endif

