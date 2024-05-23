from tkinter import *

def initialize_trie():
    return {'children': {}, 'is_end_of_word': False}

def insert(root, word):
    node = root
    for char in word:
        if char not in node['children']:
            node['children'][char] = initialize_trie()
        node = node['children'][char]
    node['is_end_of_word'] = True

def add_prompted_words():
    prompt = prompt_entry.get()
    words = prompt.split()
    prompted_words.update(words)
    for word in words:
        insert(trie, word)
    print(trie)
    prompt_entry.delete(0, END)

def suggestions(root, prefix):
    suggestions = []
    node = root
    for char in prefix:
        if char not in node['children']:
            return suggestions
        node = node['children'][char]
    _dfs(node, prefix, suggestions)
    return suggestions

def _dfs(node, prefix, suggestions):
    if node['is_end_of_word']:
        suggestions.append(prefix)
    for char, child_node in node['children'].items():
        _dfs(child_node, prefix + char, suggestions)

def initialize_autocomplete(textbox, root):
    suggestion_label = Label(textbox.master, text="")
    suggestion_label.grid(row=5, column=textbox.grid_info()['column'], padx=5, pady=5)

    def on_key_release(event):
        prefix = textbox.get("1.0", "end-1c")
        last_word = prefix.split()[-1]
        suggest = suggestions(root, last_word)
        if suggest:
            suggestion_label.config(text="Suggestions: " + ", ".join(suggest))
        else:
            suggestion_label.config(text="")

    textbox.bind('<KeyRelease>', on_key_release)


def display_words(root):
    def delete_word():
        word = listbox.get(ACTIVE)
        delete_from_trie(trie, word)
        listbox.delete(ACTIVE)

    words = []
    _display_words(trie, "", words)
    
    window = Toplevel(root)
    window.title("Words in Trie")

    listbox = Listbox(window)
    for word in words:
        listbox.insert(END, word)
    listbox.pack()

    delete_button = Button(window, text="Delete", command=delete_word)
    delete_button.pack()

def _display_words(node, prefix, words):
    if node['is_end_of_word']:
        words.append(prefix)
    for char, child_node in node['children'].items():
        _display_words(child_node, prefix + char, words)

def delete_from_trie(root, word):
    node = root
    for char in word:
        node = node['children'][char]
    node['is_end_of_word'] = False

def update_prompt():
    story_prompt.config(text="Story Prompt: " + story_prompt_entry.get("1.0", "end-1c"))
    story_prompt_entry.delete("1.0", END)
    
def calculate_score():
    story = textbox.get("1.0", END)
    story_words = story.split()
    used_words = [word for word in story_words if word in prompted_words]
    score = (len(used_words) / len(prompted_words)*100) + len(story_words)
    score_label.config(text="Score: {:.2f}".format(score))

if __name__ == "__main__":
    root = Tk()
    root.title("The Word Wizards")

    trie = initialize_trie()

    prompted_words = set()

    story_prompt_label = Label(root, text="Enter Prompt for the Story:")
    story_prompt_label.grid(row=0, column=0, padx=5, pady=5)

    story_prompt_entry = Text(root, height=2, width=30)
    story_prompt_entry.grid(row=0, column=1, padx=5, pady=5)

    update_prompt_button = Button(root, text="Update Prompt", command=update_prompt)
    update_prompt_button.grid(row=0, column=2, padx=5, pady=5)

    story_prompt = Label(root, text="")
    story_prompt.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    prompt_label = Label(root, text="Enter words to Dictionary:")
    prompt_label.grid(row=2, column=0, padx=5, pady=5)

    prompt_entry = Entry(root)
    prompt_entry.grid(row=2, column=1, padx=5, pady=5)

    add_prompt_button = Button(root, text="Add Prompted Words", command=add_prompted_words)
    add_prompt_button.grid(row=2, column=2, padx=5, pady=5)

    delete_button = Button(root, text="Delete Word", command=lambda: display_words(root))
    delete_button.grid(row=3, column=2, padx=5, pady=5)

    story_label = Label(root, text="Write your story:")
    story_label.grid(row=4, column=0, padx=5, pady=5)

    textbox = Text(root, height=10, width=50)
    textbox.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
    
    initialize_autocomplete(textbox, trie)
    
    score_button = Button(root, text="Calculate Score", command=calculate_score)
    score_button.grid(row=6, column=1, padx=5, pady=5)

    score_label = Label(root, text="Score: ")
    score_label.grid(row=6, column=2, padx=5, pady=5)

    root.mainloop()
