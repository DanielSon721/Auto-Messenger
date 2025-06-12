import gspread
import requests
import string

def send_message(message):
  resp = requests.post('http://textbelt.com/text', {
    'phone': number,
    'message': message,
    'key': 'ea31552082a7faddc2e662402c162ad559e0b7acFPbV6rJdoVQFmr6RCXpMfy2ip'
  })
  print(resp.json)

def index_to_letter(index):
    result = ''
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result

def get_target_column(sheet, row, target):

  dates = sheet.sheet1.row_values(row)
    
  column_index = None
  for i, value in enumerate(dates):
    if value.strip() == target:
      column_index = i + 1  # Google Sheets is 1-based
      break
  
  return column_index

def get_target_row(sheet, column, target):

  dates = sheet.sheet1.col_values(column)
    
  column_index = None
  for i, value in enumerate(dates):
    if value.strip() == target:
      row_index = i + 1  # Google Sheets is 1-based
      break
  
  return row_index





if __name__ == '__main__':

  gc = gspread.service_account()

  attendance_tracker = gc.open("Chapter Attendance Tracker")
  contacts = gc.open("Spring 2025 Actives Form (Responses)")

  attendance_data = attendance_tracker.sheet1.get_all_values()
  contact_data = contacts.sheet1.get_all_values()
    
  user_input = input("What would you like to do?\n1) Blast message\n2) Chapter absence notification\n\n-> ")
    
  if user_input == "1":

    message = input("Message: ")

    for row in contact_data:
      name = row[1] + " " + row[2]  # First + Last name
      number = row[3]  # Assuming column D = phone
      # send_message(number, message)
      print(f"Sent message to {name} at {number} with message \"{message}\"")

if user_input == "2":

  target_date = input("Date: ").strip()

  date_column = get_target_column(attendance_tracker, 9, target_date)

  for i in range(len(attendance_data)):
    if attendance_data[i][date_column - 1] == 'U':
      try:
        target_name = attendance_data[i][0].split(' ')[1]  # Assuming column A = full name
        for row in contact_data:
          if len(row) > 2 and row[2].strip() == target_name:  # Assuming column C = last name
            name = row[1] + " " + row[2]  # First + Last name
            number = row[3]  # Assuming column D = phone
            message = f"You were fined $5 for unexcused chapter absence on {target_date}"
            # send_message(number, message)
            print(f"Sent message to {name} at {number} with message \"{message}\"")
            break
      except IndexError:
        continue
