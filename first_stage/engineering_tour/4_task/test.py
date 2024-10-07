list1= [38.0, 38.0, 130.0, 130.0]
list2 = [7.5, 8.5, 31.0, 34.0]


relations = [x / y for x, y in zip(list1, list2)]
print(relations)

average_relation = sum(relations) / len(relations)
print(average_relation)

if all(abs(r - average_relation) < 0.2 for r in relations):
    print(True)