from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as box
import glob, os, json, random

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title('Flash card selection' )
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=100, height=100)

show = False
frame = Frame(window)

word_box = Listbox(frame)
for name in glob.glob('*.txt'):

    word_box.insert('end', name)

correct_words = Listbox(frame)

temp_list = []
compare_list = []
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - MAIN FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def list_select():
    if word_box.curselection() != ():
        displayed_word.delete("1.0", "end")
        word_list = word_box.get(word_box.curselection())           #file select based on user click
        print(word_box.curselection())
    return word_list

def create_dict():
    word_list = list_select()
    with open(word_list) as f:
        definitions_as_text = f.read()

    return definitions_as_text

def generate_random_word():
    global temp_list, compare_list

    definitions_as_text = create_dict()

    definitions_as_dicts = json.loads(definitions_as_text)      #opens and converts text to a dictionary
    val_list = list(definitions_as_dicts.values())              #creates a list of the values (word)
    key_list = list(definitions_as_dicts.keys())                #creates a list of the keys (definitions)

    definiton_list = list(definitions_as_dicts)                 #turns the dictionary into a list
    word = random.choice(val_list)                              #picks random word from the dictionary
    real_definition = key_list[val_list.index(word)]            #returns the real definition of the chosen word


    if len(compare_list) == len(definiton_list):                #prompts the user to restart or quit
        restart_window()

    elif real_definition in compare_list:                       #recursively generates a new word that has not been answered correctly
            generate_random_word()

    else:                                                       #adds items to a global list
        temp_list.clear()
        temp_list.append(word)
        temp_list.append(real_definition)
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF MAIN FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - SECONDARY FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def show_word():
    global compare_list

    generate_random_word()                                                   #generates a new word
    word = temp_list[0]
    displayed_word.insert(INSERT, word)                             #displays word on screen


def show_definition(widget):
    global compare_list

    widget.pack()                                                   #unhides the correct definition text box widget
    real_definition = temp_list[1]
    answer = input_definition.get("1.0", "end").strip()             #strips user input to get words
    the_answer = f"The correct answer is: {real_definition}"


    if  answer == real_definition:
        correct_words.insert('end', real_definition)                #adds correctly answered words into a list for user to see progress
        compare_list.append(answer)                                 #adds list to internal counter
        correct_definition.insert(INSERT, 'Correct!')               #display 'correct!' to user
    else:
        correct_definition.insert(INSERT, the_answer)               #displays the correct answer to the user


def hide_definition(widget):                                        #hides the display when generating the next word
    global show

    show = False
    widget.pack_forget()


# # # # # #  - CLEARS ALL BOXES -
def clear():                                                        #resets all text boxes
    displayed_word.delete("1.0", "end")
    correct_definition.delete("1.0", "end")
    input_definition.delete("1.0", "end")
    show_word()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - DELETING A SET -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def confirm_delete():
    delete = Toplevel(window)
    delete.geometry("500x200")
    delete.title("Delete ?")

    current_set = list_select()
    current_file_name = current_set.strip('.txt')

    Label(delete, text=f"Are you sure you want to delete {current_file_name}?").place(x=100,y=100)

    yes_button = tk.Button(delete, height = 2,width = 20,text ="Yes", command=lambda: [delete_list(current_set), quit(delete)])
    yes_button.pack()
    no_button = tk.Button(delete, height = 2,width = 20,text ="No", command=lambda: quit(delete))
    no_button.pack()


def delete_list(current_set):
    os.remove(current_set)
    word_box.delete(tk.ANCHOR)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - RESTARTING -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def restart_window():                                               #new top level window asking to restart
    top = Toplevel(window)
    top.geometry("500x200")
    top.title("Restart?")
    Label(top, text="Congrats! You got everything right! Would you like to restart?").place(x=100,y=100)

    restart_button = tk.Button(top, height = 2,width = 20,text ="Restart", command=lambda: restart(top))
    restart_button.pack()

    close_button = Button(top, height = 2,width = 20,text ="Close", command=lambda: quit(window))
    close_button.pack()


# # # # # #  - CLOSES APPLICATION -
def quit(self):
    self.destroy()


# # # # # #  - CLOSES WINDOW AND RESTARTS FLASH DECK -
def restart(self):
    self.destroy()
    correct_words.delete(0, END)                                    #clears correctly answered words list
    compare_list.clear()                                            #clears internal counter
    show_word()                                                     #generates new word
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF SECONDARY FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def create_card():
    flash = {}
