import sys
import pygal
from algorithm import Algorithm, Point, State


def main():
    point_tuples = read_cities()
    alg = Algorithm(point_tuples)
    #
    # point_tuples = ((0, 0), (1, 1))
    # alg = Algorithm(point_tuples)
    # alg.roads_length_factor = 0
    # alg.paths_length_factor = 1
    # alg.temperature = 100
    # alg.iterations = 400
    #
    # points = [Point(3, 0), Point(0, 2), Point(0, 5), Point(3, 7), Point(6, 5), Point(6, 2)]
    # edges = [(points[0], points[1]), (points[1], points[2]), (points[2], points[3]), (points[3], points[4]),
    #          (points[4], points[5]), (points[5], points[0])]
    #
    # alg.state = State(edges)
    # alg.simulated_annealing()

    fitness = alg.fitness_function(alg.state)
    save_result(alg.state, fitness, 'results')


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
