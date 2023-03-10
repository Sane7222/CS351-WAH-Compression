File Summary:

    README.txt

        File overview
        How to run assignment4.py
        Analysis on Compression methods

    assignment4.py

        create_index method to take in a file with Species, Age, Adopted status and convert that into a bitmap index for compression
            Takes in a file and outputs a new file at the specified location
            Can sort the file lexographically if sorted bool is True

        compress_index method takes a bitmap index containing 1s and 0s and can either use WAH or BBC compression methods
            Takes in bitmap file and outputs new file at specified location
            Word size parameter used for WAH compression
            Compression method parameter to specify which compression to use

How To Run:

    With assignment4.py in the cwd go into the python file that will execute tests and 'import assignment4'
    Then you can call assignment4.create_index() and assignment4.compress_index() methods with desired parameters

Analysis:

    characters    filename                     runs 0    runs 1    literals    dirty bits

    1600000       animals.txt                  
    1361320       animals.txt_BBC_8            59065     0         131915      9020
    1661728       animals.txt_WAH_16           14025     0         92631       0
    1649984       animals.txt_WAH_32           1271      0         50329       0
    1626112       animals.txt_WAH_64           26        0         25366       0
    1557976       animals.txt_WAH_8            76176     253       152131      0

    1600000       animals.txt_sorted
    339456        animals.txt_sorted_BBC_8     161702    0         38268       30
    56704         animals.txt_sorted_WAH_16    85811     19151     1694        0
    115584        animals.txt_sorted_WAH_32    41044     8794      1762        0
    227200        animals.txt_sorted_WAH_64    19737     3867      1788        0
    27846         animals.txt_sorted_WAH_8     184923    42073     1564        0

    Why are they different sizes?

        How the data is ordered (sorted, or unsorted) the type of compression (BBC, WAH) and word size will all impact the compression ratio for each file.
        If the data is mixed where 1s and 0s are distributed closer to each other, then smaller word sizes will be more useful and larger sizes won't be.
        If data is sorted then 0s and 1s will be in larger contiguous groups. This is where compression can shine.
        WAH can compress runs of 1s much better than BBC can, however BBC can compress dirty bits better than WAH can.

        For the same bitmaps these file are all using different combinations of compression methods and word sizes which makes all of them various sizes.

    Did sorting help? By how much?

        Sorting helped significatly as both compression methods were able to perform more compression due to contiguous runs.

        Sorted Compression Ratios:
            Best: 57.476 : 1        Worst: 4.731 : 1

        Unsorted Compression Ratios:
            Best: 1.176 : 1         Worst: 0.962 : 1

    Did different word sizes have different compression ratios? Why?

        For sorted data smaller word sizes were better as there partitions were smaller and they could still count a large number of these runs.
        For WAH word size 8 is could count runs of 7 up to 2^6. For WAH word size 64 it could count runs of 63 up to 2^62 which is a large number.
        The partitions and count size for these bigger word sizes was too large for the provided bitmap, so smaller word sizes were more efficient.

        On unsorted data the smallest word size 8 had the best performance as a run only had to be 7 bit long. Where word size 64 runs had to be 63 bits long.
        The larger word sizes had worse performance on unsorted data, but the largest word size was slightly better than the second and third largest.
        This was due to how the data came unsorted.
