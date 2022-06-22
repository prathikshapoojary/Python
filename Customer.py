# Name:Prathiksha
# Created Date: 15 June 2022
# Question:
# 1. How many orders did the site receive?
# 2. What was the total amount of the orders?
# 3. Get a distribution of customers who ordered exactly once, exactly twice, and so on up to 4 orders and group the rest as 5 orders and above.

records = result = []
with open('customerdata.txt') as file:
    title = next(file).split()
    records = file.readlines()
 
# Question:1 and # Question:2
count = total = 0
res = []

for record_in_records in records:
    if record_in_records == '\n':
        break
    else:
         count += 1
    res = record_in_records.split(',')
    total += int(res[-1])

print("\nReceived ",count," order\n")  
print("Total amount is : Rs/-",total,'\n') 
  
# Question:3
customer_order = {}
for record_in_records in records :
    if record_in_records == '\n':
        break
    record_item = record_in_records.split(", ")
    Phone = record_item[1]                                    #2016-05-01, 9236367267, Takshaka Sandal, 250

    if Phone in customer_order:
        customer_order[Phone] += 1               
    else :
        customer_order[Phone] = 1
        
customer_count_list = [0,0,0,0,0]

for count in customer_order.values(): 
    if count == 1 :customer_count_list[0] += 1
    elif count == 2 :customer_count_list[1] += 1
    elif count == 3 :customer_count_list[2] += 1
    elif count == 4 : customer_count_list[3] += 1
    else :customer_count_list[4] += 1

orders = ["1","2","3","4","5 or more"]

for i in range(5):
    print("Group ",orders[i]," : ", customer_count_list[i])
