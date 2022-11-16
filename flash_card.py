import random, os, json


flash = {}
create_new_deck = False
play = False


starting_choice = str(input('Would you like to create a new flash deck or study a current deck? create/study: ')).upper()

# ~~~ Creating a new set ~~~~
if starting_choice == 'CREATE':

    title = str(input("Please enter the title of the flash deck: "))
    create_new_deck = True


    while create_new_deck:
        flash_list = list(flash)
        word = str(input('Enter the name you want to add to the flash card: '))
        meaning = str(input('Enter the definition of the word: '))
        flash.update({meaning:word})
        new_term = str(input("Would you like to enter another term? yes/no: ")).upper()


        if new_term == 'NO':


            with open(f'{title}.txt', 'w') as fp:
                json.dump(flash, fp)
                break

# ~~~ Picking the set ~~~~
elif starting_choice == 'STUDY':


    for list_names in os.listdir():


        if list_names.endswith('.txt'):
            print(list_names)
            list_selection = str(input("What list would you like to study? "))


            with open(f"{list_selection}.txt") as f:
                definitions_as_text = f.read()
                definitions_as_dicts = json.loads(definitions_as_text)      #opens and converts text to a dictionary
                definiton_list = list(definitions_as_dicts)                 #turns the dictionary into a list
                val_list = list(definitions_as_dicts.values())              #creates a list of the values
                key_list = list(definitions_as_dicts.keys())                #creates a list of the keys
                compare_list = []                                           #empty list to compare against the select flash card set
                play = True                                                 #begins the flash card game

# ~~~ Studying the selected set ~~~~

    while play:
        word = random.choice(val_list)                                      #picks random word from dictionary
        real_definition = key_list[val_list.index(word)]                    #returns the definition of the word

#       ~~~ Checks if the word has been added to the list and picks a new word until all words have been picked ~~~
        if real_definition in compare_list and len(compare_list) < len(definiton_list):
            new_word = random.choice(val_list)
            continue

        else:

#           ~~~ Checking if the set has been completed ~~~~

            if len(compare_list) == len(definiton_list):
                restart = str(input("You got everything right! would you like to practice again? type no: ")).upper()

#               ~~~ Restarts the game ~~~~

                if restart == 'YES':
                    compare_list.clear()

#               ~~~ Ends the game ~~~~

                else:
                    play = False

#           ~~~ Outputs a word until the set has been completed ~~~~

            else:
                print(word)
                answer = input()


                if answer == real_definition:
                    compare_list.append(answer)
                    print('Correct! Good job!')


                else:
                    print(f"the correct answer is: {key_list[val_list.index(word)]}")
                    again = str(input("Do you want to continue? type yes/no: ")).upper()

#                   ~~~ Ends the game ~~~~

                    if again == "NO":
                        play = False


else:
    print('invalid input')
