#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
void calculate_grade_level(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    calculate_grade_level(letters, words, sentences);
}

int count_letters(string text)
{
    int num_letters = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            num_letters++;
        }
    }
    return num_letters;
}

int count_words(string text)
{
    int num_spaces = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == 32)
        {
            num_spaces++;
        }
    }
    return num_spaces + 1;
}

int count_sentences(string text)
{
    int num_sentences = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            num_sentences++;
        }
    }
    return num_sentences;
}

void calculate_grade_level(int letters, int words, int sentences)
{
    float L = (letters / (float) words) * 100;
    float S = (sentences / (float) words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (round(index) < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (round(index) > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        int rounded = (int) round(index);
        printf("Grade %d\n", rounded);
    }
}
