# 5GTDD-Radar-Visualizer
A Python script using Matplotlib to visualize 5G TDD slot patterns and pulsed radar interference.

E.g.
```
### Slots Structures
SubFramePattern = "DDDSUDDSUU"
SpecialSubFramePattern = "DDDDDDGGGGUUUU"

#UE
UeDistance = 15e3 # (m)
UeTimingAdvance = True

##Radar
RadarPW = 40 #uS
RadarPRI_Hz = 640 #Hz
RadarPRI_s = (1/RadarPRI_Hz )*1e6
RadarOffset = 400#uS
```
<img width="1423" alt="image" src="Images/ExampleOutput.jpg">



