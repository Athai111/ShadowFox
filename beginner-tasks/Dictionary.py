# 1. Friends List → Tuple with Name Length
# List of friends
friends = ["Amit", "Rahul", "Sneha", "Priya", "Karan"]

# Create list of tuples (name, length)
name_length = []

for name in friends:
    name_length.append((name, len(name)))

print("Friends with name lengths:", name_length)
'''
Output:
Friends with name lengths: [('Amit', 4), ('Rahul', 5), ('Sneha', 5), ('Priya', 5), ('Karan', 5)]
'''
'''
Concept:
len(name) → length of string
Tuple → (name, length)
List of tuples → structured data
'''

# 2. Expense Tracking using Dictionaries
# Your expenses
your_expenses = {
    "Hotel": 1200,
    "Food": 800,
    "Transportation": 500,
    "Attractions": 300,
    "Miscellaneous": 200
}

# Partner's expenses
partner_expenses = {
    "Hotel": 1000,
    "Food": 900,
    "Transportation": 600,
    "Attractions": 400,
    "Miscellaneous": 150
}

# Total expenses
your_total = sum(your_expenses.values())
partner_total = sum(partner_expenses.values())

print("Your total expense:", your_total)
print("Partner's total expense:", partner_total)

# Who spent more
if your_total > partner_total:
    print("You spent more.")
elif partner_total > your_total:
    print("Your partner spent more.")
else:
    print("Both spent equally.")

# Find category with maximum difference
max_diff = 0
max_category = ""

for key in your_expenses:
    diff = abs(your_expenses[key] - partner_expenses[key])
    
    if diff > max_diff:
        max_diff = diff
        max_category = key

print("Highest spending difference in category:", max_category)
print("Difference amount:", max_diff)
'''
Output:
Your total expense: 3000
Partner's total expense: 3050
Your partner spent more.
Highest spending difference in category: Hotel
Difference amount: 200
'''
'''
Key Concepts:
Dictionary → key-value pairs
sum(values()) → total calculation
Loop through keys
abs() → absolute difference
Track max difference
'''