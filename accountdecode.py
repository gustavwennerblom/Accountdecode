import csv
import re

counter = 0
XMLerr = 0
Inx_err = 0
UBL_err = 0

# Interprets a line and returns a dict of results
def interpret(line):
    global Inx_err
    global result
    # throw away xml junk
    if re.findall("<.*>", line):
        raise ValueError("XML caught")
        return None

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
    # Find the coordinates of the value field
    for key in result:
        try:
            keyindex= re.findall("{}.[A-Z][^A-z]*".format(key), line)[0].split(":")    # Finds the keys and splits on the colons
        # The except block catches absence of keys and trigges next iteration of the loop
        except IndexError:
            Inx_err += 1
            continue

        if keyindex[-2]=="-1":        # "-1" being the notation for no value for the field name. Triggers next iteration.
            continue
        else:
            result[key]=content_string[int(keyindex[2]):int(keyindex[2])+int(keyindex[3])]
    return result

# Processes the interpreted results (dict) and outputs to stdout or to a new csv file (default)
def process(line_dict, keyorder, format="csv"):
    global result
    assert isinstance(line_dict, dict)
    if format=="stdout":
        for key, value in line_dict.items():
            print("{0}: {1}".format(key, value))
        print("---")

    if format=="csv":
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        with open("UserAccounts-{}.csv".format(timestamp), "a") as f:
            writer = csv.DictWriter(f, keyorder)
            writer.writerow(line_dict)
            f.close()

if __name__ == "__main__":
    f = open("business_users_2.csv", "r", encoding="utf_8")
    keyorder = ("FirstName",
                "LastName",
                "Email",
                "OrganizationName",
                "OrganizationNumber",
                "Department",
                "Address",
                "City",
                "ZipCode")
    try:
        # read away first line in source file
        f.readline()

        for line in f:
            try:
                line_dict = interpret(line)
            except ValueError as error:
                XMLerr += 1
                #print(repr(error))
                continue
            process(line_dict, keyorder, format="csv")
            counter +=1
    except FileNotFoundError as error:
        print(repr(error))
    f.close()

    print("Finished with {0} successful interprets, \n\t {1} XML lines filtered, \n\t {2} IndexErrors (i.e. missing dict keys) \n\t {3} UBL errors".format(counter, XMLerr, Inx_err, UBL_err))
    #print(line)


