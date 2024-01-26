from matplotlib import pyplot as plt
from GraphAnalyzer import GraphAnalyzer, ErdosRenyiGraphGenerator, AverageDegreeCalculator
from CommonFunctions import make_directories, check_if_file_exists
import os


if __name__ == '__main__':
    N = 1000
    deg = 30
    calculator = AverageDegreeCalculator(N=N, degree_to_get=deg)

    image_path = 'images'
    make_directories([image_path])

    L = calculator.parameter_from_er_degree()
    p = calculator.parameter_from_erg_degree()
    k = calculator.parameter_from_ws_degree()
    beta = 0.3

    # ER model
    er_graph = GraphAnalyzer('ER', (N, L))
    er_graph.graph_degree_list()
    er_graph.average_degree_and_histogram()
    # er_graph.calculate_graph_diameter_nx()
    # er_graph.calculate_average_shortest_path_nx()
    er_graph.calculate_path_histogram()
    er_graph.calculate_diameter_from_histogram()
    er_graph.calculate_average_path_from_histogram()

    # ERG model
    generator = ErdosRenyiGraphGenerator(p=p, N=N)
    generator.generate_all_graph_data()
    generated_graph = generator.get_generated_graph()

    erg_graph = GraphAnalyzer('ERG', (N, p),
                              initial_graph=generated_graph)
    erg_graph.graph_degree_list()
    erg_graph.average_degree_and_histogram()
    # erg_graph.calculate_graph_diameter_nx()
    # erg_graph.calculate_average_shortest_path_nx()
    erg_graph.calculate_path_histogram()
    erg_graph.calculate_diameter_from_histogram()
    erg_graph.calculate_average_path_from_histogram()

    # WS model
    ws_graph = GraphAnalyzer('WS', (N, k, beta))
    ws_graph.graph_degree_list()
    ws_graph.average_degree_and_histogram()
    # ws_graph.calculate_graph_diameter_nx()
    # ws_graph.calculate_average_shortest_path_nx()
    ws_graph.calculate_path_histogram()
    ws_graph.calculate_diameter_from_histogram()
    ws_graph.calculate_average_path_from_histogram()

    print(er_graph.path_histogram)
    print(erg_graph.path_histogram)
    print(ws_graph.path_histogram)

    # creating plots
    figure, axis = plt.subplots(3, 1, layout='constrained', figsize=(6, 9))
    colors = ['maroon', 'green', 'blue']
    er_title = f'{er_graph.graph_type} model. N = {N}, L = {L}.\n' \
               f'diameter = {er_graph.diameter}, average path length = {er_graph.average_path}'
    erg_title = f'{erg_graph.graph_type} model. N = {N}, p = {p}.\n' \
                f'diameter = {erg_graph.diameter}, average path length = {erg_graph.average_path}'
    ws_title = f'{ws_graph.graph_type} model. N = {N}, k = {k}, beta = {beta}.\n' \
               f'diameter = {ws_graph.diameter}, average path length = {ws_graph.average_path}'
    title_list = [er_title, erg_title, ws_title]
    for graph, index in zip([er_graph, erg_graph, ws_graph], range(3)):
        x_axis = graph.path_histogram.keys()
        y_axis = graph.path_histogram.values()
        axis[index].bar(x_axis, y_axis,
                        label=f'degree = {graph.average_degree}',
                        color=colors[index])
        axis[index].set_title(title_list[index])
        axis[index].legend()

    axis[2].set(xlabel='path length')
    figure.suptitle('Shortest path distribution for each graph type.')

    file_name = f'AvgPathComparisonN{N}deg{deg}beta{beta}.png'
    image_name = os.path.join(image_path, file_name)
    if not check_if_file_exists(image_name):
        figure.savefig(image_name)
    plt.show()
