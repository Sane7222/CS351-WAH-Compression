import os
import builtins

def create_index(input_file, output_path, sorted):
    index_dict = {  'cat':    '1000', # Key, value dictionary for bitmap index
                    'dog':    '0100',
                    'turtle': '0010',
                    'bird':   '0001',
                    0:  '1000000000',
                    1:  '0100000000',
                    2:  '0010000000',
                    3:  '0001000000',
                    4:  '0000100000',
                    5:  '0000010000',
                    6:  '0000001000',
                    7:  '0000000100',
                    8:  '0000000010',
                    9:  '0000000001',
                    'True\n':  '10\n',
                    'False\n': '01\n'   }

    file = os.path.basename(input_file) # Grab just filename
    output_path = os.path.join(output_path, file) # Combine output path and filename

    if sorted:
        output_path = output_path + '_sorted' # Add sorted to filename

    with open(input_file, 'r') as i, open(output_path, 'w') as o:

        lines = i.readlines()
        if sorted:
            lines = builtins.sorted(lines) # Sort file if needed
            
        for line in lines:
            species, age, adopted = line.split(',') # Split lines

            o.write(index_dict[species]) # Species

            age = int(age) # Age
            if age % 10 == 0:
                o.write(index_dict[(age // 10) - 1])
            else:
                o.write(index_dict[age // 10])

            o.write(index_dict[adopted]) # Adopted

def compress_index(bitmap_index, output_path, compression_method, word_size):

    sum_0 = 0 # Sum of everything for analysis
    sum_1 = 0
    sum_lit = 0
    sum_dirty = 0

    file = os.path.basename(bitmap_index) # Grab just filename
    output_path = os.path.join(output_path, file) # Combine output path and filename
    grab_size = 0

    if compression_method == 'WAH':
        grab_size = word_size - 1
        output_path = output_path + '_' + str(compression_method) + '_' + str(word_size) # Append proper suffix to output file
    elif compression_method == 'BBC':
        output_path = output_path + '_' + str(compression_method) + '_' + str(8) # Append proper suffix to output file
        grab_size = 8

    runs_0 = 0
    runs_1 = 0
    literals = 0

    with open(bitmap_index, 'r') as i, open(output_path, 'w') as o:

        transpose = [''] * 16
        for line in i.readlines(): # Transpose Bitmap Index
            for j in range(16):
                transpose[j] += line[j]

        if compression_method == 'WAH':
            for line in transpose:
                s = 0
                e = grab_size

                while e <= len(line): # While not at the end of the line
                    block = line[s:e] # Grab appropriate segment
                    s += grab_size
                    e += grab_size

                    if block.count('0') == len(block): # Runs of 0's
                        sum_0 += 1

                        if runs_1 > 0: # Flush runs 1
                            runs_1 = write_runs_WAH(o, runs_1, word_size, 1)
                        runs_0 += 1

                    elif block.count('1') == len(block): # Runs of 1's
                        sum_1 += 1

                        if runs_0 > 0: # Flush runs 0
                            runs_0 = write_runs_WAH(o, runs_0, word_size, 0)
                        runs_1 += 1

                    else: # Literal
                        sum_lit += 1

                        if runs_0 > 0: # Flush runs 0 or 1
                            runs_0 = write_runs_WAH(o, runs_0, word_size, 0)
                        elif runs_1 > 0:
                            runs_1 = write_runs_WAH(o, runs_1, word_size, 1)
                        o.write('0' + block)

                if runs_1 > 0: # Flush runs of 1's
                    runs_1 = write_runs_WAH(o, runs_1, word_size, 1)
                elif runs_0 > 0: # Flush runs of 0's
                    runs_0 = write_runs_WAH(o, runs_0, word_size, 0)

                block = line[s:] # Grab remaining characters

                if len(block) != 0:
                    while len(block) < grab_size: # Fill and write as literal
                        block += '0'
                    o.write('0' + block)
                o.write('\n')
        
        elif compression_method == 'BBC':
            for line in transpose:
                lit_lst = []
                s = 0
                e = grab_size

                while e <= len(line):
                    block = line[s:e] # Grab Byte
                    s += grab_size
                    e += grab_size

                    if block.count('0') == len(block): # Runs of 0's
                        sum_0 += 1

                        if runs_0 == 32767 or literals > 0: # End Chunk
                            runs_0 = literals = write_runs_literals_BBC(o, runs_0, literals, lit_lst)
                            lit_lst = []
                        runs_0 += 1
                        
                    elif block.count('1') == 1 and literals == 0 and line[s:e].count('0') == len(block): # Dirty Bit | End Chunk
                        sum_dirty += 1

                        runs_0 = literals = write_dirty_BBC(o, runs_0, block.find('1'))

                    else: # Literal
                        sum_lit += 1

                        literals += 1
                        lit_lst.append(block)

                        if literals == 15: # End Chunk
                            runs_0 = literals = write_runs_literals_BBC(o, runs_0, literals, lit_lst)
                            lit_lst = []

                if runs_0 > 0 or literals > 0: # Flush runs or literals
                    runs_0 = literals = write_runs_literals_BBC(o, runs_0, literals, lit_lst)

                block = line[s:] # Grab remaining characters

                if len(block) != 0:
                    while len(block) < grab_size: # Fill and write as literal
                        block += '0'
                    o.write(block)

                o.write('\n')

    # print('  Runs of 0: ' + str(sum_0))
    # print('  Runs of 1: ' + str(sum_1))
    # print('  Literals: ' + str(sum_lit))
    # print('  Dirty Bits: ' + str(sum_dirty))

def write_runs_WAH(o, runs, word_size, type):
    binary = bin(runs)[2:].zfill(word_size - 2) # Convert # of runs to binary and truncate leading 0b, then pad leftmost side with 0's up to word_size - 2

    if type == 0:
        o.write('10' + binary)
    elif type == 1:
        o.write('11' + binary)
    return 0

def write_runs_literals_BBC(o, runs, literals, lst):
    lit_bin = bin(literals)[2:].zfill(4) # Convert # of literals to binary truncate 0b, then fill up to 4 with 0's
    
    if runs > 127: # Need 2 bytes
        run_bin = bin(runs)[2:].zfill(16)
        o.write('1110' + str(lit_bin) + str(run_bin))

    elif runs > 6: # Need 1 byte
        run_bin = bin(runs)[2:].zfill(8)
        o.write('1110' + str(lit_bin) + str(run_bin))

    else:
        run_bin = bin(runs)[2:].zfill(3)
        o.write(str(run_bin) + '0' + str(lit_bin))

    if literals != 0:
        for lit in lst:
            o.write(lit)

    return 0

def write_dirty_BBC(o, runs, location):
    loc_bin = bin(location)[2:].zfill(4) # Convert location of dirty bit to binary truncate 0b, then fill up to 4 with 0's

    if runs > 127: # Need 2 bytes
        run_bin = bin(runs)[2:].zfill(16)
        o.write('1111' + str(loc_bin) + str(run_bin))

    elif runs > 6: # Need 1 byte
        run_bin = bin(runs)[2:].zfill(8)
        o.write('1111' + str(loc_bin) + str(run_bin))
        
    else:
        run_bin = bin(runs)[2:].zfill(3)
        o.write(str(run_bin) + '1' + str(loc_bin))

    return 0
