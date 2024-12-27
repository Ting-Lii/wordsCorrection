import tkinter as tk
from tkinter import messagebox
from collections import Counter
from check_words_spell import Trie, build_trie, read_dictionary, correct_spelling


class WordsCorrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Words Correction Program")
        self.root.geometry("700x700")  # Increased size to accommodate larger misspelled words box
        self.root.configure(bg="#f2f2f2")  # Background color

        # Build the dictionary and Trie
        self.dictionary = read_dictionary(0)  # Default to common dictionary
        self.trie = build_trie(self.dictionary)

        # Create UI Components
        self.create_widgets()

    def create_widgets(self):
        # Dictionary Selection
        tk.Label(self.root, text="Choose Dictionary:", font=("Arial", 12), bg="#f2f2f2").pack(pady=10)
        self.dictionary_var = tk.IntVar(value=0)
        tk.Radiobutton(self.root, text="Common", variable=self.dictionary_var, value=0, command=self.load_dictionary, bg="#f2f2f2").pack()
        tk.Radiobutton(self.root, text="Comprehensive", variable=self.dictionary_var, value=1, command=self.load_dictionary, bg="#f2f2f2").pack()

        # Input Box
        tk.Label(self.root, text="Enter a Word or Sentence:", font=("Arial", 12), bg="#f2f2f2").pack(pady=10)
        self.input_text = tk.Text(self.root, height=5, width=60)
        self.input_text.pack()
        self.input_text.bind("<Return>", self.correct_spelling_enter)  # Bind Enter key
        self.input_text.bind("<Key>", self.clear_misspelled_box)  # Clear Misspelled Words Box on typing

        # Correct Button
        self.correct_button = tk.Button(self.root, text='Correct (or press "Enter")', command=self.correct_spelling, font=("Arial", 12), bg="#87CEEB")
        self.correct_button.pack(pady=10)

        # Corrected Text Output Box
        tk.Label(self.root, text="Corrected Text:", font=("Arial", 12), bg="#f2f2f2").pack(pady=10)
        self.output_text = tk.Text(self.root, height=5, width=60, state="disabled")
        self.output_text.pack()

        # Show Misspelled Words Button
        self.misspelled_button = tk.Button(self.root, text="Show me my misspelled words!", command=self.show_misspelled_words, font=("Arial", 12), bg="#FFB6C1")
        self.misspelled_button.pack(pady=10)

        # Misspelled Words Output Box (Hidden by default)
        self.misspelled_label = tk.Label(self.root, text="Misspelled Words (Sort by Frequency):", font=("Arial", 12), bg="#f2f2f2")
        self.misspelled_output = tk.Text(self.root, height=15, width=60, state="disabled")  # Enlarged box

    def load_dictionary(self):
        """Load the dictionary based on user selection."""
        dic_choice = self.dictionary_var.get()
        self.dictionary = read_dictionary(dic_choice)
        self.trie = build_trie(self.dictionary)
        messagebox.showinfo("Dictionary Loaded", "Dictionary has been successfully updated.")

    def clear_misspelled_box(self, event):
        """Clear the Misspelled Words Box and hide it when the user starts typing."""
        self.misspelled_output.pack_forget()
        self.misspelled_label.pack_forget()

    def correct_spelling_enter(self, event):
        """Correct spelling when 'Enter' key is pressed."""
        self.correct_spelling()

    def correct_spelling(self):
        """Perform spelling correction and store misspelled words."""
        user_input = self.input_text.get("1.0", tk.END).strip().lower()

        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a word or sentence.")
            return

        # Correct spelling
        corrected_result = correct_spelling(user_input, self.trie, self.dictionary)

        # Display corrected text
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, corrected_result[1])
        self.output_text.config(state="disabled")

        # Store misspelled words
        if corrected_result[0]:  # If corrections were made
            with open("wrongly_spell.txt", "a") as file:
                file.write("\n" + "\n".join(corrected_result[2]))
            messagebox.showinfo("Correction Made", "Misspelled words have been stored in 'wrongly_spell.txt'.")
        else:
            messagebox.showinfo("No Corrections", "All words were correct.")

    def show_misspelled_words(self):
        """Display the misspelled words with frequency in the app."""
        try:
            with open("wrongly_spell.txt", "r") as file:
                words = file.read().strip().splitlines()

            if words:
                word_counts = Counter(words)
                sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
                result = "\n".join([f"{word}: {count}" for word, count in sorted_words])
            else:
                result = "No misspelled words found."

            # Show Misspelled Words Box
            self.misspelled_label.pack(pady=10)
            self.misspelled_output.pack()
            self.misspelled_output.config(state="normal")
            self.misspelled_output.delete("1.0", tk.END)
            self.misspelled_output.insert(tk.END, result)
            self.misspelled_output.config(state="disabled")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file 'wrongly_spell.txt' does not exist.")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WordsCorrectionApp(root)
    root.mainloop()
