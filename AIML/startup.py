import aiml
import json
import os

fname = "ngos.json"


def capitalise(s):
    lst = [word[0].upper() + word[1:] for word in s.split()]
    return " ".join(lst)


def addNGO():
    name = capitalise(input("Enter the name of your NGO: "))
    city = capitalise(input("Which cities does your NGO serve? "))
    shelter = input("Does your NGO provide shelter? (y/n) ")
    shelter = 1 if shelter == "y" else 0
    food = input("Does your NGO provide food? (y/n) ")
    food = 1 if food == "y" else 0
    ph = input(
        "Please enter the contact number where migrant workers can reach out to you: "
    )
    ngo = {"name": name, "city": city, "shelter": shelter, "food": food, "contact": ph}
    a = []
    if not os.path.isfile(fname):
        a.append(ngo)
        with open(fname, mode="w") as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(ngo)
        with open(fname, mode="w") as f:
            f.write(json.dumps(feeds, indent=2))
    print("Thank you for your response! To fill another entry, type 'NGO'.")


def listNGO():
    with open(fname) as feedsjson:
        feeds = json.load(feedsjson)
        city = capitalise(input("Which city are you in? "))
        food = capitalise(input("Do you require food? (y/n) "))
        if food == "Y" or food == "YE" or food == "YES":
            matches = searchNGO(city, "food", feeds)
            if matches:
                print("Here are the NGOs in your city that can help with food: ")
                printNGO(matches)
            else:
                print(
                    "Sorry, we currently do not have information about NGOs in"
                    + city
                    + "that can provide food"
                )
        shelter = capitalise(input("Do you require shelter? (y/n) "))
        if shelter == "Y" or shelter == "YE" or shelter == "YES":
            matches = searchNGO(city, "shelter", feeds)
            if matches:
                print("Here are the NGOs in your city that can help with shelter: ")
                printNGO(matches)
            else:
                print(
                    "Sorry, we currently do not have information about NGOs in"
                    + city
                    + "that can provide shelter"
                )
    print(
        "Thank you for using this bot. If you need more assistance, please type 'migrant'."
    )


def searchNGO(city, foodorshelter, parsedJson):
    matches = []
    for entry in parsedJson:
        if city == entry["city"] and entry[foodorshelter]:
            matches.append(entry)
    return matches


def printNGO(matches):
    foodorshelter = ""
    for entry in matches:
        if entry["food"] == 1 and entry["shelter"] == 1:
            foodorshelter = "food and shelter"
        elif entry["food"] == 1:
            foodorshelter = "food"
        elif entry["shelter"] == 1:
            foodorshelter = "shelter"
        else:
            continue
        print(
            "\t* "
            + entry["name"]
            + " provides "
            + foodorshelter
            + ". Contact "
            + entry["contact"]
        )


kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

print(
    "\t- Welcome! This is a service connecting NGOs providing food and shelter with migrant workers who need them. Let us begin.\n\t- Press 1 if you are an NGO.\n\t- Press 2 if you are a migrant worker."
)
while True:
    message = input(">> ")
    output = kernel.respond(message)
    if output == "Thank you for your response! To fill another entry, type 'NGO'.":
        print(
            "Please fill in your responses to the following questions so we can connect you with migrants in need: "
        )
        addNGO()
    if output == "To find another NGO, type 'migrant'.":
        print(
            "Please fill in your responses to the following questions so we can connect you with an NGO: "
        )
        listNGO()
