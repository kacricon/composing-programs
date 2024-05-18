#ifndef LIST_H
#define LIST_H
#include <stdlib.h>

typedef struct node node;

struct node {
    int value;
    node *next;
};

typedef struct {
    node *head;
    size_t length;
} list;

list *init_list(int *value, size_t length);
void append_list(list *l, int value);
list *concat_lists(list *l1, list *l2);
node *pop_list(list *l);
int get_value(list *l, size_t i);

#endif

