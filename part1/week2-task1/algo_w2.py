import sys
import copy


def swap(arr, a, b):
        arr[b], arr[a] = arr[a], arr[b]

def _partition_type_comparison_median(arr, l, r):
    if l - r == 0:
        raise Exception
    if l - r == 1:
        return arr[1]
    assert r > l
    assert r < len(arr)

    three_element_arr = [arr[l], arr[r]]
    if (r - l + 1) % 2 == 0:
        median_pos = (r + l + 1)/2 - 1
    else:
        median_pos = (r + l)/2

    three_element_arr += [ arr[median_pos] ]
    assert len(three_element_arr) == 3
    #print ("three_element_arr = %s" % three_element_arr)

    if three_element_arr[0] > three_element_arr[2]:
        swap(three_element_arr, 0, 2)
    if three_element_arr[0] > three_element_arr[1]:
        swap(three_element_arr, 0, 1)
    if three_element_arr[1] > three_element_arr[2]:
        swap(three_element_arr, 1, 2)

    median_val = three_element_arr[1]
    if median_val == arr[l]:
        return (median_val, l)
    elif median_val == arr[r]:
        return (median_val, r)
    elif median_val == arr[median_pos]:
        return (median_val, median_pos)
    else:
        raise Exception

    return


def _quick_sort_count_comparisons(arr, partition_type, l, r):
    if r - l <= 1:
        return 0
    # Partition
    if partition_type == "1":
        p = arr[l]
    elif partition_type == "2":
        swap(arr, r - 1, l)
        p = arr[l]
    elif partition_type == "3":
        (median_val,median_pos) = _partition_type_comparison_median(arr, l, r - 1)
        #print("Median selected %s at %s" % (median_val, median_pos))
        assert median_pos >= l
        assert median_pos < r
        swap(arr, median_pos, l)
        p = arr[l]
    else:
        raise Exception
    i = l + 1
    for j in range(l + 1, r):
        if arr[j] < p:
            swap(arr, i, j)
            i += 1
    swap(arr, l, i - 1)
    #print("arr = %s" % arr)
    l_comparison_count = _quick_sort_count_comparisons(arr=arr,partition_type=partition_type,l=l, r=i-1)
    r_comparison_count = _quick_sort_count_comparisons(arr=arr,partition_type=partition_type,l=i, r=r)
    return l_comparison_count + r_comparison_count + ( r - l - 1)

# Wrapper to call _quick_sort_count_comparisons, since Python does not allow to overload functions
def quick_sort_count_comparisons(arr, partition_type):
    l = 0
    r = len(arr)
    n_comparisons = _quick_sort_count_comparisons(arr=arr, partition_type=partition_type, l=l, r=r)
    return (arr, n_comparisons)


def count_comparisons_from_file(file_path, partition_type):
    arr = []
    with(open(file_path, "r")) as f:
         for line in f:
             arr += [int(line)]
    return quick_sort_count_comparisons(arr, partition_type)

def run_task():

    def validate_sorted_arr_print(sorted_arr, count, partition_type):
        # Validate count
        assert len(sorted_arr) == 10000
        # Validate sorting
        for i in xrange(0, len(sorted_arr)):
            assert sorted_arr[i] == i + 1
        print("For task there are %s comparisons. Partition type = %s" % (count, partition_type))


    sorted_arr, count = count_comparisons_from_file(file_path="QuickSort.txt", partition_type="1")
    validate_sorted_arr_print(sorted_arr, count, "1")
    sorted_arr, count = count_comparisons_from_file(file_path="QuickSort.txt", partition_type="2")
    validate_sorted_arr_print(sorted_arr, count, "2")
    sorted_arr, count = count_comparisons_from_file(file_path="QuickSort.txt", partition_type="3")
    validate_sorted_arr_print(sorted_arr, count, "3")

def run_in_code_tests():
    # Unit
    median_val, median_pos = _partition_type_comparison_median([1,2,3,4], l=0, r=3)
    assert median_val == 2
    assert median_pos == 1
    median_val, median_pos = _partition_type_comparison_median([1,2], l=0, r=1)
    assert median_val == 1
    assert median_pos == 0
    median_val, median_pos = _partition_type_comparison_median([8,2,4,5,7,1], l=0, r=5)
    assert median_val == 4
    assert median_pos == 2
    median_val, median_pos = _partition_type_comparison_median([1, 2, 3, 4, 5], l=2, r=4)
    assert median_val == 4
    assert median_pos == 3

    # [3, 9, 8, 4, 6, 10, 2, 5, 7, 1] -> [3, 1, 6]
    median_val, median_pos = _partition_type_comparison_median([3, 9, 8, 4, 6, 10, 2, 5, 7, 1], l=0, r=9)
    assert median_val == 3
    assert median_pos == 0



    # High level
    sorted_arr, count = quick_sort_count_comparisons([1,2,3,4], "1")
    assert sorted_arr == [1,2,3,4]
    sorted_arr, count = quick_sort_count_comparisons([4,3,2,1], "1")
    assert sorted_arr == [1,2,3,4]
    sorted_arr, count = quick_sort_count_comparisons([6,5], "1")
    assert sorted_arr == [5,6]
    assert count == 1
    sorted_arr, count = quick_sort_count_comparisons([6,5,4], "1")
    # Level 0: pivot 6.
    # Level 1: (4,5) (6)       | 2 cmp
    # Level 2: (4) (5)         | 1 cmp
    assert sorted_arr == [4, 5, 6]
    assert count == 3
    sorted_arr, count = quick_sort_count_comparisons([6,5,4], "2")
    # Level 0: pivot 6. Do swap to (4,5,6)
    # Level 1: 4, (5,6)        | 2 cmp
    # Level 2: (5) (6)         | 1 cmp
    assert sorted_arr == [4, 5, 6]
    assert count == 3
    # sorted_arr, count = quick_sort_count_comparisons([4,3,2,1], "3")
    # assert sorted_arr == [1,2,3,4]
    sorted_arr, count = quick_sort_count_comparisons([6,5,4], "3")
    # Level 0: pivot 5. Do swap to (5,6,4) <- ok
    # Level 1: 5, (6,4)        | 2 cmp
    # Level 2: (5) (6)         | 1 cmp
    assert sorted_arr == [4, 5, 6]
    #assert count == 3


def run_coursera_tests():
    arr = [3, 9, 8, 4, 6, 10, 2, 5, 7, 1]
    sorted_arr, count = quick_sort_count_comparisons(list(arr), "1")
    assert len(sorted_arr) == 10
    assert count == 25
    sorted_arr, count = quick_sort_count_comparisons(list(arr), "2")
    assert len(sorted_arr) == 10
    assert count == 29
    sorted_arr, count = quick_sort_count_comparisons(copy.copy(arr), "3")
    assert len(sorted_arr) == 10
    assert count == 21

if __name__ == "__main__":
    run_in_code_tests()
    run_coursera_tests()
    run_task()