name_one = 'Cristiano'
name_two = 'Marcelo'

print('How many pencils would you like to use:')
pencil_count = int(input())
print(f'Who will be the first ({name_one}, {name_two}):')
player_one = str(input())
if player_one == name_one:
    player_two = name_two
else:
    player_two = name_one
print('|' * pencil_count)
while pencil_count > 0:
    print(f"{player_one}'s turn:")
    user_input = int(input())
    pencil_count -= user_input
    if pencil_count <= 0:
        break
    print('|' * pencil_count)
    print(f"{player_two}'s turn:")
    user_input = int(input())
    pencil_count -= user_input
    if pencil_count <= 0:
        break
    print('|' * pencil_count)
    
'''
Much more elegant:

name_one = 'Cristiano'
name_two = 'Marcelo'

print('How many pencils would you like to use:')
pencil_count = int(input())
print(f'Who will be the first ({name_one}, {name_two}):')
current_player = input()
while pencils > 0:
    print("|" * pencil_count)
    print(f"f"{current_player}'s turn:")
    pencil_count -= int(input())
    current_player = name_one if turn == name_two else name_two

'''
