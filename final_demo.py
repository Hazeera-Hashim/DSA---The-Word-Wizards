from tkinter import *
from visualization import visualize_trie

# initializes the trie - nested dictionary: 
# conatains a dictionary of child node(s) and a boolean variable indicating if is is the end of word or not
def initialize_trie():
    return {'children': {}, 'is_end_of_word': False}

# inserts words into the trie 
def insert(root, word):
    node = root
    # Traversing through every character in the word
    for char in word:
    # Create a new node for the character, if not already present in the children of the current node
        if char not in node['children']:
            node['children'][char] = initialize_trie()
        # Moveing the child node corresponding to the character
        node = node['children'][char]
    
    # Marking the end of the word
    node['is_end_of_word'] = True

# preprocesses the words that are being added to the trie
def add_words():
    # Getting the words from the user input
    prompt = entry_2.get("1.0", END)
    words = prompt.split()
    
    # Converting words to lowercase for consistency
    words = [word.lower() for word in words]
    print(words)
    prompted_words.update(words)
    
    # Adding each word to the trie
    for word in words:
        insert(trie, word)
    print(trie)
    entry_2.delete("1.0", END)
    
    # Updating the displayed word bank
    word_bank_display(prompted_words)

# gives suggestions when typing 
def suggestions(root, prefix):
    suggestions = []
    node = root
    
    # Traversing the trie based on the prefix
    for char in prefix:
        # If the character is not in the children of the current node, return empty suggestions
        if char not in node['children']:
            return suggestions
        node = node['children'][char]
    
    # Calling depth-first search to find words based on the prefix
    _dfs(node, prefix, suggestions)
    return suggestions

# dfs used to search for words based on prefix
def _dfs(node, prefix, suggestions):
    # If the current node marks the end of a word, add the prefix to suggestions
    if node['is_end_of_word']:
        suggestions.append(prefix)
    
    # Traversing each child node recursively
    for char, child_node in node['children'].items():
        _dfs(child_node, prefix + char, suggestions)

# autocomplete initialized, words predicted while typing (on key release)
def initialize_autocomplete(textbox, root):
    # Creating a label to display suggestions
    suggestion_label = Label(textbox.master, text="", bg="#FDE9FF")
    suggestion_label.place(x=300, y=439.0)

    def on_key_release(event):
        prefix = textbox.get("1.0", "end-1c")
        words = prefix.split()
        if words:
            last_word = words[-1]
             # Get suggestions for the last word in the prefix
            suggest = suggestions(root, last_word)
            if suggest:
                suggestion_label.config(text="Suggestions: " + ", ".join(suggest))
            else:
                suggestion_label.config(text="")
        else:
            suggestion_label.config(text="")
    
    # Binding the on_key_release function to KeyRelease event
    textbox.bind('<KeyRelease>', on_key_release)

# displays the words in the trie when delete button is pressed
def display_words(root):
    # Function to delete a word from the trie and listbox
    def delete_word():
        # Getting the word selected in the listbox
        word = listbox.get(ACTIVE)
        # Deleting the word from the trie
        delete_from_trie(trie, word)
        # Deleting the word from the listbox
        listbox.delete(ACTIVE)

    words = []
    _display_words(trie, "", words)

    # Creating a new window to display the words 
    window = Toplevel(window_2)
    window.title("Words in Trie")

    # Creating a listbox to display the words
    listbox = Listbox(window)
    for word in words:
        listbox.insert(END, word)
    listbox.pack()

    # Creating a delete button to delete selected word
    delete_button = Button(window, text="Delete", command=delete_word)
    delete_button.pack()

# Recursively collects words in the trie
def _display_words(node, prefix, words):
    if node['is_end_of_word']:
        words.append(prefix)
    for char, child_node in node['children'].items():
        _display_words(child_node, prefix + char, words)

# deletes the word from trie
def delete_from_trie(root, word):
    # Removing the word from the set of prompted words
    prompted_words.remove(word)
    node = root
    # Traversing the trie based on the characters in the word
    for char in word:
        node = node['children'][char]
    node['is_end_of_word'] = False
    # Updating the displayed word bank
    word_bank_display(prompted_words)

