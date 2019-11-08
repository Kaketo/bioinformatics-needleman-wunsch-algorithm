def read_sequence(file_name, max_seq_len):
    """
    Function to read load files with nucleotides sequences
    - max lenght of sequence is 100
    """
    file = open(file_name,'r')
    sequence = file.read().splitlines(True)
    file.close()

    header_row = sequence[0]
    assert header_row[0] == '>', 'File %a not in FASTA format' %file_name
    # Delete header row
    sequence = ''.join(sequence[1:])
    sequence = sequence.replace('*','')
    sequence = sequence.replace('\n','')

    assert isinstance(sequence, str)
    assert len(sequence) <= max_seq_len, 'Sequence in file %a is too long' %file_name
    
    return sequence

def read_config(file_name):
    """
    Function to read config file - exaclty in form as it was described in the task

    Example config file:
    GAP_PENALTY = -2
    SAME = +5
    DIFF = -5
    MAX_SEQ_LEN = 100
    MAX_NUMBER_PATHS = 10
    """
    config_file = open(file_name,'r')
    config_args = config_file.readlines()
    config_file.close()
    config = {}
    for arg in config_args:
        arg = arg.replace(' ','')
        arg = arg.replace('\n','')
        arg = arg.split('=')
        assert len(arg) == 2, 'One of arguments in config file is declared wrong'
        assert int(arg[1]) == round(int(arg[1])), 'Argument %a is not integer' %arg[0] 
        config[arg[0]] = int(arg[1])
    
    config_must_have = set(['GAP_PENALTY','SAME','DIFF','MAX_SEQ_LEN','MAX_NUMBER_PATHS'])
    config_what_is = set(config.keys())
    assert len(config_what_is.intersection(config_must_have)) == len(config_must_have), 'Config is missing one key argument'
    
    return config

