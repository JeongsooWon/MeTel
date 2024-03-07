MeTel 


Algorithm
![Figure1](https://github.com/JeongsooWon/MeTel/assets/157678300/b927a90e-815d-45b6-b1a6-41ced3f734ee)
Overview of the MeTel algorithm

MeTel takes in input somatic mutation (with VAF) profile from DNA sequencing data of multiple lung cancer samples as input. First, MeTel compares driver mutations (EGFR p.L858R, E19del and KRAS p.G12X). If there are different drivers, they are classified as MPLC, and if the drivers match, it proceeds to further steps. MeTel estimates the probability of IPM (PI) and MPLC (PM). It outputs classification score (s) and the log-scale value of the ratio of PI and PM. The confidence level is another output from MeTel. Based on |s|, cutoffs of 0.6 and 1.28 represent one of the three: Likely, Probable and Confident. Final classification IPM or MPLC: If s > 0, samples classified as IPM, or if s < 0, MPLC. The process of combining with histopathology data with MeTel's results (only with the ‘Likely’ confidence level).
