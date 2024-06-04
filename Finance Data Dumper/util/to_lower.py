def lowercase_file(filename):
  with open(filename, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    lowercased_lines = [line.lower() for line in lines]
  with open(filename, 'w', encoding='utf-8') as file:
    file.writelines(lowercased_lines)

lowercase_file("category_mapping.txt")
lowercase_file("key.txt")

print("done")