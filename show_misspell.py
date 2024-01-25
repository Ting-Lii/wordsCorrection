#Adapted from professor Rasika
#Name: Ting Li; Date: Dec2, 2023

# Reads in the content of the file called filename
# Returns a list of the contents
# (Each element of the list is one line in the file)
def read_file(filename: str) -> list:
    with open(filename, 'r') as file:
        return file.readlines()

# Takes the contents of the file (returned by read_file), returns a dictionary of word frequencies.
def count_word_frequencies(contents: list) -> dict:
    word_counts = {}
    for line in contents:
        for word in line.strip().lower().split():
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

# Prints the contents of a sorted dictionary.
def print_frequencies(word_frequencies):
    print('Word Frequencies:')
    for word in sorted(word_frequencies, key=word_frequencies.get, reverse=True):
        print(f'{word}: {word_frequencies[word]}')

def main():
    # Read the contents of the file
    contents = read_file('wrongly_spell.txt')
    
    # Count word frequencies
    word_frequencies = count_word_frequencies(contents)
    
    # Print the word frequencies
    print_frequencies(word_frequencies)

if __name__ == '__main__':
    main()
