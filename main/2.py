import numpy as np

def ellipsoid(x, D, A, b, t, n):
    # Constants
    x_factor = 1/(n+1)
    D_factor1 = n**2/(n**2 - 1)
    D_factor2 = 2/(n+1)

    i = 0
    status = "Infeasible"

    # Run for fixed iterations
    while i < t:
        # Check feasibility
        z = np.dot(A, x.T)
        rowIdx = -1
        for j in range(m):
            if z[j] < b[j]:
                rowIdx = j
                break
        if rowIdx == -1:
            status = "Feasible"
            break

        # Violated constraint
        a = A[rowIdx][:]

        # Update step
        Da = np.dot(D, a.T)
        quadratic = np.dot(a, Da)

        x += x_factor/quadratic * Da
        D = D_factor1 * (D - D_factor2/quadratic * np.dot(Da, Da.T))
        i += 1
    
    return x, D, status


# Input
n, m = list(map(int, input().strip().split()))
c = np.fromiter(map(float, input().strip().split()), dtype=np.float64)
A = []
for _ in range(m):
    row = list(map(float, input().strip().split()))
    A.append(row)
A = np.array(A)
b = np.fromiter(map(float, input().strip().split()), dtype=np.float64)

# Largest absolute value in A and b
largest_val = max(np.max(A), np.max(b))
smallest_val = min(np.min(A), np.min(b))
U = max(abs(largest_val), abs(smallest_val))

# Epsilon perturbation
epsilon = 2*(n+1)*pow((n+1)*U, (n+1))
epsilon = 1/epsilon
e = np.ones(m)
b -= epsilon*e

################################### Initialize algorithm ###################################

# Initial ball
r = n*pow(n*U, 2*n)
I = np.identity(n)
D = r*I

# Initial center
x = np.zeros(n)

# Volume bounds
V = pow(2*n*pow(n*U, n), n)
v = pow(n, n) * pow(n*U, (n**2)*(n+1))
v = 1/v

# Max iterations
t = 2*(n+1)*np.log(V/v)
t = np.ceil(t)

############################################################################################

# Run ellipsoid algorithm
x, D, status = ellipsoid(x, D, A, b, t, n)

if status == "Infeasible":
    print(status)
else:
    # Sliding objective method
    pass
