#Name: Ting Li; Date: Dec2, 2023.

'''
This is a words correction program by using Levenshtein algorithm, and has two dictionary to choose.
It could collect users' misspelled words into 'wrongly_spell.txt', and user could access
their misspelled words by frequency in 'show_misspell.py'.
'''
import Levenshtein

#This function return the Levenshtein distance between 2 string.
def levenshtein_distance(w1, w2):
    return Levenshtein.distance(w1, w2)

#This function ask user to choose one of the two dictionaries, and ensure
#a valid input (0 or 1).
def dictionary_choose():
    while True:
        try:
            decision_dic_value = int(input('Please choose the dictionary that you prefer. Enter 0 for the common version, '
                                           '1 for the comprehensive version: '))
            if decision_dic_value != 1 and decision_dic_value != 0:
                raise ValueError("Not a valid input. Please enter 0 or 1!")
            return decision_dic_value
        except ValueError as e:
            print(f"Error:{e}")

#This function ask user to enter a word or sentence, and ensure input only alphabetic characters. 
def word_enter():
    while True:
        user_input = input("Please type in a word or a sentence ('q' to exit the program): ").lower()
        # Check if the input contains only alphabetic characters or spaces
        if all(char.isalpha() or char.isspace() for char in user_input):
            return user_input
        else:
            print("Invalid input! Please enter a valid word containing only alphabetic characters. Try again.")


#This function open and read different dictionary as user chose.
def read_dictionary(dic_choose: int):
    file_path = "popularWords.txt" if dic_choose == 0 else "dictionaryUSA.txt"
    try:
        with open(file_path, "r") as file:
            dictionary = [line.strip() for line in file]
            return dictionary
    except FileNotFoundError:
        print(f"Error: Dictionary file '{file_path}' not found.")
        return []

#This function return a tuple includes if any corrections were made(bool), the corrected string(str), and the wrongly spelled words(str). 
def correct_spelling(user_input:str, dictionary:list):
    input_words = user_input.split()

    corrected_words = []
    wrongly_spelled_words = []

    for word in input_words:
        if word in dictionary:
            corrected_words.append(word)
        else:
            closest_word = min(dictionary, key=lambda x: levenshtein_distance(word, x))
            corrected_words.append(closest_word)
            wrongly_spelled_words.append(word)

    corrected_string = ' '.join(corrected_words)
    # Return a tuple indicating if any corrections were made, the corrected string, and the wrongly spelled words
    return corrected_string != user_input, corrected_string, wrongly_spelled_words


# Main function. First ask user to choose dictionary, then kepp ask user to enter word, 
# untile user type in "q" indicating exit the program. Besides, if correct_spelling() first tuple
#is True, append the wrongly spelled words into wrongly_spell.txt, and show user the corrected words.
def main():
    dic_choose = dictionary_choose()
    
    while True:
        user_input = word_enter()

        if user_input == "q":
            print("Successfully exit the program.")
            break

        dictionary = read_dictionary(dic_choose)

        corrected_result = correct_spelling(user_input, dictionary)

        # Storing the wrongly spelled words into a text file
        if corrected_result[0]:  # Check if any corrections were made
            with open("wrongly_spell.txt", "a") as file:
                file.write("\n" + "\n".join(corrected_result[2]))
            print(f"Corrected Result: {corrected_result[1]}")
        else: #if user type into correct words, just print user input without comment.
            print(user_input)


if __name__ == "__main__":
    main()
