#!/usr/bin/python3
#Script Used to graph 5G TDD slot patterns, and calculate symbol interfeerence based on radar charcterisitics. 
__author__ = "Eric Forbes"
__version__ = "0.1.0"
__license__ = "MIT"
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import matplotlib.cbook as cbook
import math
import argparse

### Colors
cpColor = 'c'
syColor = 'b'

## Numerology
numerology = 1
Tc = 1/(480 * 1000 * 4096) #Basic NR time Unit
CpNormal        = Tc * 1e6 * 144 * 64 * pow(2,-numerology) #uS
CpLong          = Tc * 1e6 * (144+16) * 64 * pow(2,-numerology)   #uS 
SymbolDuration  = Tc * 1e6 * 2048 * 64 * pow(2,-numerology) #uS
SCS = 15*pow(2,numerology)
#For Reference: See https://www.techplayon.com/5g-nr-cyclic-prefix-cp-design/
# numParams_NorCP_dict = { 
#     0: { "SCS": 15, "symbolDur": 66.6667, "cpDurL": 5.2,  "cpDurN": 4.69, "OFDMDur": 71.35},
#     1: { "SCS": 30, "symbolDur": 33.3333, "cpDurL": 2.86, "cpDurN": 2.34, "OFDMDur": 35.68},
#     2: { "SCS": 60, "symbolDur": 16.6667, "cpDurL": 1.69, "cpDurN": 1.17, "OFDMDur": 17.84},
#     3: { "SCS": 120,"symbolDur": 08.3333, "cpDurL": 1.11, "cpDurN": 0.59, "OFDMDur": 8.92},
#     4: { "SCS": 240,"symbolDur": 04.1711, "cpDurL": 0.81, "cpDurN": 0.29, "OFDMDur": 4.46}
# }


#Setting Variables
# print("Symbol Duration:{} CP Normal:{} CP Long:{}".format(SymbolDuration,CpNormal,CpLong))
symbolsPerSlot = 14
symbolYheight = 5
#symbolYindex = 0


def plotSymbol(ax,printIndex,index,Yindex,cpColor,syColor):
    # index = numPar["OFDMDur"]
    if printIndex == 0 or printIndex == 7: 
        cpDuration = CpLong
    else: 
        cpDuration = CpNormal
    # print(printIndex,cpDuration)
    cp = plt.Rectangle((index, Yindex), cpDuration, SCS, fill=True, color = cpColor)
    symbol = plt.Rectangle((index+cpDuration, Yindex), SymbolDuration, SCS, fill=True, color = syColor) 
    ax.add_patch(cp)
    ax.add_patch(symbol)
    return index+SymbolDuration+cpDuration

def plotGuardSymbol(ax,printIndex,index,Yindex,cpColor,syColor):
    # index = numPar["OFDMDur"]
    if printIndex == 0 or printIndex == 7: 
        cpDuration = CpLong
    else: 
        cpDuration = CpNormal
    # print(printIndex,cpDuration)
    guardTime = cpDuration + SymbolDuration
    cp = plt.Rectangle((index, Yindex), guardTime, SCS, fill=False)
    # symbol = plt.Rectangle((index+cpDuration, symbolYindex), SymbolDuration, SCS, fill=True, color = syColor) 
    ax.add_patch(cp)
    # ax.add_patch(symbol)
    return index+guardTime

def plot5GSlotAnnotations(ax,startIndex,stopIndex,slotIndexText,slotTypeText):
    #print("Annotation Start:{} Stop:{}".format(startIndex,stopIndex))
    arr = patches.FancyArrowPatch((startIndex, SCS+10), (stopIndex, SCS+10),
                               arrowstyle='|-|', mutation_scale=10,
                               shrinkA=0,shrinkB=0
                               )
    ax.add_patch(arr)
    ax.annotate(slotIndexText, (startIndex+(stopIndex-startIndex)/2, SCS+10), ha='center', va='bottom')
    ax.annotate(slotTypeText, (startIndex+(stopIndex-startIndex)/2, SCS+20), ha='center', va='bottom')
    return

def plotSlotAnnotations(ax,slotIndexText,startIndex,stopIndex):
    arr = patches.FancyArrowPatch((startIndex, SCS+3), (stopIndex, SCS+3),
                               arrowstyle='|-|', mutation_scale=2,
                               shrinkA=0,shrinkB=0
                               )
    ax.add_patch(arr)
    ax.annotate(slotIndexText, (startIndex+(stopIndex-startIndex)/2, SCS+3), ha='center', va='bottom')
    return

