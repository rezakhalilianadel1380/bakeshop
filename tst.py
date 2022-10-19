# import string
# import random


# def generate_unique_code(length:int) -> str:
#     "generate unique code " 
#     unique_code=''
#     char_number_symbols=string.ascii_letters+string.digits
#     for i in range(0,length):
#         unique_code+=random.choice(char_number_symbols)
#     return unique_code


# print(generate_unique_code(16))



# from colorama import Fore, Back, Style


# user_rate=0
# bot_rate=0
# print('rock is 1 , paper is 2 , scissors is 3')
# while True:
#     if bot_rate==3 or user_rate==3:
#         break 
#     user_number=int(input("enter your number : "))
#     robot_choice=random.choice([1,2,3])
#     print(f'robot choice is {robot_choice}')
#     if user_number==3 and robot_choice==1:
#         bot_rate+=1
#     elif user_number==1 and robot_choice==3:
#         user_rate+=1
#     elif user_number==3 and robot_choice==2:
#         user_rate+=1
#     elif user_number==2 and robot_choice==3:
#         bot_rate+=1
#     elif user_number==1 and robot_choice==2:
#         bot_rate+=1
#     elif user_rate==2 and robot_choice==1:
#         user_rate+=1
    
# print(f'bot rate is {bot_rate} your rate is {user_rate}')
# if bot_rate>user_rate:
#     print(Fore.RED+'bot win')
# else:
#     print(Fore.GREEN+'user win')

# print(Style.RESET_ALL)



