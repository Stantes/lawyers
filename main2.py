import sys


def read_input(file):
    for line in file:
        yield line.split()



# data = read_input(sys.stdin)

with open('lawyers_cards.csv', 'a') as file:
	data = read_input(file)
	print(data)