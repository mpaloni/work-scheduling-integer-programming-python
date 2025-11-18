# Work Shift Scheduling with Integer Programming

### A Simple Example in Python

This project shows how to build a basic work-shift scheduling system using Integer Programming (IP) in Python. The goal is to create a weekly schedule that assigns employees to shifts while keeping costs low and making sure all rules are followed.

The model chooses which employee works which shift based on availability, preferences, and staffing needs.

---

## Overview

Scheduling employees can be challenging because many factors need to be considered. In this example, each employee can work different shifts, but we must respect:

- When employees are available  
- How many people each shift requires  
- Salary differences  
- Employee shift preferences  
- Holidays or special days  
- Basic fairness in workload  

To solve this, we use **PuLP**, a Python library that helps build and solve optimization models.

---

## Goal of the Optimization

The main goal is to **reduce total scheduling cost**, which includes:

- Each employee’s pay per shift  
- A small penalty if an employee prefers not to work a certain shift  

The schedule must also follow important rules:

- Every shift has enough workers  
- Employees only work when they are available  
- No one works more than one shift per day  
- Optional: Limit how many shifts a person works each week  

