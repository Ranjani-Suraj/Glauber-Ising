import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


#so the thing is that X has every edge to begin with.
#so what would need to happen is that an edge that has been removed from X would need to be added to Y
#is that possible? its often that an edge is added to Y but not X.
# We would just need to check if said edge is also in X

#visited = set() # Set to keep track of visited nodes of graph.

# DFS algorithm
def explore(graph, start, visited=None):
    #print("start", graph, start, visited)
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
            explore(graph, next, visited)
    return visited

def dfs_stack(graph, source):
    n = len(graph)
    stack = [source]
    visited = set()
    visited.add(source)
    remaining_unvisited = set([i for i in range(len(graph))]) - visited
    while len(remaining_unvisited) > 0:
        # while stack:
        #     node = stack.pop()
        #     for nbr in graph[node]:
        #         if nbr not in visited:
        #             visited.add(nbr)
        #             stack.append(nbr)
        visited.add(explore_stack(graph, remaining_unvisited.pop()))
        remaining_unvisited = set([i for i in range(len(graph))]) - visited
        # if len(remaining_unvisited) > 0:
        #     stack = [remaining_unvisited.pop()]
    return visited

def explore_stack(graph, start):
    stack = [start]
    visited = set()
    visited.add(start)
    # print(graph)
    while stack:
        v = stack.pop()
        #print(v, graph[v])
        for u in graph[v]:
            if u not in visited:
               # print(u)
                visited.add(u)
                stack.append(u)
            if len(visited) == len(graph):
                stack = []
                break

    return visited


def dfs(graph, start = 0):
    visited = list()
    v = list()
    for start in range(len(graph)):

        if start in v:
            #print("found")
            start+=1
            continue
        new_visited = explore(graph, start)
        visited.append(new_visited)
        v+=new_visited

    #print(v)
    #print("visited", visited)
    return visited

