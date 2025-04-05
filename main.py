# This is a sample Python script.
import random
import time

#for 1000 nodes 1/1000 is was maxsize was 7??? damn
#25 for 2/rows
import time

import matplotlib
from matplotlib import pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import plot_glauber

import numpy as np

#G1 = nx.DiGraph()
#G2 = nx.DiGraph()
rows, columns = 1000, 1000

adjacent1 = []
graph1 = dict()
graph2 = dict()
adjacent2 = []
#edges1, edges2 = 3, 0
for i in range(rows):
    adjacent1.append([])
    adjacent2.append([])
    graph2[i] = set()
    graph1[i] = set()
    for j in range(columns):
        #if adjacent1[i][j] == 1:
        if i!=j:
            adjacent1[i].append(1)
            graph1[i].add(j)
            #G1.add_edge(i,j)
        else:
            adjacent1[i].append((0))
        #adjacent2[i].append(0)

        # if adjacent2[i][j] == 1:
        #     G2.add_edge(i, j)

print(graph1)
start = time.time()
max_size, t = plot_glauber.glauber_q(graph1.copy(), graph2.copy(), 2.1/rows, 3)
end = time.time()
print("component", max_size, "]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]"
                                              "]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
print(max_size)
print("time:", end-start)
num = 1
# largest_component = {0.7: [7, 4, 4, 5, 7, 5, 6, 4, 4, 4, 7, 5, 5, 6],
#                      1.3: [6, 7, 5, 7, 6, 9, 9, 10, 9, 8, 11, 17, 9, 4, 22, 11],
#                      1.1: [8, 10, 7, 6, 3, 7, 12], 1: [3, 5, 7, 13, 5, 10, 4, 4, 6, 7, 9],
#                      0.6: [4, 3, 5, 6, 4, 3, 3, 6, 3, 3, 5, 3, 4, 4],
#                      1.2: [8, 10, 9, 9, 6, 6, 5, 4, 9, 9, 5, 10, 6],
#                      0.8: [7, 4, 4, 5, 7, 4, 4, 7, 9],
#                      1.4: [10, 10, 9, 6, 15, 8],
#                      0.9: [10, 14, 4, 6, 4, 3, 12, 6, 8, 5]}
# largest_component = dict()
# choices = [0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3]
# for i in range(100):
#     num = random.randint(0, len(choices)-1)
#     num = choices[num]
#     if num not in largest_component.keys():
#         largest_component[num] = []
#     max_size, t = plot_glauber.glauber_q(graph1.copy(), graph2.copy(), num/rows, 2)
#     print("num:", num, "component ", max_size, "time ", t)
#     largest_component[num].append(max_size)
#     print(largest_component)
#
#     adjacent1 = []
#     graph1 = dict()
#     graph2 = dict()
#     adjacent2 = []
#     # edges1, edges2 = 3, 0
#     for i in range(rows):
#         adjacent1.append([])
#         adjacent2.append([])
#         graph2[i] = set()
#         graph1[i] = set()
#         for j in range(columns):
#             # if adjacent1[i][j] == 1:
#             if i != j:
#                 adjacent1[i].append(1)
#                 graph1[i].add(j)
#                 # G1.add_edge(i,j)
#             else:
#                 adjacent1[i].append((0))
#
# print(largest_component)
# avgs = dict()
# for x in largest_component.keys():
#     print(x)
#     avgs[x] = 0
#     for y in largest_component[x]:
#         print(x, y)
#         avgs[x]+=y
#         plt.scatter(x, y)
#     avgs[x]/=len(largest_component[x])
#
# plt.show()
#
# plt.bar(largest_component.keys(), avgs.values())
#
# plt.show()
# #
# print(graph1)
# print(graph2)