#                              *  *  *  *  *  *  *  *  - CREATING CREATE WINDOW -  *  *  *  *  *  *  *  *
    create = Toplevel(window)
    create.title("Flash Card Creator")
    create.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    create_frame = Frame(create)
    file_title = ''

    create_ui = top_level_ui(create, create_frame, file_title, flash)
    create_ui.create_functions(create)


def edit_list():
#                              *  *  *  *  *  *  *  *  - SELECTING FILE -  *  *  *  *  *  *  *  *
    current_set = list_select()
    current_file_name = current_set.strip('.txt')


#                              *  *  *  *  *  *  *  *  - CREATING EDIT WINDOW -  *  *  *  *  *  *  *  *
    edit = Toplevel(window)
    edit.title("Flash Card Editor")
    edit.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    edit_frame = Frame(edit)
#                              *  *  *  *  *  *  *  *  - INITIALIZING DICTIONARY -  *  *  *  *  *  *  *  *
    definitions_as_text = create_dict()
    definitions_as_dicts = json.loads(definitions_as_text)
    val_list = list(definitions_as_dicts.values())
    key_list = list(definitions_as_dicts.keys())
    edit_ui = top_level_ui(edit, edit_frame, current_file_name, definitions_as_dicts)
    edit_ui.edit_functions(edit, current_set, val_list, key_list)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL INTERFACE -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class top_level_ui():
    def __init__(self, window_name, frame_name, a_file_name, dictionary):
        self.window_name = window_name                #root name
        self.frame_name = frame_name
        self.a_file_name = a_file_name
        self.dictionary = dictionary


#                              *  *  *  *  *  *  *  *  - CURRENT WORDS ADDED -  *  *  *  *  *  *  *  *
        self.current_words = Label(frame_name, text="Current Words")
        self.current_words.pack(side=TOP)

        self.current_words = Listbox(frame_name)
        self.current_words.pack(side = LEFT, expand=True)


#                              *  *  *  *  *  *  *  *  - CURRENT DEFINITIONS ADDED -  *  *  *  *  *  *  *  *
        self.current_definitions = Label(frame_name, text="Current Definitions")
        self.current_definitions.pack(side=TOP)

        self.current_definitions = Listbox(frame_name)
        self.current_definitions.pack(side = TOP, expand=True)

        frame_name.pack(side=LEFT)


#                              *  *  *  *  *  *  *  *  - ADD NEW Title -  *  *  *  *  *  *  *  *
        self.new_title_label = Label(window_name, text="Enter new title")
        self.new_title_label.pack(padx=0, pady=5)

        self.new_title = Text(window_name, wrap=WORD, height = 1, width = 20, bg = 'light pink')
        self.new_title.pack(fill="none", expand=TRUE)


#                              *  *  *  *  *  *  *  *  - ADD NEW WORD -   *  *  *  *  *  *  *  *  *
        self.new_word_label = Label(window_name, text="Enter a new word")
        self.new_word_label.pack(padx=0, pady=5)

        self.new_word = Text(window_name, wrap=WORD, height = 1, width = 20, bg = 'light yellow')
        self.new_word.pack(fill="none", expand=TRUE)


#                               *  *  *  *  *  *  *  *  - ADDING NEW DEFINITION -  *  *  *  *  *  *  *  *
        self.new_definition_label = Label(window_name, text="Enter a new definition")
        self.new_definition_label.pack(padx=10, pady=5)

        self.new_definition = Text(window_name, wrap=WORD, height = 5, width = 100, bg = 'light blue')
        self.new_definition.pack(fill="none", expand=TRUE)

        self.delete_set = tk.Button(window_name, height = 2,width = 20,text ="Delete selection", command=lambda: self.word_delete())
        self.delete_set.pack()

        self.current_words.bind('<<ListboxSelect>>', self.word_edit_on_click)


    def create_functions(self, window_name):

#                              *  *  *  *  *  *  *  *  - CREATE BUTTONS - *  *  *  *  *  *  *  *
        self.add_button = tk.Button(window_name, height = 2,width = 20,text ="Add card", command=lambda: self.add('create'))
        self.add_button.pack()

        self.save_button = tk.Button(window_name, height = 2,width = 20,text ="Save set", command=lambda: [save(self.dictionary, self.new_title), quit(window_name), list_select()])
        self.save_button.pack()


    def edit_functions(self, window_name, a_current_set, a_val_list, a_key_list):
        self.a_current_set = a_current_set
        self.val_list = a_val_list
        self.key_list = a_key_list


#                              *  *  *  *  *  *  *  *  - POPULATIIN TEXT BOXES - *  *  *  *  *  *  *  *
        self.new_title.insert(INSERT, self.a_file_name)
        for values in a_val_list:
            self.current_words.insert('end', values)
        for keys in a_key_list:
            self.current_definitions.insert('end', keys)


