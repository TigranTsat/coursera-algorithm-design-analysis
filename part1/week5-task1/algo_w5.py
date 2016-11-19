import sys


# !!! Graph indices are left as they are. Hence to access right nodes, we nee to add 1 to all operations (in python arrays start from 0)


def validate_graph(adjacency_lists):
    assert adjacency_lists[0][0] == 1
    assert len(adjacency_lists[len(adjacency_lists) - 1]) >= 1


def dijkstra_extended(adjacency_lists, s):
    x = [s]
    A = [1000000] * len(adjacency_lists)
    A[s - 1] = 0
    B = [[]] * len(adjacency_lists)
    while len(x) != len(adjacency_lists):
        min_dijkstra_score = sys.maxint
        min_next_node = None
        min_from_node = None
        for node_from in range(1, len(adjacency_lists) + 1):
            # HashMap will be better data structure for that purpose
            if node_from not in x:
                continue # Ignoring one that are not in x
            adjacency_list = adjacency_lists[node_from - 1]
            if len(adjacency_list) == 1:
                continue
            for edge_index in range(1, len(adjacency_list)):
                edge = adjacency_list[edge_index]
                assert isinstance(edge, tuple)
                to_node, score = edge
                if to_node in x:
                    continue # Ignoring paths within x
                new_length = score + A[node_from - 1]
                if new_length < min_dijkstra_score:
                    min_dijkstra_score = new_length
                    min_next_node = edge[0]
                    min_from_node = node_from

        assert min_next_node is not None
        assert min_from_node is not None
        # print("Found min_next_node = %s, min_from_node = %s with dijkstra score = %s" %
        #       (min_next_node, min_from_node, min_dijkstra_score))
        # print("A = %s" % A)
        A[min_next_node - 1] = min_dijkstra_score
        B[min_next_node - 1] = B[min_from_node - 1] + [ min_next_node ]
        x += [min_next_node]

    # print("x = %s, A = %s, B = %s" % (x, A, B))
    return (A, B)



def dijkstra(adjacency_lists, s, t):
    if s == t:
        return (0, [])
    A, B = dijkstra_extended(adjacency_lists, s)
    return (A[t - 1], B[t - 1])

def run_in_code_tests():
    graph1 = [
        [1, (2, 100), (3, 200)],
        [2],
        [3]
    ]
    validate_graph(graph1)
    (min_len,path) = dijkstra(adjacency_lists=graph1, s=1, t=2)
    # print("For graph 1: min_len=%s, path=%s" % (min_len, path))
    assert min_len == 100
    assert path == [2]

    (min_len,path) = dijkstra(adjacency_lists=graph1, s=1, t=3)
    # print("For graph 1: min_len=%s, path=%s" % (min_len, path))
    assert min_len == 200
    assert path == [3]


def run_coursera_tests():
    graph1 = [
        [1,	(2,1),	(8,2) ],
        [2,	(1,1),	(3,1) ],
        [3,	(2,1),	(4,1) ],
        [4,	(3,1),	(5,1) ],
        [5,	(4,1),	(6,1) ],
        [6,	(5,1),	(7,1) ],
        [7,	(6,1),	(8,1) ],
        [8,	(7,1),	(1,2) ]
    ]
    validate_graph(graph1)

    # (min_len,path) = dijkstra(adjacency_lists=graph1, s=1, t=6)
    # print("For graph 1: min_len=%s, path=%s" % (min_len, path))

    # !!! Indexing here starting from 1
    min_lengths = [0] * (len(graph1) + 1)
    min_paths = [None] * (len(graph1) + 1)
    for to_node in range(1, len(graph1) + 1):
        (min_len, path) = dijkstra(adjacency_lists=graph1, s=1, t=to_node)
        min_lengths[to_node] = min_len
        min_paths[to_node] = path
    print("min_lengths = %s; min_paths = %s" % (min_lengths, min_paths))
    assert min_lengths[1] == 0
    assert min_paths[1]   == []
    assert min_lengths[2] == 1
    assert min_paths[2]   == [2]
    assert min_lengths[3] == 2
    assert min_paths[3]   == [2, 3]
    assert min_lengths[4] == 3
    assert min_paths[4]   == [2, 3, 4]

    assert min_lengths[5] == 4
    assert min_paths[5]   == [2, 3, 4, 5]
    assert min_lengths[6] == 4
    assert min_paths[6]   == [8, 7, 6]
    assert min_lengths[7] == 3
    assert min_paths[7]   == [8, 7]
    assert min_lengths[8] == 2
    assert min_paths[8]   == [8]


def run_task():
    input_len = 200
    adjacency_lists = [None] * input_len
    file_path = "dijkstraData.txt"
    with(open(file_path, "r")) as f:
        for line in f:
            line = line.replace("\r\n", "")
            input_sections = line.split("\t")
            row_index = int(input_sections[0])
            adjacency_lists[row_index - 1] = [row_index]
            for edge in input_sections[1:]:
                if len(edge) < 1:
                    continue
                edge_tuple = tuple([int(x) for x in edge.split(",")])
                assert len(edge_tuple) == 2
                adjacency_lists[row_index - 1].append(edge_tuple)

    validate_graph(adjacency_lists)

    (A, B) = dijkstra_extended(adjacency_lists=adjacency_lists, s=1)
    print(A)
    reported_vertices = [int(x) for x in "7,37,59,82,99,115,133,165,188,197".split(",") ]
    # This is not correct:
    # 1875,3548,2592,3997,2970,3513,1257,3814,2340,1724
    result = [str(A[x - 1]) for x in reported_vertices]
    print("Result = %s" % result)
    print(",".join(result))




if __name__ == "__main__":
    run_in_code_tests()
    run_coursera_tests()
    run_task()