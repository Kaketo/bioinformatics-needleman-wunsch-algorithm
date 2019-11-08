import os
import unittest
import sys 
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from src.files_handling import read_sequence, read_config

class sequence_read_tests(unittest.TestCase):
    def test_no_fasta_format(self):
        """
        no_sata_format.txt:
        ASKNDSALKDNAKSDNLASKDNALSDJB
        """
        my_data_path = os.path.join(THIS_DIR, 'no_sata_format.txt')
        with self.assertRaises(AssertionError):
            read_sequence(my_data_path, max_seq_len = 1000)

    def test_fasta_format(self):
        """
        File sata_format.txt:
        >MCHU - Calmodulin - Human, rabbit, bovine, rat, and chicken
        ADQLTEEQIAEFKEAFSLFDKDGDGTITTKELGTVMRSLG
        """
        my_data_path = os.path.join(THIS_DIR, 'sata_format.txt')
        self.assertEqual(read_sequence(my_data_path,  max_seq_len = 1000),'ADQLTEEQIAEFKEAFSLFDKDGDGTITTKELGTVMRSLG')

    def test_too_long_sequence(self):
        """
        File sata_format.txt:
        >MCHU - Calmodulin - Human, rabbit, bovine, rat, and chicken
        ADQLTEEQIAEFKEAFSLFDKDGDGTITTKELGTVMRSLG
        """
        my_data_path = os.path.join(THIS_DIR, 'sata_format.txt')
        with self.assertRaises(AssertionError):
            read_sequence(my_data_path, max_seq_len = 10)

class config_read_tests(unittest.TestCase):
    def test_missing_one_argument(self):
        """
        missing_one_argument.txt:
        GAP_PENALTY = -2
        SAME = +5
        DIFF = -5
        MAX_NUMBER_PATHS = 10
        """
        my_data_path = os.path.join(THIS_DIR, 'missing_one_argument.txt')
        with self.assertRaises(AssertionError):
            read_sequence(my_data_path,max_seq_len = 10000)

    def test_too_many_arguments(self):
        """
        too_many_arguments.txt:
        GAP_PENALTY = -2
        SAME = +5
        DIFF = -5
        MAX_SEQ_LEN = 100
        MAX_NUMBER_PATHS = 10
        RANDOM_ARGUMENT = 42
        """
        my_data_path = os.path.join(THIS_DIR, 'too_many_arguments.txt')

        returned_keys = set(read_config(my_data_path).keys())
        proper_keys = set(['GAP_PENALTY', 'SAME', 'DIFF', 'MAX_SEQ_LEN', 'MAX_NUMBER_PATHS'])
        returned_keys = returned_keys.intersection(proper_keys)
        self.assertEqual(returned_keys, proper_keys)
    
    def test_empty_file(self):
        """
        empty_config.txt:
        """
        my_data_path = os.path.join(THIS_DIR, 'empty_config.txt')

        with self.assertRaises(AssertionError):
            read_config(my_data_path)


if __name__ == '__main__':
    unittest.main(verbosity=True)