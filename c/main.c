#include <stdio.h>
#include <stdint.h>

int64_t foo();

int main() {
    printf("%ld", foo(2));
    return 0;
}