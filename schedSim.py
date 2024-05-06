class process: 
    def __init__(self, burst, arrival): 
        self.id = -1
        self.name = None
        self.arrival = arrival
        self.burst = burst 
        self.wait = -1
        self.completion = -1
        self.turnaround = -1
  
    def __repr__(self): 
        return str((self.name, self.arrival, self.burst, self.wait, self.completion, self.turnaround))
    
    def compute_ta(self):
        self.turnaround = self.completion - self.arrival

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
    jobs = fifo(processes)
    print(jobs)
    for job in jobs:
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (job.id, job.turnaround, job.wait))
        print("        Arrival %3.2f  Burst %3.2f  Complete %3.2f" % (job.arrival, job.burst, job.completion))
    print("\nAverage -- Turnaround %3.2f  Wait %3.2f" % (avg_ta(jobs), avg_wait(jobs)))

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
        if (time - p.arrival > 0):
            p.wait = time - p.arrival
        else:
            p.wait = 0
        p.completion = time + p.burst
        p.compute_ta()
        time += p.burst
    return processes

if __name__=='__main__':
    main()