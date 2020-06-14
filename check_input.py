import sys
import colors as col

if len(sys.argv) < 3:
    sys.exit(col.RED + "\nYou haven't given the program enough arguments!\nUsage: ./ratp [Start station] [Finish Station]\n" + col.RESET)
if len(sys.argv) > 3:
    sys.exit(col.RED + "\nYou have given the program too many arguments!\nUsage: ./ratp [Start station] [Finish Station]\n" + col.RESET)

def check_Start(list):
    matchingStart = [item for item in list if sys.argv[1].lower() in item.lower()]
    return matchingStart

def check_Finish(list):
    matchingFinish = [item for item in list if sys.argv[2].lower() in item.lower()]
    return matchingFinish