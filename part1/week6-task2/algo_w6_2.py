import copy
import math

class Heap(object):
    @staticmethod
    def __min_foo(a, b):
        return a <= b
    @staticmethod
    def __max_foo(a, b):
        return a >= b

    def __init__(self, comparison_op, size):
        self.cmp_foo = None
        if comparison_op == "min":
            self.cmp_foo = Heap.__min_foo
        elif comparison_op == "max":
            self.cmp_foo = Heap.__max_foo
        else:
            raise ValueError
        self.size = size
        self.data = [None] * size
        self.data_pos = 0

    def get_length(self):
        return self.data_pos

    # Note: Destructive operation on heap
    def self_test(self):
        heap_data = [1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 11]
        self.data = heap_data + [None, None, None, None]
        self.data_pos = len(heap_data)
        self.cmp_foo = Heap.__min_foo
        self.validate()

        # __get_parent tests
        assert self.__get_parent(1) == 0
        assert self.__get_parent(2) == 0
        assert self.__get_parent(3) == 1
        assert self.__get_parent(4) == 1
        assert self.__get_parent(5) == 2
        assert self.__get_parent(6) == 2
        assert self.__get_parent(7) == 3
        assert self.__get_parent(8) == 3

    def __get_parent(self, child_index):
        parent_pos = child_index / 2 - 1 if child_index % 2 == 0 else (child_index - 1) / 2
        if child_index == 1: parent_pos = 0 # Special case
        return parent_pos

    def validate(self):
        for i in xrange(self.data_pos - 1, 0, -1):
            assert self.data[i] is not None
            try:
                j = i
                while True:
                    if j == 0:
                        break
                    parent_pos = self.__get_parent(j)
                    assert self.data[parent_pos] is not None
                    cmp_res = self.cmp_foo(self.data[parent_pos], self.data[j])
                    if not cmp_res:
                        print("[ERROR] Comparison failed for val %s (parent, index %s) and val %s (leaf, index %s)" %
                              (self.data[parent_pos], parent_pos, self.data[j], j))
                        raise AssertionError
                    j = parent_pos
            except AssertionError as ex:
                print("[ERROR] Validation failed for j = %s" % j)
                print("[ERROR] Affected heap: %s" % self.get_data())
                raise ex

    def add(self, value):
        self.data[self.data_pos] = value
        i = self.data_pos
        parent = self.__get_parent(i)
        while True:
            if i == 0:
                break
            if self.cmp_foo(self.data[parent], self.data[i]) == False:
                # Swap
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                # print("Swapping %s and %s. Heap: %s" % (parent, i, self.get_data()))
            i = parent
            parent = self.__get_parent(i)
        self.data_pos += 1

    def add_all(self, lst):
        for item in lst:
            self.add(item)

    def get_data(self):
        return copy.copy(self.data)

    def get_top(self):
        return self.data[0]

    # Note: does not guarantee that children exist
    def get_children_indices(self, parent_index):
        assert parent_index >= 0
        return (parent_index * 2 + 1, parent_index * 2 + 2)

    def has_more(self):
        return self.data_pos > 0

    def extract_top(self):
        if self.data_pos == 0:
            raise IndexError
        extracted_val = self.data[0]
        self.data[0] = self.data[self.data_pos - 1]
        self.data[self.data_pos - 1] = None
        self.data_pos -= 1
        # print("extract_top Data = %s" % self.data)
        # Do swapping to right position
        i = 0
        while True:
            child1_index, child2_index = self.get_children_indices(i)
            if child1_index >= self.data_pos and child2_index >= self.data_pos:
                # No children
                break
            elif child1_index == self.data_pos - 1:
                # Only one child - swap if cmp
                if self.cmp_foo(self.data[i], self.data[child1_index]) == False:
                    self.data[child1_index], self.data[i] = self.data[i], self.data[child1_index]
                break
            else:
                # Two children
                if self.cmp_foo(self.data[i], self.data[child1_index]) \
                        and self.cmp_foo(self.data[i], self.data[child2_index]):
                    # Position is correct
                    break
                else:
                    # Making decision which one to choose
                    child1_val = self.data[child1_index]
                    child2_val = self.data[child2_index]
                    if self.cmp_foo(child1_val, child2_val):
                        # Swapping with first child
                        self.data[child1_index], self.data[i] = self.data[i], self.data[child1_index]
                        i = child1_index
                        # print("Swap 1: data %s" % self.data)
                    else:
                        # Swapping with second child
                        self.data[child2_index], self.data[i] = self.data[i], self.data[child2_index]
                        i = child2_index
                        # print("Swap 2: data %s" % self.data)

        return extracted_val



