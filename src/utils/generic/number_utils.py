def normalize(val, range_before, range_after):
    range_before_length = float(range_before[1] - range_before[0])
    range_after_length = range_after[1] - range_after[0]
    if type(val) is int or type(val) is float:
        return range_after_length * (val - range_before[0])/ range_before_length + range_after[0]
    else:
        return [range_after_length * (elem - range_before[0])/ range_before_length + range_after[0] for elem in val]
