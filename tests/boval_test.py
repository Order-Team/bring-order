import unittest
from bring_order.boval import BOVal

class TestBoval(unittest.TestCase):
    def setUp(self):
        self.boval = BOVal()

    def test_get_first_words_returns_correct_string_with_short_list(self):
        words = ['Short', 'list']
        first_words = self.boval.get_first_words(words)
        self.assertEqual(first_words, 'Short list')

    def test_get_first_words_returns_correct_string_with_long_list(self):
        words = ['Long', 'list', 'has', 'more', 'words', 'than', 'short', 'list']
        first_words = self.boval.get_first_words(words)
        self.assertEqual(first_words, 'Long list has more words...')

    def test_get_first_words_returns_first_short_sentence(self):
        words = ['My', 'sentence', 'is', 'short.', 'It', 'is', 'ok.']
        first_words = self.boval.get_first_words(words)
        self.assertEqual(first_words, 'My sentence is short')

    def test_get_first_words_returns_first_short_question(self):
        words = ['What', 'to', 'ask?', 'I', 'do', 'not', 'know.']
        first_words = self.boval.get_first_words(words)
        self.assertEqual(first_words, 'What to ask?')

    def test_get_first_words_returns_first_short_exclamation(self):
        words = ['I', 'want', 'ice', 'cream!', 'Preferably', 'mint', 'Puffet.']
        first_words = self.boval.get_first_words(words)
        self.assertEqual(first_words, 'I want ice cream!')
    
    def test_empty_value_returns_false(self):
        self.assertFalse(self.boval.check_value_not_empty(''))
    
    def test_not_empty_value_returns_true(self):
        self.assertTrue(self.boval.check_value_not_empty('test text'))
    
    def test_value_to_short(self):
        self.assertFalse(self.boval.value_is_min_length('one text'))
    
    def test_correct_value_returns_true(self):
        self.assertTrue(self.boval.value_is_min_length('test value'))

    def test_value_contains_symbols(self):
        self.assertFalse(self.boval.value_not_contains_symbols('print(a=5)'))
    
    def test_value_contains_code(self):
        self.assertFalse(self.boval.value_not_contains_symbols('<h1>This is heading</h1>'))
    
    def test_value_contains_allowed_symbol(self):
        self.assertTrue(self.boval.value_not_contains_symbols('test value?'))
    
    def test_value_not_contain_symbols(self):
        self.assertTrue(self.boval.value_not_contains_symbols('test 1234'))
    
    def test_sentence_to_short_with_whitespace(self):
        self.assertFalse(self.boval.sentence_is_min_length('Small book '))
    
    def test_sentence_to_short(self):
        self.assertFalse(self.boval.sentence_is_min_length('Small book'))
    
    def test_correct_sentence_returns_true(self):
        self.assertTrue(self.boval.sentence_is_min_length('The Earth is round.'))

    def test_short_sentence_without_verb(self):
        self.assertFalse(self.boval.value_contain_predicate('An interesting book'))
    
    def test_long_sentence_without_verb(self):
        self.assertFalse(self.boval.value_contain_predicate('And now for something completely different'))
    
    def test_sentence_with_verb(self):
        self.assertTrue(self.boval.value_contain_predicate('I want an interesting book'))
    
    def test_sentence_contains_subject1(self):
        self.assertTrue(self.boval.value_contain_nlp_subject('I want an interesting book'))
    
    def test_sentence_not_contain_subject(self):
        self.assertFalse(self.boval.value_contain_nlp_subject('Running eating sleeping'))
    
    def test_sentence_not_contain_subject_with_random_input(self):
        self.assertFalse(self.boval.value_contain_nlp_subject('dsfsdf fdfsfs fdsfsdf fsdfsf'))
    
    def test_sentence_not_contain_object_with_random_input(self):
        self.assertFalse(self.boval.value_contain_nlp_object('dsfsdf fdfsfs fdsfsdf fsdfsf'))
    
    def test_sentence_not_contain_predicate_with_random_input(self):
        self.assertFalse(self.boval.value_contain_predicate('dsfsdf fdfsfs fdsfsdf fsdfsf'))
    
    def test_sentence_contains_passive_subject(self):
        self.assertTrue(self.boval.value_contain_nlp_subject('The cake was eaten'))
    
    def test_sentence_contain_object1(self):
        self.assertTrue(self.boval.value_contain_nlp_object('The students eat cake'))
    
    def test_sentence_contain_object2(self):
        self.assertTrue(self.boval.value_contain_nlp_object('The students in the library'))
    
    def test_sentence_not_contain_object(self):
        self.assertFalse(self.boval.value_contain_nlp_object('Running eating sleeping'))
    
    def test_empty_value_returns_false_in_all_methods(self):
        self.assertFalse(self.boval.sentence_is_min_length(''))
        self.assertFalse(self.boval.value_is_min_length(''))
        self.assertFalse(self.boval.value_contain_predicate(''))
        self.assertFalse(self.boval.value_contain_nlp_object(''))
        self.assertFalse(self.boval.value_contain_nlp_subject(''))
    
    def test_correct_lemmatization(self):
        lemmas = self.boval.lemmatization_of_value('She is going to buy an interesting book.')
        self.assertEqual(lemmas, ['she', 'be', 'go', 'to', 'buy', 'an', 'interesting', 'book', '.'])

    def test_incorrect_lemmatization(self):
        lemmas = self.boval.lemmatization_of_value('She is going to buy an interesting book.')
        self.assertNotEqual(lemmas, ['she', 'is', 'going', 'to', 'buy', 'an', 'interesting', 'book', '.'])
    
    def test_empty_value_lemmatization(self):
        lemmas = self.boval.lemmatization_of_value('')
        self.assertEqual(lemmas, [])
    
    def test_string_value_is_not_lemmatized(self):
        value = 'She is going to buy an interesting book.'
        self.assertFalse(self.boval.check_text_is_lemmatized(value))
    
    def test_string_value_is_lemmatized(self):
        value = 'she be go to buy an interesting book'
        self.assertTrue(self.boval.check_text_is_lemmatized(value))

    def test_list_value_is_lemmatized(self):
        value = ['she', 'be', 'go', 'to', 'buy', 'an', 'interesting', 'book']
        self.assertTrue(self.boval.check_text_is_lemmatized(value))

    def test_list_value_is_not_lemmatized(self):
        value = ['she', 'is', 'going', 'to', 'buy', 'an', 'interesting', 'book']
        self.assertFalse(self.boval.check_text_is_lemmatized(value))

    def test_value_contains_only_special_character(self):
        self.assertFalse(self.boval.value_not_empty_or_contains_symbols("@"))
