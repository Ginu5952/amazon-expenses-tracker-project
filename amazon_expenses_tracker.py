import re 
import time
from datetime import datetime
import sys

user_name = input('Enter your name:')
user_number = 0
choice = 0
purchase_details = dict()
temporary_list = list()

# Validating password

def validate_credentials(pswd):

    validation_pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}|:<>?~-]).{6,20}$'

    if re.search(validation_pattern,pswd):
        return True
    else:
        return False

# Validating password
    
def valid_password():
    while True:
        password = input('Enter the password:')

        if validate_credentials(password):
            return password
        else:
            print('Invalid password! Please Try again with valid password') 

validPassword = valid_password()

if validPassword:
    print('Registration successful!') 
    print('---------------------')
    print('| Welcome to Amazon! |')
    print('---------------------')  
else:
    print('Unsuccesful')     


# Mobile number Validation

def mask_mobile_number(num):

    pattern = r'(\+\d{2})(\d*)(\d{2})'
    result =  re.sub(pattern, lambda match: match.group(1) + '*' * len(match.group(2)) + match.group(3), num)
    return result
          
def validate_mobile_number(mobile_number):

    mob_validation_pattern = r'^\+49'

    if re.search(mob_validation_pattern,mobile_number):
        
        return True
    else:
        return False
    
# validating user details 
    
def enter_your_choice():
       
       while True:
        date = input('Enter the date of the purchase (MM/DD/YYYY) or (MM-DD-YYYY):')  
        
        if validate_date(date):
            while True:
                item = input('Enter the item purchased:')    
                if validate_item(item):
                    while True:
                        cost_str = input('Enter the cost of the item in Euro:')
                        cost = validate_cost(cost_str)
                        if cost is not None:
                            while True:
                                weightt = input('Enter the weight of the item in kg:')
                                weight = validate_weight(weightt)
                                if weight is not None:
                                    while True:
                                        quantityy = input('Enter the quantity purchased:')
                                        quantity = validate_quantity(quantityy)
                                        
                                        if quantity is not None:
                                            purchase_details['item'] = item
                                            purchase_details['cost'] = cost
                                            purchase_details['weight'] = weight
                                            purchase_details['quantity'] = quantity
                                            return purchase_details
                                        else:
                                            print('Please enter a valid quantity.')           
                                else:
                                    print('Please enter a valid weight.')
                else:
                    print('Item should be at least 3 characters.')    
        else:
            print('Invalid format! Please Try again with valid format')

# Validating date
            
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
            print('Cost shold be greater than 0')
    else:
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
    
       

def generate_amazon_report():

    output = calculations_amazon_report(temporary_list)
    number = mask_mobile_number(user_number)
    today_date = datetime.today().strftime("%m/%d/%Y")
    print('\n\t\t\t-------------------------')
    print('\t\t\t| Amazon Expense Report |')
    print('\t\t\t-------------------------')
    print(f'name: {user_name.title()} \t password: **** \t Tel: {number} \t Date:{today_date}')
    print('----------------------------------')
    print('DELIVERY CHARGES','TOTAL ITEM COST',sep='\t')
    print(f'{round(output[2])} EURO\t\t\t{round(output[3])} EURO\n')
    print('MOST EXPENSIVE','LEAST EXPENSIVE',sep='\t')
    print(f'name: {output[0]}\tname: {output[1]}')
    print(f'cost: {round(output[4])} EURO\tcost: {round(output[5])} EURO\n')
    print(f'AVERAGE COST OF ITEM PER ORDER: {round(output[6])} EURO')
    print(f'PURCHASE DATE RANGE: {output[7]}')
    print('--------')
    if output[4] > 500 :
        print('Note: You have  exceeded the spending limit of 500 EURO')
    else:
        print('Note: You have not exceeded the spending limit of 500 EURO')    

    menu()    


def choose(choices):
    if choices == '1':
            
            saved_details = enter_your_choice()
            if saved_details is not None and len(saved_details) == 5:
                print('Purchase saved')
                temporary_list.append([saved_details.copy()])
                menu()
            else:
                print('Purchase not saved')
                   
    elif choices == '2':

        print('Generating report...')
        print('...')
        time.sleep(2)
        
        if not temporary_list:
            print('You need to purchase atleast one item inorder to generate report')  
        else:
            
            generate_amazon_report()
       
    elif choices == '3':
        print('Quitting program...')  
        time.sleep(1)
        print(f'Thank you for your visit, {user_name.title()}. Goodbye!') 
        sys.exit()
    else:
        print('invalid choice press a valid choice')  
        menu()


def menu():
    
        print('What would you like to do?')
        print('1. Enter a purchase')
        print('2. Generate a report')
        print('3. Quit')
        choice = input('Enter your choice (1/2/3):')
        print('...')
        choose(choice)
    
def check_mobile_number():
    while True:
        user_mobile_number = input('Please enter phone number to continue: ') 
        
        if validate_mobile_number(user_mobile_number):
            
            return user_mobile_number
        else:
            print('invalid country code') 

checkMobileNumber = check_mobile_number()  
user_number = checkMobileNumber


if checkMobileNumber:
    print(f'Hello, {user_name.title()}! Welcome to the Amazon Expense Tracker!')
    menu()

else:
    print('Unsuccessful')


#----------------------------------------------------------------------------------------------
    

    
        

    

    
         




       
  
          





       