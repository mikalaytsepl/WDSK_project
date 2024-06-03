import re

import matplotlib.pyplot as plt

data_for_graphs = []


def get_data_return(name: str) -> list:
    res = []
    with open(f'Outputs/{name}/stats/{name}_statiscics_file.txt', 'r') as file:
        res.extend(re.findall(r'\d+\.\d+', row) for row in file)
        return res


def get_data(name: str) -> None:
    with open(f'Outputs/{name}/stats/{name}_statiscics_file.txt', 'r') as file:
        data_for_graphs.extend(re.findall(r'\d+\.\d+', row) for row in file)
        print(data_for_graphs)


def prepare_bar_waiting():
    left = [i for i in range(1, len(data_for_graphs) + 1)]
    print(left)
    height = [float(h[2]) for h in data_for_graphs]

    print(sorted(height))

    plt.bar(left, height, width=0.8, color=['red', 'green'])

    plt.xlabel('numery pomiarów')
    plt.ylabel('średni czas czekania')
    plt.title('Reprezentacja czasów czekania')

    plt.show()


'''get_data("sjf_wyw")
prepare_bar_waiting()'''

'''get_data("sjf_niew")
prepare_bar_waiting()'''

'''get_data("fcfs")
prepare_bar_waiting()'''


def prepare_bar_iteration():
    left = [i for i in range(1, len(data_for_graphs) + 1)]
    print(left)
    height = [float(h[1]) for h in data_for_graphs]

    print(sorted(height))

    plt.bar(left, height, width=0.8, color=['blue', 'green'])

    plt.xlabel('numery pomiarów')
    plt.ylabel('średni czas iteracji')
    plt.title('Reprezentacja czasów iteracji algorytmu')

    plt.show()


def prepare_graph_for_three_waiting():
    height_fcfs = [float(h[2]) for h in get_data_return("fcfs")]
    height_sjf_niew = [float(h[2]) for h in get_data_return("sjf_niew")]
    height_sjf_wyw = [float(h[2]) for h in get_data_return("sjf_wyw")]

    left = [float(i) for i in range(1, len(height_fcfs) + 1)]

    print(height_fcfs)
    print(height_sjf_niew)
    print(height_sjf_wyw)

    plt.plot(left, height_fcfs, label="fcfs_czekanie")
    plt.plot(left, height_sjf_niew, label="sjf_niew_czekanie")
    plt.plot(left, height_sjf_wyw, label="sjf_wyw_czekanie")

    plt.xlabel('numery pomiarów')
    plt.ylabel('czas [ms]')
    plt.title('Porównanie średnich czasów czekania')

    plt.legend()
    plt.show()


# prepare_graph_for_three_waiting()

def prepare_graph_for_three_iteration():
    height_fcfs = [float(h[1]) for h in get_data_return("fcfs")]
    height_sjf_niew = [float(h[1]) for h in get_data_return("sjf_niew")]
    height_sjf_wyw = [float(h[1]) for h in get_data_return("sjf_wyw")]

    left = [float(i) for i in range(1, len(height_fcfs) + 1)]

    print(height_fcfs)
    print(height_sjf_niew)
    print(height_sjf_wyw)

    plt.plot(left, height_fcfs, label="fcfs_iteracje")
    plt.plot(left, height_sjf_niew, label="sjf_niew_iteracje")
    plt.plot(left, height_sjf_wyw, label="sjf_wyw_iteracje")

    plt.xlabel('numery pomiarów')
    plt.ylabel('czas [ms]')
    plt.title('Porównanie średnich czasów iteracji')

    plt.legend()
    plt.show()


# prepare_graph_for_three_iteration()

def prepare_graph_for_three_overall_execution():
    height_fcfs = [float(h[0]) for h in get_data_return("fcfs")]
    height_sjf_niew = [float(h[0]) for h in get_data_return("sjf_niew")]
    height_sjf_wyw = [float(h[0]) for h in get_data_return("sjf_wyw")]

    left = [float(i) for i in range(1, len(height_fcfs) + 1)]

    print(height_fcfs)
    print(height_sjf_niew)
    print(height_sjf_wyw)

    plt.plot(left, height_fcfs, label="fcfs")
    plt.plot(left, height_sjf_niew, label="sjf_niew")
    plt.plot(left, height_sjf_wyw, label="sjf_wyw")

    plt.xlabel('numery pomiarów')
    plt.ylabel('czas [ms]')
    plt.title('Porównanie ogólnych średnich czasów wykonania symulacji')

    plt.legend()
    plt.show()

prepare_graph_for_three_overall_execution()
