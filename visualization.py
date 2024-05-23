import matplotlib.pyplot as plt

# Function to visualize a trie
def visualize_trie(trie):
    # Visualization helper function
    def _visualize_helper(node, x_offset, y_offset, depth):
        if not node:
            return

        # Plotting current node
        num_children = len(node['children'])
        child_offset = x_offset - 0.5 * (num_children - 1)
        for char, child in node['children'].items():
            child_x_offset = child_offset + list(node['children']).index(char)

            # If end of word, node color black with white text to make it more distinguished
            if child['is_end_of_word']:
                plt.scatter(child_x_offset, y_offset - depth, marker='s', s=200, color='black')
                plt.text(child_x_offset, y_offset - depth, char, ha='center', va='center', color='white')
            else:
                plt.text(child_x_offset, y_offset - depth, char, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))
            plt.plot([x_offset, child_x_offset], [y_offset, y_offset - depth], 'b-')
            _visualize_helper(child, child_x_offset, y_offset - depth, depth + 1)

    # Initializing visualization
    plt.figure(figsize=(12, 6))
    plt.axis('off')

    # Calling visualization helper function
    _visualize_helper(trie, 0, 0, 1)

    # Showing the visualization
    plt.show()