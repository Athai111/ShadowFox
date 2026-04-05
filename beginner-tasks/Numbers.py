# 1. format() function with 145 and 'o'
result = format(145, 'o')
print("Formatted result:", result)
'''
Output:
Formatted result: 221
'''
'''
Explanation:
'o' is used for octal (base 8) representation
So:
Decimal 145 → Octal 221
Conclusion: The representation used is Octal Number System
'''

# 2. Area of Circular Pond + Water Calculation
'''
Given:
Radius = 84 m
π = 3.14
Water per sq meter = 1.4 liters
'''
# Given values
r = 84
pi = 3.14
# Area of circle
area = pi * r * r
# Water calculation
water_per_sqm = 1.4
total_water = area * water_per_sqm
# Print results
print("Area of pond:", area)
print("Total water (liters):", int(total_water))
'''
Explanation
Formula: Area = πr²
Then:
Total Water = Area * Water per sq meter
int() is used to remove decimal part
'''
'''
Output:
Area of pond: 22155.84
Total water (liters): 31018
'''

# 3. Speed Calculation
'''
Given:
Distance = 490 meters
Time = 7 minutes = 420 seconds
'''
# Given values
distance = 490
time_minutes = 7
# Convert time to seconds
time_seconds = time_minutes * 60
# Speed calculation
speed = distance / time_seconds
# Print without decimal
print("Speed (m/s):", int(speed))
'''
Explanation
Convert minutes → seconds
Use formula: Speed = Distance / Time
int() removes decimal
'''
'''
Output:
Speed (m/s): 1
'''