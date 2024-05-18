#include "rational.h"
#include <assert.h>
#include <errno.h>
#include <stdio.h>

void test_constructor_selectors() {
    // test invalid
    rational i = init_rational(1, 0);
    assert(numer(i) == 0);
    assert(denom(i) == 0);
    assert(errno == EINVAL);

    // test valid + invert denom sign
    rational d = init_rational(3, -2);
    assert(numer(d) == -3);
    assert(denom(d) == 2);

    // test valid + reduce
    rational x = init_rational(15, 6);
    assert(numer(x) == 5);
    assert(denom(x) == 2);

    printf("All constructor and selector tests passed.\n");
}

void test_operators() {
    rational half = init_rational(1, 2);
    rational third = init_rational(1, 3);

    rational summed = init_rational(5, 6);
    rational summed_f = sum_rationals(half, third);
    assert(numer(summed_f) == 5);
    assert(denom(summed_f) == 6);
    assert(rationals_are_equal(summed, summed_f));

    rational multiplied = init_rational(1, 6);
    rational multiplied_f = mul_rationals(half, third);
    assert(numer(multiplied_f) == 1);
    assert(denom(multiplied_f) == 6);
    assert(rationals_are_equal(multiplied, multiplied_f));

    printf("All operator tests passed.\n");
}

void test_print_rational() {
    printf("Manual test for print_rational function\n");

    rational x = init_rational(3, 4);
    printf("A rational with numerator %i and denominator %i is printed as: ", numer(x), denom(x));
    print_rational(x);
}

int main() {
    test_constructor_selectors();
    test_operators();
    test_print_rational();

    return 0;
}

