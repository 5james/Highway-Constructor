import sys
import argparse
import random


def generate(n, m):
    if m * m < 5 * n:
        raise ValueError('Too many points to generate.')
    points = set()
    for i in range(0, n):
        while True:
            x = random.randint(0, m - 1)
            y = random.randint(0, m - 1)

            if (x, y) not in points:
                break
        points.add((x, y))

    return list(points)


def main(argv):
    parser = argparse.ArgumentParser(description='Program generating unique points.')
    parser.add_argument('-n', metavar='N', required=True, type=int, help='Generate N points.')
    parser.add_argument('-m', metavar='M', required=False, type=int, help='Specify maximum value of x or y coordinate.')

    args = parser.parse_args()

    if args.n < 2:
        print('Minimal number of points is 2.')

    n = args.n

    if args.m:
        if args.m * args.m < 5 * n:
            print('M too low.')
        m = args.m
    else:
        m = 10 * n

    points = generate(n, m)

    for point in points:
        print(str(point[0]) + ',' + str(point[1]))

if __name__ == '__main__':
    main(sys.argv)
