def load_processed_links(filepath, return_set):
    with open(filepath, 'r') as file:
        for line in file:
            return_set.add(line.strip())


def load_links_stack(filepath, return_array):
    with open(filepath, 'r') as file:
        for line in file:
            return_array.add(line.strip())


def store_links(filepath, array):
    with open(filepath, 'w') as file:
        for line in array:
            file.write(line + '\n')