def plotTimingAdvanceAnnotations(ax,xstart,xstop,yindex):
    if not plotTaAnnotations: return
    arr = patches.FancyArrowPatch((xstart, yindex), (xstop, yindex),
                               arrowstyle='|-|', mutation_scale=2,
                               shrinkA=0,shrinkB=0
                               )
    ax.add_patch(arr)
    ax.annotate('', (xstart+(xstop-xstart)/2, yindex), ha='right', va='bottom')
    ax.annotate('TA', (xstop + 10, yindex-1))

    return

def plotPropDelayAnnotations(ax,start,stop):

    return

def plot5GTDD(ax,xaxisOffset,yaxisOffset,bool_plotSlot,bool_ta):
    print("Graphing 5G TDD...")
    slotNum = 0
    printIndex = xaxisOffset
    for subFrameIndex in range(len(SubFramePattern)):
        slotType = SubFramePattern[subFrameIndex]
        SlotStartIndex = printIndex
        # print(slotType,slotNum)
        if slotType == 'D':
            for i in range((pow(2,numerology))):
                slotStartIndex = printIndex
                for j in range(symbolsPerSlot): 
                    printIndex = plotSymbol(ax,j,printIndex,yaxisOffset,'c','b')
                if(bool_plotSlot):plotSlotAnnotations(ax,"S"+str(i),slotStartIndex,printIndex)
        if slotType == 'U':
            for i in range((pow(2,numerology))):
                slotStartIndex = printIndex
                for j in range(symbolsPerSlot): 
                    printIndex = plotSymbol(ax,j,printIndex,yaxisOffset,'pink','red')
                if(bool_plotSlot):plotSlotAnnotations(ax,"S"+str(i),slotStartIndex,printIndex)    
            if bool_ta and subFrameIndex<len(SubFramePattern)-1:
                #print(subFrameIndex,len(SubFramePattern))
                if (SubFramePattern[subFrameIndex+1] != 'U'): 
                    printIndex += 2*UePropDelay
        if slotType == 'S':
            j = 0
            slotStartIndex = printIndex
            slotCnt = 0
            appliedTA = False
            for symbol in SpecialSubFramePattern:
                #print(j,printIndex)
                if symbol == 'D': cpColor = 'c';syColor = 'b'
                if symbol == 'U': 
                    if bool_ta and not appliedTA: printIndex -= 2*UePropDelay; appliedTA = True; plotTimingAdvanceAnnotations(ax,printIndex,printIndex+UePropDelay,-5)
                    cpColor = 'pink'; syColor = 'r' 
                if symbol == 'G': cpColor = 'w'; syColor = 'w'
                for s in range((pow(2,numerology))): 
                    if symbol!= 'G' : printIndex = plotSymbol(ax,j,printIndex,yaxisOffset,cpColor,syColor)
                    else: printIndex = plotGuardSymbol(ax,j,printIndex,yaxisOffset,cpColor,syColor)
                    slotCnt += 1
                    if slotCnt%symbolsPerSlot == 0: 
                        if(bool_plotSlot):plotSlotAnnotations(ax,"S"+str(int((slotCnt-symbolsPerSlot)/symbolsPerSlot)),slotStartIndex,printIndex);
                        slotStartIndex = printIndex  
                j += 1
            # plotSlot(ax,"S"+str(j),slotStartIndex,printIndex)

        SlotStopIndex = printIndex
        if(bool_plotSlot):plot5GSlotAnnotations(ax,SlotStartIndex,SlotStopIndex,"SF "+str(slotNum),slotType)
        slotNum +=1
        #print(printIndex)

def plotPictures(ax,name,x0,x1,y0,y1):
    image = mpimg.imread(name)
    extent = [x0,x1,y0,y1]
    ax.imshow(image, extent=extent, interpolation='none', aspect='auto')
    return

def plotPulseRadar(ax,Yindex,RadarHeight,RadarColor):
    print("Graphing Radar Pulses...")
    Index = 0 + RadarOffset
    RadarGraphRange = 10000
    while Index < RadarGraphRange:
        Pulse = plt.Rectangle((Index, Yindex), RadarPW, RadarHeight, fill=True, color = RadarColor) 
        ax.add_patch(Pulse)
        Index += RadarPW + RadarPRI_s
        # if Index > RadarGraphRange: return

