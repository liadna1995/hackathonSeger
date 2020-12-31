import msvcrt

def main():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("Key is {}".format(key))


if __name__ == '__main__':

    main()