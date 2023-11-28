print('Welcome to StartGame! \nStartGame is a text based role-playing game.\nRespond to questions by typing in any of the capitalized words in the question.')
create_or_random = True
def Start_Game_Prompt():
    Ready_Start = input('Start Game? \nYES or NO \n')
    if Ready_Start == 'YES':
        create_or_random = input('CREATE character or play a RANDOM build? \n')
        if create_or_random == 'CREATE':
            create_or_random = True
            return 
        elif create_or_random == 'RANDOM':
            create_or_random = False
            return
    elif Ready_Start == 'NO':
        return 
    else: 
        print('Input not valid \n')

while Start_Game_Prompt():
    pass
def Create_Character():
    char_class = input('Do you want to play a SORCERER or PALADIN?\n')
while Create_Character():
    pass
