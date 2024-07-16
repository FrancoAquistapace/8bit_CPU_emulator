# Here we define all of the binary logic required

def to_int(b):
    return int(b, base=2)

def bin_sum(a, b, bits=16):
    a_digits = [int(x) for x in list(a.replace('0b', ''))]
    b_digits = [int(x) for x in list(b.replace('0b', ''))]
    c_digits = []
    c_overflows = ['0']

    # Check consistency
    if len(a_digits) > bits or len(b_digits) > bits:
        print('Error: length of operands is bigger than amount of bits in operation.')
        return
    
    # Do sum
    sum_range = min([bits, len(a_digits), len(b_digits)])
    for i in range(sum_range):
        int_sum = b_digits[-(i+1)] + a_digits[-(i+1)]
        new_val, overflow = int_sum % 2, int_sum // 2
        c_digits.insert(0, str(new_val))
        c_overflows.insert(0, str(overflow))

    # Turn into strings
    c = '0b' + ''.join(c_digits)
    c_over = '0b' + ''.join(c_overflows)

    if '1' in c_overflows:
        # Add overflows
        c = bin_sum(c, c_over)

    return c

def bin_split(b):
    return [int(x) for x in list(b.replace('0b', ''))]

def list_to_bin(b_list):
    b_list = [str(b) for b in b_list]
    return '0b' + ''.join(b_list)