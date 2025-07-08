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

# gets entire column of target cell
def get_target_column(sheet, row, target):

  dates = sheet.sheet1.row_values(row)
    
  column_index = None
  for i, value in enumerate(dates):
    if value.strip().lower() == target.lower():
      column_index = i + 1  # Google Sheets is 1-based
      break
  
  return column_index

# gets entire row of target cell
def get_target_row(sheet, column, target):

  dates = sheet.sheet1.col_values(column)
    
  row_index = None
  for i, value in enumerate(dates):
    if value.strip().lower() == target.lower():
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
  
  active = True # continue/end program

  print("---------------------------------------------------------")
  print("Welcome to the SigPhi Auto Messenger made by Daniel Son!")
  print("---------------------------------------------------------")

  while active:

    time.sleep(1.5)

    print("\n---------------------------")
    print("What would you like to do?")
    print("---------------------------\n")
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

      if confirmation.lower() == "confirm":
        for row in member_data:
          name = row[0] + " " + row[1]  # first + last name
          number = row[2]  # phone number
          # send_message(number, message)
          print(f"Sent message to {name} at {number} with message \"{message}\"")
      else:
        print("Cancelled\n")

    elif user_input == "2":

      target_date = input("\nChapter date: ").strip()
  
      confirmation = input("\nPlease confirm that this is the date of the chapter you wish to fine.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation.lower() == "confirm":

        try:

          date_column = get_target_column(attendance_tracker, 9, target_date)

          for i in range(len(attendance_data)): # loops through every member on given date

            if attendance_data[i][date_column - 1] == 'U':
              target_name = attendance_data[i][0].split(' ')[1]  # gets last name

              for row in member_data: # loops through every members' contact info
                if row[1].strip().lower() == target_name.lower():  # if last name matches
                  name = row[0] + " " + row[1]  # first + last name
                  number = row[2]  # phone number
                  message = f"You were fined $5 for unexcused chapter absence on {target_date}"

                  # send_message(number, message)
                  print(f"Sent message to {name} at {number} with message \"{message}\"")
                  break
        
        except Exception as e:
          print("Error: Invalid chapter date")
      else:
        print("Cancelled\n")

    elif user_input == "3":

      target_people = input("Who do you want to send a message to? ([last name], [last name], [last name]): ").strip()
      target_people = target_people.replace(" ", "").split(',')
      message = input("What is your message?: ")

      confirmation = input("\nPlease confirm that this is the message you wish to send.\nType \"confirm\" to proceed: ")

      print("")

      if confirmation.lower() == "confirm":
        for row in member_data: # loops through every members' contact info
          if row[1].strip().lower() in target_people:
            name = row[0] + " " + row[1]  # first + last name
            number = row[2]  # phone number
            # send_message(number, message)
            print(f"Sent message to {name} at {number} with message \"{message}\"")

    elif user_input == "4":

      confirmation = input("\nPlease confirm that you wish to send every member their dues breakdown.\nType \"confirm\" to proceed: ")

      if confirmation.lower() == "confirm":

        for row in member_data: # loops through every members' contact info

          name = row[0] + " " + row[1]
          number = row[2]

          base_due = 620
          tenant_discount = float(row[4]) if row[4] else 0  # already negative
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

          # formats breakdown
          df = pd.DataFrame(data)
          df["Amount"] = df["Amount"].apply(lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x)

          message = f"Dues breakdown for {name}:\n\n\n{df.to_string(index=False)}\n\nText Daniel Son with any questions or concerns."
          # send_message(number, message)
          print(f"Sent message to {name} at {number} with message\n\n{message}")
          print("-----------------------------------------------------------")

    elif user_input == "5":

      active = False

      print("\nQuitting...\n")
      time.sleep(1.5)
  
    else:
      print("\nInvalid choice. Please enter a number to pick your choice.")