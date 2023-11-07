import sys


def remove_docstring(myfile, output_file):
    fileOpening = open(myfile, 'r')
    fileWriting = open(output_file, 'w')
    for line in fileOpening:
        if line.strip().startswith('"""') or line.strip().startswith("'''") or len(line.strip()) == 0:
            continue
        else:
            fileWriting.write(line)

    fileOpening.close()
    fileWriting.close()




if __name__ == '__main__':
    if len(sys.argv) > 0:
        remove_docstring(sys.argv[1], sys.argv[2])
    else:
        input_file = input("Enter name of the file to format")
        output_file = input("Enter name of the output file")
        remove_docstring(input_file, output_file)
