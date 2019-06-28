import pandas as pd
import argparse
import csv


# Main function will be called when file is executed
def change_datatype_to_xbos(t):
    if t == 'dobule':
        return 'Double'
    if t == 'double':
        return 'Double'
    if 'float' in t:
        return 'Double'
    elif t == 'boolean':
        return 'Bool'
    elif t == 'int':
        return 'Int64'
    else:
        return t

def get_proto_contents(filename,message_name,proto_file):
    with open(filename, "r") as f:
        lines = f.readlines()

    with open(proto_file, "w") as output_file:
        output_file.write('syntax = "proto3";\n')
        output_file.write('package xbospb;\n')
        output_file.write('import "nullabletypes.proto";\n')
        output_file.write('message %s {\n' % message_name)
        i = 1
        for line in lines[1:]:
            line = line[:-1]
            words = line.split(',')
            #print(words)
            if words[3] == 'TRUE':
                name = words[0]
                desc = words[1]
                unit = words[6]
                datatype = change_datatype_to_xbos(words[4])
                if words[5] == 'V':
                    continue
                if words[5] == 'W':
                    continue
                #if (datatype == 'Bool'):
                #    continue
                if desc != "":
                    #print("//%s"%desc)
                    output_file.write("\t//%s\n" % desc)
                if unit != "":
                    #print("//unit: %s"%unit)
                    output_file.write("\t//unit: %s\n" % unit)
                #print("%s %s = %d;"%(datatype, name, i))
                output_file.write("\t%s %s = %d;\n"%(datatype, name, i))
        #     words[2], words[3], words[4])
                i+=1
        output_file.write('}\n')



def main():

    # Setup signal handler to allow for exiting on Keyboard Interrupt (Ctrl +C)

    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file with details for generating protobuf")
    parser.add_argument("message_name", help="name of message in the protobuf")
    parser.add_argument("proto_file", help="name of proto file to output")
    args = parser.parse_args()
    csv_file = args.csv_file
    message_name = args.message_name
    proto_file = args.proto_file
    get_proto_contents(csv_file,message_name,proto_file)

    """
    print(csv_file)
    df = pd.read_csv(csv_file)
    print(df.head(5))
    print(df.shape[0])
    """
    """
    for x in range(df.shape[0]):
        print(df.iloc[x][''])
    """
    #print("message IslandController {")

    return

if __name__ == "__main__":
    main()
"""
    //
    //unit:
    double ac_voltage_ca = 24;
"""
