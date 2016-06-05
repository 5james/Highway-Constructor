import argparse
import sys
import pygal
import time
from algorithm import Algorithm, Point, State


def main():
    parser = argparse.ArgumentParser(description='Highway builder.')
    parser.add_argument('-a', required=True, type=int, help='Roads length factor.')
    parser.add_argument('-b', required=True, type=int, help='Path length factor.')
    parser.add_argument('-i', default=20, type=int, help='Number of iterations.')

    args = parser.parse_args()

    if args.a < 0:
        print('Roads length factor should be greater or equal 0.')
        exit()

    if args.b < 0:
        print('Path length factor should be greater or equal 0.')
        exit()

    if args.i < 1:
        print('Number of iterations should be greater than 0.')

    point_tuples = read_cities()
    alg = Algorithm(point_tuples, roads_length_factor=args.a, paths_length_factor=args.b, iterations=args.i)

    iters_ended = alg.simulated_annealing()

    fitness = alg.fitness_function(alg.state)
    file_name = "result"
    millis = int(round(time.time() * 1000))
    file_name += str(millis)
    header = str(fitness) \
             + "\na = " + str(alg.roads_length_factor) \
             + "\nb = " + str(alg.paths_length_factor) \
             + "\niterations = " + str(alg.iterations) \
             + "\nended after = " + str(iters_ended) \
             + "\nsame_state = " + str(alg.max_same_state_iterations) \
             + "\n" + str(point_tuples)
    save_result(alg.state, header, file_name)


def read_cities():
    mynumbers = []
    point_tuples = []
    for line in sys.stdin:
        new_list = [int(elem) for elem in line.split(',')]
        mynumbers = mynumbers + new_list
    if len(mynumbers) % 2 == 1:
        print(mynumbers)
        print(len(mynumbers))
        print('Invalid input')
        sys.exit(-1)
    else:
        for i in range(0, len(mynumbers), 2):
            x = mynumbers[i]
            y = mynumbers[i+1]
            point_tuples.append((x, y))
    return point_tuples


def save_result(state, fitness, filename):
    custom_style = pygal.style.Style(
        show_legend=False,
        colors=('#000000',))

    chart = pygal.XY(title=str(fitness), style=custom_style)

    # Disable autoscaling
    max_x = max(point.x for point in state.points)
    max_y = max(point.y for point in state.points)

    chart_length = max_x if max_x > max_y else max_y

    labels = [int(chart_length / 9 * i) for i in range(0, 10)]
    chart.x_labels = labels
    chart.y_labels = labels

    for edge in state.edges:
        chart.add('', [
            {
                'value': (edge[0].x, edge[0].y),
                'node': {'r': 4 if edge[0].type == Point.TYPE_TOWN else 2}
            },
            {
                'value': (edge[1].x, edge[1].y),
                'node': {'r': 4 if edge[1].type == Point.TYPE_TOWN else 2}
            }])

    chart.render_to_file(filename)


if __name__ == "__main__":
    main()
