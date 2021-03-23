def qsort(lst):
    if not lst:
        return []
    else:
        pivot = lst[0]
        less = [x for x in lst if x < pivot]
        more = [x for x in lst[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(more)

print(qsort([4, 65, 2, -31, 0, 99, 83, 782, 1]))