print("Baris Erkus")
print(2 + 2)

"""
This is testing
Testing for comments
"""

first_name = "Baris"
last_name = "Erkus"

print(f"My Name is {first_name} {last_name}")

new_sentence = "New Sentence: My name is {} {}"
print(new_sentence.format(first_name, last_name))

print(new_sentence)

first_name = input("Enter your first name: ")
birthdays = int(input("Enter the days before your birthday: "))

print("Your name is {}, and your birthday"
      " is {} days away".format(first_name, birthdays))

print(f"Your name is {first_name}, and your birthday"
      f" is {birthdays} days away")

print(f"Your name is {first_name}, and your birthday"
      f" is {round(birthdays/7, 2)} weeks away")