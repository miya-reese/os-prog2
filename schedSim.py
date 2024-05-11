class process: 
    def __init__(self, burst, arrival): 
        self.id = -1
        self.name = None
        self.arrival = arrival
        self.burst = burst
        self.time_remaining = burst
        self.wait = -1
        self.completion = -1
        self.turnaround = -1
  
    def __repr__(self): 
        return str((self.name, self.arrival, self.burst, self.wait, self.completion, self.turnaround))
    
    def compute_ta(self):
        self.turnaround = self.completion - self.arrival

    def compute_wait(self):
        self.wait = self.turnaround - self.burst

    def update_burst(self):
        self.time_remaining -= 1

def avg_wait(jobs):
    sum = 0
    for job in jobs:
        sum += job.wait
    return sum/len(jobs)

def avg_ta(jobs):
    sum = 0
    for job in jobs:
        sum += job.turnaround
    return sum/len(jobs)

def fifo(processes):
    time = 0
    for p in processes:
        # busy wait until time = arrival
        while (time < p.arrival):
            time+=1
        # process has arrived
        p.completion = time + p.burst
        p.compute_ta()
        p.compute_wait()
        time += p.burst
    return processes

def srtn(processes):
    time = 0
    finished = []
    temp = [] # job queue
    while (len(finished) < len(processes)):
        # add the arriving processes
        temp = temp + [p for p in processes if p.arrival == time]
        temp = sorted(temp, key=lambda x: x.time_remaining)
        # schedule process
        if (len(temp) > 0):
            next_p = temp[0]
            next_p.update_burst()
            time += 1
            # process is finished
            if (next_p.time_remaining == 0):
                next_p.completion = time
                next_p.compute_ta()
                next_p.compute_wait()
                # remove job from queue and add to finished
                finished.append(next_p)
                temp.pop(0)
        else:
            time += 1
    return sorted(finished, key=lambda x: x.time_remaining)

def rr(processes, quantum):
    time = 0 
    finished = [] 
    queue = [] # job queue 
    last_time = -1 
    while (len(finished) < len(processes)): 
        temp_finished = []
        queue = queue + [p for p in processes if (p.arrival <= time and p.arrival > last_time)] 
        last_time = time # used to only add the processes which arrived during the quantum 
        if len(queue) > 0: 
            for process in queue:
                # do quantum units of computation
                for _ in range(quantum): 
                    process.update_burst() 
                    time += 1 
                    # complete processes that are completed
                    if process.time_remaining <= 0:
                        process.completion = time
                        process.compute_ta() 
                        process.compute_wait() 
                        temp_finished.append(process) 
                        break
            # remove temp_finished processes 
            for finished_process in temp_finished: 
                queue.remove(finished_process) 
                finished.append(finished_process)
        else: 
            time += 1 
    return sorted(processes, key=lambda x: x.arrival)

def main():
    # read file
    with open('jobs.txt') as job_file:
        unsorted = [process(int(line.rstrip().split(' ')[0]), int(line.rstrip().split(' ')[1])) for line in job_file]
    job_file.close()
    # sort processes by arrival time
    processes = sorted(unsorted, key=lambda x: x.arrival)
    for i in range(0, len(processes)):
        processes[i].id = i
        processes[i].name = 'P' + str(i)
    # algorithm
    jobs = rr(processes)
    print(jobs)
    for job in jobs:
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (job.id, job.turnaround, job.wait))
        print("        Arrival %3.2f  Burst %3.2f  Complete %3.2f" % (job.arrival, job.burst, job.completion))
    print("\nAverage -- Turnaround %3.2f  Wait %3.2f" % (avg_ta(jobs), avg_wait(jobs)))

if __name__=='__main__':
    main()