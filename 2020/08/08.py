# PART 1
def first_part(lines):
    acc = 0
    visited_lines = []
    next_line = 0
    while(next_line >= 0 and next_line not in visited_lines):
        visited_lines.append(next_line)
        line = lines[next_line]
        operation, value = line.split(" ")
        value = int(value)
        print("operation", operation, "value", value)
        if operation == "acc":
            acc += value
            next_line += 1
        elif operation == "nop":
            next_line += 1
        elif operation == "jmp":        
            next_line += value
    print('next_line', next_line)
    print('acc', acc)


# PART 2
def second_part(original_lines):
    success = False

    # for line_index in [0,1,5]:
    for line_index in range(len(original_lines)):
        print('line_index', line_index)
        if(success):
            break
        acc = 0
        visited_lines = []
        next_line = 0
        lines = original_lines[::]

        line_to_change = original_lines[line_index]
        operation, value = line_to_change.split(" ")
        value = int(value)
        new_line_changed = line_to_change
        if operation == "jmp":
            new_line_changed = line_to_change.replace("jmp", "nop")
        elif operation == "nop":
            new_line_changed = line_to_change.replace("nop", "jmp")
        else:
            continue
        lines[line_index] = new_line_changed

        while(next_line >= 0):
            visited_lines.append(next_line)
            line = lines[next_line]
            operation, value = line.split(" ")
            value = int(value)
            print("next_line", next_line, "operation", operation, "value", value)
            if operation == "acc":
                acc += value
                next_line += 1
            elif operation == "nop":
                next_line += 1
            elif operation == "jmp":        
                next_line += value
            if next_line in visited_lines:
                success = False
                break
            elif next_line >= len(lines):
                success = True
                break

    print('success', success)
    print('next_line', next_line)
    print('acc', acc)

if __name__ == '__main__':
    file = open("08/08.data.txt", "r")
    # file = open("08/08.data-test.txt", "r")
    lines = file.read().split('\n')
    # first_part(lines)
    second_part(lines)
    file.close()