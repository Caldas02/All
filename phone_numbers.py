import csv
import random

def generate_phone_number():
    first_three = "07"  # Start with "07" for mobile numbers
    middle_three = random.randint(100, 999)
    last_four = random.randint(1000, 9999)
    return f"{first_three}-{middle_three}-{last_four}"

def generate_phone_numbers_csv(filename, num_numbers):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Phone Number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for _ in range(num_numbers):
            writer.writerow({'Phone Number': generate_phone_number()})

# Specify the filename and the number of phone numbers to generate
filename = 'phone_numbers.csv'
num_numbers = 100  # Change this to the desired number of phone numbers

# Generate phone numbers and save to CSV
generate_phone_numbers_csv(filename, num_numbers)
print(f"{num_numbers} random phone numbers have been generated and saved in '{filename}'.")