#                              *  *  *  *  *  *  *  *  - EDIT BUTTONS - *  *  *  *  *  *  *  *
        self.add_button = tk.Button(window_name, height = 2,width = 20,text ="Add card", command=lambda: self.add('edit'))
        self.add_button.pack()
        self.save_button = tk.Button(window_name, height = 2,width = 20,text ="save set", command=lambda: [save(self.dictionary, self.new_title), quit(window_name), list_select()])
        self.save_button.pack()


    def word_edit_on_click(self, event):
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)
        self.new_word.delete("1.0", "end")
        self.new_word.insert(INSERT, data)
        definition = create_dict_list(self.dictionary, data)
        self.new_definition.delete("1.0", "end")
        self.new_definition.insert(INSERT, definition)


    def word_delete(self):
        cursor_selection = self.current_words.curselection()
        word = str(self.new_word.get("1.0", "end").strip())
        definition = self.new_definition.get("1.0", "end").strip()
        self.current_words.delete(cursor_selection)
        self.current_definitions.delete(cursor_selection)
        del self.dictionary[definition]


    def add(self, method):
        if method == 'create':
            self.added_word = self.new_word.get("1.0", "end").strip()
            self.added_definition = self.new_definition.get("1.0", "end").strip()
            self.dictionary.update({self.added_definition:self.added_word})
            self.current_words.insert('end', self.added_word)
            self.current_definitions.insert('end', self.added_definition)
            self.new_word.delete("1.0", "end")
            self.new_definition.delete("1.0", "end")
        else:
            with open(self.a_current_set, 'a') as fp:
                self.added_word = self.new_word.get("1.0", "end").strip()
                self.added_definition = self.new_definition.get("1.0", "end").strip()
                self.dictionary.update({self.added_definition:self.added_word})
                self.current_words.insert('end', self.added_word)
                self.current_definitions.insert('end', self.added_definition)
                self.new_word.delete("1.0", "end")
                self.new_definition.delete("1.0", "end")


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL INTERFACE -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - TOP LEVEL UI FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def create_dict_list(dictionary, word):
    val_list = list(dictionary.values())
    key_list = list(dictionary.keys())
    definition = key_list[val_list.index(word)]
    return definition


def save(dict_name, title):
    file_name = str(title.get("1.0", "end").strip())+".txt"
    with open(file_name, 'w') as f:
        json.dump(dict_name, f)
        word_box.delete(tk.ANCHOR)
        word_box.insert('end', file_name)
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF TOP LEVEL UI FUNCTIONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - DISPLAY -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# # # # # #  - FLASH CARD SETS -
word_box.pack(side = LEFT)
frame.pack(padx = 30, pady = 30)


# # # # # #  - CORRECT WORDS -
correct_words.pack(side=RIGHT)
frame.pack(padx=30, pady=30)


# # # # # #  - CURRENT WORD -
displayed_word = Text(window, wrap=WORD, height = 5, width = 20, bg = 'light yellow')
displayed_word.pack(fill="none", expand=TRUE)


# # # # # #  - HIDDEN ANSWER -
correct_definition = Text(window, wrap=WORD, height = 5, width = 100, bg = 'light green')
if show == True:
    correct_definition.pack(fill="none", expand=TRUE)


# # # # # #  - USER INPUT -
input_definition = Text(window, wrap=WORD, height = 5, width = 100, bg = 'light cyan')
input_definition.pack(fill="none", expand=TRUE)
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF DISPLAY -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - BUTTONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# # # # # #  - DELETE BUTTON -
delete_button = Button(frame, text = 'Delete set', command=confirm_delete)
delete_button.pack(side = BOTTOM , padx = 5)

# # # # # #  - CREATE BUTTON -
create_button = Button(frame, text = 'Create set', command=create_card)
create_button.pack(side = BOTTOM , padx = 5)

# # # # # #  - EDIT BUTTON -
select_button = Button(frame, text = 'Edit', command=edit_list)
select_button.pack(side = BOTTOM , padx = 5)

# # # # # #  - SELECT BUTTON -
select_button = Button(frame, text = 'Select set', command=show_word)
select_button.pack(side = BOTTOM , padx = 5)



# # # # # #  - CHECK ANSWER BUTTON -
answer_button = Button(window, height = 2,width = 20,text ="Check answer", command=lambda: show_definition(correct_definition))
answer_button.pack()


# # # # # #  - NEXY WORD BUTTON -
next_word = Button(window, height = 2,width = 20,text ="Next word", command=lambda: [clear(), hide_definition(correct_definition)])
next_word.pack()
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  - END OF BUTTONS -  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


window.mainloop()
