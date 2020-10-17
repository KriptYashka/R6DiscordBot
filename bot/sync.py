import jager

def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]