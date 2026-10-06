import unittest

from text_stats import count_sentences, count_words, longest_word


class TestCountWords(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("   \n\t "), 0)

    def test_simple(self):
        self.assertEqual(count_words("Xin chào thế giới"), 4)

    def test_punctuation_not_counted(self):
        self.assertEqual(count_words("Hello, world! ... ?"), 2)
        self.assertEqual(count_words('"Xin chào" - (bạn) ; : … «ơi»!'), 4)

    def test_apostrophe_and_hyphen(self):
        self.assertEqual(count_words("Don't use e-mail"), 3)


class TestCountSentences(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_sentences(""), 0)
        self.assertEqual(count_sentences("..."), 0)

    def test_multiple(self):
        self.assertEqual(count_sentences("Một. Hai! Ba?"), 3)

    def test_repeated_marks(self):
        self.assertEqual(count_sentences("Thật sao?! Ừ... Được."), 3)

    def test_no_final_mark(self):
        self.assertEqual(count_sentences("Câu một. Câu hai chưa xong"), 2)


class TestLongestWord(unittest.TestCase):
    def test_empty(self):
        self.assertIsNone(longest_word(""))
        self.assertIsNone(longest_word("!!!"))

    def test_simple(self):
        self.assertEqual(longest_word("Claude viết code nhanh"), "Claude")

    def test_tie_returns_first(self):
        self.assertEqual(longest_word("cat dog bat"), "cat")

    def test_ignores_punctuation(self):
        self.assertEqual(longest_word("Hi, extraordinary!"), "extraordinary")

    def test_vietnamese(self):
        self.assertEqual(longest_word("Tôi học nghiêng"), "nghiêng")


if __name__ == "__main__":
    unittest.main()
