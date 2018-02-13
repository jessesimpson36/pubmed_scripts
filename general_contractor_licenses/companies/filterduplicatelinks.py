# searches and removes duplicate license numbers.

listOfLicensesWithoutDuplicates = []

with open("organizationLinks.txt", "r") as licenseNumberFile:
    for line in licenseNumberFile:
        if line not in listOfLicensesWithoutDuplicates:
            listOfLicensesWithoutDuplicates.append(line)

with open("listOfNonDuplicateOrganizationLinks.txt", "w") as otherOutput:
    for entry in listOfLicensesWithoutDuplicates:
        print(entry)
        otherOutput.write("https://nclbgc.org/search/" + entry)