# updates/displays the prompt given by user
def update_prompt():
    # Get text from entry_1
    prompt_text = entry_1.get("1.0", "end-1c")

    # Clear the text in entry_1 widget
    entry_1.delete("1.0", END)
    
    # Set the text of the story_prompt label
    story_prompt.config(text="Story Prompt: " + prompt_text)

    # Get the required width and height of the label based on the text
    width = story_prompt.winfo_reqwidth()
    height = story_prompt.winfo_reqheight()
    
    # Maximum width to prevent the label from going off the screen
    max_width = 600

    # If the width exceeds the maximum width, wrap the text within the label
    if width > max_width:
        story_prompt.config(wraplength=max_width, justify='left')
        width = max_width

    # Place the label dynamically to ensure it fits on the screen
    story_prompt.place(x=20.0, y=100.0, height=height+50, width=width, anchor="nw")

    
# displays word bank
def word_bank_display(prompted_words):
    # Concatenate all the words into a single string
    words = 'Word bank: ' + ' '.join(prompted_words)

    # Set the text of the label
    word_bank.config(text=words)

    # Adjust label position and size based on the updated text
    width = word_bank.winfo_reqwidth()  # Get the required width of the label
    height = word_bank.winfo_reqheight()  # Get the required height of the label
    max_width = 400  # Maximum width to prevent the label from going off the screen

    # If the width exceeds the maximum width, wrap the text within the label
    if width > max_width:
        word_bank.config(wraplength=max_width, justify='left')
        width = max_width

    # Place the label dynamically to ensure it fits on the screen
    word_bank.place(x=700.0, y=175.0, width=width, height=height+20, anchor="nw")


# calculates the score: percentage of given words used + length of essay
def calculate_score():
    story = entry_3.get("1.0", END)
    story_words = story.split()
    used_words = [word for word in story_words if word in prompted_words]
    score = (len(used_words) / len(prompted_words)*100) + len(story_words)

    # Create a label to display the score
    score_label = Label(window_2, text=f"Score: {score:.2f}")
    score_label.place(x=32.0, y=480.0)  

    score_label.config(
        bg="#FDE9FF",
        fg="#000000",
        font=("Inika", 12)
    )

# displays the start screen
def show_main_screen():
    start_screen_frame.pack_forget()
    main_screen_frame.pack()


