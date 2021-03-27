def qsort(L):
    return (qsort([y for y in L[1:] if y < L[0]]) + 
            L[:1] + 
            qsort([y for y in L[1:] if y >= L[0]])) if len(L) > 1 else L

qsort([4, 65, 2, -31, 0, 99, 83, 782, 1])