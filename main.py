import sys
import pygal
from algorithm import Algorithm, Point


def main():
    point_tuples = read_cities()
    alg = Algorithm(point_tuples)


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


def save_result(state, filename):
    custom_style = pygal.style.Style(
        show_legend=False,
        show_x_labels=False,
        show_y_labels=False,
        colors=('#000000',))

    chart = pygal.XY(style=custom_style)
    chart.show_legend = False
    chart.show_x_labels = False
    chart.show_y_labels = False

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