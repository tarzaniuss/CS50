#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Height:");
    }
    while (height > 8 || height < 1);

    for (int i = 0; i < height; i++)
    {
        for (int o = 1; o < height - i; o++)
        {
            printf(" ");
        }
        for (int g = 0; g < i + 1; g++)
        {
            printf("#");
        }
        printf("  ");
        for (int g = 0; g < i + 1; g++)
        {
            printf("#");
        }
        printf("\n");
    }
}
