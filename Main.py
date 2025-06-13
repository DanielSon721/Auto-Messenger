import gspread
import requests
import string

def send_message(message):
  resp = requests.post('http://textbelt.com/text', {
    'phone': number,
    'message': message,
    'key': 'textbelt'
  })
  print(resp.json)

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
    
  row_index = None
  for i, value in enumerate(dates):
    if value.strip() == target:
      row_index = i + 1  # Google Sheets is 1-based
      break
  
  return row_index

#######################################################################################################################

if __name__ == '__main__':

  gc = gspread.service_account()

  attendance_tracker = gc.open("Chapter Attendance Tracker")
  contacts = gc.open("Spring 2025 Actives Form (Responses)")

  attendance_data = attendance_tracker.sheet1.get_all_values()
  contact_data = contacts.sheet1.get_all_values()
  contact_data.pop(0)
  
  active = True

  print("\nWelcome to the SigPhi Auto Messenger made by Daniel!")

  while active:

    print("\n\n\nWhat would you like to do?")
    print("1) Send a blast message")
    print("2) Send out chapter absence and fine notifications")
    print("3) Send a message to specific people")
    print("4) Quit")
    user_input = input("\n-> ")
    
    if user_input == "1":

      message = input("\nYour message: ")

      confirmation = input("\nPlease confirm that this is the message you wish to send.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation == "confirm":
        for row in contact_data:
          name = row[1] + " " + row[2]  # First + Last name
          number = row[3]  # Assuming column D = phone
          # send_message(number, message)
          print(f"Sent message to {name} at {number} with message \"{message}\"")
      else:
        print("Cancelled\n")

    elif user_input == "2":

      target_date = input("\nChapter date: ").strip()
  
      confirmation = input("\nPlease confirm that this is the date of the chapter you wish to fine.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation == "confirm":

        date_column = get_target_column(attendance_tracker, 9, target_date)

        for i in range(len(attendance_data)):

          if attendance_data[i][date_column - 1] == 'U':
            target_name = attendance_data[i][0].split(' ')[1]  # Assuming column A = full name

            for row in contact_data:
              if row[2].strip() == target_name:  # Assuming column C = last name
                name = row[1] + " " + row[2]  # First + Last name
                number = row[3]  # Assuming column D = phone
                message = f"You were fined $5 for unexcused chapter absence on {target_date}"

                # send_message(number, message)
                print(f"Sent message to {name} at {number} with message \"{message}\"")
                break
      else:
        print("Cancelled\n")

    elif user_input == "3":
      target_people = input("Who do you want to send a message to? (last name): ").strip()
      print("WIP")
    
    elif user_input == "4":
      active = False
  
    else:
      print("\nInvalid choice. Please enter a number to pick your choice.")