from math import pow
import logging
import gettext
import os
import json
from datetime import datetime


_ = None  # Placeholder
HISTORY = []
def load_history():
    p = "./Projects/calc_history.json"
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):  # Sanity check
                    HISTORY.clear()
                    HISTORY.extend(data)
                else:
                    print("Invalid format in history file. Resetting history.")
                    HISTORY.clear()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Failed to load history: {e}. Resetting history.")
            HISTORY.clear()
    else:
        HISTORY.clear()
def save_history():
    os.makedirs("./Projects", exist_ok=True)
    with open('calc_history.json', 'w', encoding='utf-8') as f:
        json.dump(HISTORY, f, ensure_ascii=False, indent=2)


def history_entry(op, inp, res, err):
    time = datetime.now().isoformat()
    rec = {
       "timestamp": time,
       "operation": op,
        "inputs": inp,
        "result": res,
        "error": err
    }
    HISTORY.append(rec)
    save_history()

def show_history():
    if not HISTORY:
        print("There is no history yet.")
        return
    for i in HISTORY:
        time = i["timestamp"].split("T")[0] + " " + i["timestamp"].split("T")[1][:5]
        print("-" * 30)
        print("Time:      ", time)
        print("Operation: ", i["operation"])
        print("Inputs:    ", i["inputs"])
        print("Result:    ", i["result"])
        print("Error:     ", i["error"])
    print("-" * 30)



def translation(chosen_language):
    global _
    localedir = os.path.join(os.path.dirname(__file__), 'locales')
    try:
        lang = gettext.translation('messages', localedir, [chosen_language])
        _ = lang.gettext  # Use without installing
    except Exception:
        _ = lambda s: s  # Fallback identity function
    
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("calculator.log")
    ]
)

# Function to safely get a number from the user, or "Stop" to stop

def RealNum(x):
    while True:
        try:
            iinput = input(x).strip()  # Ask the user for input and remove spaces around it
            if iinput == _("Stop"):
                logging.info("The user entered 'Stop' to stop input collection for '{x}'")    # If the user types "Stop", stop asking
                return iinput
            return float(iinput)      # Try to convert to a float number
        except ValueError:
            logging.error("Invalid input received: '{iinput}'. Expected a number.")
            print(_("Error: Please enter a number like 1, 2.5, -3.")) # Show this if the input is not a valid number

def Addition():
    numbers = []  # Empty list to store numbers entered by the user
    logging.info("The function 'Addition' started.")
    while True:
        a = RealNum(_("Enter a number or type 'Stop' to stop: "))  # Keep asking for numbers
        if a == _("Stop"):  # Stop when user says "Stop"
            break
        numbers.append(a)  # Add the number to the list
    logging.info("The function Addition has completed successfully.")
    # Return the sum of all numbers
    result = sum(numbers) 
    history_entry(op = "add" , inp=numbers, res=result, err= None)
    return result


def Sub():
    logging.info("The function 'Subtraction' started.")
    numbers = []

    while True:
        a = RealNum(_("Enter a number or type 'Stop' to stop: "))
        if a == _("Stop"):
            break
        numbers.append(a)
    logging.info("The function Subtraction has completed successfully.")
    r = numbers[0] - sum(numbers[1:])
    # We Subtract all other numbers from the first one: a - b - c - ...
    history_entry("sub", numbers, r, None)
    return r

def Multiplication1(numbers):
    x = 1
    for num in numbers:
        x *= num  # Multiply each number one by one
    logging.info("The function multiplication1 has completed successfully.")
    history_entry("multiplication", numbers, x, None)
    return x


def MultiHelper():
    logging.info("The function 'multiplication1' started.")
    numbers = []

    while True:
        a = RealNum(_("Enter a number or type 'Stop' to stop: "))
        if a == _("Stop"):
            break
        numbers.append(a)
    return Multiplication1(numbers)  # Use helper to multiply

def Division():
    logging.info("The function 'Division' started.")
    while True:
        a = RealNum(_("Enter first number: "))
        # You should add handling for "Stop" here, if the user can exit from Division by typing "Stop"
        # Example:
        if a == _("Stop"):
            logging.info("Division cancelled by user for first number.")
            return None # Return None or handle cancellation appropriately

        b = RealNum(_("Enter second number: "))
        # Example:
        if b == _("Stop"):
            logging.info("Division cancelled by user for second number.")
            return None # Return None or handle cancellation appropriately

        try:
            x = a / b  # Try to divide
            logging.info(f"The function Division has completed successfully: {a} / {b} = {x}")
            history_entry("div", [a, b], x, None)
            return x
        except ZeroDivisionError:
            logging.error(f"There was an attempt of division by 0 {a}/{b}. Prompting user again.")
            history_entry("division", [a, b], None, "Division by zero")  
            print(_("Cannot divide by zero. Please try again."))  # Show this if user tries to divide by zero

def power():
    logging.info("The function 'Exponentiation' started.")
    a = RealNum(_("Enter the base number: "))
    # Example: Handle "Stop" cancellation
    if a == _("Stop"):
        logging.info("Exponentiation cancelled by user for base number.")
        return None

    b = RealNum(_("Enter the exponent: "))
    # Example: Handle "Stop" cancellation
    if b == _("Stop"):
        logging.info("Exponentiation cancelled by user for exponent.")
        return None

    result = pow(a,b)
    logging.info("The function 'Exponentiation' has completed successfully: {a} ** {b} = {result}")
    history_entry("power", [a,b], result, None)
    return result


def main():
    lang = input(f"Choose from the languages: en, fr or ar: ")
    if lang  in ["en","fr","ar"]:
        translation(lang)
    logging.info("Calculator application started.")

    load_history()
    # Ask the user which operation to perform
    o = input(_("Choose an operation: add, Subtract, multiply, divide, exponentiate (or 'exit'), or history: ")).strip().lower()

    while True:
        logging.info(f"User selected operation: '{o}'") # Log user's choice

        if o == _("exit"):
            logging.info("User chose to exit. Shutting down application.")
            print(_("Goodbye!"))  # Exit the program
            break

        valid_operations = [_("add"), _("subtract"), _("multiply"), _("divide"), _("exponentiate"),_("history")]
# Updated valid operations
        if o not in valid_operations:
            # If the user didn't enter a valid option
            logging.warning(f"Invalid operation input: '{o}'. Displaying error to user.")
            o = input(_("That's not a valid option. Please choose from: add, Subtract, multiply, divide, exponentiate (or 'exit'), or history: ")).strip().lower()
            continue

        # Perform the chosen operation
        if o == "add":
            print(Addition())
        elif o == "subtract":
            print(Sub())
        elif o == "multiply":
            print(MultiHelper())
        elif o == "divide":
            print(Division())
        elif o == "history":
            show_history()
        elif o == "exponentiate":
            print(power())

            logging.info(f"Operation '{o}' completed, result displayed")
        else:
            logging.info(f"Operation '{o}' was cancelled by user or encountered a handled error.")

        # Ask again for a new operation
        o = input(_("Choose another operation: add, Subtract, multiply, divide, exponentiate (or 'exit'): ")).strip().lower()

# Start the program
main()