import sys


def sort_count_inversions(arr):
    len_arr = len(arr)
    if len_arr == 1:
        return (arr, 0)
    n = len_arr / 2
    sorted_1, inversions1 = sort_count_inversions(arr[0:n])
    sorted_2, inversions2 = sort_count_inversions(arr[n:])

    # Merge and count
    merged_arr = [0] * len_arr
    i1 = i2 = 0
    len_1 = len(sorted_1)
    len_2 = len(sorted_2)
    inversion_count = inversions1 + inversions2
    for i_s in range(0, len_arr):
        if i1 < len_1 and i2 < len_2:
            if sorted_1[i1] < sorted_2[i2]:
                merged_arr[i_s] = sorted_1[i1]
                i1 += 1
            else:
                merged_arr[i_s] = sorted_2[i2]
                i2 += 1
                inversion_count += (len_1 - i1)
        elif i1 < len_1:
            # Copy from 1
            merged_arr[i_s] = sorted_1[i1]
            i1 += 1
        elif i2 < len_2:
            merged_arr[i_s] = sorted_2[i2]
            i2 += 1
        else:
            #print("Wrong index for i_s = %s. lst = %s " % (i_s, lst))
            raise Exception
    return (merged_arr, inversion_count)


def run_in_code_tests():
    def _count_inversions(pairs):
        return len(pairs)

    sorted_arr, count = sort_count_inversions([1,2,3,4])
    assert sorted_arr == [1,2,3,4]
    assert count == 0
    sorted_arr, count = sort_count_inversions([4,3,2,1])
    assert sorted_arr == [1,2,3,4]
    assert count == 6
    sorted_arr, count = sort_count_inversions([4,3,2])
    assert sorted_arr == [2,3,4]
    assert count == _count_inversions([(4,3), (4,2), (3,2)])
    sorted_arr, count = sort_count_inversions([7, 9, 5, 1, 2])
    assert sorted_arr == [1,2,5,7,9]
    assert count == _count_inversions([ (7, 5), (7, 1), (7,2), (9,5), (9,1), (9,2), (5,1), (5,2)])


def count_inversions_from_file(file_path):
    arr = []
    with(open(file_path, "r")) as f:
         for line in f:
             arr += [int(line)]
    return sort_count_inversions(arr)


def run_from_file_tests():
    # http://www.geeksforgeeks.org/count-inversions-array-set-3-using-bit/
    sorted_arr, count = count_inversions_from_file(file_path="IntegerArray_test_1.txt")
    assert count == 6
    sorted_arr, count = count_inversions_from_file(file_path="IntegerArray_test_2.txt")
    assert count == 11*10/2
    print("run_from_file_tests completed")


def run_task():
    sorted_arr, count = count_inversions_from_file(file_path="IntegerArray.txt")
    # Validate count
    assert len(sorted_arr) == 100000
    # Validate sorting
    for i in xrange(0, len(sorted_arr)):
        assert sorted_arr[i] == i + 1
    print("For task there are %s inversions. max int = %s" % (count, sys.maxint))


if __name__ == "__main__":
    run_in_code_tests()
    run_from_file_tests()
    run_task()