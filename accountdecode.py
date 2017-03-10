import re
import sys


#Interprets a line and returns a dict of results
def interpret(line):
    # throw away xml junk
    if re.findall("<.*>", line):
        raise ValueError("XML caught")

    content_string = (re.findall("\s.*", line))[0].lstrip()
    result={
        "FirstName":None,
        "LastName":None,
        "Email": None,
        "OrganizationName":None,
        "OrganizationNumber": None,
        "Department": None,
        "Address": None,
        "City": None,
        "ZipCode": None
    }
    #Find location of Organization Number
    for key in result:
        keyindex= re.findall("{}.[A-Z][^A-z]*".format(key), line)[0].split(":")
        #except IndexError as e:
        #    print("Index Error caught for key={0}, when parsing: {1}".format(key, line))
        #    print(repr(e))
        #    #input("WAITING")

        #try:
        if keyindex[-2]=="-1":
            continue
        else:
                #print(content_string)
                #print("Start pos: %s" % str(int(orgno_list[2])))
                #print("End pos: %s" % str(int(orgno_list[2]) + int(orgno_list[3])))
            result[key]=content_string[int(keyindex[2]):int(keyindex[2])+int(keyindex[3])]
        #except UnboundLocalError as e:
        #    print("Error parsing: {0} for key={1}".format(line, key))
        #    print(repr(e))
        #    #input("WAITING")

    return result

#processes the interpreted results in a dict
def process(line_dict, format="stdout"):
    assert isinstance(line_dict, dict)
    if format=="stdout":
        for key, value in line_dict.items():
            print("{0}: {1}".format(key, value))
        print("---")


if __name__ == "__main__":
    f = open("business_users_2.csv", "r", encoding="latin-1")
    counter=0
    XMLerr=0
    Inx_UB_err=0
    try:
        #read away first line
        f.readline()
        for line in f:
            try:
                line_dict = interpret(line)
            except ValueError as error:
                XMLerr += 1
                print(repr(error))
            except IndexError as e:
                #print("Index Error caught for key={0}, when parsing: {1}".format(key, line))
                Inx_UB_err +=1
            except UnboundLocalError as e:
                Inx_UB_err += 1
            process(line_dict, format="stdout")
            counter +=1
    except FileNotFoundError as error:
        print(repr(error))
    f.close()

    print("Finished with {0} successful interprets, {1} XML lines filtered, {2} IndexErrors".format(counter, XMLerr, Inx_UB_err))
    #print(line)


