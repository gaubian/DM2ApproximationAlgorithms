# Auxiliary function for bipartite matching.
def augment(u, A, visit, match):
    for v in A[u]:
        if not visit[v]:
            visit[v] = True
            if match[v] is None or augment(match[v], A, visit, match):
                match[v] = u
                return True
    return False

# Takes as input a bipartite graph, and returns a matching.
def bipartite_matching(A):
    nU, nV = len(A), 0
    for adjlist in A:
        for v in adjlist:
            if v + 1 > nV:
                nV = v + 1
    match, ans = [None] * nV, [None] * nU
    for u in range(nU):
        augment(u, A, [False] * nV, match)
    for v in range(nV):
        if match[v] is not None:
            ans[match[v]] = v
    return ans

# Takes as input a bipartite graph and two integers a < b such that there
# exists an assignment with its makespan in ]a,b], and returns an
# assignment of minimal makespan at least a.
def exists_assignment(A, a, b):
    mid = (1 + a + b) // 2
    new_A = []
    for line in A:
        new_line = []
        for x in line:
            for i in range(mid):
                new_line.append(mid * x + i)
        new_A.append(new_line)
    matching = bipartite_matching(new_A)
    if b == a+1:
        return matching
    if None in matching:
        return exists_assignment(A, mid, b)
    else:
        return exists_assignment(A, a, mid)

# Given jobs and their weights, extract only those of a certain weight.
def extract_weight(A, w, weight_to_extract):
    new_A = []
    corr_id = []
    for i in range(len(A)):
        if w[i] == weight_to_extract:
            new_A.append(A[i])
            corr_id.append(i)
    return new_A, corr_id

# Given which machines can execute which jobs, and jobs' weights, returns an assignment which is a 2-approximation of the optimal.
def solve(A, w):
    assignment = len(A) * [-1]
    for weight in [1, 2]:
        new_A, corr_id = extract_weight(A, w, weight)
        partial_assign = exists_assignment(new_A, 0, len(new_A))
        for i in range(len(new_A)):
            assignment[corr_id[i]] = partial_assign[i]
    return assignment

def example():
    print(solve([[0,1],[0,1],[0,1]],[1,1,2]))

example()
