import dice

def test():
    def g(s, res):
        assert(dice.execute(s) == dice.execute(res))

    with open("tests.txt", "r") as file:
        file.readline()
        for line in file:
            print(line)
            line = line.strip().split()
            if len(line) == 2:
                yield g, line[0], line[1]
            elif len(line) == 0:
                continue
            else:
                raise Exception("Badly formatted tests.txt file.")
