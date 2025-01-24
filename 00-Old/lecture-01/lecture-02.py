my_list = [1, 2, 3, 100, 80, -7]
print(my_list)

people_list= ["Baris", "Ann", "Emek", "Leyla"]
print(people_list)

print(people_list[2])


print(people_list[-1])

print(people_list[0:2])

people_list.append("Andy")
print(people_list)

people_list.remove("Ann")
print(people_list)

people_list.append("Ann")
print(people_list)

people_list.sort()
print(people_list)

for x in people_list[0:3]:
    print(x)