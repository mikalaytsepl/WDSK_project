from numpy.random import randint as rint
from datetime import datetime as dt
# import re
# import uuid

start = dt.now()


def create_process_list(count, arrival_low, arrival_high, execution_low, executon_high, test):
    proc_list = [[pid, rint(low=arrival_low, high=arrival_high),
                  rint(low=execution_low, high=executon_high), 0] for pid in range(count)]
    try:
        with open(f'Test_cases/Test{test}.txt', "w+") as proc_file:
            for process in proc_list:
                proc_file.write(f'{process}\n')
    except Exception:
        print('Error in creating file')
    return proc_list


for i in range(5):
    process_dict = create_process_list(101, 0, 30, 1, 15, i)
