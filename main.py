
import sys

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
    response_times = []
    wait_times = []
    turnaround_times = []
    
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
        turnaround_time[1] += 1
        
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
    response_times = []
    wait_times = []
    turnaround_times = []

    #each prossess object is [arrival_time, remaining_time, running_wait_time]
    prossess_queue = []
    clock = 0
    cur_prossess = [] #where the current prossess is stored

    while(True):
        #check for a ready prossess
        for i in list:
            if i[0] == clock:
                i[2] = 0
                prossess_queue.append(i)
        #check if a ready prossess is shorter
        if cur_prossess:
            #iterate over a copy to avoid errors removing items from the list
            for i in prossess_queue[:]:
                if i[1] < cur_prossess[1]:
                    prossess_queue.append(cur_prossess)
                    prossess_queue.remove(i)
                    cur_prossess = i
        cur_prossess[1] -= 1
        if cur_prossess == 0:
            response_times[0] += clock - cur_prossess[0]
            response_times[1] += 1

            wait_times[0]L

        #increment wait times
        for i in prossess_queue:
            i[2] += 1
        clock += 1

def shortest_time_remaining_first():
    pass

def round_robin():
    pass

def main():
    inputs = read_input()
    
    # Test FCFS
    avg_resp, avg_wait, avg_turnaround = first_come_first_served(inputs)
    print(f"First Come, First Served")
    print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}")

if __name__ == "__main__":
    main()