def addLegend(ax):
    textSize = 5
    #first legend
    Downlink = patches.Patch(color='blue', label='Downlink')
    Uplink = patches.Patch(color='red',label='Uplink')
    Guard = patches.Patch(color='black',fill=None,label='Guard')
    Radar = patches.Patch(color='green',label='Radar Pulse')
    ax.add_artist(ax.legend(handles=[Downlink,Uplink,Guard,Radar], loc='upper right',fontsize=textSize))

    #second legend
    SFAllocation = patches.Patch(color='white',label =  ('SF Allocation: '+SubFramePattern))
    SpecialSymbol = patches.Patch(color='white',label = ('Special Ptrn  : '+SpecialSubFramePattern))
    RadarPulseWidth = patches.Patch(color='white',label =        ('Radar PW  : '+str(RadarPW) +" "+ chr(956)+"S"))
    RadarPulseWithInterval = patches.Patch(color='white',label = ('Radar PRI  : '+str(RadarPRI_Hz)+" Hz"))
    RadarOffsetLgnd = patches.Patch(color='white',label =        ('Radar Offset: '+str(RadarOffset)+" "+chr(956)+"S"))
    ax.add_artist(ax.legend(handles=[SFAllocation,SpecialSymbol,RadarPulseWidth,RadarPulseWithInterval,RadarOffsetLgnd],loc='upper left',fontsize=textSize) )

    #third Legend
    UeDistanceLgnd = patches.Patch(color='white',label =  ('UE Distance: '+str(UeDistance/1e3) + "km"))
    UePropDelayLgnd = patches.Patch(color='white',label = ('UE PropDelay: '+str(int(UePropDelay)) + chr(956)+"S"))
    ax.legend(handles=[UeDistanceLgnd,UePropDelayLgnd],loc='lower left',fontsize=textSize)

    return

def main(args):

    # RadarPW = args.RadarPW
    # print(RadarPW,args.RadarPW)
    fig = plt.figure(figsize=(25,5)) 
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(-500,10200)
    ax.set_ylim(-70,pow(2,numerology)*15+60) 
    plt.ylabel("SCS Freq (kHz)")
    plt.xlabel(chr(956)+"S")
    plot5GTDD(ax,0,0,True,False)
    plot5GTDD(ax,UePropDelay,- (15*pow(2,numerology) + 10),False,True)
    plotPulseRadar(ax,-60,10,'g')
    if showImages:
        plotPictures(ax,'Images/Tower.jpg',-400,-50,5,25)
        plotPictures(ax,'Images/Ue.jpg',-350,-50,-35,-20)

    addLegend(ax)
    if FileName is None: print("Showing Plot"); plt.show() 
    else: print("Saving plt as: {}".format(FileName));plt.savefig(FileName)
    
         

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
    # ... other options ...
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Required positional argument
    # parser.add_argument("arg", help="Required positional argument")


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
    

    parser.add_argument('--subFramePattern', type = str, default="DDDSUDDSUU",
                        help='Slot Frame Pattern Must be 10 char. Down Special Up'
    )
    parser.add_argument('--SpecialSubFramePattern',type=str,default='DDDDDDDDGGUUUU',
                        help='14 Slot pattern for transtion G = Guard.')
    parser.add_argument('--UeDistance',type=int,default=5e3,
                        help="UE Distance from gNB in (m)")
    parser.add_argument('--TA',type=bool,default=True,help="Apply UE Timing Advance")
    parser.add_argument('--RadarPW',type=int,default=40,help="Radar Pulse Width in uS")
    parser.add_argument('--RadarPRI',type=int,default=640,help="Radar Pulse Repeition Interval in Hz")
    parser.add_argument('--RadarOffset',type=int,default=0,help='Radar StartTime Offset')
    parser.add_argument('-f','--fileName',required=False,type=str,help='File to Write PlotOutput')
    parser.add_argument('-i','--noImages',default=True,action='store_false',help='If displaying UE/Tower Images')
    args = parser.parse_args()
    ### Slots Structures
    SubFramePattern = args.subFramePattern
    SpecialSubFramePattern = args.SpecialSubFramePattern


    #Slot Len Checks
    if len(SubFramePattern) != 10: print("SubFramePattern {} ! len=10".format(SubFramePattern));exit()
    if len(SpecialSubFramePattern) != 14: print("SpecialSubFramePattern {} ! len=14".format(SpecialSubFramePattern));exit()

    #UE
    UeDistance = args.UeDistance # (m)
    SpeedOfLight = 299792458 # (m/s)
    UePropDelay = 1e6 * UeDistance/(SpeedOfLight) # (us)
    UeTimingAdvance = args.TA
    plotTaAnnotations = args.TA

    ##Radar
    RadarPW = args.RadarPW #uS
    RadarPRI_Hz = args.RadarPRI #Hz
    RadarPRI_s = (1/RadarPRI_Hz )*1e6
    RadarOffset = args.RadarOffset #uS

    #plot related
    FileName = args.fileName
    showImages = args.noImages
    #Print What we're using
    print("Using the Following: ")
    print("Slot Pattern: {} SpecialPattern {}".format(SubFramePattern,SpecialSubFramePattern))
    print("Ue Distance From gNB {} , PropDelay:{} with TA: {}".format(UeDistance,UePropDelay,UeTimingAdvance))
    print("Radar PW:{} PRI:{} Offset{}".format(RadarPW,RadarPRI_Hz,RadarOffset))
    print("FileName: {}".format(FileName))

    main(args)

