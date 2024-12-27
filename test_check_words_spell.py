# test_check_words_spell.py
import unittest
from check_words_spell import *

class TestCheckWordsSpell(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.dictionary = ["apple", "banana", "grape", "orange", "pineapple"]
        self.trie = build_trie(self.dictionary)

    # Test for Trie.insert and Trie.search
    def test_trie(self):
        # Common case: Word exists in the dictionary
        self.assertTrue(self.trie.search("apple"))
        # Edge case: Word is a prefix of another word
        self.assertFalse(self.trie.search("app"))
        # Error case: Word not in the dictionary
        self.assertFalse(self.trie.search("mango"))

    def test_build_trie(self):
        # Common case: Build trie with a normal dictionary
        trie = build_trie(["cat", "dog", "mouse"])
        self.assertTrue(trie.search("cat"))
        self.assertFalse(trie.search("bat"))
        
        # Edge case: Empty dictionary
        empty_trie = build_trie([])
        self.assertFalse(empty_trie.search("anything"))
        
        # Error case: Non-alphabetical characters
        with self.assertRaises(ValueError):
            trie_with_special_chars = build_trie(["cat!", "dog@"])


    # Test for find_closest_match
    def test_find_closest_match(self):
        # Common case: Find closest match for a misspelled word
        self.assertEqual(find_closest_match("appl", self.dictionary), "apple")
        # Edge case: Word with equal distances
        close_words = ["boat", "coat"]
        self.assertIn(find_closest_match("bcat", close_words), close_words)
        # Error case: Dictionary is empty
        with self.assertRaises(ValueError):
            find_closest_match("apple", [])

    # Test for correct_spelling
    def test_correct_spelling(self):
        # Common case: Correct a misspelled sentence
        result = correct_spelling("appl banan", self.trie, self.dictionary)
        self.assertTrue(result[0])  # Corrections were made
        self.assertEqual(result[1], "apple banana")  # Corrected result
        self.assertEqual(result[2], ["appl", "banan"])  # Misspelled words

        # Edge case: Input contains only correct words
        result = correct_spelling("apple banana", self.trie, self.dictionary)
        self.assertFalse(result[0])  # No corrections made
        self.assertEqual(result[1], "apple banana")
        self.assertEqual(result[2], [])

        # Error case: Input contains entirely unknown words
        result = correct_spelling("asdf qwerty", self.trie, self.dictionary)
        self.assertTrue(result[0])
        self.assertEqual(result[2], ["asdf", "qwerty"])  # All words misspelled



if __name__ == "__main__":
    unittest.main()
