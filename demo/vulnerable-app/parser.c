#include <stdio.h>
#include <string.h>

void handle(char *input) {
    char buf[64];
    strcpy(buf, input);
    printf(input);
    sprintf(buf, "%s", input);
}
