import csv
import sqlite3
import os

FILES = {
  "bofa credit.csv",
  "bofa savings.csv",
  "chase credit.csv"
}

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

######################################################################################### load_mappings
def load_mappings(file_path):
  mapping = {}
  with open(file_path, 'r') as file:
    for line in file:
      key, value = line.strip().split('=')
      mapping[key] = value
  return mapping

description_mapping = load_mappings("description_mapping.txt")
category_mapping = load_mappings("category_mapping.txt")

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
def read_files(cursor, data_folder_path):
    for file in os.listdir(data_folder_path):
        csv_map = {
            "bofa credit.csv": fill_table_bofa_credit,
            "bofa savings.csv": fill_table_bofa_savings,
            "chase credit.csv": fill_table_chase_credit,
        }

        if file in csv_map:
            print(f"Processing: {file}")
            csv_map[file](cursor, os.path.join(data_folder_path, file))
        else:
            print(f"Error: {file} Function Not Found")

def fill_table(cursor, file_path):
  with open(file_path, 'r') as file:
      reader = csv.reader(file)
      next(reader)

      for row in reader:
          month, day, year = row[0].split('/')
          month = MONTHS.get(int(month))
          date = str(row[0])
          description = description_mapping.get(row[2])
          amount = row[4].get(None, "0.00")
          category = category_mapping.get(row[2])

          insert_query = """
              INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
              VALUES (?, ?, ?, ?, ?, ?, "BofA", "Credit")  
          """
          cursor.execute(insert_query, (year, month, date, description, amount, category))

  cursor.connection.commit()

#=============================================================================== fill_table_bofa_credit
def fill_table_bofa_credit(cursor, file_path):
  with open(file_path, 'r') as file:
      reader = csv.reader(file)
      next(reader)

      for row in reader:
          month, day, year = row[0].split('/')
          month = MONTHS.get(int(month))
          date = str(row[0])
          description = description_mapping.get(row[2])
          amount = row[4].get(None, "0.00")
          category = category_mapping.get(row[2])

          insert_query = """
              INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
              VALUES (?, ?, ?, ?, ?, ?, "BofA", "Credit")  
          """
          cursor.execute(insert_query, (year, month, date, description, amount, category))

  cursor.connection.commit()
   
#============================================================================== fill_table_bofa_savings
def fill_table_bofa_savings(cursor, file_path):
  with open(file_path, 'r') as file:
      reader = csv.reader(file)
      # next(reader)
      # next(reader)
      # next(reader)
      # next(reader)
      # next(reader)
      # next(reader)
      # next(reader)
      for _ in range(7):
        next(reader)

# Date,                  Description,                 Amount,      Running Bal.
# 10/31/2022,   Beginning balance as of 10/31/2022,         ,       "60,278.23"
# 11/03/2022,         "Interest Earned",             "1.44",        "60,287.36"

      for row in reader:
          month, day, year = row[0].split('/')
          month = MONTHS.get(int(month))
          date = str(row[0])
          description = description_mapping.get(row[1], "NULL")
          amount = row[2].get(None, "0.00")
          category = category_mapping.get(row[1], "NULL")

          insert_query = """
              INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
              VALUES (?, ?, ?, ?, ?, ?, "BofA", "Savings")  
          """
          cursor.execute(insert_query, (year, month, date, description, amount, category))

  cursor.connection.commit()

#============================================================================== fill_table_chase_credit
def fill_table_chase_credit(cursor, file_path):
  with open(file_path, 'r') as file:
      reader = csv.reader(file)
      next(reader)

      for row in reader:
          
# Transaction Date,     Post Date,     Description,       Category,    Type,   Amount,    Memo
# 04/21/2024,          04/22/2024, Amazon.com*2J00H23M3,  Shopping,    Sale,   -22.99
          month, day, year = row[0].split('/')
          month = MONTHS.get(int(month))
          date = str(row[0])
          description = description_mapping.get(row[2], "NULL")
          amount = row[5].get(None, "0.00")
          category = category_mapping.get(row[2], "NULL")

          insert_query = """
              INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
              VALUES (?, ?, ?, ?, ?, ?, "Chase", "Credit")  
          """
          cursor.execute(insert_query, (year, month, date, description, amount, category))

  cursor.connection.commit()

###################################################################################### remove_duplicate
def remove_duplicate(cursor):
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

#######################################################################################################
################################################################################################## Main
#######################################################################################################
def main():
    data_folder_path = "data"
    database_file = "main.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    create_table(cursor)
    read_files(cursor, data_folder_path)
    remove_duplicate(cursor)

    connection.commit()
    connection.close()

    print("Success")

if __name__ == "__main__":
  main()