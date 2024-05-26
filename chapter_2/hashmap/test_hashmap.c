#include "hashmap.h"
#include <assert.h>
#include <errno.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define ERR 0.0001

bool is_close(float x, float y) {
    return fabs(x - y) <= ERR;
}

void test_create() {
    // hashmap must have a positive capacity
    hashmap_t *new_hashmap = hashmap_create(0);
    assert(errno == EINVAL);
    assert(new_hashmap == NULL);
    
    // create a hashmap successfully
    new_hashmap = hashmap_create(2);
    assert(new_hashmap != NULL);
    assert(new_hashmap->buckets[0] == NULL);
    assert(new_hashmap->buckets[1] == NULL);
    assert(new_hashmap->capacity == 2);
    assert(new_hashmap->size == 0);

    printf("All `hashmap_create` tests passed!\n");
}

void test_set() {
    // simple set
    char *key = "test";
    float value = 5.0;
    hashmap_t *new_hashmap = hashmap_create(1); // capacity 1 ensures collisions
    hashmap_set(new_hashmap, key, value);
    assert(new_hashmap->buckets[0] != NULL);
    assert(strcmp(new_hashmap->buckets[0]->key, key) == 0);
    assert(is_close(new_hashmap->buckets[0]->value, value));
    assert(new_hashmap->size == 1);

    // set with collision (insert into chain)
    char *key2 = "test2";
    float value2 = 12.0;
    hashmap_set(new_hashmap, key2, value2);
    assert(new_hashmap->buckets[0]->next != NULL);
    assert(strcmp(new_hashmap->buckets[0]->next->key, key2) == 0);
    assert(is_close(new_hashmap->buckets[0]->next->value, value2));
    assert(new_hashmap->size == 2);

    printf("All `hashmap_set` tests passed!\n");
}

void test_get() {
    // simple get
    char *key = "test";
    float value = 5.0;
    hashmap_t *new_hashmap = hashmap_create(1);
    hashmap_set(new_hashmap, key, value);
    assert(is_close(hashmap_get(new_hashmap, key), value));
     
    // get with collision (get from chain)
    char *key2 = "test2";
    float value2 = 12.0;
    hashmap_set(new_hashmap, key2, value2);
    assert(is_close(hashmap_get(new_hashmap, key2), value2));

    printf("All `hashmap_get` tests passed!\n");
}

int main() {
    test_create();
    test_set();
    test_get();
    return 0;
}
