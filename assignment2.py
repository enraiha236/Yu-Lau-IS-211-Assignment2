import argparse as a
import urllib.request as u
import logging as l
import datetime as d

def downloadData(url):
    response = u.urlopen(url)
    data = response.read().decode("utf-8")
    return data

def processData(file_content):
    personData = {}
    logger = l.getLogger ("assignment 2")

    lines = file_content.strip().split("\n")

    for i,line in enumerate(lines,start = 1):
        try:
            parts = line.split(",")
            id_num = int(parts[0].strip())
            name = parts[1].strip()
            birthday_str = parts[2].strip()
            birthday = d.datetime.strptime(birthday_str,"%d/%m/%Y").date()

            personData[id_num] = (name, birthday)
        except Exception:
            logger.error(
                "Error process line #%d for ID #%s",
                i, 
                parts[0].strip() if parts else "UNKNOWN"
            )        
    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print("Person #{} is {} with a birthday of {}".format(
            id, name, birthday.strftime("%Y%m%d")))
    else:
        print("No user found.")

def main(url):
    print(f"Running main with URL = {url}...")
    l.basicConfig(
        filename = "errors.log",
        level = l.ERROR,
        format = "%(message)s"
    )

    try:
        csvData = downloadData(url)
    except Exception as e:
        print (f"Error downloading data: {e}")
        return
    
    personData = processData(csvData)

    while True:
        try:
            user_input = int(input("Enter an ID to lookup (<=0 to exit)"))
        except ValueError:
            print("Invalid input. Please enter a numeber.")
            continue
        
        if user_input <= 0:
            break
        displayPerson(user_input,personData)

if __name__ == "__main__":
    """Main entry point"""
    parser = a.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)