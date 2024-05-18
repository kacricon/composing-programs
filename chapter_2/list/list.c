#include "list.h"
#include <errno.h>

list *init_list(int *values, size_t length) {
    // initialize empty list
    list *new_list = malloc(sizeof(list));
    if (!new_list)
        return NULL;
    new_list->head = NULL;
    new_list->length = 0;

    if (!values | (length == 0))
        return new_list;

    // create list head
    new_list->head = malloc(sizeof(node));
    if (!new_list->head)
        return NULL;
    new_list->head->value = values[0];
    new_list->head->next = NULL;
    node *prev = new_list->head;

    // append rest of values
    for (size_t i = 1; i < length; i++) {
        node *new_node = malloc(sizeof(node));
        if (!new_node)
            return NULL;
        new_node->value = values[i];
        prev->next = new_node;
        prev = new_node;
    }
    new_list->length = length;

    return new_list;
}

void append_list(list *l, int value) {
    // create new node
    node *new_node = malloc(sizeof(node));
    if (!new_node)
        return;
    new_node->value = value;
    new_node->next = NULL;

    // append new node to tail
    if (!l->head)
        l->head = new_node;
    else {
        node *curr = l->head;
        while (curr->next) {
            curr = curr->next;
        }
        curr->next = new_node;
    }
    l->length++;
}

list *concat_lists(list *l1, list *l2) {
    // create new empty list
    list *new_list = init_list(NULL, 0);
    if (!new_list)
        return NULL;
    node *tail;

    // append l1 to new list
    if (l1->head) {
        new_list->head = malloc(sizeof(node));
        if (!new_list->head)
            return NULL;
        new_list->head->value = l1->head->value;
        new_list->head->next = NULL;
        tail = new_list->head;
        
        node *curr = l1->head;
        while (curr->next) {
            curr = curr->next;
            node *new_node = malloc(sizeof(node));
            if (!new_node)
                return NULL;
            new_node->value = curr->value;
            new_node->next = NULL;
            tail->next = new_node;
            tail = tail->next;
        }
        new_list->length += l1->length;
    }

    // append l2 to new list
    if (l2->head) {
        if (!new_list->head) {
            new_list->head = malloc(sizeof(node));
            if (!new_list->head)
                return NULL;
            new_list->head->value = l2->head->value;
            new_list->head->next = NULL;
            tail = new_list->head;
        } else {
            node *new_node = malloc(sizeof(node));
            if (!new_node)
                return NULL;
            new_node->value = l2->head->value;
            new_node->next = NULL;
            tail->next = new_node;
            tail = tail->next;
        }

        node *curr = l2->head;
        while (curr->next) {
            curr = curr->next;
            node *new_node = malloc(sizeof(node));
            if (!new_node)
                return NULL;
            new_node->value = curr->value;
            new_node->next = NULL;
            tail->next = new_node;
            tail = tail->next;
        }
        new_list->length += l2->length;
    }

    return new_list;
}

node *pop_list(list *l) {
    if (!l | !l->head) { // can't pop a NULL or empty list
        errno = EINVAL;
        return NULL;
    }
    node *popped;

    if (!l->head->next) {
        popped = l->head;
        l->head = NULL;
    } else {
        node *prev = l->head;
        node *curr = prev->next;
        while (curr->next) {
            prev = curr;
            curr = curr->next;
        }
        prev->next = NULL; 
        popped = curr;
    }
    l->length--;

    return popped;
}

int get_value(list *l, size_t i) {
    if (i >= l->length) { // out of bounds
        errno = EINVAL;
        return -1;
    }

    node *curr = l->head;
    for (size_t j = 1; j <= i; j++)
        curr = curr->next;
    return curr->value;
}

