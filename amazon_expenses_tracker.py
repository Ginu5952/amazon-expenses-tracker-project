import re 
import time
from datetime import datetime
import sys

# Colors

RESET = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'

# Font Styles

BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'


# Global variables

user_name = input(YELLOW + ITALIC + '\nEnter your name: ' + RESET)
user_number = 0
choice = 0
purchase_details = dict()
temporary_list = list()


# Validating password

def validate_credentials(pswd):

    validation_pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!])(?!.*[:_-])(?!.*\s).{8,}$'

    if re.match(validation_pattern,pswd):
        return True
    else:
        return False

    
def valid_password():

    password_attempt = 0
    while True:
        print('\n')
        password = input(YELLOW + ITALIC + 'Enter the password: ' + RESET)

        if validate_credentials(password):
            return password
        else:
            password_attempt += 1
            print('\n')
            print(RED + BOLD + 'Invalid password! Please Try again with valid password\n' + RESET) 
            if password_attempt == 3:
                print('\n')
                print(RED + BOLD + "You've used all attempts. Please wait for 5 seconds........." + RESET)
                time.sleep(5)
            elif password_attempt > 3:
                print(RED + 'Please register again.......' + RESET)
                print('\n')
                break

# Validating Mobile Number            

def validate_mobile_number(mobile_number):

    mob_validation_pattern = r'^\+49\d{11}$'

    if re.search(mob_validation_pattern,mobile_number):
        
        return True
    else:
        return False

validPassword = valid_password()

def check_mobile_number():
    while True:
        print('\n')
        user_mobile_number = input(GREEN + ITALIC + 'Please enter phone number to continue: ' + RESET) 
        
        if validate_mobile_number(user_mobile_number):
            
            return user_mobile_number
        else:
            print('\n')
            print(RED + 'invalid country code or it should be an 11 digit number.' + RESET) 

# Menu Choices
            
def choose(choices):
    if choices == '1':
            
            saved_details = enter_your_choice()
            
            if saved_details is not None and len(saved_details) == 5:
                print('\n')
                print(GREEN + 'Purchase saved*******' + RESET)
                temporary_list.append([saved_details.copy()])
                menu()
            else:
                
                print('Purchase not saved')
                   
    elif choices == '2':
        print('\n')
        print(GREEN + 'Generating report...' + RESET)
        print('...')
        time.sleep(2)
        
        if not temporary_list:
            print('You need to purchase atleast one item inorder to generate report')  
        else: 
            generate_amazon_report()
            print('\n')
            menu()   

    elif choices == '3':
        
        print('\n')
        user_input = input(RED + BOLD + "Are you sure you want to quit? [Y/N]: " + RESET).strip().lower()
    
        if user_input == 'y':
            print(RED + ITALIC + '\nQuitting program...' + RESET)  
            time.sleep(1)
            print('\n')
            print(BLUE + BOLD + f'Thank you for your visit, {user_name.title()}. Goodbye!\n' + RESET) 
            for i in range(len(user_name.title())):
                print(GREEN + BOLD + " " * i + user_name[i] + RESET)
            sys.exit()
        elif user_input == 'n':
            print('\n')
            print(GREEN + BOLD + "Cancelled. Continuing..." + RESET)
            menu()
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
        
    else:
        print(RED + ITALIC + 'invalid choice press a valid choice' + RESET)  
        menu()
           

 # Validating date,item,cost,weight,quantity
            
def validate_date(datee):

    date_pattern = r'^(0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])[-/]\d{4}$'
    if re.search(date_pattern,datee):
        modified = re.sub(r'-', '/', datee)
        purchase_details['date'] = modified
        return True
    else:
        return False
    
def validate_item(itm):

    if len(itm) > 3:
        return True
    else:
        return False

def validate_cost(price):
    
    if price.replace('.', '', 1).isdigit():  # Check if the string is a valid float
        cost = float(price)
        if cost > 0:
            return cost
        else:
            print('\n')
            print('Cost shold be greater than 0')
    else:
        print('\n')
        print('Cost should be a integer or float')
        return None
    
def validate_weight(weightt):
    if weightt.replace('.', '', 1).isdigit():
        weight = float(weightt)
        if weight >= 0:
            return weight
    print('Invalid weight format! Please enter a valid non-negative number.')
    return None  

def validate_quantity(quantityy):
    if quantityy.isdigit():
        quantity = int(quantityy)
        if quantity >= 1:
            return quantity
    print('Invalid quantity format! Please enter a valid integer greater than or equal to 1.')
    return None 
          
# Input User's choice
          
def enter_your_choice():
       
       while True:
        print('\n')
        date = input(YELLOW + ITALIC + 'Enter the date of the purchase (MM/DD/YYYY) or (MM-DD-YYYY): ' + RESET)  
        
        if validate_date(date):
            while True:
                item = input(YELLOW + ITALIC + 'Enter the item purchased: ' + RESET)    
                if validate_item(item):
                    while True:
                        cost_str = input(YELLOW + ITALIC + 'Enter the cost of the item in Euro: ' + RESET)
                        cost = validate_cost(cost_str)
                        if cost is not None:
                            while True:
                                weightt = input(YELLOW + ITALIC + 'Enter the weight of the item in kg: ' + RESET)
                                weight = validate_weight(weightt)
                                if weight is not None:
                                    while True:
                                        quantityy = input(YELLOW + ITALIC + 'Enter the quantity purchased: ' + RESET)
                                        quantity = validate_quantity(quantityy)
                                        
                                        if quantity is not None:
                                            purchase_details['item'] = item
                                            purchase_details['cost'] = cost
                                            purchase_details['weight'] = weight
                                            purchase_details['quantity'] = quantity
                                            return purchase_details
                                        else:
                                            print('Please enter a valid quantity....')           
                                else:
                                    print('Please enter a valid weight...')
                else:
                    print('\n')
                    print(RED + BOLD + 'Item should be at least 3 characters.' + RESET)    
        else:
            print('\n')
            print('Invalid format! Please Try again with valid format')


