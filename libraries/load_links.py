# Load processed links to received Set
def load_processed_links(filepath, return_set):
    with open(filepath, 'r') as file:
        for line in file:
            return_set.add(line.strip())


# Load links to be processed into received array
def load_links_stack(filepath, return_array):
    with open(filepath, 'r') as file:
        for line in file:
            return_array.add(line.strip())


# Store links to received filepath
def store_links(filepath, array):
    with open(filepath, 'w') as file:
        for line in array:
            file.write(line + '\n')
