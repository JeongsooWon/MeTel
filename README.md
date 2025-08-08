# MeTel (Metastasis Teller) 
A Bayesian probabilistic model for the genomic classification of intrapulmonary metastasis (IPM) and multiple primary lung cancer (MPLC).

- Classification Algorithm: Differentiates between IPM and MPLC in patients with multiple lung tumors using somatic mutation profiles.
- Probabilistic Model: Built on a Bayesian model to ensure platform-independent and robust results.
- Decision Support: Provides a confidence level to aid in clinical decision-making, supporting the integration of clinical and histological data.
- Experimental Race-Specific Models: Offers experimental models (asian, black, hispanic) tailored with public population frequency data.
<br/><br/>

## Repository Contents
This repository provides the Python script for the MeTel algorithm, example datasets for demonstration, and the reference mutation frequency data required for its calculations.


- `MeTel.py`: The main script for running the MeTel algorithm.


- `GENIE/`: Contains population-specific mutation frequency data derived from the AACR Project GENIE. These files are used as a reference by the algorithm.
  
* `Examples/`: A directory containing example input and output files to show how to use MeTel and to reproduce the results. The structure is as follows:
   * `input/original_vaf/`: Example input files using the somatic mutation profiles with their original Variant Allele Frequencies (VAFs) from in-house samples.
   * `input/fixed_vaf_0.3/`: The same examples but with VAFs uniformly set to 0.3, as suggested for cases with unknown VAFs.
   * `output/from_original_vaf/`: The corresponding output files generated from the original_vaf inputs.
   * `output/from_fixed_vaf_0.3/`: The corresponding output files generated from the fixed_vaf_0.3 inputs.



**Overview of the MeTel algorithm**
------
![Figure1](https://github.com/user-attachments/assets/01107d11-9473-4373-9676-1bc47e86ed33)

1. MeTel takes in input somatic mutation (with VAF) profile from DNA sequencing data of multiple lung cancer samples as input.
2. First, MeTel compares driver mutations (EGFR p.L858R, E19del and KRAS p.G12X). If there are different drivers, they are classified as MPLC, and if the drivers match, it proceeds to further steps.
3. MeTel estimates the probability of IPM (P<sub>I</sub>) and MPLC (P<sub>M</sub>).
4. It outputs classification score (s) and the log-scale value of the ratio of P<sub>I</sub> and P<sub>M</sub>.
5. The confidence level is another output from MeTel. Based on maximum number of , Based on the maximum mutation count of the two samples, if 2 or fewer the confidence level is 'Likely'; otherwise, it is 'Confident.'
6. Final classification IPM or MPLC: If s > 0, samples classified as IPM; otherwise, MPLC
7. The process of combining with histopathology data with MeTel's results (only with the ‘Likely’ confidence level).

Notices (Before running the script)
------
If your samples contain the specified driver mutations (EGFR p.L858R, EGFR E19del, KRAS G12X) and these drivers do not match between the two samples, the algorithm will immediately classify them as MPLC. <br/>Therefore, proceed to the next steps of the algorithm and run the script only if the drivers in both samples match or if neither sample contains the listed drivers.

Input format
-------
For MeTel.py input, a text file is prepared in the following format, constituting a union set of the somatic mutation profiles from two samples of a single patient.
Examples of input file is shown in "INPUT" directory.
+ **1st column:** Patient ID
+ **2nd column:** Gene
+ **3rd column:** HGVSc 
+ **4th column:** HGVSp
+ **5th column:** A_VAF (Variant Allele Frequency for the first occurring sample)
+ **6th column:** B_VAF (Variant Allele Frequency for the later occurring sample)

Notes:
1. If the ordering of the samples is unknown or they are synchronous, the ordering does not matter.
2. If VAF cannot be determined, input the expected VAF (0.3 is recommended).
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

Examples of output file is shown in "OUTPUT" directory.
+ **Classification_Score(s):** The log-scale value of the ratio of probability of IPM and MPLC
+ **Diagnosis_Result:** If s > 0, samples classified as IPM; otherwise, MPLC
+ **Confidence_Level:** Likely, Confident
+ **Race:** Racial information (asian, non-asian, Unspecified)
