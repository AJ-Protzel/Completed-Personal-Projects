csv_key_map = {
  "redneck checking.csv": [1,1,3,4,5],
  "redneck savings.csv": [1,1,3,4,5],
  "bofa credit.csv": [1,0,2,4,0],
  "bofa savings.csv": [7,0,1,2,0],
  "prime credit.csv": [1,1,2,5,0],
  "sapphire credit.csv": [1,1,2,5,0], # not done
  "freedom credit.csv": [1,1,2,5,0], # not done
  "wealthfront checking.csv": [1,1,2,5,0], # not done
  "bilt checking.csv": [1,1,2,5,0], # not done
}

# Open the output file in write mode with UTF-8 encoding
with open("csv_key_map.txt", "w", encoding="utf-8") as output_file:
  # Write a header line
  output_file.write("CSV File Name | Key Mapping\n")
  output_file.write("--------------|-------------\n")

  # Loop through each key-value pair in the dictionary
  for csv_file, key_list in csv_key_map.items():
    # Convert the key list to a comma-separated string
    key_string = ",".join(str(key) for key in key_list)
    # Write the formatted line to the file
    output_file.write(f"{csv_file} | {key_string}\n")

print("CSV key map successfully written to csv_key_map.txt")


# with open("csv_key_map.txt", 'r') as file:
#     reader = csv.reader(file)


with open("csv_key_map.txt", 'r', encoding='utf-8') as file:
    for lines in file:
        print(lines)
