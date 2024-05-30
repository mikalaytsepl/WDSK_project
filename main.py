from threading import Thread, Event
import ast
import time
from datetime import datetime as dt

elapsed = -1
pool = []
done = []
iter_time = []

counter_event = Event()
checker_event = Event()
stop_event = Event()

fcfs_event = Event()

sjf_niew_event = Event()
sjf_wyw_ivent = Event()


def get_from_file(testcase_file) -> list:
    result = []
    with open(f'Test_cases/{testcase_file}.txt', "r+") as proc_file:
        for line in proc_file:
            result.append(ast.literal_eval(line.strip()))
    return result


def counter(algorythm: Event):
    global elapsed
    while not stop_event.is_set() or len(pool):
        algorythm.wait()
        algorythm.clear()
        print(elapsed)
        elapsed += 1
        counter_event.set()


def checker(file: str) -> None:
    global elapsed
    global pool
    proc_list = get_from_file(file)
    while proc_list or len(pool) != 0:

        counter_event.wait()
        counter_event.clear()

        for process in proc_list[:]:
            if process[1] <= elapsed:
                pool.append(process)
                proc_list.remove(process)

        checker_event.set()
    stop_event.set()


def fcfs() -> None:
    global pool
    global elapsed
    global done
    global iter_time
    while not stop_event.is_set():

        start = dt.now()

        checker_event.wait()
        checker_event.clear()

        try:

            print(elapsed)
            run: list = pool.pop(0)
            run[3] = elapsed - run[1]
            for _ in range(run[2]):
                fcfs_event.set()
                time.sleep(0.001)
            done.append(run)

        except IndexError:
            fcfs_event.set()

        finish = dt.now()
        iter_time.append((finish - start).total_seconds() * 1000)  # elapsed time during iteration in miliseconds


def sjf_niew() -> None:
    global pool
    global elapsed
    global done
    while not stop_event.is_set():

        checker_event.wait()
        checker_event.clear()

        pool = sorted(pool, key=lambda item: item[2], reverse=False)
        try:

            run: list = pool.pop(0)
            run[3] = elapsed - run[1]
            for _ in range(run[2]):
                sjf_niew_event.set()
                time.sleep(0.001)
            done.append(run)

        except IndexError:
            print(f'pool is empty, lehght:{len(pool)}')
            sjf_niew_event.set()


def sjf_wyw() -> None:
    global pool
    global elapsed
    global done
    while not stop_event.is_set():
        checker_event.wait()
        checker_event.clear()

        pool = sorted(pool, key=lambda item: item[2], reverse=False)
        try:
            run: list = pool.pop(0)
            for process in pool:
                process[3] += 1
            if run[2] >= 0:
                run[2] -= 1
                time.sleep(0.001)
                sjf_wyw_ivent.set()
                if run[2] == 0:
                    done.append(run)
                else:
                    pool.append(run)
            else:
                done.append(run)

        except IndexError:
            sjf_wyw_ivent.set()


# works hehe
def run_fcfs(event, file):
    event.set()  # determine wether to switch to global or to continue pushing them as params
    counter_thread = Thread(target=counter, args=(event,))
    fcfs_thread = Thread(target=fcfs)
    sorter_thread = Thread(target=checker, args=(file,))

    fcfs_thread.start()
    sorter_thread.start()
    counter_thread.start()

    fcfs_thread.join()
    sorter_thread.join()
    counter_thread.join()


def run_sjf_new(event, file):
    sjf_niew_event.set()
    counter_thread = Thread(target=counter, args=(event,))
    sjf_new_thread = Thread(target=sjf_niew)
    sorter_thread = Thread(target=checker, args=(file,))

    sjf_new_thread.start()
    sorter_thread.start()
    counter_thread.start()

    sjf_new_thread.join()
    sorter_thread.join()
    counter_thread.join()


def run_sjf_wyw(event, file):
    event.set()

    counter_thread = Thread(target=counter, args=(event,))
    sjf_wyw_thread = Thread(target=sjf_wyw)
    sorter_thread = Thread(target=checker, args=(file,))

    sjf_wyw_thread.start()
    sorter_thread.start()
    counter_thread.start()

    sjf_wyw_thread.join()
    sorter_thread.join()
    counter_thread.join()


'''run_fcfs(fcfs_event, "Test0")
print(done)'''


class Tester:

    @staticmethod  # works
    def _make_table(proc_list: list, num: int, path: str) -> None:
        with open(f"Outputs/{path}/Test{num}.txt", "w+") as file:
            file.write(f"{'PID'.center(3)} | {'AT'.center(3)} | {'ET'.center(3)} | {'WT'.center(3)}\n")
            for proc in proc_list:
                line = (f"{str(proc[0]).center(3)} | {str(proc[1]).center(3)} |"
                        f" {str(proc[2]).center(3)} | {str(proc[3]).center(3)}\n")
                file.write(line)

    @staticmethod
    def _av_wait() -> float:
        global done
        return sum(i[3] for i in done) / len(done)  # sum wylicza całą sume wszystkich elementów
        # podanych przez cykl w środku a póżniej to sie dzieli przez ilość procesów

    @staticmethod
    def _av_iter_time() -> float:
        global iter_time
        return sum(time for time in iter_time) / len(iter_time)  # sum wylicza całą sume wszystkich elementów
        # podanych przez cykl w środku a póżniej to sie dzieli przez ilość procesów

    def make_stats(self, name: str, count: int) -> None:
        global done
        global iter_time
        global elapsed
        global pool

        for i in range(count):
            done.clear()
            iter_time.clear()
            elapsed = -1
            pool.clear()
            # start_global = dt.now()

            stop_event.clear()

            run_fcfs(fcfs_event, f"Test{i}")

            # end_global = dt.now()

            self._make_table(done, i, name)

            with open(f'Outputs/{name}/stats/{name}_statiscics_file.txt', 'w+') as file: # tests work, make a working
                # stats file (seems like it is owerwriting the thing ove and over again)
                file.write(f"Test{i} \n")  # does not write this in the file for some reason


test = Tester()
test.make_stats("fcfs", 5)
