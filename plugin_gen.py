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

        output_file.write('')
def get_plugin_contents(filename,message_name,proto_file):
    with open(filename, "r") as f:
        lines = f.readlines()

    with open(proto_file, "w") as output_file:
        DeviceStateName = message_name

        output_file.write('package main\n')
        output_file.write('import (\n')
        output_file.write('\t"fmt"\n')
        output_file.write('\t"github.com/gtfierro/xboswave/ingester/types"\n')
        output_file.write('\txbospb "github.com/gtfierro/xboswave/proto"\n')
        output_file.write(')\n')
        output_file.write('func has_device(msg xbospb.XBOS) bool {\n')
        output_file.write('\treturn msg.XBOSIoTDeviceState.'+ DeviceStateName + '!= nil\n')
        output_file.write('}\n')
        output_file.write('var device_units = map[string]string{\n')

        # Create unit map
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
                """
                if desc != "":
                    #print("//%s"%desc)
                    output_file.write("\t//%s\n" % desc)
                if unit != "":
                    #print("//unit: %s"%unit)
                    output_file.write("\t//unit: %s\n" % unit)
                #print("%s %s = %d;"%(datatype, name, i))
                """
                output_file.write('\t"%s":\t"%s",\n'%(name, unit))
        #     words[2], words[3], words[4])
                i+=1
        output_file.write('}\n')
        # Device lookup
        output_file.write('var device_lookup = map[string]func(msg xbospb.XBOS) (float64, bool){\n')
        output_file.write('\n')


        i = 1
        for line in lines[1:]:
            line = line[:-1]
            words = line.split(',')
            #print(words)
            if words[3] == 'TRUE':
                final_name = ""
                name = words[0]
                desc = words[1]
                unit = words[6]
                name_list = name.split("_")
                # In the future make this some sort of flag capitalization is weird with protoc

                if len(name_list) > 1:
                    for x in range(len(name_list)):
                        name_list[x] = name_list[x].capitalize()
                    #print(final_name.join(name_list))
                    name = final_name.join(name_list)
                else:
                    name = name.capitalize()
                for x in range(len(name_list)):
                    name_list[x] = name_list[x].capitalize()
                print(final_name.join(name_list))
                #name = final_name.join(name_list)
                datatype = change_datatype_to_xbos(words[4])
                if words[5] == 'V':
                    continue
                if words[5] == 'W':
                    continue
                if words[4] == 'boolean':
                    output_file.write('\t"%s": func(msg xbospb.XBOS) (float64, bool) {\n'%(name))
                    output_file.write('\t\tif has_device(msg) && msg.XBOSIoTDeviceState.%s.%s != nil {\n'%(DeviceStateName,name))
                    output_file.write('\t\t\tif msg.XBOSIoTDeviceState.%s.%s.Value{\n'%(DeviceStateName,name))
                    output_file.write('\t\t\t\treturn 1, true\n')
                    output_file.write('\t\t\t} else {\n')
                    output_file.write('\t\t\t\treturn 0, true\n')
                    output_file.write('\t\t\t}\n')
                    output_file.write('\t\t}\n')
                    output_file.write('\t\treturn 0, false\n')
                    output_file.write("\t},\n")
                else:
                    output_file.write('\t"%s": func(msg xbospb.XBOS) (float64, bool) {\n'%(name))
                    output_file.write('\t\tif has_device(msg) && msg.XBOSIoTDeviceState.%s.%s != nil {\n'%(DeviceStateName,name))
                    output_file.write('\t\t\treturn float64(msg.XBOSIoTDeviceState.%s.%s.Value), true\n'%(DeviceStateName,name))
                    output_file.write('\t\t}\n')
                    output_file.write('\t\treturn 0, false\n')
                    output_file.write('\t},\n')
        #     words[2], words[3], words[4])
                i+=1
        output_file.write('}\n')


        #put these two functions in a go file somewhere would be better than this
        # Build device function
        output_file.write('func build_device(uri types.SubscriptionURI, name string, msg xbospb.XBOS) types.ExtractedTimeseries {\n')
        output_file.write('\t\n')
        output_file.write('\tif extractfunc, found := device_lookup[name]; found {\n')
        output_file.write('\t\tif value, found := extractfunc(msg); found {\n')
        output_file.write('\t\t\tvar extracted types.ExtractedTimeseries\n')
        output_file.write('\t\t\ttime := int64(msg.XBOSIoTDeviceState.Time)\n')
        output_file.write('\t\t\textracted.Values = append(extracted.Values, value)\n')
        output_file.write('\t\t\textracted.Times = append(extracted.Times, time)\n')
        output_file.write('\t\t\textracted.UUID = types.GenerateUUID(uri, []byte(name))\n')
        output_file.write('\t\t\textracted.Collection = fmt.Sprintf("xbos/%s", uri.Resource)\n')
        output_file.write('\t\t\textracted.Tags = map[string]string{\n')
        output_file.write('\t\t\t\t"unit": device_units[name],\n')
        output_file.write('\t\t\t\t"name": name,\n')
        output_file.write('\t\t\t}\n')
        output_file.write('\t\t\treturn extracted\n')
        output_file.write('\t\t}\n')
        output_file.write('\t}\n')
        output_file.write('return types.ExtractedTimeseries{}\n')
        output_file.write('}\n')
        output_file.write('\n')
        # Build extract function
        output_file.write('func Extract(uri types.SubscriptionURI, msg xbospb.XBOS, add func(types.ExtractedTimeseries) error) error {\n')
        output_file.write('\tif msg.XBOSIoTDeviceState != nil {\n')
        output_file.write('\t\tif has_device(msg) {\n')
        output_file.write('\t\t\tfor name := range device_lookup {\n')
        output_file.write('\t\t\t\textracted := build_device(uri, name, msg)\n')
        output_file.write('\t\t\t\tif err := add(extracted); err != nil {\n')
        output_file.write('\t\t\t\t\treturn err\n')
        output_file.write('\t\t\t\t}\n')
        output_file.write('\t\t\t}\n')
        output_file.write('\t\t}\n')
        output_file.write('\t}\n')
        output_file.write('\treturn nil\n')
        output_file.write('}\n')






def main():

    # Setup signal handler to allow for exiting on Keyboard Interrupt (Ctrl +C)

    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file with details for generating protobuf")
    parser.add_argument("message_name", help="name of message in the protobuf")
    parser.add_argument("plugin_file", help="name of proto file to output")
    args = parser.parse_args()
    csv_file = args.csv_file
    message_name = args.message_name
    plugin_file = args.plugin_file
    get_plugin_contents(csv_file,message_name,plugin_file)

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