def glauber_q(graph1, graph2, p, q, t = 0):
    rows = columns = len(graph1)
    edges1 = ((rows * columns) - rows) / 2
    edges2 = 0
    # adjacent1, adjacent2 = [], []
    # for i in range(rows):
    #     adjacent1.append([])
    #     adjacent2.append([])
    #     for j in range(columns):
    #         #if adjacent1[i][j] == 1:
    #         if i!=j:
    #             adjacent1[i].append(1)
    #             #G1.add_edge(i,j)
    #         else:
    #             adjacent1[i].append((0))
    #         #adjacent2[i].append(0)

    #print(edges1, edges2)
    #p = 0.1/rows
    #q = 2
    pi = p/(p+q*(1-p))
    t = 0
    ans1 = [range(rows)]
    ans2 = [[i] for i in range(rows)]

    while edges1!=edges2:
        #print("current ans1: ", ans1)
        #print("current ans2: ", ans2)
        #print(list(nx.generate_adjlist(G1)))
        #print("===========================================================================================")
        t+=1
        r = np.random.random()
        #print(r, pi, p)
        edge = [np.random.randint(0, rows), np.random.randint(0, rows)] #randomly choose an edge
        #print(edge)
        if edge[0] == edge[1]:
            t-=1
            continue

        cut_edge1 = True
        cut_edge2 = True


        #you need to find a way to split the connected component into the 2 parts it would become.
        #instead of calculating dfs every time just check the cut edge and seperate into 2 components:
        # if we are adding a cut edge, combine the ccs.
        # if we remove a cut edge then just split the cc

        # pretend uv is not in the graph
        # run explore from u to v.
        # if there is not a path then its a cut edge.

        g1rem = False
        g2rem = False

        #i can just check in that single cc
        # in that case, i could have a global var with all of the ccs, see which one it is in, and update accordingly?
        # if it is not a cut edge, then i dont need to change it, if it is, i remove it and al 2 new ones
        #this assumes that the edge is in a cc already
        #if it is not then ofc its not a cut edge
        #subgraph1, subgraph2 = list(), list()

        # if the edge exists, they must be in the same cc
        if edge[1] in graph1[edge[0]]:
            graph1[edge[0]].remove(edge[1])
            graph1[edge[1]].remove(edge[0])
            g1rem = True

        if edge[1] in graph2[edge[0]]:
            graph2[edge[0]].remove(edge[1])
            graph2[edge[1]].remove(edge[0])
            g2rem = True

        u_cc1 = (list(explore_stack(graph1, edge[0])))
        v_cc1 = (list(explore_stack(graph1, edge[1])))

        if edge[0] in u_cc1 and edge[1] in u_cc1:
            cut_edge1 = False

        #this splits them into 2 ccs
        u_cc2 = (list(explore(graph2, edge[0])))
        v_cc2 = (list(explore(graph2, edge[1])))

        if edge[0] in u_cc2 and edge[1] in u_cc2:
            cut_edge2 = False


        #if they were originally in the graph, we add them back

        if g2rem:
            graph2[edge[0]].add(edge[1])
            graph2[edge[1]].add(edge[0])

        if g1rem:
            graph1[edge[0]].add(edge[1])
            graph1[edge[1]].add(edge[0])


        # print("sccs2:", ans2)
        # for i in range(len(ans2)):
        #     scc2 = ans2[i]
        #
        #     if edge[0] in scc2 and edge[1] in scc2:
        #             cut_edge2 = True

        same_cc1, same_cc2 = False, False
        for cc in ans1:
            if edge[0] in cc and edge[1] in cc:
                same_cc1 = True
                ans1.remove(cc)

        for cc in ans2:
            if edge[0] in cc and edge[1] in cc:
                same_cc2 = True
                ans2.remove(cc)

        #if its not in the same cc, then we merge the ccs theyre from when adding, and do nothing when removing
        #if they ARE in the same cc, then when adding we do nothing, and we split the cc when removing
        if(cut_edge1):
            if r <= pi:

                if edge[1] not in graph1[edge[0]]: #for it to be a cut edge it would need to be in the graph
                    edges1 += 1
                    #print("add,", edge, "to graph1")
                    graph1[edge[0]].add(edge[1])
                    graph1[edge[1]].add(edge[0])

                    # it IS a cut edge so we have the 2 sets that would be created if they were seperated, so we just join them
                if same_cc1:  # if they are in the same cc we dont need to do anything
                    ans1.append(v_cc1 + u_cc1)  # basically we didnt need to change anything
                else:
                        # we remove the 2 individual ccs that they started in, and merge them
                    for cc in ans1:
                        if edge[0] in cc or edge[1] in cc:
                            ans1.remove(cc)

                    ans1.append(v_cc1 + u_cc1)

            else:
                if edge[1] in graph1[edge[0]]:
                    graph1[edge[1]].remove(edge[0])
                    graph1[edge[0]].remove(edge[1])
                    edges1 -= 1
                #we are removing the edge, so we add u and v to seperate ccs.

                if same_cc1:  # if they are in the same cc, then we add them seperately
                    ans1.append(u_cc1)
                    ans1.append(v_cc1)
                    #if they are not in the same cc, we dont need to do anything

                    #print("remove,", edge, "to graph1 ------------//////////////")
        elif r <= p:
            # adjacent1[edge[0]].append(edge[1])
            # adjacent1[edge[1]].append(edge[0])
            if edge[1] not in graph1[edge[0]]:
                edges1 += 1
                #print("add,", edge, "to graph1 r")
                graph1[edge[0]].add(edge[1])
                graph1[edge[1]].add(edge[0])
            #it is not a cut edge, so we just need to add u_cc1
            if same_cc1:
                    ans1.append(u_cc1)
            else: #we merge them if they are not in the same cc
                    for cc in ans1:
                        if edge[0] in cc or edge[1] in cc:
                            ans1.remove(cc)

                    ans1.append(v_cc1 + u_cc1)

        else:   # we are removing it, so
            if edge[1] in graph1[edge[0]]:
                graph1[edge[1]].remove(edge[0])
                graph1[edge[0]].remove(edge[1])
                edges1 -= 1

            #we are removing it, but it is not a cut edge, so both their ccs are the same anywyas
            if same_cc1:
                ans1.append(u_cc1)
            # if we are removing it but theyre not in the same cc,
            # then we know theres no edge  bw them, so no need to do anything
                #print("remove,", edge, "to graph1 ---------///////////////////")


        if (cut_edge2):
            if r <= pi:
                # adjacent2[edge[0]].append(edge[1])
                # adjacent2[edge[1]].append(edge[0])
                if edge[1] not in graph2[edge[0]]:
                    edges2 += 1
                    #print("add,", edge, "to graph2")
                graph2[edge[0]].add(edge[1])
                graph2[edge[1]].add(edge[0])
                #we are adding it, and it is a cut edge

                if same_cc2:  # if they are in the same cc we dont need to do anything
                    ans2.append(v_cc2 + u_cc2)  # basically we didnt need to change anything
                else: #idk if this will ever tick since we only consider it to be a cut edge if it exists in the graph alr
                    # we remove the 2 individual ccs that they started in, and merge them
                    for cc in ans2:
                        if edge[0] in cc or edge[1] in cc:
                            ans2.remove(cc)

                    ans2.append(((v_cc2) + (u_cc2)))

            else:
                if edge[1] in graph2[edge[0]]:
                    graph2[edge[1]].remove(edge[0])
                    graph2[edge[0]].remove(edge[1])
                    edges2 -= 1
                    #if is a cut edge, but we are removing it, we add u and v to seperate ccs
                    #if it is a cut edge it means it WAS in the graph
                if same_cc2:  # if they are in the same cc, then we add them seperately
                        ans2.append(u_cc2)
                        ans2.append(v_cc2)
                    # if they are not in the same cc, we dont need to do anything`

                    #print("remove,", edge, "to graph2 ---------///////////////////")
        elif r <= p:
            # adjacent2[edge[0]].append(edge[1])
            # adjacent2[edge[1]].append(edge[0])
            if edge[1] not in graph2[edge[0]]:
                edges2 += 1
                #print("add,", edge, "to graph2 r")
                graph2[edge[0]].add(edge[1])
                graph2[edge[1]].add(edge[0])
                #it is not a cut edge so even adding the edge will still have the same cc
            if same_cc2:
                    ans2.append(u_cc2)
            else:  # we merge them if they are not in the same cc
                    for cc in ans2:
                        if edge[0] in cc or edge[1] in cc:
                            ans2.remove(cc)

                    ans2.append(v_cc2 + u_cc2)

        else:
            if edge[1] in graph2[edge[0]]:
                graph2[edge[1]].remove(edge[0])
                graph2[edge[0]].remove(edge[1])
                edges2 -= 1
                #print("remove,", edge, "to graph2 ---------///////////////////")
                #it is not a cut edge and we are removing it, so nothing changes
                #this assumes that they were in the same cc to begin with. if they werent its ofc not a cut_edge? ugh
                # we are removing it, but it is not a cut edge, so both their ccs are the same anywyas
            if same_cc2:
                    ans2.append(u_cc2)
                # if we are removing it but theyre not in the same cc,
                # then we know theres no edge  bw them, so no need to do anything
        #print(edges1, edges2, "+++++++++++++++++++++++++++===================================================================+++")
        #print("edges1: ", edges1, "edges2: ", edges2)

    max_size = 0
    for scc in ans1:
        if len(scc) > max_size:
            max_size = len(scc)
            print(scc)
    print(graph1, graph2)
    print(ans1)
    print(ans2)
    print(max_size)
    return max_size, t





