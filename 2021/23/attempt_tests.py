from attempt import dist, heuristic_distance

start_pos, depth = 'DDCABCDDABBACABC...........', 4
end_pos = ''.join([e*depth for e in 'ABCD']) + 11*'.'
print(start_pos, depth)
# start_pos = end_pos

# print(heuristic_distance())


def test_dist():
    assert(dist(4, 0, 1) == 1)
    assert(dist(4, 0, 26) == 12)
    assert(dist(4, 0, 5) == 9)
    assert(dist(4, 16, 26) == 10)
    assert(dist(4, 16, 10) == 8)

def test_heuristic_distance():
    assert(heuristic_distance('AAAABBBBCCCCDDD..........D.', 4) == 2000)
    assert(heuristic_distance('AAABBBB.CCCCDDD.A........D.', 4) == 2043)

