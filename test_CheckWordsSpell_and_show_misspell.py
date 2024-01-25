#Name: Ting Li; Date: Dec2, 2023.

'''
This file test 'CheckWordsSpell.py' and 'show_misspell.py'. 
'''

import CheckWordsSpell
import show_misspell
import unittest


class TestCheckWordsSpell(unittest.TestCase):
    def test_levenshtein_distance(self):
        #valid
        w1 = 'love'
        w2 = 'live'
        result1 = CheckWordsSpell.levenshtein_distance(w1, w2)
        self.assertEqual(result1, 1)
        #edge
        w3 = 'love'
        w4 = 'love'
        result2 = CheckWordsSpell.levenshtein_distance(w3, w4)
        self.assertEqual(result2, 0)
        #invalid
        w5 = 12
        w6 = 11
        with self.assertRaises(TypeError):
            CheckWordsSpell.levenshtein_distance(w5, w6)

    def test_read_dictionary(self):
        dic_choose1 = 0
        result1 = CheckWordsSpell.read_dictionary(dic_choose1)
        self.assertIsInstance(result1, list)
 
        dic_choose2 = 1
        result2 = CheckWordsSpell.read_dictionary(dic_choose2)
        self.assertIsInstance(result2, list)
        
    def test_correct_spelling(self):
        # valid
        user_input = 'hte'
        dictionary = ['the', 'large', 'brown', 'dog']
        result1 = CheckWordsSpell.correct_spelling(user_input, dictionary)
        self.assertTrue(result1[0])  # Expecting corrections
        self.assertEqual(result1[1], 'the')  # Expecting 'the' as the corrected string
        self.assertListEqual(result1[2], ['hte'])  # Expecting 'hte' as the wrongly spelled word
        # edge
        user_input = 'correct'
        dictionary = ['correct']
        result2 = CheckWordsSpell.correct_spelling(user_input, dictionary)
        self.assertFalse(result2[0])  # No corrections should be made
        self.assertEqual(result2[1], 'correct')  # Expecting the same word as the corrected string
        self.assertListEqual(result2[2], [])  # No wrongly spelled words
        # invalid
        user_input = 123
        dictionary = ['valid', 'words']
        with self.assertRaises(AttributeError):
            CheckWordsSpell.correct_spelling(user_input, dictionary)


class TestShow_misspell(unittest.TestCase):
    def test_read_file(self):
        #valid
        result1 = show_misspell.read_file("wrongly_spell.txt")
        self.assertIsInstance(result1, list)
        #invalid
        with self.assertRaises(FileNotFoundError):
            show_misspell.read_file("NoSuchFile.txt")
    
    def test_count_word_frequencies(self):
        content1 = ["oak", "land", "school"]
        self.assertIsInstance(show_misspell.count_word_frequencies(content1), dict)


if __name__ == "__main__":
    unittest.main()