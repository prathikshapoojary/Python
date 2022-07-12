import sys
from colorama import Fore

file1 = sys.argv[1]
file2 = sys.argv[2]
f1 = open(file1, "r")  
f2 = open(file2, "r")  
  
i = 0
for line1 in f1:
    i += 1
    for line2 in f2:
        if line1 == line2:  
            print(Fore.WHITE + "Line ", i,":", Fore.GREEN + " Matched")       
        else:
            print("Line ", i, ":")
            print(Fore.RED + "\tMismatch found :File ",file1," :", line1, end='')
            print(Fore.RED + "\tMismatch found :File ",file2," :", line2, end='')
        break
  
f1.close()                                       
f2.close()   
