# Name:Prathiksha
# Created Date: 10 June 2022
# Question:
# 1. How many orders did the site receive?
# 2. What was the total amount of the orders?
# 3. Get a distribution of customers who ordered exactly once, exactly twice, and so on up to 4 orders and group the rest as 5 orders and above.

import pandas as pd #pip install pandas
import csv
from tabulate import tabulate #pip install tabulate
from os.path import exists

df = pd.read_csv("customerdata.txt", sep=",")  
df.columns = df.columns.str.replace(' ', '')

CRED = '\033[33m'#yellow color
CEND = '\033[0m'#white color
CGEN = '\033[92m'#green color
CBLU = '\033[34m'#blue color
CRED = '\033[31m'#red color

print(CRED + "\nGiven data:\n" )
print(tabulate(df, headers=["Date","Phone","Name","Amount"]), CEND)

#Output for - Question1
last_column = df.iloc[: , 3:4].sum()
no_order = len(df)
print(CGEN+'\n\nTotal no of orders received is : ',CEND,no_order,"\n")

#Output for - Question2
print(CGEN+'Total amount of order is : RS.',CEND,int(last_column.values),"\n")

#Output for - Question3
new_df = df.groupby(["Phone","Name"])["Phone"].count()
new_df = new_df.sort_values()
df = pd.DataFrame()  
data = {'Total no of orders': new_df} 
df = pd.DataFrame(data)  
j = 0
gruop_one, gruop_two, gruop_three, gruop_four, gruop_five = ([] for i in range(5))
for i in new_df:
    if(i == 1):gruop_one.append(df.iloc[j])
    elif i == 2:gruop_two.append(df.iloc[j])
    elif i == 3:gruop_three.append(df.iloc[j])
    elif i == 4:gruop_four.append(df.iloc[j])
    elif i > 4:gruop_five.append(df.iloc[j])
    j += 1
print(CBLU,gruop_one,"\n\n",gruop_two,"\n\n",gruop_three,"\n\n",gruop_four,"\n\n",gruop_five,"\n")

new_df.to_csv('gruop.csv', header=None)
file_exists = exists('gruop.csv')
if file_exists:
    print(CGEN,"File genereted for Group..\n")
else:
    print(CRED,"Failed to genrate file..\n")
