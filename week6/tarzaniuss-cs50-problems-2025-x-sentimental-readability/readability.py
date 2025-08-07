from cs50 import get_string
import re


def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    calculate_grade_level(letters, words, sentences)


def count_letters(text):

    num_letters = 0

    for i in text:
        if (i.isalpha()):
            num_letters += 1

    return num_letters


def count_words(text):

    num_words = len(text.split())

    return num_words


def count_sentences(text):

    return sum(1 for c in text if c in '.!?')


def calculate_grade_level(letters, words, sentences):

    L = (letters / float(words)) * 100
    S = (sentences / float(words)) * 100

    index = 0.0588 * L - 0.296 * S - 15.8

    if round(index) < 1:
        print("Before Grade 1")

    elif round(index) > 16:
        print("Grade 16+")
    else:
        rounded = int(round(index))
        print("Grade", rounded)


main()
