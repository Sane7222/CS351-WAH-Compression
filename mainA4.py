import assignment4 as a

def compare_files(file_1, file_2):
    with open(file_1, 'r') as f1, open(file_2, 'r') as f2:
        return f1.read() == f2.read()

if __name__ == '__main__': # Assumes running from a4
    a.create_index('data/animals.txt', 'myOutput/', False) # Tests if all my bitmap creation works

    a.create_index('data/animals.txt', 'myOutput/', True) # Sorting

    # Unsorted
    a.compress_index('myOutput/animals.txt', 'myOutput/', 'WAH', 8)
    a.compress_index('myOutput/animals.txt', 'myOutput/', 'WAH', 16)
    a.compress_index('myOutput/animals.txt', 'myOutput/', 'WAH', 32)
    a.compress_index('myOutput/animals.txt', 'myOutput/', 'WAH', 64)
    a.compress_index('myOutput/animals.txt', 'myOutput/', 'BBC', 64) # Test Byte-Aligned Bitmap Compression

    # Sorted
    a.compress_index('myOutput/animals.txt_sorted', 'myOutput/', 'WAH', 8)
    a.compress_index('myOutput/animals.txt_sorted', 'myOutput/', 'WAH', 16)
    a.compress_index('myOutput/animals.txt_sorted', 'myOutput/', 'WAH', 32)
    a.compress_index('myOutput/animals.txt_sorted', 'myOutput/', 'WAH', 64)
    a.compress_index('myOutput/animals.txt_sorted', 'myOutput/', 'BBC', 64) # Test Byte-Aligned Bitmap Compression

