def remove_duplicates(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        unique_lines = set(lines)
    with open(filename, 'w') as file:
        file.writelines(unique_lines)

remove_duplicates("category_mapping.txt")
remove_duplicates("key.txt")

print("done")