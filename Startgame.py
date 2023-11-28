print('Welcome to StartGame! \nStartGame is a text based role-playing game.\nRespond to questions by typing in any of the capitalized words in the question.')
create_or_random = True
def Start_Game_Prompt():
    Ready_Start = input('Start Game? \nYES or NO \n')
    while Ready_Start is not 'YES':
        if Ready_Start == 'YES':
            create_or_random = input('CREATE character or play a RANDOM build? \n')
            if create_or_random == 'CREATE':
                create_or_random = True
                #need to assign this value to a dictionary that store player info?
                return create_or_random
            elif create_or_random == 'RANDOM':
                create_or_random = False
                return create_or_random
        elif Ready_Start == 'NO':
            return 
        #what do I do when the player selects no? should I close the program?
        else: 
            print('Input not valid \n')
            break
            #I want to print this and then loop back to Ready_Start

while Start_Game_Prompt():
    pass
def Create_Character():
    char_class = input('Do you want to play a SORCERER or PALADIN?\n')
while Create_Character():
    pass
