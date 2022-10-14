import random

if __name__ == '__main__':
    with open("trash", 'w') as f:
        f.write(str(random.Random().random()))
