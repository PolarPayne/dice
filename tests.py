def test():
    def f(c, mi, ma):
        float(mi), float(ma)
        assert mi != ma
        print(c, mi, ma)

    def g(c, r):
        float(r)
        print(c, r)

    with open("tests.txt", "r") as file:
        file.readline()
        for line in file:
            print(line)
            line = line.strip().split()
            if len(line) == 2:
                yield g, line[0], line[1]
            elif len(line) == 3:
                yield f, line[0], line[1], line[2]
            else:
                raise Exception("Badly formatted tests.txt file.")
