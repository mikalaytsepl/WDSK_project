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
        print(elapsed)  # of course this one is optional
        elapsed += 1
        counter_event.set()


def checker(file: str) -> None:
    global elapsed
    global pool
    global done
    proc_list = get_from_file(file)
    count = len(proc_list)
    while len(done) != count: # remake a stop event (try based on some counter and lenght of the done pool)

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

        if pool:

            run: list = pool.pop(0)
            run[3] = elapsed - run[1]
            for _ in range(run[2]):
                fcfs_event.set()
                time.sleep(0.001)

            done.append(run)
        else:
            fcfs_event.set()

        finish = dt.now()
        iter_time.append((finish - start).total_seconds() * 1000)  # elapsed time during iteration in miliseconds


def sjf_niew() -> None:
    global pool
    global elapsed
    global done
    while not stop_event.is_set():

        start = dt.now()

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

        except IndexError:  # w przypadku gdy pool jest pusty (w chwili obecnej nie ma procesów), to wyzwalamy event sjf aby dodać "click" i skanować dalej
            sjf_niew_event.set()

        finish = dt.now()
        iter_time.append((finish - start).total_seconds() * 1000)  # elapsed time during iteration in miliseconds


def sjf_wyw() -> None:
    global pool
    global elapsed
    global done
    while not stop_event.is_set():
        checker_event.wait()
        checker_event.clear()

        start = dt.now()

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

        finish = dt.now()
        iter_time.append((finish - start).total_seconds() * 1000)  # elapsed time during iteration in miliseconds


# works hehe
def run_fcfs(file):
    fcfs_event.set()
    counter_thread = Thread(target=counter, args=(fcfs_event,))
    fcfs_thread = Thread(target=fcfs)
    sorter_thread = Thread(target=checker, args=(file,))

    counter_thread.start()
    sorter_thread.start()
    fcfs_thread.start()

    fcfs_thread.join()
    sorter_thread.join()
    counter_thread.join()


def run_sjf_new(file):
    sjf_niew_event.set()
    counter_thread = Thread(target=counter, args=(sjf_niew_event,))
    sjf_new_thread = Thread(target=sjf_niew)
    sorter_thread = Thread(target=checker, args=(file,))

    sjf_new_thread.start()
    sorter_thread.start()
    counter_thread.start()

    sjf_new_thread.join()
    sorter_thread.join()
    counter_thread.join()


def run_sjf_wyw(file):
    sjf_wyw_ivent.set()

    counter_thread = Thread(target=counter, args=(sjf_wyw_ivent,))
    sjf_wyw_thread = Thread(target=sjf_wyw)
    sorter_thread = Thread(target=checker, args=(file,))

    sjf_wyw_thread.start()
    sorter_thread.start()
    counter_thread.start()

    sjf_wyw_thread.join()
    sorter_thread.join()
    counter_thread.join()


class Tester:

    @staticmethod
    def _make_table(proc_list: list, num: int, path: str) -> None:
        with open(f"Outputs/{path}/Test{num}_output.txt", "w+") as file:
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
        return sum(time_it for time_it in iter_time) / len(iter_time)  # sum wylicza całą sume wszystkich elementów
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
            start_global = dt.now()

            stop_event.clear()

            match name:
                case "fcfs":
                    run_fcfs(f"Test{i}")

                case "sjf_niew":
                    run_sjf_new(f"Test{i}")

                case "sjf_wyw":
                    run_sjf_wyw(f"Test{i}")

                case _:
                    print("Error in selecting algorythm")
                    return None

            end_global = dt.now()

            self._make_table(done, i, name)

            with open(f'Outputs/{name}/stats/{name}_statiscics_file.txt', 'a') as file:
                file.write(
                    f"Stats of Test{i}: overall executon time: {(end_global - start_global).total_seconds() * 1000} ms,"
                    f"average interation time:{self._av_iter_time()} ms, average waiting time:{self._av_wait()}\n")
                file.close()


test = Tester()
# test.make_stats("fcfs", 100)
# test.make_stats("sjf_niew", 100) # works perfectly
test.make_stats("sjf_wyw", 100)