# Accessing most expensive and least expensive item

def calculations_amazon_report(collected_details):
   
   
    most_expensive_item = max(collected_details, key=lambda x: x[0]['cost'])
    least_expensive_item = min(collected_details, key=lambda x: x[0]['cost'])
   
    
    for i,j in zip(most_expensive_item,least_expensive_item):
        most_expensive_cost = i['cost'] - i['weight']
        least_expensive_cost = j['cost'] - j['weight']

        if i == j:
            delivery_charge = i['weight'] * i['quantity']
            average_cost = i['cost']/len(collected_details)
            purchase_date = f"{i['date']} to {i['date']}"
        else:
            delivery_charge = (i['weight'] * i['quantity']) + (j['weight'] * j['quantity']) 
            total_cost = i['cost'] + j['cost']
            total_orders = len(collected_details)
            average_cost = total_cost / total_orders
            purchase_date = f"{i['date']} to {j['date']}"
            

        totalSum = most_expensive_cost + least_expensive_cost
        most_expensive = i['item']
        least_expensive = j['item']   

    return most_expensive,least_expensive,delivery_charge,totalSum,most_expensive_cost,least_expensive_cost,average_cost,purchase_date   
    
# Mask Mobile number with ****

def mask_mobile_number(num):

    pattern = r'(\+\d{2})(\d*)(\d{2})'
    result =  re.sub(pattern, lambda match: match.group(1) + '*' * len(match.group(2)) + match.group(3), num)
    return result
                 

# Generating Amazon Report

def generate_amazon_report():

    output = calculations_amazon_report(temporary_list)
    number = mask_mobile_number(user_number)
    today_date = datetime.today().strftime("%m/%d/%Y")
    print(PURPLE + BOLD + '\n\t\t\t-------------------------' + RESET)
    print(PURPLE + BOLD + '\t\t\t| Amazon Expense Report |' + RESET)
    print(PURPLE + BOLD + '\t\t\t-------------------------' + RESET)
    print('\n')
    print(BLUE + ITALIC + f'name: {user_name.title()} \t password: **** \t Tel: {number} \t Date:{today_date}' + RESET)
    print(PURPLE + BOLD + '--------------------------------------------------------------------------------' + RESET)
    print(BLUE + ITALIC + 'DELIVERY CHARGES',BLUE + ITALIC + 'TOTAL ITEM COST',sep='\t' + RESET)
    print(PURPLE + BOLD + f'{round(output[2])} EURO\t\t\t{round(output[3])} EURO\n' + RESET)
    print(BLUE + ITALIC + 'MOST EXPENSIVE',BLUE + ITALIC + 'LEAST EXPENSIVE',sep='\t\t' + RESET)
    print(BLUE + BOLD + f'name: {output[0]}\t\tname: {output[1]}' + RESET)
    print(BLUE + BOLD + f'cost: {round(output[4])} EURO\t\tcost: {round(output[5])} EURO\n' + RESET)
    print(GREEN + ITALIC + f'AVERAGE COST OF ITEM PER ORDER: {round(output[6])} EURO' + RESET)
    print(GREEN + ITALIC + f'PURCHASE DATE RANGE: {output[7]}' + RESET)
    print(PURPLE + BOLD + '---------------------------------' + RESET)
    if output[3] > 500 :
        print(RED + BOLD + 'Note: You have  exceeded the spending limit of 500 EURO' + RESET)
    else:
        print(GREEN + ITALIC + 'Note: You have not exceeded the spending limit of 500 EURO' + RESET)  

 # Creating Menu  
                 
def menu():
        print('\n')
        print(YELLOW + ITALIC + 'What would you like to do?' + RESET)
        print(PURPLE + ITALIC + '1. Enter a purchase' + RESET)
        print(GREEN + ITALIC + '2. Generate a report' + RESET)
        print(RED + BOLD + '3. Quit' + RESET)
        print('\n')
        choice = input(YELLOW + ITALIC + 'Enter your choice (1/2/3): ' + RESET)
        choose(choice)            

if validPassword:

    print('\n')
    print(PURPLE + '\t\tRegistration successful!' + RESET)  
    print(BLUE + '\t\t=======================' + RESET)
    print(PURPLE + '\t\t| Welcome to Amazon! |' + RESET)
    print(BLUE + '\t\t***********************' + RESET)  
    checkMobileNumber = check_mobile_number()  
    user_number = checkMobileNumber

    if checkMobileNumber:
        print('\n')
        print(YELLOW + BOLD + f'Hello, {user_name.title()}! Welcome to the Amazon Expense Tracker!' + RESET)
        menu()
    else:
        print('Unsuccessful')
else:
    print('Unsuccesful')  


#----------------------------------------------------------------------------------------------
    

    
        

    

    
         




       
  
          





       
