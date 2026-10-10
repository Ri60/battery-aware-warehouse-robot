\# Battery-Aware Warehouse Delivery Robot



\## SOFE 3720 - Introduction to Artificial Intelligence



This project implements and evaluates a battery-aware route-planning agent in a simulated warehouse environment.



The robot must travel from a selected start location to a delivery goal while minimizing total travel time and never violating its battery constraint.



The warehouse contains:



\- Blocked cells

\- Charging stations

\- Variable movement-time costs

\- Limited battery capacity

\- Four-directional movement



A route that appears geometrically short may not be feasible if the robot does not have enough battery to complete it.



\---



\## Project Objective



The goal is to find the minimum-total-time feasible route from the start state to the goal state.



Total path cost includes:



\- Movement time

\- Charging time



The robot must maintain:



```text

battery >= 0

