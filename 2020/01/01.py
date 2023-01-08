# PART 1
def first_part(lines):
    result_found = False
    for i in range(len(lines)):
        if result_found:
            break
        num = int(lines[i])
        print("i", i, "num", num)
        for j in range(len(lines)):
            if(j!=i):
                num2 = int(lines[j])
                print("j", j, "num2", num2)
                if num + num2 == 2020:
                    print("RESULT", num, num2, num*num2)
                    result_found = True
                    break

# PART 2
def second_part(lines):
    result_found = False
    for i in range(len(lines)):
        if result_found:
            break
        num = int(lines[i])
        print("i", i, "num", num)
        for j in range(len(lines)):
            if result_found:
                break
            if(j!=i):
                num2 = int(lines[j])
                print("j", j, "num2", num2)
                for k in range(len(lines)):
                    if(k!=i and k!=j):
                        num3 = int(lines[k])
                        if num + num2 + num3 == 2020:
                            print("RESULT", num, num2, num3, num*num2*num3)
                            result_found = True
                            break

if __name__ == '__main__':
    file = open("01/01.data.txt", "r")
    lines = file.read().split('\n')
    first_part(lines)
    second_part(lines)
    file.close()