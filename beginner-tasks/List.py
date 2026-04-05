# Initial list
justice_league = ["Superman", "Batman", "Wonder Woman", "Flash", "Aquaman", "Green Lantern"]

# 1. Number of members
print("Step 1 - Total Members:", len(justice_league))

# 2. Add Batgirl and Nightwing
justice_league.append("Batgirl")
justice_league.append("Nightwing")
print("Step 2 - After Adding Members:", justice_league)

# 3. Move Wonder Woman to the beginning
justice_league.remove("Wonder Woman")
justice_league.insert(0, "Wonder Woman")
print("Step 3 - Wonder Woman as Leader:", justice_league)

# 4. Separate Aquaman and Flash
# Insert 'Superman' between them (after Aquaman)
justice_league.remove("Superman")
aquaman_index = justice_league.index("Aquaman")
justice_league.insert(aquaman_index + 1, "Superman")
print("Step 4 - After Separating Aquaman & Flash:", justice_league)

# 5. Replace entire list with new team
justice_league = ["Cyborg", "Shazam", "Hawkgirl", "Martian Manhunter", "Green Arrow"]
print("Step 5 - New Team:", justice_league)

# 6. Sort alphabetically
justice_league.sort()
print("Step 6 - Sorted List:", justice_league)

# New leader (0th index)
print("New Leader:", justice_league[0])
'''
Expected Output:
Step 1 - Total Members: 6
Step 2 - After Adding Members:
['Superman', 'Batman', 'Wonder Woman', 'Flash', 'Aquaman', 'Green Lantern', 'Batgirl', 'Nightwing']
Step 3 - Wonder Woman as Leader:
['Wonder Woman', 'Superman', 'Batman', 'Flash', 'Aquaman', 'Green Lantern', 'Batgirl', 'Nightwing']
Step 4 - After Separating Aquaman & Flash:
['Wonder Woman', 'Batman', 'Flash', 'Aquaman', 'Superman', 'Green Lantern', 'Batgirl', 'Nightwing']
Step 5 - New Team:
['Cyborg', 'Shazam', 'Hawkgirl', 'Martian Manhunter', 'Green Arrow']
Step 6 - Sorted List:
['Cyborg', 'Green Arrow', 'Hawkgirl', 'Martian Manhunter', 'Shazam']
New Leader: Cyborg
'''
'''
Key Concepts learnt:
len() → count elements
append() → add element
remove() → delete element
insert(index, value) → add at specific position
index() → find position
sort() → alphabetical sorting
'''
'''
BONUS ANSWER:
New Leader = Cyborg
(Because alphabetical sorting puts it first)
'''