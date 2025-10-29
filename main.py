
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
    pass

def shortest_time_remaining_first(inputs: list):
    #lists are stored as: [running_sum, counter]
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]

    prossess_queue = []
    clock = 0
    cur_prossess = None
    unarrived = len(inputs)
    processed_count = 0

    while(True):
        #check for a ready prossess
        for i in inputs:
            if i[0] == clock:
                ready_prossess = Process(clock, i[1])
                prossess_queue.append(ready_prossess)
                unarrived -= 1

        # Find the process with shortest remaining time
        if prossess_queue:
            shortest_process = min(prossess_queue, key=lambda p: p.remaining_time)
            
            # If no current process or found a shorter one, switch
            if not cur_prossess or shortest_process.remaining_time < cur_prossess.remaining_time:
                if cur_prossess:
                    prossess_queue.append(cur_prossess)
                prossess_queue.remove(shortest_process)
                cur_prossess = shortest_process

        # Track first start for response time
        if cur_prossess and cur_prossess.start_time is None:
            cur_prossess.start_time = clock
            response_times[0] += cur_prossess.start_time - cur_prossess.arrival_time
            response_times[1] += 1

        #incremnt one tick on the current prosses, if this ends the prosses greab its data
        if cur_prossess:
            cur_prossess.remaining_time -= 1
        #if prossess is done on this cycle, complete it and add stats to return values
        if cur_prossess and cur_prossess.remaining_time == 0:
            completion_time = clock + 1#competes at the end of the tick
            wait_times[0] += cur_prossess.wait_time
            wait_times[1] += 1

            turnaround_times[0] += completion_time - cur_prossess.arrival_time
            turnaround_times[1] += 1
            cur_prossess = None
            processed_count += 1
        #increment wait times and clock
        for i in prossess_queue:
            i.wait_time += 1
        clock += 1
        
        #check for no work left
        if processed_count == len(inputs):
            break

    avg_response = response_times[0] / response_times[1]
    avg_wait = wait_times[0] / wait_times[1]
    avg_turnaround = turnaround_times[0] / turnaround_times[1]
    return avg_response, avg_wait, avg_turnaround

def round_robin():
    pass

def main():
    inputs = read_input()
    
    # Test FCFS
    avg_resp, avg_wait, avg_turnaround = first_come_first_served(inputs)
    print(f"First Come, First Served")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}")
    
    # Test SRTF
    avg_resp, avg_wait, avg_turnaround = shortest_time_remaining_first(inputs)
    print(f"Shortest Remaining Time First")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}")

if __name__ == "__main__":
    main()
