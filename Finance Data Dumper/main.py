import os
import csv
import sqlite3
import configparser

MONTHS = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December"
}

file_description_map = r"Mappings/description_map.txt"
file_category_map = r"Mappings/category_map.txt"
file_account_map = r"Mappings/account_map.txt"
file_key = r"Mappings/key.txt"

#======================================================================================== load_mappings
def load_mappings(file_path):
  mapping = {}
  with open(file_path, 'r') as file:
    for line in file:
      key, value = line.strip().split('=')
      mapping[key] = value
  return mapping

description_map = load_mappings(file_description_map)
category_map = load_mappings(file_category_map)
account_map = load_mappings(file_account_map)

#===================================================================================== contains_keyword
def contains_keyword(text):
  with open(file_key, "r") as file:
    words = file.readlines()
    words = [word.strip() for word in words]
  
  for word in words:
    if word.lower() in text.lower():
      return word.lower()
  return None

########################################################################################## create_table
def create_table(cursor):
  create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
      year INTEGER,
      month TEXT,
      date TEXT,
      description TEXT,
      amount REAL,
      category TEXT,
      bank TEXT,
      account TEXT
    )
  """
  cursor.execute(create_table_query)

############################################################################################ read_files
def read_files(cursor):
  print("READING")
  # config = configparser.ConfigParser()
  # config.read(file_account_map)  # Replace with path if needed
  # print(config)

  # for i in account_map:
  #   print(i)
  # print(account_map)
  # for i in category_map:
  #   print(i["amazon"])
  # print(category_map["amazon"])

  # for file in os.listdir("Accounts"):
  #   print(file)
    # account_map = [int(x) for x in config['DEFAULT'][file].split(',')]
    # fill_table(cursor, os.path.join(path, file), account_map)

############################################################################################ fill_table
def fill_table(cursor, file_path, key):
  with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for _ in range(key[0]):
      next(reader)

    for row in reader:
      if row[key[3]] == '' and row[key[4]] == '':
        continue

      month, day, year = row[key[1]].split('/')
      month = MONTHS.get(int(month))
      date = str(row[key[1]])

      filename = os.path.basename(file_path).split(" ", 1)
      bank = filename[0]
      account = filename[1].split(".")[0]
      
      amount = get_amount(row[key[3]], row[key[4]], bank, account)

      description = get_description(row[key[2]], amount)

      category = get_category(description)

      insert_query = """
        INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)  
      """
      cursor.execute(insert_query, (year, month, date, description, amount, category, bank, account))

  cursor.connection.commit()

#-------------------------------------------------------------------------------------- get_description
def get_description(desc, amount):
  description = contains_keyword(desc)
  if description == "ach debit" or "ach credit":
    description = "transfer"

  if description is None:
    description = description_map.get(desc, None)
    if description is None:
      user_input = input(f"Description {amount} {desc} = ")
      user_input.lower()
      with open(file_description_map, 'a') as mapping_file:
        mapping_file.write(f"{desc}={user_input}\n")
      description = user_input
  
    with open(file_key, 'a') as key_file:
      key_file.write(f"{description}\n")

  return description.lower()

#----------------------------------------------------------------------------------------- get_category
def get_category(desc):
  category = category_map.get(desc, None)
  if category is None:
    user_input = input(f"Category {desc} = ")
    user_input.lower()
    with open(file_category_map, 'a') as mapping_file:
      mapping_file.write(f"{desc}={user_input}\n")
    category = user_input
  
  return category.lower()

#------------------------------------------------------------------------------------------- get_amount
def get_amount(debit, credit, bank, account):
  if bank == "redneck":
    if debit != '':
      amount = float(debit) * -1
    else:
      amount = float(credit)
  else:
    print("=========",debit)
    amount = float(debit.replace(",", ""))
    if account == "credit":
      amount = amount * -1
  
  return amount

##################################################################################### remove_duplicates
def remove_duplicates(cursor):
    deduplication_query = """
        DELETE FROM transactions AS t1
        WHERE EXISTS (
            SELECT 1
            FROM transactions AS t2
            WHERE t1.year = t2.year
                AND t1.month = t2.month
                AND t1.date = t2.date
                AND t1.description = t2.description
                AND t1.amount = t2.amount
                AND t1.category = t2.category
                AND t1.bank = t2.bank
                AND t1.account = t2.account
                AND t1.rowid > t2.rowid
        );
    """
    cursor.execute(deduplication_query)

    files = [file_category_map, file_key]
    for f in files:
      with open(f, 'r+') as file:
        lines = set(line.lower() for line in file)
        file.seek(0)
        file.writelines(lines)

    print("data cleaned")

#######################################################################################################
################################################################################################## Main
#######################################################################################################
def main():


    database_file = "main.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    create_table(cursor)
    read_files(cursor)
    remove_duplicates(cursor)

    connection.commit()
    connection.close()

    print("Success")

if __name__ == "__main__":
  main()