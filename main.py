from yacc import yacc, parse_and_execute

# filename = input("Enter filename: ")
filename = "demo.paint"

try:
    with open(filename, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f"File '{filename}' not found.")
    exit(1)

parse_and_execute(data, filename)