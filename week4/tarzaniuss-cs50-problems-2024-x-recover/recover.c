#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the memory card file
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];
    FILE *img = NULL;
    int file_count = 0;
    char filename[8];

    // Read the memory card until the end
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check if we found a JPEG's beginning
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If an image file is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new file for the JPEG
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        // If a JPEG file is open, write to it
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;
}
