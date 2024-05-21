from numpy.random import randint as rint
from datetime import datetime as dt
import re

start = dt.now()


def create_process_list(count, arrival_low, arrival_high, execution_low, executon_high):
    proc_list = [[i, rint(low=arrival_low, high=arrival_high),
                  rint(low=execution_low, high=executon_high)] for i in range(count)]
    try:
        format = re.sub(r'[/:]', '.', dt.now().strftime('%D %H:%M%S'))
        with open(f'Test_cases/{format}.txt', "w+") as proc_file:
            for process in proc_list:
                proc_file.write(f'{process}\n')
    except Exception:
        print('Error in creating file')
    return proc_list


process_dict = create_process_list(10, 1000, 6000, 3000, 7000)
finish = dt.now()
elapsed_ms = (finish - start).total_seconds() * 1000
