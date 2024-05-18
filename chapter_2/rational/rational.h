#ifndef RATIONAL_H
#define RATIONAL_H

typedef struct {
    int numerator;
    int denominator;
} rational;

rational init_rational(int numerator, int denominator);
int numer(rational x);
int denom(rational x);
rational reduce_rational(rational x);
rational sum_rationals(rational x, rational y);
rational mul_rationals(rational x, rational y);
void print_rational(rational x);
int rationals_are_equal(rational x, rational y);

#endif

