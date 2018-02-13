# this script is used to generate a table in sql code.
# the output is intended to be copied into a sql console.
import sys

# checks the length of the python command.
if len(sys.argv) != 3:
    print("Usage:  python <csv-filename> <desired-table-name>")
    exit(0)

output = "CREATE TABLE " + sys.argv[2] + '(\n'

# opens the csv
with open(sys.argv[1], 'r') as csv:
    first_line = csv.readline()
    tokenized = first_line.split(',')
    counter = 0

    # extracts the headers out of the first line of the csv.
    for column_header in tokenized:
        counter += 1
        stripped_column = column_header.strip()
        if( stripped_column == '' or  ' ' in stripped_column):
            print("Error: columns must have a name and cannot contain spaces.")
            exit(0)
        output = output + '    ' + stripped_column + ' VARCHAR(255)'
        if( counter < len(tokenized)):
            output = output + ','
        output = output + '\n'
    output = output + ');\n\n'


output = output + '\\copy ' + sys.argv[2] + ' FROM \'' + sys.argv[1] + '\' DELIMITER \',\' CSV HEADER;'

print(output)

