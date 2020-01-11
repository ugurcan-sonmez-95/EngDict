import mysql.connector
from difflib import get_close_matches

### Connects to the MySQL database
connect = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)

### Gets results from the MySQL database
cursor = connect.cursor(dictionary=True)
query = cursor.execute("SELECT Expression FROM Dictionary")
expressions = cursor.fetchall()
expressionslst = []
for expression in expressions:
    expressionslst.append(expression['Expression'])

### Dictionary logic
def definition(word):
    cursor.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{word}'")
    results = cursor.fetchall()
    ### Checks if the word is in the dictionary
    if results:
        return '\n'.join([res["Definition"] for res in results])
    ### Checks for the closest match and asks the user if he/she meant the closest match
    elif len(get_close_matches(word, expressionslst, cutoff=0.8)) > 0:
        closest = get_close_matches(word, expressionslst)[0]
        ans = input(f"Did you mean {closest} ? Enter y for yes, n for no: ")
        ans = ans.lower()
        if ans == 'y':
            cursor.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{closest}'")
            results = cursor.fetchall()
            for res in results:
                return res["Definition"]
        elif ans == "n":
            return "The word does not exist. Please try again."
        else:
            return "Something went wrong!"
    ### If the input is not in the dictionary, the program warns the user
    else:
        return "The word does not exist. Please try again."

### Asks the user for input and gives the user a choice to quit
while True:
    word = input("Enter word or enter q to quit: ")
    if word.lower() != 'q':
        print(definition(word))
    else:
        print("Thank you for using the dictionary.")
        break