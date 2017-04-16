def load_properties(filename):
    r_map = {}
    with open(filename) as file:
        for line in file:
            if (not line.startswith("#")) and '=' in line:
                key, value = line.split("=", 1)
                r_map[key.strip()] = value.strip()

    return r_map
