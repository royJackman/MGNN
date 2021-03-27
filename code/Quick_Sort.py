def qsort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = qsort(less)
        more = qsort(more)
        return less + pivotList + more

qsort([4, 65, 2, -31, 0, 99, 83, 782, 1])
