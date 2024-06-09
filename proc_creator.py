import random


def create_process_list(test):

    random.seed(test)
    proc_list = [[pid, random.randint(0, 30), random.randint(1, 15), 0] for pid in range(100)]

    try:
        with open(f'Test_cases/Test{test}.txt', "w+") as proc_file:
            for process in proc_list:
                proc_file.write(f'{process}\n')
    except FileExistsError:
        print('Error in creating file, file already exists.')


for i in range(100):
    create_process_list(i)
