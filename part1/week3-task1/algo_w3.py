import copy
import sys
from random import randint

# Counting starts with 1 (!!!)


def _contract_graph_by_edge(adjacency_lists, edge):
    (edge_start, edge_end) = edge
    assert adjacency_lists[edge_start - 1] is not None
    assert adjacency_lists[edge_end - 1] is not None
    assert edge_start == adjacency_lists[edge_start - 1][0]
    assert edge_end == adjacency_lists[edge_end - 1][0]
    # edge_end will be removed and all references updated to edge_start
    for vertex_to in adjacency_lists[edge_end - 1][1:]:
        # print("Processing vertex: %s from %s" % (vertex_to, adjacency_lists[edge_end - 1]))
        if vertex_to == edge_start:
            # Just remove vertex_to from edge_start adjacency list to avoid loop
            adjacency_lists[edge_start - 1].remove(edge_end)
        elif vertex_to == edge_end:
            # This is loop to itself, should not be the case, since loops are removed prior to this
            raise Exception
        else:
            adjacency_lists[vertex_to - 1].append(edge_start)
            adjacency_lists[edge_start - 1].append(vertex_to)
            # print("Removing %s from %s" % (edge_end, adjacency_lists[vertex_to - 1]))
            adjacency_lists[vertex_to - 1].remove(edge_end)
    adjacency_lists[edge_end - 1] = None
    validate_graph(adjacency_lists)


def _graph_to_str(adjacency_lists):
    graph_str = "["
    for adjacency_list in adjacency_lists:
        graph_str += ( str(adjacency_list) + "\n")
    return graph_str + "]"


def find_rand_contraction_length(adjacency_lists):
    def get_rand_vertex():
        while True:
            rand_vertex = randint(0, len(adjacency_lists) - 1)
            if adjacency_lists[rand_vertex] is None:
                continue
            else:
                return rand_vertex + 1

    def get_live_vertices():
        return [ x for x in adjacency_lists if x is not None]

    while True:
        rand_vertex_start = get_rand_vertex()
        rand_vertex_end_index = randint(1, len(adjacency_lists[rand_vertex_start - 1]) - 1)
        rand_vertex_end = adjacency_lists[rand_vertex_start - 1][rand_vertex_end_index]
        #print("Selected  %s and %s for contraction. live %s :" % (rand_vertex_start, rand_vertex_end, len(get_live_vertices())))
        _contract_graph_by_edge(adjacency_lists, (rand_vertex_start, rand_vertex_end))
        l_vert = get_live_vertices()
        if len(l_vert) == 2:
            assert len(l_vert[0]) == len(l_vert[1])
            return len(l_vert[0]) - 1

def find_min_contraction_length(adjacency_lists):
    min_contraction = sys.maxint
    for i in xrange(0, len(adjacency_lists)):
        adjacency_lists_cp = copy.deepcopy(adjacency_lists)
        min_try = find_rand_contraction_length(adjacency_lists_cp)
        print("Found possible contraction of %s. Iteration %s" % (min_try, i))
        if min_try < min_contraction:
            min_contraction = min_try
    return min_contraction

def validate_graph(adjacency_lists):
    try:
        if len(adjacency_lists) == 0:
            return
        list_of_vertices = []
        for vertex_descr in adjacency_lists:
            if vertex_descr is None:
                continue
            list_of_vertices.append(vertex_descr[0])
        # Checking no duplicates and vertices numbers starts from 1
        sorted_vertices = sorted(list_of_vertices)
        assert len(list_of_vertices) == len(sorted_vertices)
        assert sorted_vertices[0] >= 1
        # Checking all edges are correct
        for adjacency_list in adjacency_lists:
            if adjacency_list is None:
                continue
            for vertex in adjacency_list[1:]:
                assert vertex in list_of_vertices, "Vertex not found"
                assert adjacency_list[0] in adjacency_lists[vertex - 1][1:], "Joint edge not found"
    except AssertionError as ex:
        print("Graph validation failure: %s" % _graph_to_str(adjacency_lists))
        raise ex


def run_in_code_tests():
    # Test 1
    adjacency_lists = [
        None,
        None,
        [1]
    ]
    validate_graph(adjacency_lists)


    # Test 2
    adjacency_lists = [
        [1, 3],
        None,
        [3, 1, 4],
        [4, 3]
    ]
    # ( 1 -> 3; 3 -> 1 ), (3 -> 4, 4 -> 3):
    #  (1 <----> 3 <-----> 4)
    validate_graph(adjacency_lists)
    # Contract using element 3
    _contract_graph_by_edge(adjacency_lists, (1, 3))
    #  (1 <----> 4)
    assert len(adjacency_lists) == 4
    assert adjacency_lists[0] == [1, 4]
    assert adjacency_lists[1] is None
    assert adjacency_lists[2] is None
    assert adjacency_lists[3] == [4, 1]


    # Test 3
    #     (1) <--------> (2)
    #      |         //// |
    #      |     ////     |
    #      | ////         |
    #     (3) <--------> (4)
    #
    adjacency_lists_base = [
        [1, 2, 3],
        [2, 1, 3, 4],
        [3, 1, 2, 4],
        [4, 2, 3]
    ]
    adjacency_lists = copy.deepcopy(adjacency_lists_base)
    validate_graph(adjacency_lists)
    _contract_graph_by_edge(adjacency_lists, (3, 1))
    #print(_graph_to_str(adjacency_lists))
    #            //      //(2)
    #          //     ///   |
    #        //   ///       |
    #       (3) <--------> (4)
    assert adjacency_lists[0] is None
    assert adjacency_lists[1] == [2, 3, 4, 3]
    assert adjacency_lists[2] == [3, 2, 4, 2]
    assert adjacency_lists[3] == [4, 2, 3]
    _contract_graph_by_edge(adjacency_lists, (3, 2))
    assert adjacency_lists[0] is None
    assert adjacency_lists[1] is None
    assert adjacency_lists[2] == [3, 4, 4]
    assert adjacency_lists[3] == [4, 3, 3]


    adjacency_lists = copy.deepcopy(adjacency_lists_base)
    validate_graph(adjacency_lists)
    _contract_graph_by_edge(adjacency_lists, (3, 2))

    adjacency_lists = copy.deepcopy(adjacency_lists_base)
    assert find_rand_contraction_length(adjacency_lists) >= 2


def run_coursera_tests():
    adjacency_lists = [
        [1, 2, 3, 4, 7],
        [2, 1, 3, 4],
        [3, 1, 2, 4],
        [4, 1, 2, 3, 5],
        [5, 4, 6, 7, 8],
        [6, 5, 7, 8],
        [7, 1, 5, 6, 8],
        [8, 5, 6, 7]
    ]
    min_count = find_min_contraction_length(adjacency_lists)
    assert min_count == 2


def run_task():
    adjacency_lists = []
    file_path = "kargerMinCut.txt"
    with(open(file_path, "r")) as f:
        for line in f:
            values = [ x for x in line.split("\t") if x.isdigit() ]
            adjacency_lists.append([ int(x) for x in values ])
    assert len(adjacency_lists) == 200
    # print(_graph_to_str(adjacency_lists))
    validate_graph(adjacency_lists)
    min_count = find_min_contraction_length(adjacency_lists)
    print("Found min count = %s" % min_count)

if __name__ == "__main__":
    run_in_code_tests()
    run_coursera_tests()
    run_task()
