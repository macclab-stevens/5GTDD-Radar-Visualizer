#!/usr/bin/python3
#Script Used to graph 5G TDD slot patterns, and calculate symbol interfeerence based on radar charcterisitics. 
__author__ = "Eric Forbes"
__version__ = "0.1.0"
__license__ = "MIT"
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import math
import argparse

### Slots Structures
slotPattern = "DDDSUDDSUU"
# slotPattern = "D"
SpecialSlotPattern = "DDDDDDDDGGGGUU"

#Slot Len Checks
# if len(slotPattern) != 10: print("SlotPattern {} ! len=10".format(slotPattern));exit()
if len(SpecialSlotPattern) != 14: print("SpecialSlotPattern {} ! len=14".format(SpecialSlotPattern));exit()

##Radar
RadarPW = 40 #uS
RadarPRI_Hz = 640 #Hz
RadarPRI_s = (1/RadarPRI_Hz )*1e6

### Colors
cpColor = 'c'
syColor = 'b'

## Numerology
numerology = 1
Ts = 1/(480 * 1000 * 4096)
CpNormal        = Ts * 1e6 * 144 * 64 * pow(2,-numerology) #uS
CpLong          = Ts * 1e6 * (144+16) * 64 * pow(2,-numerology)  #uS
SymbolDuration  = Ts * 1e6 * 2048 * 64 * pow(2,-numerology) #uS
SCS = 15*pow(2,numerology)
numParams_NorCP_dict = {
    0: { "SCS": 15, "symbolDur": 66.6667, "cpDurL": 5.2,  "cpDurN": 4.69, "OFDMDur": 71.35},
    1: { "SCS": 30, "symbolDur": 33.3333, "cpDurL": 2.86, "cpDurN": 2.343, "OFDMDur": 35.68},
    2: { "SCS": 60, "symbolDur": 16.6667, "cpDurL": 1.69, "cpDurN": 1.1718, "OFDMDur": 17.84},
    3: { "SCS": 120,"symbolDur": 08.3333, "cpDurL": 1.11, "cpDurN": 0.59, "OFDMDur": 8.92},
    4: { "SCS": 240,"symbolDur": 04.1711, "cpDurL": 0.81, "cpDurN": 0.29, "OFDMDur": 4.46}
}


#Setting Variables

numPar = numParams_NorCP_dict.get(numerology)
print("Numerology {} Selected: {}".format(numerology,numPar))
print("Symbol Duration:{} CP Normal:{} CP Long:{}".format(SymbolDuration,CpNormal,CpLong))
symbolsPerSlot = 14
symbolYheight = 5
symbolYindex = 0


def printSymbol(ax,printIndex,index,cpColor,syColor):
    # index = numPar["OFDMDur"]
    if printIndex == 0 or printIndex == 7: 
        cpDuration = CpLong
    else: 
        cpDuration = CpNormal
    print(printIndex,cpDuration)
    cp = plt.Rectangle((index, symbolYindex), cpDuration, numPar["SCS"], fill=True, color = cpColor)
    symbol = plt.Rectangle((index+cpDuration, symbolYindex), SymbolDuration, numPar["SCS"], fill=True, color = syColor) 
    ax.add_patch(cp)
    ax.add_patch(symbol)
    return index+SymbolDuration+cpDuration

def plot5GSlotAnnotations(ax,startIndex,stopIndex,slotIndexText,slotTypeText):
    print("Annotation Start:{} Stop:{}".format(startIndex,stopIndex))
    arr = patches.FancyArrowPatch((startIndex, SCS+10), (stopIndex, SCS+10),
                               arrowstyle='|-|', mutation_scale=10,
                               shrinkA=0,shrinkB=0
                               )
    ax.add_patch(arr)
    ax.annotate(slotIndexText, (startIndex+(stopIndex-startIndex)/2, SCS+10), ha='center', va='bottom')
    ax.annotate(slotTypeText, (startIndex+(stopIndex-startIndex)/2, SCS+7), ha='center', va='bottom')

    return

def plot5GTDD(ax):
    print("Graphing 5G TDD...")
    slotNum = 0
    printIndex = 0
    for slotType in slotPattern:
        SlotStartIndex = printIndex
        print(slotType,slotNum)
        if slotType == 'D':
            for i in range((pow(2,numerology))):
                for j in range(symbolsPerSlot): print(j,printIndex);printIndex = printSymbol(ax,j,printIndex,'c','b')
        if slotType == 'U':
            for i in range((pow(2,numerology))):
                for j in range(symbolsPerSlot): print(j,printIndex);printIndex = printSymbol(ax,j,printIndex,'pink','red')
        if slotType == 'S':
            j = 0
            for symbol in SpecialSlotPattern:
                print(j,printIndex)
                if symbol == 'D': cpColor = 'c';syColor = 'b'
                if symbol == 'U': cpColor = 'pink'; syColor = 'r'
                if symbol == 'G': cpColor = 'w'; syColor = 'w'
                for s in range((pow(2,numerology))): 
                    printIndex = printSymbol(ax,j,printIndex,cpColor,syColor)
                j += 1
        SlotStopIndex = printIndex
        plot5GSlotAnnotations(ax,SlotStartIndex,SlotStopIndex,"S"+str(slotNum),slotType)
        slotNum +=1
        print(printIndex)

def plotPulseRadar(ax,RadarHeight,RadarColor):
    print("Graphing Radar Pulses...")
    Index = 0
    RadarGraphRange = 10000
    while Index < RadarGraphRange:
        Pulse = plt.Rectangle((Index, -20), RadarPW, RadarHeight, fill=True, color = RadarColor) 
        ax.add_patch(Pulse)
        Index += RadarPW + RadarPRI_s
        # if Index > RadarGraphRange: return

def main(args):
    # RadarPW = args.RadarPW
    # print(RadarPW,args.RadarPW)
    fig = plt.figure(figsize=(25,5)) 
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(-50,11000)
    ax.set_ylim(-20,50) 
    plt.ylabel("kHz")
    microSeconds = chr(956)+"S"
    plt.xlabel(microSeconds)
    # plt.arrow(-2, -4, 300, 0, head_width=0.05, head_length=0.03, linewidth=4, color='r', length_includes_head=True)
    plot5GTDD(ax)
    plotPulseRadar(ax,10,'g')
    print("Showing Plot")
    plt.show()  

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    # parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    # parser.add_argument("--RadarPW", action="store", default=40, type=int, help="Radar Pulse Width in uS")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
