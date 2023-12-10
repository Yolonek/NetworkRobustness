def read_tuple_data(connections_string):
    connections_string = connections_string.replace('\n', '')
    connections = connections_string.split(' ')
    return int(connections[0]), int(connections[1])