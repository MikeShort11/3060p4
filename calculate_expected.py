#!/usr/bin/env python3

class Process:
    def __init__(self, arrival_time: int, burst_time: int):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.wait_time = 0

def shortest_time_remaining_first(inputs: list):
    response_times = [0, 0]
    wait_times = [0, 0]
    turnaround_times = [0, 0]

    prossess_queue = []
    clock = 0
    cur_prossess = None
    processed_count = 0

    while(True):
        # Add arriving processes
        for i in inputs:
            if i[0] == clock:
                ready_prossess = Process(clock, i[1])
                prossess_queue.append(ready_prossess)

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

        # Execute current process
        if cur_prossess:
            cur_prossess.remaining_time -= 1
            
        # Check if process completed
        if cur_prossess and cur_prossess.remaining_time == 0:
            completion_time = clock + 1
            wait_times[0] += cur_prossess.wait_time
            wait_times[1] += 1
            turnaround_times[0] += completion_time - cur_prossess.arrival_time
            turnaround_times[1] += 1
            cur_prossess = None
            processed_count += 1
            
        # Increment wait times for processes in queue
        for i in prossess_queue:
            i.wait_time += 1
        clock += 1
        
        # Check for completion
        if processed_count == len(inputs):
            break

    avg_response = response_times[0] / response_times[1] if response_times[1] > 0 else 0
    avg_wait = wait_times[0] / wait_times[1] if wait_times[1] > 0 else 0
    avg_turnaround = turnaround_times[0] / turnaround_times[1] if turnaround_times[1] > 0 else 0
    return avg_response, avg_wait, avg_turnaround

# Test with sample data
inputs = [(0, 5), (2, 3), (4, 8), (6, 2), (8, 4), (10, 6), (12, 1), (14, 7), (16, 3), (18, 5)]
print("Sample data:", inputs)
avg_resp, avg_wait, avg_turnaround = shortest_time_remaining_first(inputs)
print(f"SRTF Results:")
print(f"Avg. Resp.: {avg_resp:.2f}, Avg. T.A.: {avg_turnaround:.2f}, Avg. Wait: {avg_wait:.2f}")
