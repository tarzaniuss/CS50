import csv
import sys


def main():

    if len(sys.argv) == 3:
        rows = []
        try:
            with open(f"{sys.argv[1]}") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
        except:
            print("INVALID PATH OF DATABASE")

        try:
            with open(f"{sys.argv[2]}", "r") as file:
                sequence = file.read()
        except:
            print("INVALID PATH OF SEQUENCE")

        STR_keys = list(rows[0].keys())[1:]

        dna_dict = {}

        for key in STR_keys:
            dna_dict[key] = longest_match(sequence, key)

        for person in rows:
            if all(int(person[key]) == int(value) for key, value in dna_dict.items()):
                print(person['name'])
                break
        else:
            print("No match")

    else:
        print("Please enter database path and sequence path in argv")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