class Median(object):
    def __init__(self, size):
        self.large_heap = Heap("min", size / 2 + 1)
        self.small_heap = Heap("max", size / 2 + 1)
        self.not_usable = False

    def __calc_median(self):
        if self.large_heap.get_length() == self.small_heap.get_length():
            # return (self.large_heap.get_top() + self.small_heap.get_top() ) / 2.0
            return self.small_heap.get_top()
        elif self.large_heap.get_length() > self.small_heap.get_length():
            return self.large_heap.get_top()
        else:
            return self.small_heap.get_top()

    def __insert_item(self, item):
        if item > self.small_heap.get_top():
            # Put to large
            self.large_heap.add(item)
        else:
            # Put to small
            self.small_heap.add(item)
        # Balance
        if self.large_heap.get_length() >= self.small_heap.get_length() + 2:
            # Move 1 element to small heap
            self.small_heap.add(self.large_heap.extract_top())
        elif self.small_heap.get_length() >= self.large_heap.get_length() + 2:
            # Move 1 element to large heap
            self.large_heap.add(self.small_heap.extract_top())
        assert abs(self.large_heap.get_length() - self.small_heap.get_length()) <= 1


    def median(self, lst):
        if self.not_usable:
            raise Exception
        self.not_usable = True

        for item in lst:
            self.__insert_item(item)

        return self.__calc_median()

    def running_median(self, lst):
        if self.not_usable:
            raise Exception
        self.not_usable = True
        median_sum = 0
        for item in lst:
            self.__insert_item(item)
            median_sum += self.__calc_median()
        return median_sum


def run_in_code_tests():
    min_heap_test = Heap("min", 10)
    min_heap_test.self_test()
    max_heap_test = Heap("max", 10)
    max_heap_test.self_test()

    min_heap_test = Heap("min", 10)
    min_heap_test.add(1)
    min_heap_test.add(2)
    min_heap_test.add(3)
    min_heap_test.add(4)
    min_heap_test.add(5)
    min_heap_test.add(5)
    min_heap_test.add(6)
    min_heap_test.add(7)
    min_heap_test.validate()
    child1, child2 = min_heap_test.get_children_indices(0)
    assert child1 == 1
    assert child2 == 2
    child1, child2 = min_heap_test.get_children_indices(3)
    assert child1 == 7
    assert child2 == 8

    min_heap_test = Heap("min", 5)
    min_heap_test.add(3)
    min_heap_test.add(2)
    min_heap_test.add(1)
    min_heap_test.validate()
    top = min_heap_test.extract_top()
    assert top == 1
    min_heap_test.validate()
    top = min_heap_test.extract_top()
    min_heap_test.validate()


    min_heap_test = Heap("min", 20)
    lst = [1,4, 7, 5, 3, 5, 7, 4, 5, 7, 2, 3, 8, 9]
    min_heap_test.add_all(lst)
    min_heap_test.validate()
    assert min_heap_test.get_length() == len(lst)
    top = min_heap_test.extract_top()
    min_heap_test.validate()
    assert top == 1
    #
    top = min_heap_test.extract_top()
    min_heap_test.validate()
    assert top == 2
    #
    top = min_heap_test.extract_top()
    min_heap_test.validate()
    assert top == 3
    #
    top = min_heap_test.extract_top()
    min_heap_test.validate()
    assert top == 3

    median_val = Median(10).median([1,2,3,4])
    assert median_val == 2
    median_val = Median(10).median([1,2,3,4,5])
    assert median_val == 3
    median_val = Median(10).median([5,4,3,2,1])
    assert median_val == 3
    median_val = Median(10).median([8])
    assert median_val == 8

    median_val = Median(10).running_median([15])
    assert median_val == 15
    median_val = Median(10).running_median([3,5])
    assert median_val == 3 + 3
    median_val = Median(10).running_median([4,8,6])
    assert median_val == 4 + 4 + 6

    print("Tests passed")


def run_task():
    numbers = []
    file_name = "Median.txt"
    with(open(file_name, "r")) as f:
        for line in f:
            numbers.append(int(line))
    assert len(numbers) == 10000
    median_val = Median(len(numbers)).running_median(numbers)
    print("Task answer =  %s " % (median_val % 10000))

if __name__ == '__main__':
    run_in_code_tests()
    run_task()