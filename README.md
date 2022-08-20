# Bioinformatics Mini Projects  

## main-1: Semi-Global Alignment  

This project contains an implementation of the proteins' Semi-Global alignment algorithm using dynamic programming and the PAM250 scoring matrix to score matches and mismatches penalties. For gaps, the constant penalty value is equal to 9.  

### Input and output formats  

The inputs are two protein strings that need to be semi-globally aligned with each other. The output contains the total alignment score in the first line, and the following lines are all the possible alignment forms.  

```
# input 

AAAAA
AA

# output

4
AAAAA
---AA
AAAAA
--AA-
AAAAA
-AA--
AAAAA
AA---
```

## main-2: Multiple Sequence Alignment using Star-Alignment

This project contains an implementation of the proteins' Multiple Sequence Alignment algorithm 'Star-Alignment.' The scores in this particular mini-project are equal to:
- match: 3
- mismatch: -1
- gap: -2
In this project, in order to optimize the process, blocks containing more than or equal to two positins with at least one gap or mismatch will be chosen to be substituted and aligned with the original block repeatedly, until the score doesn't get higher and the original block would be substituted by the aligned one.

### Input and output formats  

In the first line of the input comes the number of to be aligned sequences and in the following come the sequences. The output contains the total alignment score and after that comes the MSA.

```
# input 

4 
TYIMREAQYESAQ
TCIVMREAYE
YIMQEVQQER
WRYIAMREQYES

# output

51
-TYI-MREAQYESAQ
-TCIVMREA-YE---
--YI-MQEVQQER--
WRYIAMRE-QYES--
```