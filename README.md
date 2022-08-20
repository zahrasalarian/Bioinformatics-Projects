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
