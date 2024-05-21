from threading import Thread, Event
import ast
import time

elapsed = -1
pool = []
done = []

counter_event = Event()
checker_event = Event()
fcfs_event = Event()

fcfs_event.set()


def get_from_file(testcase_file) -> list:
    result = []
    with open(f'Test_cases/{testcase_file}.txt', "r+") as proc_file:
        for line in proc_file:
            result.append(ast.literal_eval(line.strip()))
    return result


def counter():
    global elapsed
    while True:
        fcfs_event.wait()
        fcfs_event.clear()

        time.sleep(0.001)
        elapsed += 1
        print(f'counter incremented, current counter value: {elapsed}')
        counter_event.set()

        '''fcfs_event.wait()  # pauses the execution of the counter waits for the checker event to be changed to true
        # somewhere (in this case inside checker which will mark the end of its iteration)'''


def checker(file: str) -> None:
    global elapsed
    global pool
    proc_list = get_from_file(file)
    while True:

        counter_event.wait()  # blocks for some reason
        counter_event.clear()

        for process in proc_list[:]:
            if process[1] <= elapsed:
                pool.append(process)
                proc_list.remove(process)

        checker_event.set()


def fcfs():  # check and think of smth to do with events to run this in propper order
    global pool
    global elapsed
    global done
    while True:

        checker_event.wait()
        checker_event.clear()

        try:

            run: list = pool[0]
            run.append(elapsed - run[1])# elapse timer
            for _ in range(run[2]):
                fcfs_event.set()
            done.append(run)
            pool.remove(run)

        except IndexError:
            print(f'pool is empty, lehght:{len(pool)}')
            fcfs_event.set()


counter_thread = Thread(target=counter)
fcfs_thread = Thread(target=fcfs)
sorter_thread = Thread(target=checker, args=("05.20.24 20.3625",))

fcfs_thread.start()
sorter_thread.start()
counter_thread.start()

fcfs_thread.join()
sorter_thread.join()
counter_thread.join()

# make a stop somehow
