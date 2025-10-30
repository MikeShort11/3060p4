
from multiprocessing.process import current_process
import sys


class Process:
    def __init__(self, arrival_time: int, burst_time: int):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.wait_time = 0  

def read_input() -> list:
    output_list = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            parts = line.split()
            output_list.append((int(parts[0]), int(parts[1])))
    return output_list

def first_come_first_served(inputs: list):
    #lists are stored as: [running_sum, counter]
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]
    
    clock = 0
    
    for process in inputs:
        arrival_time = process[0]
        burst_time = process[1]
        
        start_time = max(clock, arrival_time)
        
        response_time = start_time - arrival_time
        response_times[0] += response_time
        response_times[1] += 1
        
        completion_time = start_time + burst_time
        
        turnaround_time = completion_time - arrival_time
        turnaround_times[0] += turnaround_time
        turnaround_times[1] += 1
        
        wait_time = turnaround_time - burst_time
        wait_times[0] += wait_time
        wait_times[1] += 1
        
        clock = completion_time
    
    avg_response = response_times[0] / response_times[1]
    avg_wait = wait_times[0] / wait_times[1]
    avg_turnaround = turnaround_times[0] / turnaround_times[1]
    return avg_response, avg_wait, avg_turnaround

def shortest_job_first(inputs: list):
    #lists are stored as: [running_sum, counter]
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]

    process_queue = []
    clock = 0
    cur_process = None
    unarrived = len(inputs)
    processed_count = 0

    while(True):
        #check for a ready process
        for i in inputs:
            if i[0] == clock:
                ready_process = Process(clock, i[1])
                process_queue.append(ready_process)
                unarrived -= 1

        #if there is no current prosses grab the shortest one
        if not cur_process and process_queue:
            cur_process = min(process_queue, key=lambda p: p.burst_time)
            process_queue.remove(cur_process)

        # Track first start for response time
        if cur_process and cur_process.start_time is None:
            cur_process.start_time = clock
            response_times[0] += cur_process.start_time - cur_process.arrival_time
            response_times[1] += 1

        #incremnt one tick on the current prosses, if this ends the prosses greab its data
        if cur_process:
            cur_process.remaining_time -= 1
        #if process is done on this cycle, complete it and add stats to return values
        if cur_process and cur_process.remaining_time == 0:
            completion_time = clock + 1#competes at the end of the tick
            wait_times[0] += cur_process.wait_time
            wait_times[1] += 1

            turnaround_times[0] += completion_time - cur_process.arrival_time
            turnaround_times[1] += 1
            cur_process = None
            processed_count += 1
        #increment wait times and clock
        for i in process_queue:
            i.wait_time += 1
        clock += 1
        
        #check for no work left
        if processed_count == len(inputs):
            break

    avg_response = response_times[0] / response_times[1]
    avg_wait = wait_times[0] / wait_times[1]
    avg_turnaround = turnaround_times[0] / turnaround_times[1]
    return avg_response, avg_wait, avg_turnaround
def shortest_time_remaining_first(inputs: list):
    #lists are stored as: [running_sum, counter]
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]

    process_queue = []
    clock = 0
    cur_process = None
    unarrived = len(inputs)
    processed_count = 0

    while(True):
        #check for a ready process
        for i in inputs:
            if i[0] == clock:
                ready_process = Process(clock, i[1])
                process_queue.append(ready_process)
                unarrived -= 1

        # Find the process with shortest remaining time
        if process_queue:
            shortest_process = min(process_queue, key=lambda p: p.remaining_time)
            
            # If no current process or found a shorter one, switch
            if not cur_process or shortest_process.remaining_time < cur_process.remaining_time:
                if cur_process:
                    process_queue.append(cur_process)
                process_queue.remove(shortest_process)
                cur_process = shortest_process

        # Track first start for response time
        if cur_process and cur_process.start_time is None:
            cur_process.start_time = clock
            response_times[0] += cur_process.start_time - cur_process.arrival_time
            response_times[1] += 1

        #incremnt one tick on the current prosses, if this ends the prosses greab its data
        if cur_process:
            cur_process.remaining_time -= 1
        #if process is done on this cycle, complete it and add stats to return values
        if cur_process and cur_process.remaining_time == 0:
            completion_time = clock + 1#competes at the end of the tick
            wait_times[0] += cur_process.wait_time
            wait_times[1] += 1

            turnaround_times[0] += completion_time - cur_process.arrival_time
            turnaround_times[1] += 1
            cur_process = None
            processed_count += 1
        #increment wait times and clock
        for i in process_queue:
            i.wait_time += 1
        clock += 1
        
        #check for no work left
        if processed_count == len(inputs):
            break

    avg_response = response_times[0] / response_times[1]
    avg_wait = wait_times[0] / wait_times[1]
    avg_turnaround = turnaround_times[0] / turnaround_times[1]
    return avg_response, avg_wait, avg_turnaround

def round_robin(inputs: list, quantum:int):
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]

    process_queue = []
    clock = 0
    processed_count = 0

    #check for a ready process at zero
    for i in inputs:
        if i[0] == clock:
            ready_process = Process(clock, i[1])
            process_queue.append(ready_process)

    while(True):
        #if there is somthing in the queue
        if process_queue:
            cur_process = process_queue.pop(0)
            print("new process selected")
            #check if the process already has a responce time
            if cur_process.start_time is None:
                cur_process.start_time = clock
            for i in range(quantum):

                #increment clock and process
                cur_process.remaining_time -= 1
                clock += 1
                for i in process_queue:
                    i.wait_time+=1

                if cur_process.remaining_time == 0:
                    print("cur_process ended")
                    completion_time = clock
                    wait_times[0] += cur_process.wait_time
                    wait_times[1] += 1

                    turnaround_times[0] += completion_time - cur_process.arrival_time
                    turnaround_times[1] += 1

                    response_times[0] += cur_process.start_time
                    response_times[1] += 1

                    processed_count += 1
                    print(f"processed_count = {processed_count}")
                    break
            #after the quantum loop, if there is still time on the process re-add it
            if cur_process.remaining_time > 0:
                process_queue.append(cur_process)

            #check for a ready process(clock ticks in the for loop)
            for i in inputs:
                if i[0] == clock:
                    ready_process = Process(clock, i[1])
                    process_queue.append(ready_process)
        #if queue is empty
        else:
            clock += 1
            for i in inputs:
                if i[0] == clock:
                    ready_process = Process(clock, i[1])
                    process_queue.append(ready_process)

        for i in process_queue:
            i.wait_time+=1

        if processed_count == len(inputs):
            break

    avg_response = response_times[0] / response_times[1]
    avg_wait = wait_times[0] / wait_times[1]
    avg_turnaround = turnaround_times[0] / turnaround_times[1]
    return avg_response, avg_wait, avg_turnaround



def main():
    quantum = int(sys.argv[1])
    inputs = read_input()
    
    # Test FCFS
    avg_resp, avg_wait, avg_turnaround = first_come_first_served(inputs)
    print(f"First Come, First Served")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}\n")
    
    # Test SJF
    avg_resp, avg_wait, avg_turnaround = shortest_job_first(inputs)
    print(f"Shortest Job First")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}\n")
    
    # Test SRTF
    avg_resp, avg_wait, avg_turnaround = shortest_time_remaining_first(inputs)
    print(f"Shortest Remaining Time First")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}\n")

    avg_resp, avg_wait, avg_turnaround = round_robin(inputs, quantum)
    print(f"Round Robin with a quantam of {quantum}")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}\n")


if __name__ == "__main__":
    main()
