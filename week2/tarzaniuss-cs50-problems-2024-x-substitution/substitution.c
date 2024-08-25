#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int keyValidation(int argc, string argv[]);
string encryptMessage(string message, string key);

int main(int argc, string argv[])
{
    if (keyValidation(argc, argv))
    {
        return 1;
    }

    string key = argv[1];

    string plainText = get_string("plaintext:  ");

    string ciphertext = encryptMessage(plainText, key);

    printf("ciphertext: %s\n", ciphertext);
}

string encryptMessage(string message, string key)
{
    string encryptedMessage = message;

    for (int i = 0, length = strlen(message); i < length; i++)
    {

        int numOfLetter;

        if (isupper(message[i]))
        {
            numOfLetter = message[i] - 'A';
            encryptedMessage[i] = toupper(key[numOfLetter]);
            continue;
        }

        if (islower(message[i]))
        {
            numOfLetter = message[i] - 'a';
            encryptedMessage[i] = tolower(key[numOfLetter]);
            continue;
        }

        encryptedMessage[i] = message[i];
    }

    return encryptedMessage;
}

int keyValidation(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage ./substitution key\n");
        return 1;
    }

    for (int i = 0, length = strlen(argv[1]); i < length; i++)
    {
        if (length != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alpabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < length; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    return 0;
}
