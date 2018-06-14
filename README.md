
---
## Operating System Simulation
---
Simulation of a single core operating system with a variable number of hard disks. Issue commands via the command line to create and manage activity of processes to observe the behavior of the CPU and disk scheduling algorithms.

Written in Python 3.5.

Built for CSCI 340: Operating Systems.

---
### Run Instructions
---
With Python version 3.5 or above installed, run

```$ python3 main.py```


---
### Commands
---
A  -  Create a new process and send it to the ready queue.

Q  -  One time quantum has passed for process in CPU.

t  -  Process in CPU terminates.

d number file_name  -  Request I/O for specified disk number and file.

D number  -  Terminate I/O for specified disk number.

m address  -  Request a memory operation at specified logical address.

S r  -  Show what process is in the CPU and what processes are in the ready queue at each level.

S i  -  Show what processes are using each disk and what processes are in the I/O queue for each disk.

S m  -  Show the memory table.


If command has multiple parts, enter separated by spaces (ie. "d 0 file.txt").

Disks are enumerated starting at 0.

---
### CPU Scheduling Algorithm
---
Multilevel ready queue with 3 levels, enumerated from 0. The 0th level is round robin where a process is allowed 1 time quantum in the CPU before it is demoted a level, and on the 1st level it is allowed 2 time quantums. The 2nd level is First Come First Serve. There is no way for a process to be promoted up a priority level in this simulation.

---
### Disk Scheduling Algorithm
---
First Come First Serve. All processes have the same priority.

---
### Error Checking
---
Values entered for RAM, page size, and disk number must be non-zero positive integers.

RAM must be evenly divided by page size.

If any of the above conditions are not met, the user will be prompted to re-enter the values.