#
# def glauber(graph1, graph2, p, t = 0):
#     rows = columns = len(graph1)
#     edges1 = ((rows * columns) - rows) / 2
#     edges2 = 0
#     adjacent1, adjacent2 = [], []
#     for i in range(rows):
#         adjacent1.append([])
#         adjacent2.append([])
#         for j in range(columns):
#             # if adjacent1[i][j] == 1:
#             if i != j:
#                 adjacent1[i].append(1)
#                 # G1.add_edge(i,j)
#             else:
#                 adjacent1[i].append((0))
#             # adjacent2[i].append(0)
#
#     print(edges1, edges2)
#     # p = 0.1/rows
#     # q = 2
#     #pi = p / (p + q * (1 - p))
#     t = 0
#     # ans1 = [range(rows)]
#     # ans2 = []
#     while edges1 != edges2:
#         # print(list(nx.generate_adjlist(G1)))
#         print("===========================================================================================")
#         t += 1
#         r = np.random.random()
#         print(r, p)
#         edge = [np.random.randint(0, rows),
#                 np.random.randint(0, rows)]  # round(np.random.random()*len(G1))  #randomly choose an edge
#         print(edge)
#         if edge[0] == edge[1]:
#             t -= 1
#             continue
#         cut_edge1 = False
#         cut_edge2 = False
#
#         ans1 = list(dfs(graph1, 0))
#         ans2 = list(dfs(graph2, 0))
#
#         print("sccs1: ", ans1)
#         for i in range(len(ans1)):
#             scc1 = ans1[i]
#
#             if edge[0] in scc1 and edge[1] in scc1:
#                 cut_edge1 = True
#
#         print("sccs2:", ans2)
#         for i in range(len(ans2)):
#             scc2 = ans2[i]
#
#             if edge[0] in scc2 and edge[1] in scc2:
#                 cut_edge2 = True
#
#         #graph1
#         if r < p:
#             adjacent1[edge[0]].append(edge[1])
#             adjacent1[edge[1]].append(edge[0])
#             if edge[1] not in graph1[edge[0]]:
#                 edges1 += 1
#                 print("add,", edge, "to graph1 r", cut_edge1)
#             graph1[edge[0]].add(edge[1])
#             graph1[edge[1]].add(edge[0])
#         else:
#             if edge[1] in graph1[edge[0]]:
#                 graph1[edge[1]].remove(edge[0])
#                 graph1[edge[0]].remove(edge[1])
#                 edges1 -= 1
#                 print("remove,", edge, "to graph1 ---------///////////////////", cut_edge1)
#         #graph2
#         if r < p:
#             adjacent2[edge[0]].append(edge[1])
#             adjacent2[edge[1]].append(edge[0])
#             if edge[1] not in graph2[edge[0]]:
#                 edges2 += 1
#                 print("add,", edge, "to graph2 r", cut_edge2)
#             graph2[edge[0]].add(edge[1])
#             graph2[edge[1]].add(edge[0])
#         else:
#             if edge[1] in graph2[edge[0]]:
#                 graph2[edge[1]].remove(edge[0])
#                 graph2[edge[0]].remove(edge[1])
#                 edges2 -= 1
#                 print("remove,", edge, "to graph2 ---------///////////////////", cut_edge2)
#
#         print(edges1, edges2,
#               "+++++++++++++++++++++++++++===================================================================+++")
#
#     max_size = 1
#     for scc in ans1:
#         if len(scc) > max_size:
#             max_size = len(scc)
#     print(max_size)
#     return t

        #if r is a cut edge

#print(glauber(graph1, graph2, 0.1/rows))

#remove networkx, just work with matrix
#change the stopping condition to check unmber of edges
#read coupling textbook
