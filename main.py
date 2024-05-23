from threading import Thread, Event
import ast
import time

elapsed = -1
pool = []
done = []

counter_event = Event()
checker_event = Event()
stop_event = Event()

fcfs_event = Event()

sjf_niew_event = Event()
sjf_wyw_ivent = Event()


# fcfs_event.set()


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

        elapsed += 1
        print(f'counter incremented, current counter value: {elapsed}')
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
    while not stop_event.is_set():

        checker_event.wait()
        checker_event.clear()

        try:

            run: list = pool.pop(0)
            waiting_time = elapsed - run[1]
            run.append(waiting_time)
            for _ in range(run[2]):
                fcfs_event.set()
                time.sleep(0.001)
            done.append(run)

        except IndexError:
            fcfs_event.set()


def av_wait(done_processes: list) -> float:
    return sum(i[3] for i in done_processes) / len(done_processes)  # sum wylicza całą sume wszystkich elementów
    # podanych przez cykl w środku a póżniej to sie dzieli przez ilość procesów


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
            waiting_time = elapsed - run[1]
            run.append(waiting_time)
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
             # make waiting time
            if run[2] >= 0:
                run[2] -= 1
                time.sleep(0.001)
                sjf_wyw_ivent.set()
                if run[2] == 0:
                    waiting_time = run[3] - run[1]  # check what is wrong with waiting time
                    run.append(waiting_time)
                    done.append(run)
                else:
                    pool.append(run)
            else:
                done.append(run)

        except IndexError:
            sjf_wyw_ivent.set()


# works hehe
def run_fcfs(event, file):
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


run_sjf_wyw(sjf_wyw_ivent, "05.21.24 13.3626")

print(done)
