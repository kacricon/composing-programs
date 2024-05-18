#include "rational.h"
#include <stdlib.h>
#include <errno.h>
#include <stdio.h>

rational init_rational(int numerator, int denominator) {
    rational x;
    if (denominator == 0) { // invalid rational
        errno = EINVAL;
        x.numerator = 0;
        x.denominator = 0;
        return x;
    }
    if (denominator < 0) {
        numerator = -numerator;
        denominator = -denominator;
    }
    x.numerator = numerator;
    x.denominator = denominator;
    return reduce_rational(x);
}

rational reduce_rational(rational x) {
    // finds GCD
    int a, b, tmp;
    a = abs(x.numerator);
    b = abs(x.denominator);
    while (b) {
        tmp = a % b; 
        a = b;
        b = tmp;
    }

    // reduce rational
    x.numerator /= a;
    x.denominator /= a;
    return x;
}

int numer(rational x) {
    return x.numerator;
}

int denom(rational x) {
    return x.denominator;
}

rational sum_rationals(rational x, rational y) {
    return init_rational(numer(x) * denom(y) + numer(y) * denom(x), denom(x) * denom(y));
}

rational mul_rationals(rational x, rational y) {
    return init_rational(numer(x) * numer(y), denom(x) * denom(y));
}

void print_rational(rational x) {
    printf("%i / %i\n", numer(x), denom(x));
}

int rationals_are_equal(rational x, rational y) {
    return numer(x) * denom(y) == numer(y) * denom(x);
}

