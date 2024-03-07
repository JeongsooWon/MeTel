MeTel (Metastasis Teller)
---------------------
+ Classification algorithm for intrapulmonary metastasis (IPM) and multiple primary lung cancer (MPLC) in multiple lung cancer.
+ Bayesian probabilistic model, ensures platform-independent results.
+ The confidence level aids in clinical decision-making and supports the integration of clinical and histological data.
+ Support an ethnic-specific mode, tailored by population-specific mutation frequency data, enhancing its global applicability.

**Overview of the MeTel algorithm**
------
![Figure1](https://github.com/JeongsooWon/MeTel/assets/157678300/b927a90e-815d-45b6-b1a6-41ced3f734ee)

1. MeTel takes in input somatic mutation (with VAF) profile from DNA sequencing data of multiple lung cancer samples as input.
2. First, MeTel compares driver mutations (EGFR p.L858R, E19del and KRAS p.G12X). If there are different drivers, they are classified as MPLC, and if the drivers match, it proceeds to further steps.
3. MeTel estimates the probability of IPM (PI) and MPLC (PM).
4. It outputs classification score (s) and the log-scale value of the ratio of PI and PM.
5. The confidence level is another output from MeTel. Based on |s|, cutoffs of 0.6 and 1.28 represent one of the three: Likely, Probable and Confident.
6. Final classification IPM or MPLC: If s > 0, samples classified as IPM, or if s < 0, MPLC.
7. The process of combining with histopathology data with MeTel's results (only with the ‘Likely’ confidence level).

Notices (Before running script)
------
If your samples contain the specified driver mutations (EGFR p.L858R, EGFR E19del, KRAS G12X) and these drivers do not match between the two samples, the algorithm will immediately classify them as MPLC. Therefore, proceed to the next steps of the algorithm and run the analysis only if the drivers in both samples match or if neither sample contains the listed drivers.

Input format
-------
For MeTel.py input, a text file is prepared in the following format, constituting a union set of the somatic mutation profiles from two samples.
Examples of input file is shown in "INPUT" directory.
+ 1st column: Sample ID
+ 2nd column: Gene
+ 3rd column: HGVSc 
+ 4th column: HGVSp
+ 5th column: A_VAF (Variant Allele Frequency for the first occurring sample)
+ 6th column: B_VAF (Variant Allele Frequency for the later occurring sample)

Notes:
1. If the ordering of the samples is unknown or they are synchronous, the ordering does not matter.
2. If VAF cannot be determined, input the expected average VAF (0.3 is recommended).
3. Enter a VAF of 0 for samples where the mutation does not occur.

Running
--------
**Command line interface**

```
python3 MeTel.py {input.txt} {output.txt} [Options]
```

**Options**
```
-s {syn, meta}, --synmeta {syn, meta}   Synchronocity Information (default : syn)
-r {asian, non-asian} --race {asian, non-asian}    Race Mode (default : Unspecified(use all population))
```
**Output**
+ **Classification_Score(s):** The log-scale value of the ratio of probability of IPM and MPLC
+ **Diagnosis_Result:** If s > 0, samples classified as IPM, or if s < 0, MPLC
+ **Confidence_Level:** Likley, Probable, Confident
+ **Race:** Racial information (asian, non-asian, Unspecified)
