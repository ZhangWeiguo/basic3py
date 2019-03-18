import sys

if __name__ == "__main__":
    d = {}
    for i in sys.argv:
        line = i.split("=")
        if len(line) == 2:
            keyline,value = line[0],line[1]
            if keyline.startswith("--"):
                key = keyline[2:]
                d[key] = value
        
    print(d)