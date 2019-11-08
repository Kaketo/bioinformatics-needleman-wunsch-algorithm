import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from src.needleman_wunch import create_score_matrix, needleman_wunch_alghoritm

class score_matrix_tests(unittest.TestCase):
    def test_size(self):
        A = 'ABCD'
        B = 'ABCDFG'
        gap_penalty = -10
        score_matrix = create_score_matrix(A,B, gap_penalty)
        self.assertEqual(score_matrix.shape[0], len(A) + 1)
        self.assertEqual(score_matrix.shape[1], len(B) + 1)

    def test_gap_penalty_last_value(self):
        A = 'ABCD'
        B = 'ABCDFG'
        gap_penalty = -10
        score_matrix = create_score_matrix(A,B, gap_penalty)        
        self.assertEqual(score_matrix[-1,0], gap_penalty*len(A))
        self.assertEqual(score_matrix[0,-1], gap_penalty*len(B))
    
class needleman_wunch_tests(unittest.TestCase):
    def test_max_number_paths(self):
        A = 'SUM'
        B = 'SAM'
        _, adjusted_sequences_list = needleman_wunch_alghoritm(A,B,
                                            max_number_paths = 1, 
                                            match_score = 5, 
                                            miss_score = -5, 
                                            gap_penalty = -2)
        
        self.assertEqual(len(adjusted_sequences_list), 1)

    def test_output_list_sizes(self):
        A = 'TCTTGAAATGATGTAGAAAT'
        B = 'ATTGTTTCTCAAATATCTTG'
        _, adjusted_sequences_list = needleman_wunch_alghoritm(A,B,
                                            max_number_paths = 10, 
                                            match_score = 5, 
                                            miss_score = -5, 
                                            gap_penalty = -2)
        for adj_seq in adjusted_sequences_list:
            self.assertEquals(len(adj_seq),2)

if __name__ == '__main__':
    unittest.main(verbosity=True)