import pandas as pd
import argparse
import csv


# Main function will be called when file is executed
def change_datatype_to_xbos(t):
    if 'double' in t:
        return 'Double'
    if 'dobule' in t:
        return 'Double'
    if 'int' in t:
        return 'Int64'
    if 'float' in t:
        return 'Double'
    elif t == 'boolean':
        return 'Bool'
    else:
        return t

def get_proto_contents(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    i = 1
    for line in lines[1:]:
        line = line[:-1]
        words = line.split(',')
        if words[5] == 'V':
            continue
        if words[5] == 'W':
            continue
        #if words[4] == 'boolean':
        #    continue
        if words[3] == 'TRUE':
            name = words[0]
            desc = words[1]
            unit = words[6]
            if words[4] == 'string':
                #print(name + "  =  output['" + name + "'],")
                print(name + "  =  output.get('" + name + "',None),")
                continue
            datatype = change_datatype_to_xbos(words[4])
            print(name + "  =   types." + datatype + "(value=" + "output.get('" + name + "',None)),")
            #precipIntensity = types.Double(value=output.get('precipIntensity', None))



def main():

    # Setup signal handler to allow for exiting on Keyboard Interrupt (Ctrl +C)

    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file with details for generating protobuf")
    args = parser.parse_args()
    csv_file = args.csv_file
    get_proto_contents(csv_file)


    return

if __name__ == "__main__":
    main()
