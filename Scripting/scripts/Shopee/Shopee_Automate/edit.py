import csv

# Open the CSV file
with open('test_1.csv', 'r', newline='',encoding='utf-8') as csvfile:
    # Read the CSV data
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

# Loop through all rows in the CSV data
for row in reversed(range(len(rows))):
    # Check if all cells in the row are empty
    if all(cell.strip() == '' for cell in rows[row]):
        # Delete the row
        del rows[row]

# Write the updated CSV data to a new file
with open('updated_test_1.csv', 'w', newline='',encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)