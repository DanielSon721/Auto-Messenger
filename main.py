import gspread
import requests
import pandas as pd
import time

def send_message(number, message):
  resp = requests.post('http://textbelt.com/text', {
    'phone': number,
    'message': message,
    'key': 'ea31552082a7faddc2e662402c162ad559e0b7acFPbV6rJdoVQFmr6RCXpMfy2ip'
  })
  print(resp.json)

def get_target_column(sheet, row, target): # gets entire column of target cell

  dates = sheet.sheet1.row_values(row)
    
  column_index = None
  for i, value in enumerate(dates):
    if value.strip() == target:
      column_index = i + 1  # Google Sheets is 1-based
      break
  
  return column_index

def get_target_row(sheet, column, target): # gets entire row of target cell

  dates = sheet.sheet1.col_values(column)
    
  row_index = None
  for i, value in enumerate(dates):
    if value.strip() == target:
      row_index = i + 1  # Google Sheets is 1-based
      break
  
  return row_index

#######################################################################################################################

if __name__ == '__main__':

  print("\nLoading...\n")

  gc = gspread.service_account()

  attendance_tracker = gc.open("Chapter Attendance Tracker")
  dues = gc.open("Budget Calculations Fall 2025")

  attendance_data = attendance_tracker.sheet1.get_all_values()
  member_data = dues.sheet1.get_all_values()[1:51]
  
  active = True

  print("Welcome to the SigPhi Auto Messenger made by Daniel!")

  while active:

    print("\n\n")

    time.sleep(2)

    print("What would you like to do?\n")
    print("1) Send a blast message")
    print("2) Send out chapter absence and fine notifications")
    print("3) Send a message to specific people")
    print("4) Send dues breakdown")
    print("5) Quit")
    
    user_input = input("\n-> ")
    
    if user_input == "1":

      message = input("\nYour message: ")

      confirmation = input("\nPlease confirm that this is the message you wish to send.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation == "confirm":
        for row in member_data:
          name = row[0] + " " + row[1]  # First + Last name
          number = row[2]  # Assuming column D = phone
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

            for row in member_data:
              if row[1].strip() == target_name:  # Assuming column C = last name
                name = row[0] + " " + row[1]  # First + Last name
                number = row[2]  # Assuming column D = phone
                message = f"You were fined $5 for unexcused chapter absence on {target_date}"

                # send_message(number, message)
                print(f"Sent message to {name} at {number} with message \"{message}\"")
                break
      else:
        print("Cancelled\n")

    elif user_input == "3":

      target_people = input("Who do you want to send a message to? (name, name, name): ").strip()
      target_people = target_people.split(', ')
      message = input("What is your message?: ")

      confirmation = input("\nPlease confirm that this is the message you wish to send.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation == "confirm":
        for row in member_data:
          if row[1].strip() in target_people:
            name = row[0] + " " + row[1]  # First + Last name
            number = row[2]  # Assuming column D = phone
            # send_message(number, message)
            print(f"Sent message to {name} at {number} with message \"{message}\"")
    elif user_input == "4":
      for row in member_data:
        name = row[0] + " " + row[1]
        number = row[2]

        base_due = 620
        tenant_discount = float(row[4]) if row[4] else 0  # Already negative
        senior_discount_rate = float(row[5]) if row[5] else 0  # e.g., -0.25

        # Apply senior discount on base due AFTER tenant discount
        base_after_tenant = base_due + tenant_discount
        senior_discount = base_after_tenant * senior_discount_rate
        national_dues = 200
        ifc_dues = 30
        total_due = base_due + tenant_discount + senior_discount + national_dues + ifc_dues

        data = {
            "Description": [
              "",
              "Chapter dues",
              "Tenant discount",
              "Senior discount",
              "National dues",
              "IFC dues",
              "",
              "TOTAL"
            ],
            "Amount": [
              "",
              base_due,
              tenant_discount,
              senior_discount,
              national_dues,
              ifc_dues,
              "",
              total_due
            ]
        }

        df = pd.DataFrame(data)
        df["Amount"] = df["Amount"].apply(lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x)

        message = f"Dues breakdown for {name}:\n\n\n{df.to_string(index=False)}"
        # send_message(number, message)
        print(f"Sent message to {name} at {number} with message\n\n{message}")
        print("-----------------------------------------------------------")

    elif user_input == "5":

      active = False

      print("\nQuitting...\n")
      time.sleep(2)
  
    else:
      print("\nInvalid choice. Please enter a number to pick your choice.")