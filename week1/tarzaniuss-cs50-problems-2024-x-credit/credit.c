#include <cs50.h>
#include <stdio.h>

int first_sum(long number)
{
    int sum = 0;
    bool is_even_place = false;

    while (number > 0)
    {
        int digit = number % 10;

        if (is_even_place)
        {
            int product = digit * 2;
            sum += (product % 10) + (product / 10);
        }

        number /= 10;
        is_even_place = !is_even_place;
    }

    return sum;
}

int second_sum(long number)
{
    int sum = 0;
    bool is_even_place = false;

    while (number > 0)
    {
        int digit = number % 10;

        if (!is_even_place)
        {
            sum += digit;
        }

        number /= 10;
        is_even_place = !is_even_place;
    }

    return sum;
}

void check_card_type(long number)
{
    int length = 0;
    long start_digits = number;

    while (start_digits >= 100)
    {
        start_digits /= 10;
        length++;
    }
    length += 2;

    if (length == 15 && (start_digits == 34 || start_digits == 37))
    {
        printf("AMEX\n");
    }

    else if (length == 16 && (start_digits >= 51 && start_digits <= 55))
    {
        printf("MASTERCARD\n");
    }

    else if ((length == 13 || length == 16) && (start_digits / 10 == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

bool validate_card(long number)
{
    int sum = first_sum(number) + second_sum(number);

    return (sum % 10) == 0;
}

int main(void)
{

    long number = get_long("Number: ");

    if (validate_card(number))
    {
        check_card_type(number);
    }
    else
    {
        printf("INVALID\n");
    }
}
