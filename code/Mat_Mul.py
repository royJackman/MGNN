a = ((1, 1, 1, 1), (2, 4, 8, 16), (3, 9, 27, 81), (4, 16, 64, 256))

b = (
    (4, -3, 4 / 3.0, -1 / 4.0),
    (-13 / 3.0, 19 / 4.0, -7 / 3.0, 11 / 24.0),
    (3 / 2.0, -2.0, 7 / 6.0, -1 / 4.0),
    (-1 / 6.0, 1 / 4.0, -1 / 6.0, 1 / 24.0),
)


def MatrixMul(A, B):
    tpos_b = zip(*B)
    rtn = [[sum(ea * eb for ea, eb in zip(a, b)) for b in tpos_b] for a in A]
    return rtn


v = MatrixMul(a, b)
