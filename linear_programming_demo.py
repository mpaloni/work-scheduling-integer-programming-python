import pulp
import random
import pandas as pd

# ---------------------------
# SAMPLE DATA GENERATION
# ---------------------------

# Employees
employees = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Peter","Patrick","Paula"]

# Salary cost per shift
salary = {
    "Alice": 80,
    "Bob": 70,
    "Charlie": 75,
    "Diana": 90,
    "Ethan": 65,
    "Peter": 50,
    "Patrick": 75,
    "Paula": 65,
}

# Preferences: lower number = more preferred
preferences = {
    "Alice": {"Day": 1, "Evening": 3, "Night": 4},
    "Bob": {"Day": 2, "Evening": 1, "Night": 4},
    "Charlie": {"Day": 3, "Evening": 2, "Night": 1},
    "Diana": {"Day": 1, "Evening": 2, "Night": 3},
    "Ethan": {"Day": 2, "Evening": 3, "Night": 1},
    "Peter": {"Day": 1, "Evening": 2, "Night": 3},
    "Patrick": {"Day": 1, "Evening": 2, "Night": 3},
    "Paula": {"Day": 1, "Evening": 2, "Night": 3}
}

# Availability matrix (1 = available, 0 = not available)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
shifts = ["Day", "Evening", "Night"]

availability = {
    emp: {
        (day, shift): random.choice([0, 1])
        for day in days for shift in shifts
    }
    for emp in employees
}

# Shift requirements (more on weekdays, fewer on weekends)
shift_requirements = {
    day: {
        "Day": (3 if day in ["Mon", "Tue", "Wed", "Thu", "Fri"] else 1),
        "Evening": (2 if day in ["Mon", "Tue", "Wed", "Thu", "Fri"] else 1),
        "Night": 1
    }
    for day in days
}

# Add holiday/special event (e.g. Sunday holiday)
shift_requirements["Sun"]["Day"] = 4   # Open longer
shift_requirements["Sun"]["Evening"] = 3


# ---------------------------
# OPTIMIZATION MODEL
# ---------------------------

model = pulp.LpProblem("WorkShiftScheduling", pulp.LpMinimize)

# Decision variable: x[e,d,s] = 1 if employee e works shift s on day d
x = pulp.LpVariable.dicts(
    "assign",
    (employees, days, shifts),
    cat="Binary"
)

# ---------------------------
# OBJECTIVE FUNCTION
# Minimize salary + preference penalty
# ---------------------------

model += pulp.lpSum(
    x[e][d][s] * (salary[e] + 10 * preferences[e][s])
    for e in employees
    for d in days
    for s in shifts
)

# ---------------------------
# CONSTRAINTS
# ---------------------------

# 1. Shift coverage requirement
for d in days:
    for s in shifts:
        model += pulp.lpSum(x[e][d][s] for e in employees) >= shift_requirements[d][s]

# 2. Respect employee availability
for e in employees:
    for d in days:
        for s in shifts:
            if availability[e][(d, s)] == 0:
                model += x[e][d][s] == 0

# 3. Max 1 shift per employee per day
for e in employees:
    for d in days:
        model += pulp.lpSum(x[e][d][s] for s in shifts) <= 1

# 4. Optional: max 5 shifts per week per employee
for e in employees:
    model += pulp.lpSum(x[e][d][s] for d in days for s in shifts) <= 5

# ---------------------------
# SOLVE
# ---------------------------

model.solve(pulp.PULP_CBC_CMD(msg=False))

print(f"Status: {pulp.LpStatus[model.status]}")

# ---------------------------
# RESULTS
# ---------------------------

assigned = []
for d in days:
    for s in shifts:
        workers = [e for e in employees if pulp.value(x[e][d][s]) == 1]
        assigned.append([d, s, workers, len(workers)])

df = pd.DataFrame(assigned, columns=["Day", "Shift", "Assigned Employees", "Count"])
df["Required"] = df.apply(lambda x: shift_requirements[x["Day"]][x["Shift"]], axis=1)
print(df)
