a = ((1, 1, 1, 1), (2, 4, 8, 16), (3, 9, 27, 81), (4, 16, 64, 256))

b = (
    (4, -3, 4 / 3.0, -1 / 4.0),
    (-13 / 3.0, 19 / 4.0, -7 / 3.0, 11 / 24.0),
    (3 / 2.0, -2.0, 7 / 6.0, -1 / 4.0),
    (-1 / 6.0, 1 / 4.0, -1 / 6.0, 1 / 24.0),
)


def MatrixMul(A, B):
    return [
        [sum(x * B[i][col] for i, x in enumerate(row)) 
        for col in range(len(B[0]))]
        for row in A]


v = MatrixMul(a, b)
