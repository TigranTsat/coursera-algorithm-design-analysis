import time


def calculate_num_sums(numbers, min_n, max_n):
    numbers_hashtable = {}
    for number in numbers:
        numbers_hashtable[number] = True

    found_pairs = []

    counter = 0
    target_count = 0
    for target_sum in range(min_n, max_n + 1):
        # print("Calculating for %s" % target_sum)
        time1 = time.time()
        sub_cycle_counter = 0
        for x in numbers:
            remainder = target_sum - x
            if remainder == x:
                continue
            if remainder in numbers_hashtable:
                # print("Found %s and %s = %s" % (x, remainder, target_sum))
                found_pairs.append((x, remainder))
                sub_cycle_counter += 1
        time2 = time.time()
        found_target = sub_cycle_counter != 0
        if found_target:
            target_count += 1
        print 'For target %s, loop took %0.3f ms. Target found %s. Found numbers %s' % \
              (target_sum, (time2-time1)*1000.0, found_target, sub_cycle_counter)
        counter += sub_cycle_counter
    # Validating
    assert len(found_pairs) == counter
    for found_pair in found_pairs:
        a,b = found_pair
        assert a + b >= min_n
        assert a + b <= max_n
    assert target_count >= 0
    assert target_count <= (max_n - min_n + 1)
    return (counter, target_count)


def run_in_code_tests():
    numbers_1 = [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]
    res1, target_sum = calculate_num_sums(numbers=numbers_1, min_n=8, max_n=10)
    res2 = calculate_num_sum_sorted(numbers=numbers_1, min_n=8, max_n=10)
    print("Test1: Res1 = %s, res2 = %s" % (res1, res2))
    assert res1 == res2
    assert target_sum == 3

    numbers_2 = set([-2, -10, -5, -8, -3, -4, -6, 10, 20, 13, 0, 3, 5, 6, 3, 4, 5])
    res1, target_sum = calculate_num_sums(numbers=numbers_2, min_n=-5, max_n=5)
    res2 = calculate_num_sum_sorted(numbers=numbers_2, min_n=-5, max_n=5)
    print("Test2: Res1 = %s, res2 = %s" % (res1, res2))
    assert res1 == res2



def calculate_num_sum_sorted(numbers, min_n, max_n):
    debug = False
    sorted_arr = sorted(numbers)
    print("Array was sorted: start: %s, end: %s" % (sorted_arr[0], sorted_arr[len(sorted_arr) - 1]))
    last_known = len(sorted_arr) - 1
    counter = 0

    for i in xrange(0, len(sorted_arr) - 1):
        if sorted_arr[i] > max_n:
            break # No point going further
        diff_next = sorted_arr[i + 1] - sorted_arr[i]
        if diff_next <= 0:
            print("i = %s, sorted_arr[i + 1] = %s, sorted_arr[i] = %s" % (i, sorted_arr[i + 1], sorted_arr[i]))
        assert diff_next > 0
        next_last_knows = None
        if debug:
            print("Running cycle from %s downto %s.    diff_next=%s" % (last_known, i, diff_next))
        sorted_arr_last_known = sorted_arr[last_known] # To avoid accessing every time within inner loop
        for j in xrange(last_known, i, -1):
            if sorted_arr[j] > sorted_arr_last_known - diff_next:
                next_last_knows = j
            new_sum = sorted_arr[i] + sorted_arr[j]
            if new_sum >= min_n and new_sum <= max_n:
                if sorted_arr[i] == sorted_arr[j]:
                    continue
                print("Found %s and %s = %s" % (sorted_arr[i], sorted_arr[j], new_sum))
                counter += 1
            if new_sum < min_n:
                if debug:
                    print("Break at %s" % j)
                break # Going down will only decrease sum
        assert next_last_knows is not None
        # print("Shifting last_known to %s from %s" % (next_last_knows, last_known))
        last_known = next_last_knows
        if i % 100 == 0:
            print("Finished cycle for i = %s" % i)
    return counter * 2



def run_task():
    numbers = []
    file_name = "algo1-programming_prob-2sum.txt"
    with(open(file_name, "r")) as f:
        for line in f:
            numbers.append(int(line))
    duplicate_found = (len(set(numbers)) != len(numbers))
    # There are duplicates so dirty trick
    numbers_uniq = set(numbers)
    print("Data loaded. Total: %s, Min: %s, Max: %s. duplicate_found = %s" %
          (len(numbers), min(numbers), max(numbers), duplicate_found))
    assert 28206910625 in numbers_uniq
    assert -60012933873 in numbers_uniq

    # assert not duplicate_found # This is done otherwise sorted algorithm will not work properly

    # numbers_test = numbers[0:(len(numbers) / 10)]
    # numbers_test_uniq = set(numbers_test)
    # res1 = calculate_num_sums(numbers=numbers_test_uniq, min_n=-15, max_n=15)
    # res2 = calculate_num_sum_sorted(numbers=numbers_test_uniq, min_n=-15, max_n=15)
    # print("Res1 = %s, res2 = %s" % (res1, res2))
    # assert res1 == res2
    count_pairs, target_count = calculate_num_sums(numbers=numbers_uniq, min_n=-5, max_n=5)
    assert target_count == 1
    assert count_pairs > 0

    count_pairs, target_count = calculate_num_sums(numbers=numbers_uniq, min_n=-10*1000, max_n=10*1000)
    # answer_2 = calculate_num_sum_sorted(numbers=numbers_uniq, min_n=-10*1000, max_n=10*1000)
    print("count_pairs = %s, target_count = %s" % (count_pairs, target_count))



if __name__ == "__main__":
    run_in_code_tests()
    run_task()