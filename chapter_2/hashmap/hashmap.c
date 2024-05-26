#include "hashmap.h"
#include "djb2.h"
#include <errno.h>
#include <string.h>

hashmap_t *hashmap_create(size_t capacity) {
    if (capacity == 0) { // capacity must be >= 1
        errno = EINVAL;
        return NULL;
    }

    hashmap_t *new_hashmap = malloc(sizeof(hashmap_t));
    if (!new_hashmap) {
        return NULL;
    }

    new_hashmap->buckets = malloc(capacity * sizeof(entry_t *));
    if (!new_hashmap->buckets) {
        free(new_hashmap);
        return NULL;
    }

    for (size_t i = 0; i < capacity; i++) {
        new_hashmap->buckets[i] = NULL;
    }

    new_hashmap->capacity = capacity;
    new_hashmap->size = 0;

    return new_hashmap;
}

void hashmap_set(hashmap_t *hashmap, char *key, size_t value) {
    unsigned long index = djb2(key) % hashmap->capacity;

    // check if index is already filled with an entry
    if (hashmap->buckets[index]) {
        // check if first in chain is the same key as argument
        entry_t *e = hashmap->buckets[index];
        if (strcmp(e->key, key) == 0) {
            e->value = value; // update value
            return;
        }

        // if first does not match key, continue search through the chain
        while (e->next) {
            e = e->next;
            if (strcmp(e->key, key) == 0) {
                e->value = value; // update value
                return;
            }
        }

        // if no match is found, create entry and add to chain
        entry_t *new_entry = malloc(sizeof(entry_t));
        if (!new_entry) {
            return;
        }
        size_t key_len = strlen(key);
        new_entry->key = malloc(key_len * sizeof(char));
        strcpy(new_entry->key, key);
        new_entry->value = value;
        new_entry->next = NULL;
        e->next = new_entry;
        hashmap->size++;
        return;
    }
     
    // if index is not filled, create new entry and insert in index
    entry_t *new_entry = malloc(sizeof(entry_t));
    if (!new_entry) {
        return;
    }
    size_t key_len = strlen(key);
    new_entry->key = malloc(key_len * sizeof(char));
    strcpy(new_entry->key, key);
    new_entry->value = value;
    new_entry->next = NULL;
    hashmap->buckets[index] = new_entry;
    hashmap->size++;
}

float hashmap_get(hashmap_t *hashmap, char *key) {
    unsigned long index = djb2(key) % hashmap->capacity;
    
    // check if index has an entry
    if (!hashmap->buckets[index]) {
        errno = ENOENT;
        return -1;
    }
    
    // check if key matches argument
    entry_t *e = hashmap->buckets[index];
    if (strcmp(e->key, key) == 0) {
        return e->value; 
    }

    // if does not match, search the chain
    while (e->next) {
        e = e->next;
        if (strcmp(e->key, key) == 0) {
            return e->value;
        }
    }

    // if key is not found, return error
    errno = ENOENT;
    return -1;
}

