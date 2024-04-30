def getData(filePath, name) -> str | list[str] | float | int:
    """
    Inputs: 
    filePath - formatted like a normal file path (forward slash)
    name: str - name of data that you are extracting
    Returns the value from the pyson file with the desired name
    """
    # Raise an exception if the file is not pyson-compatible
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    foundValue = None
    foundType = None
    # Loop through the lines in the file
    for line in open(filePath, "r").read().split("\n"):
        # Split the pyson value stored into [name, type, value]
        splitted = line.split(":")
        # If the name is correct, store the value and type
        if splitted[0] == name:
            foundValue = splitted[2]
            foundType = splitted[1]
            break
    # If the name desired is not in the file, raise an exception
    if foundValue is None:
        raise Exception(f"Data with name \"{name}\" not found. Maybe try a different file?")
    
    # Check what type it is
    match foundType:
        case "str":
            return str(foundValue)
        case "int":
            return int(foundValue)
        case "float":
            return float(foundValue)
        case "list":
            return foundValue.split("(*)")
        case _:
            raise Exception(f"Invalid pyson type {foundType}")

# Get the list of values from a pyson file
def getWhole(filePath) -> list[str | list[str] | float | int]:
    # Checks whether the file is valid pyson
    if not checkCompatible(filePath):
        raise Exception("File passed to getWhole() is not compatible with pyson format")

    whole: list[str | list[str] | float | int] = []
    for item in open(filePath,"r").read().split("\n"):
        data: list[str] = item.split(":")
        match data[1]:
            case "str":
                whole.append(data[2])
            case "int":
                whole.append(int(data[2]))
            case "float":
                whole.append(float(data[2]))
            case "list":
                whole.append(data[2].split("(*)"))
            case _:
                raise Exception(f"Unknown type {data[1]} in {filePath} found during getWhole()")
    return whole

# Append pyson value to pyson file
# TODO: optimize
def write(filePath: str, name: str, type: str, value: str | list[str] | int | float, mode = "a"):
    # Create the file if it doesn't exist
    open(filePath, "w+").close()

    # Make value be a str
    if isinstance(value, list):
        value = "(*)".join(value)
    if isinstance(value, float) or isinstance(value, int):
        value = str(value)
    if not isinstance(value, str):
        raise Exception("Parameter value has invalid type")

    # Make sure the write mode is either append or write
    if not (mode == "a" or mode == "w"):
        raise Exception("Invalid writing mode, must be 'a' (append) or 'w' (write)")
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    file = open(filePath,"r").read().split("\n")
    names = []

    data = ""
    for item in file:
        data = item.split(":")
        match data[1]:
            case "str" | "int" | "list" | "float":
                names.append(data[0])
            case _:
                raise Exception("Unreachable, type correctness is checked in checkCompatible()")
    if name in names:
        raise Exception("Cannot have two items with the same call.")
    # Checks for .pyson compatability with the new item
    match type:
        case "str" | "list":
            pass
        case "int":
            # Make sure the value is actually an int
            int(value)
        case "float":
            # Make sure the value is actually a float
            float(value)
        case _:
            raise Exception(f"Data type {type} not supported")
    toWrite = "\n" + name + ":" + type + ":" + value
    with open(filePath, mode) as file:
        file.write(toWrite)


def updateData(filePath, name, data):
    # Read in the data
    file = open(filePath, "r")
    fileData = file.read().split("\n")
    file.close()
    # Look through the data to find the value to update
    index = 0
    foundItem = False
    for line in fileData:
        splitted = line.split(":")
        if splitted[0] == name:
            splitted[2] = data
            fileData[index] = ":".join(splitted)
            foundItem = True
            break
        index += 1
    # If no value had the desired name, raise an exception
    if not foundItem:
        raise Exception("Couldn't write to non-existent item")
    # Write out the data
    open(filePath, "w").write("\n".join(fileData))
    return True
            
        
# Returns `true` if the file at filePath is a valid pyson file, and false otherwise.
def checkCompatible(filePath: str) -> bool:
    file = open(filePath,"r").read().split("\n")
    whole = []
    # Go through the items, check if they have correct types, and if there it is [dataname, type, value]
    for item in file:
        data = item.split(":")
        if len(data) != 3:
            return False
        match data[1]:
            case "str" | "int" | "list" | "float":
                whole.append(data[0])
            case _:
                return False

    # Returns true if a list has duplications, false otherwise
    def duplications(list):
        hash_table = {}
        for item in list:
            if item in hash_table:
                return True
            hash_table[item] = True
        return False
        
    # Check for duplications
    if duplications(whole):
        return False
    
    return True