if __name__ == "__main__": 
    trie = initialize_trie()
    prompted_words = set()

    # Creates the starting window
    window_1 = Tk()
    window_1.title("The Word Wizards")
    window_1.geometry("1200x600")
    window_1.configure(bg="#FDE9FF")

    # Background for starting window
    canvas = Canvas(
        window_1,
        bg="#FDE9FF",
        height=660,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    background = PhotoImage(
        file="image_w1.png")
    image_1 = canvas.create_image(
        600.0,
        226.0,
        image=background
    )

    # Start button on the starting window
    start_btn = PhotoImage(
        file="button_w1.png")
    button_1 = Button(
        image=start_btn,
        borderwidth=0,
        highlightthickness=0,
        command=window_1.destroy,
        relief="flat"
    )
    button_1.place(
        x=400.0,
        y=414.0,
        width=343.0,
        height=69.0
    )
    window_1.resizable(False, False)
    window_1.mainloop()

    # Creates the second window
    window_2 = Tk()
    window_2.title("The Word Wizards")
    window_2.geometry("1200x600")
    window_2.configure(bg="#FDE9FF")

    # Start screen frame
    start_screen_frame = Frame(window_2, bg="#FDE9FF")
    start_button = Button(start_screen_frame, text="Start", command=show_main_screen)
    start_button.pack()
    start_screen_frame.pack(expand=True, fill="both")

    # Main screen frame
    main_screen_frame = Frame(window_2, bg="#FDE9FF")

    # Background of the main screen
    canvas = Canvas(
        window_2,
        bg = "#FDE9FF",
        height = 660,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.pack()  
    canvas.place(x = 0, y = 0)    
    delete_btn = PhotoImage(
    file="button_1.png")
    button_1 = Button(
    image=delete_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: display_words(trie),
    relief="flat"
    )

    # Srory Prompt entry
    enter_prompt = PhotoImage(
        file="image_2.png")
    image_2 = canvas.create_image(
        92.0,
        34.0,
        image=enter_prompt
    )
    entry_image_1 = PhotoImage(
        file="entry_1.png")
    entry_bg_1= canvas.create_image(
        415.0,
        34.0,
        image=entry_image_1
    )
    entry_1 = Text(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=169.0,
        y=20.0,
        width=492.0,
        height=26.0
    )

    # Word Bank entry
    entry_image_2 = PhotoImage(
        file="entry_2.png")
    entry_bg_2 = canvas.create_image(
        422.5,
        79.0,
        image=entry_image_2
    )
    entry_2 = Text(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=184.0,
        y=65.0,
        width=477.0,
        height=26.0
    )
    word_dict = PhotoImage(
        file="image_3.png")
    image_3 = canvas.create_image(
        100.0,
        79.0,
        image=word_dict
    )

    # TextBox and Label for story writing
    canvas.create_text(
        27.0,
        175.0,
        anchor="nw",
        text="Write Your Story:",
        fill="#030303",
        font=("Inika", 12 * -1)
    )
    entry_image_3 = PhotoImage(
        file="entry_3.png")
    entry_bg_3 = canvas.create_image(
        346.5,
        308.0,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        bg="#E4E4E4",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=27.0,
        y=193.0,
        width=639.0,
        height=228.0
    )
    
    # Autocomplete suggestions initialized
    initialize_autocomplete(entry_3, trie)
    
    # Delete button
    button_1.place(
        x=870.0,
        y=65.0,
        width=127.0,
        height=30.0
    )
    bg = PhotoImage(
        file="image_1.png")
    image_1 = canvas.create_image(
        592.0,
        485.0,
        image=bg
    )

    # Update prompt button
    update_btn = PhotoImage(
        file="button_2.png")
    button_2 = Button(
        image=update_btn,
        borderwidth=0,
        highlightthickness=0,
        command=update_prompt,
        relief="flat"
    )
    button_2.place(
        x=700.0,
        y=20.0,
        width=127.0,
        height=29.0
    )

    # Score button
    score = PhotoImage(
        file="button_3.png")
    button_3 = Button(
        image=score,
        borderwidth=0,
        highlightthickness=0,
        command=calculate_score,
        relief="flat"
    )
    button_3.place(
        x=31.0,
        y=439.0,
        width=127.0,
        height=29.0
    )
    
    # Add words button
    add_btn = PhotoImage(
        file="button_4.png")
    button_4 = Button(
        image=add_btn,
        borderwidth=0,
        highlightthickness=0,
        command=add_words,
        relief="flat"
    )
    button_4.place(
        x=700.0,
        y=65.0,
        width=127.0,
        height=29.0
    )

    # Visualize trie button
    button_image_5 = PhotoImage(
        file=("button_5.png"))
    visualize_btn = Button(
        image= button_image_5, 
        text = 'visualize',
        borderwidth=0,
        highlightthickness=0,
        command=lambda: visualize_trie(trie),
        relief="flat"
    )
    visualize_btn.place(
        x=870.0,
        y=20.0,
        width=127.0,
        height=29.0
    )

    # Label to display the story prompt when update prompt is clicked
    story_prompt = Label(
        window_2,  
        text="",
        bg="#FDE9FF",
        fg="#030303",
        font=("Inika", 10)
    )

    # Label to display the word bank when add words is clicked
    word_bank = Label(
        window_2,  
        text="",
        bg="#FDE9FF",
        fg="#030303",
        font=("Inika", 10)
    )
    
    window_2.resizable(False, False)
    window_2.mainloop()