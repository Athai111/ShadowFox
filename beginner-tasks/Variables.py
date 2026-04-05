# 1. Create variable pi and check datatype
pi = 22/7
print("Value of pi:", pi)
print("Data type of pi:", type(pi))
'''
Explanation
22/7 performs floating point division in Python
So pi becomes a float
'''
'''
 Output
Value of pi: 3.142857142857143
Data type of pi: <class 'float'>
'''

# 2.Create variable for = 4
for = 4
'''
What happens?
You get an error:
SyntaxError: invalid syntax
'''
'''
Reason :
for is a reserved keyword in Python
Keywords have special meaning (used in loops, conditions, etc.)
You cannot use keywords as variable names
'''
'''
Fix:
Use a different name:
'''
num = 4

# 3. Simple Interest Calculation
''' 
Formula:
Simple Interest = (Principal * Rate * Time) / 100
'''
# Given values
P = 1000   # Principal
R = 5      # Rate of interest
T = 3      # Time in years
# Calculate Simple Interest
SI = (P * R * T) / 100
print("Simple Interest:", SI)
'''
Output:
Simple Interest: 150.0
'''