from threading import Thread, Event
import ast
import time

elapsed = 0
pool = []
done = []

counter_event = Event()
checker_event = Event()
fcfs_event = Event()
stop_event = Event()


def get_from_file(testcase_file) -> list:
    result = []
    with open(f'Test_cases/{testcase_file}.txt', "r+") as proc_file:
        for line in proc_file:
            result.append(ast.literal_eval(line.strip()))
    return result


def counter(stopper: Event):
    global elapsed
    while not stopper.is_set():
        counter_event.set()

        time.sleep(0.001)
        elapsed += 1

        checker_event.wait()  # pauses the execution of the counter waits for the checker event to be changed to true
        # somewhere (in this case inside checker which will mark the end of its iteration)
        checker_event.clear()


def checker(file: str, stopper: Event) -> None:
    global elapsed
    global pool
    proc_list = get_from_file(file)
    while proc_list:
        counter_event.wait()
        for process in proc_list[:]:
            if process[1] <= elapsed:
                pool.append(process)
                proc_list.remove(process)

        counter_event.clear()
        checker_event.set()

    stopper.set()


def fcfs(): # check and think of smth to do with events to run this in propper order
    global pool
    global elapsed
    global done
    while True:
        try:

            run: list = pool[0]
            pool.remove(run)
            time.sleep(run[1] / 1000)
            done.append(run.append(run[1] - elapsed))

        except IndexError:
            fcfs_event.set()
            pass


sorter_thread = Thread(target=checker, args=("05.20.24 20.3625", stop_event))
thr2 = Thread(target=counter, args=(stop_event,))

sorter_thread.start()
thr2.start()

sorter_thread.join()
thr2.join()
