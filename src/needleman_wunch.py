import numpy as np
import networkx as nx

def create_score_matrix(A,B, gap_penalty):
    """
    Function to create outline of score matrix - without proper values now

    Arguments:
    - A - sequence A (str)
    - B - sequence B (str)
    - gap_penalty (int)
    
    Returns:
    - matrix of size [len(A) + 1 , len(B) + 1]
    """
    score_matrix = np.empty([len(A),len(B)])
    score_matrix = np.vstack((np.arange(gap_penalty, len(B)*(gap_penalty) + gap_penalty, gap_penalty), score_matrix))
    score_matrix = np.hstack((np.array([np.arange(0, len(A)*(gap_penalty) + gap_penalty, gap_penalty)]).T, score_matrix))
    return score_matrix

def missmatch_score(x,y, match_score, miss_score):
    if x == y:
        return match_score
    else:
        return miss_score
    
def adjusted_sequences_from_graph_path(seq_1, seq_2, path):
    """
    Function that translates path in score matrix (directed graph) to adjusted sequence

    Arguments:
    - seq_1 (str)
    - seq_2 (str)
    - object returned by function all_simple_paths from library networkx

    Returns:
    adj_seq_1 (str)
    adj_seq_2 (str)

    """
    adj_seq_1 = ''
    adj_seq_2 = ''
    seq_1_iterator = 0
    seq_2_iterator = 0

    seq_1 = seq_1[::-1]
    seq_2 = seq_2[::-1]

    for i in range(len(path)-1):
        if (path[i][0] - 1 == path[i+1][0]) and (path[i][1] - 1 == path[i+1][1]):
            adj_seq_1 = adj_seq_1 + seq_1[seq_1_iterator]
            adj_seq_2 = adj_seq_2 + seq_2[seq_2_iterator]
            seq_1_iterator += 1
            seq_2_iterator += 1

        if (path[i][0] - 1 == path[i+1][0]) and (path[i][1] == path[i+1][1]):
            adj_seq_1 = adj_seq_1 + '-'
            adj_seq_2 = adj_seq_2 + seq_2[seq_2_iterator]
            seq_2_iterator += 1

        if (path[i][0] == path[i+1][0]) and (path[i][1] - 1 == path[i+1][1]):
            adj_seq_1 = adj_seq_1 + seq_1[seq_1_iterator]
            adj_seq_2 = adj_seq_2 + '-'
            seq_1_iterator += 1

    adj_seq_1 = adj_seq_1[::-1]
    adj_seq_2 = adj_seq_2[::-1]

    return adj_seq_1, adj_seq_2
    
def find_source_and_target_node(score_matrix):
    """
    Function to find source node and target node in score matrix

    Arguments:
    - score matrix

    Returns:
    - source_node - tuple (row,col)
    - target_node - tuple (row,col)
    """
    source_node = ((score_matrix.shape[0] - 1),(score_matrix.shape[1] - 1))
    target_node = (0,0)
    return source_node, target_node

def find_all_paths_and_convert_to_adjusted_sequences(A,B,path_graph, source, target, max_number_paths):
    """
    Function to find all paths that satisfies given conditions

    Arguments:
    - max_number_paths - max number of paths to be returned
    - max_seq_len - max lenght of path in graph 

    Returns:
    - adjusted_sequences_list - list of adjusted sequences, each element is lenght of 2.
    First is first adjusted sequence, second is second adjusted sequence.
    """
    adjusted_sequences_list = []
    all_paths = nx.all_simple_paths(path_graph, source=source, target=target)
    for i,path in enumerate(all_paths):
        if i >= max_number_paths:
            break
        adjusted_sequences_list.append(adjusted_sequences_from_graph_path(B,A,path))
    return adjusted_sequences_list
   

def needleman_wunch_alghoritm(A, B, max_number_paths = 1, match_score = 5, miss_score = -5, gap_penalty = -2): 
    """
    Main alghoritm 

    Returns:
    - score - score of adjustment
    - adjusted_sequences_list - list of adjusted sequences, each element is lenght of 2.
    First is first adjusted sequence, second is second adjusted sequence.
    """
    # Directed graph to save paths
    path_graph = nx.DiGraph()
    # Score matrix
    score_matrix = create_score_matrix(A, B, gap_penalty)
    
    for i in range(1, score_matrix.shape[0]):
        path_graph.add_edge((i,0),(i-1,0))
        for j in range(1, score_matrix.shape[1]):
            path_graph.add_edge((0,j),(0,j-1))

            score = missmatch_score(A[i - 1],B[j - 1], match_score, miss_score)            
            diag = score_matrix[i-1, j-1] + score
            left = score_matrix[i, j-1] + gap_penalty
            up = score_matrix[i-1, j] + gap_penalty

            if max(diag,left,up) == diag:
                new_value = diag
                path_graph.add_edge((i,j), ((i-1),(j-1)))
            if max(diag,left,up) == left:
                new_value = left
                path_graph.add_edge((i,j), ((i),(j-1)))
            if max(diag,left,up) == up:
                new_value = up
                path_graph.add_edge((i,j), ((i-1),(j)))

            # New value to score matrix
            score_matrix[i,j] = new_value

    # Get score of paths
    score = score_matrix[-1,-1]
        
    # Find all paths from end to begining in path graph
    source_node, target_node = find_source_and_target_node(score_matrix)
    adjusted_sequences_list = find_all_paths_and_convert_to_adjusted_sequences(A,B,
                                                                                path_graph = path_graph, 
                                                                                source = source_node, 
                                                                                target = target_node, 
                                                                                max_number_paths = max_number_paths)
    
    return score, adjusted_sequences_list