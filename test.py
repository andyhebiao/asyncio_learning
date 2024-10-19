# -*- utf-8 -*-
# @Time:  2024/10/12 16:58
# @Autor: Andy Ye
# @File:  test.py



value = list(range(100))
print(value)
s = sum(value)
average = s / len(value)
print(s, average)

#  编写一个冒泡法排序算法
def bubble_sort(list_data):
    for i in range(len(list_data) - 1):
        for j in range(len(list_data) - 1 - i):
            if list_data[j] > list_data[j + 1]:
                list_data[j], list_data[j + 1] = list_data[j + 1], list_data[j]
    return list_data
