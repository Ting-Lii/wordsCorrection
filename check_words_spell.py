#Name: Ting Li; Date: Dec26, 2024.

'''
This is a words correction program by using Levenshtein algorithm and Trie structure for efficient dictionary lookup.
It collects users' misspelled words into 'wrongly_spell.txt', and users can access
their misspelled words by frequency in 'show_misspell.py'.
'''
import Levenshtein

class TrieNode:
    """Node structure for the Trie."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """Trie (prefix tree) for efficient word lookup."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # Validate word to contain only alphabetic characters
        if not word.isalpha():
            raise ValueError(f"Invalid word '{word}'. Only alphabetic characters are allowed.")

        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word


# Clean the dictionary file
def clean_dictionary(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        words = [line.strip() for line in file if line.strip().isalpha()]
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(words))

# Clean both dictionaries
clean_dictionary("popular_dictionary_USA.txt")
clean_dictionary("wholesome_dictionary_USA.txt")

# Function to build a Trie from the dictionary file
def build_trie(dictionary_words):
    trie = Trie()
    for word in dictionary_words:
        trie.insert(word)
    return trie


# Function to find the closest match for a word not found in the Trie
def find_closest_match(word, dictionary):
    return min(dictionary, key=lambda x: Levenshtein.distance(word, x))


# Function to choose the dictionary (0 or 1)
def dictionary_choose():
    while True:
        try:
            decision_dic_value = int(input('Please choose the dictionary that you prefer. Enter 0 for the common version, '
                                           '1 for the comprehensive version: '))
            if decision_dic_value not in [0, 1]:
                raise ValueError("Not a valid input. Please enter 0 or 1!")
            return decision_dic_value
        except ValueError as e:
            print(f"Error: {e}")


# Function to get user input for words or sentences
def word_enter():
    while True:
        user_input = input("Please type in a word or a sentence ('q' to exit the program): ").lower()
        if all(char.isalpha() or char.isspace() for char in user_input):
            return user_input
        else:
            print("Invalid input! Please enter a valid word containing only alphabetic characters. Try again.")


# Function to read the dictionary file and return a list of words
def read_dictionary(dic_choose: int):
    file_path = "popular_dictionary_USA.txt" if dic_choose == 0 else "wholesome_dictionary_USA.txt"
    try:
        with open(file_path, "r") as file:
            dictionary = [line.strip() for line in file]
            return dictionary
    except FileNotFoundError:
        print(f"Error: Dictionary file '{file_path}' not found.")
        return []


# Function to correct spelling using Trie and Levenshtein distance
def correct_spelling(user_input: str, trie: Trie, dictionary: list):
    input_words = user_input.split()
    corrected_words = []
    wrongly_spelled_words = []

    for word in input_words:
        if trie.search(word):
            corrected_words.append(word)
        else:
            closest_word = find_closest_match(word, dictionary)
            corrected_words.append(closest_word)
            wrongly_spelled_words.append(word)

    corrected_string = ' '.join(corrected_words)
    return corrected_string != user_input, corrected_string, wrongly_spelled_words


# Main function
def main():
    dic_choose = dictionary_choose()
    dictionary = read_dictionary(dic_choose)

    # Build a Trie for efficient word lookup
    trie = build_trie(dictionary)

    while True:
        user_input = word_enter()

        if user_input == "q":
            print("Successfully exited the program.")
            break

        corrected_result = correct_spelling(user_input, trie, dictionary)

        # Store misspelled words in a text file
        if corrected_result[0]:  # If corrections were made
            with open("wrongly_spell.txt", "a") as file:
                file.write("\n" + "\n".join(corrected_result[2]))
            print(f"Corrected Result: {corrected_result[1]}")
        else:  # No corrections needed
            print("No corrections needed:", user_input)


if __name__ == "__main__":
    main()
