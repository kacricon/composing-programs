#include "list.h"
#include <assert.h>
#include <errno.h>
#include <stdio.h>

void check_values(list *l, int *values) {
    node *curr = l->head;
    size_t i = 0;
    while (curr) {
       assert(curr->value == values[i]); 
       curr = curr->next;
       i++;
    }
}

void test_init_list() {
    int values[] = { 0, 1, 2, 3 };
    size_t length = 4;
    list *l = init_list(values, length);

    check_values(l, values);
    printf("All init_list tests passed!\n");
}

void test_append_list() {
    int values[] = { 0, 1, 2, 3 };
    size_t length = 4;
    list *l = init_list(NULL, 0); // empty list

    for (size_t i = 0; i < length; i++) {
        append_list(l, values[i]);
    }

    check_values(l, values);
    printf("All append_list tests passed!\n");
}

void test_concat_lists() {
    // concatenate two empty lists
    list *empty1 = init_list(NULL, 0);
    list *empty2 = init_list(NULL, 0);
    list *empty3 = concat_lists(empty1, empty2);
    assert(empty3->length == 0);
    assert(!empty3->head);

    // concatenate an empty list with a non-empty list
    int values1[] = { 0, 1, 2, 3 };
    list *l1 = init_list(values1, 4);
    list *l2 = concat_lists(empty1, l1);
    assert(l2->length == 4);
    check_values(l2, values1);
    
    l2 = concat_lists(l1, empty1);
    assert(l2->length == 4);
    check_values(l2, values1);

    // concatenate two non-empty lists
    int values2[] = { 4, 5, 6 };
    int values3[] = { 0, 1, 2, 3, 4, 5, 6 };
    l2 = init_list(values2, 3);
    list *l3 = concat_lists(l1, l2);
    assert(l3->length == 7);
    check_values(l3, values3);
    
    printf("All concat_lists tests passed!\n");
}

void test_pop_list() {
    // pop empty list
    list *empty = init_list(NULL, 0);
    assert(!pop_list(empty));
    assert(errno == EINVAL);

    // pop non-empty list until empty
    int values[] = { 0, 3, 5 };
    list *l = init_list(values, 3);

    node *popped = pop_list(l);
    assert(popped->value == 5);
    assert(l->length == 2);
    popped = pop_list(l);
    assert(popped->value == 3);
    assert(l->length == 1);
    popped = pop_list(l);
    assert(popped->value == 0);
    assert(l->length == 0);
    assert(!l->head);

    printf("All pop_list tests passed!\n");
}

void test_get_value() {
    // get empty list
    list *empty = init_list(NULL, 0);
    assert(get_value(empty, 2) == -1);
    assert(errno == EINVAL);
    
    // get valid index positions
    int values[] = { 1, 2, 3, 4, 5, 6, 7 };
    list *l = init_list(values, 7);
    
    for (size_t i = 0; i < 7; i++) {
        assert(get_value(l, i) == i + 1);
    }

    // get out of bounds
    assert(get_value(l, 10) == -1);
    assert(errno == EINVAL);

    printf("All get_value tests passed!\n");
}

int main() {
    test_init_list();
    test_append_list();
    test_concat_lists();
    test_pop_list();
    test_get_value();
    return 0;
}

