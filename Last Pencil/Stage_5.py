import random

name_one = 'Cris'
name_two = 'Marcelo'
possible_values = ['1', '2', '3']

def bot_strategy(pencil_count):
    global user_input
    if pencil_count % 4 == 0:
        user_input = '3'
    elif pencil_count % 4 == 3:
        user_input = '2'
    elif pencil_count % 4 == 2:
        user_input = '1'
    elif pencil_count == 1:
        user_input = '1'
    else:
        user_input = random.choice(['1', '2', '3'])
    print(user_input)
    return user_input

print('How many pencils would you like to use:')
while True:
    pencil_count = input()
    if pencil_count.isdigit() and int(pencil_count) > 0:
        break
    elif pencil_count == '0':
        print('The number of pencils should be positive')
    else:
        print('The number of pencils should be numeric')
print(f'Who will be the first ({name_one}, {name_two}):')

while True:
    current_player = input()
    if current_player in [name_one, name_two]:
        break
    else:
        print(f'Choose between {name_one} and {name_two}')

print("|" * int(pencil_count))
print(f"{current_player}'s turn:")

pencil_count = int(pencil_count)
while pencil_count > 0:
    if current_player == name_one:
        user_input = input()
        if user_input not in possible_values:
            print("Possible values: '1', '2' or '3'")
        elif int(user_input) > pencil_count:
            print('Too many pencils were taken')
        else:
            pencil_count -= int(user_input)
            current_player = name_one if current_player == name_two else name_two
            if pencil_count == 0:
                break
            print("|" * int(pencil_count))
            print(f"{current_player}'s turn:")
    else:
        bot_strategy(pencil_count)
        pencil_count -= int(user_input)
        current_player = name_one if current_player == name_two else name_two
        if pencil_count == 0:
            break
        print("|" * int(pencil_count))
        print(f"{current_player}'s turn:")

print(f'{current_player} won!')



