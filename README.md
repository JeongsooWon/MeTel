# MeTel (Metastasis Teller)
A Bayesian probabilistic model for the genomic classification of intrapulmonary metastasis (IPM) and multiple primary lung cancer (MPLC).

- Classification Algorithm: Differentiates between IPM and MPLC in patients with multiple lung tumors using somatic mutation profiles.
- Probabilistic Model: Built on a Bayesian model to ensure platform-independent and robust results.
- Decision Support: Provides a confidence level to aid in clinical decision-making, supporting the integration of clinical and histological data.
- Experimental Race-Specific Models: Offers experimental models (asian, black, hispanic) tailored with public population frequency data.
<br><br>


## Repository Contents
This repository provides the Python script for the MeTel algorithm, example datasets for demonstration, and the reference mutation frequency data required for its calculations.


- `MeTel.py`: The main script for running the MeTel algorithm.


- `GENIE/`: Contains population-specific mutation frequency data derived from the AACR Project GENIE. These files are used as a reference by the algorithm.
  
* `Examples/`: A directory containing example input and output files to show how to use MeTel and to reproduce the results. The structure is as follows:
  * `input/original_vaf/`: Example input files using the somatic mutation profiles with their original Variant Allele Frequencies (VAFs) from in-house samples.
  * `input/fixed_vaf_0.3/`: The same examples but with VAFs uniformly set to 0.3, as suggested for cases with unknown VAFs.
  * `output/from_original_vaf/`: The corresponding output files generated from the original_vaf inputs.
  * `output/from_fixed_vaf_0.3/`: The corresponding output files generated from the fixed_vaf_0.3 inputs.
<br><br>
## Overview of the MeTel algorithm
![Figure1](https://github.com/user-attachments/assets/01107d11-9473-4373-9676-1bc47e86ed33)

1. MeTel takes a somatic mutation profile (including VAF) from the DNA sequencing data of two lung tumor samples as input.
2. . First, MeTel compares a predefined list of clinically actionable driver alterations (e.g., EGFR exon 19 deletion, KRAS G12C mutation, ALK rearrangement). For the complete list, please refer to Supplementary Table S1 in our publication. If the drivers differ between the two tumors, they are classified as MPLC. If the drivers match or are absent, the algorithm proceeds to the next steps.
3. MeTel estimates the probability of IPM (P<sub>I</sub>) and MPLC (P<sub>M</sub>).
4. It outputs classification score (s) and the log-scale value of the ratio of P<sub>I</sub> and P<sub>M</sub>.
5. It provides a confidence level. This is determined by the number of shared mutations between the two samples. If the count is 2 or fewer, the confidence level is 'Likely'; otherwise, it is 'Confident'
6. A final classification of IPM or MPLC is made: If s > 0, samples are classified as IPM; otherwise, MPLC
7. The process allows for the integration of histopathology data with MeTel's results, especially for cases with a ‘Likely’ confidence level.

## Getting Started
### Prerequisites
**Important Notice**: MeTel performs an initial check for a predefined set of clinically actionable driver alterations. If tumor samples show discordance for any of these drivers (e.g., one tumor has an EGFR mutation and the other has a KRAS mutation), the algorithm will immediately classify them as MPLC.
Therefore, run the analysis script only if the samples either share the same driver mutation from this list or if neither sample contains any of the listed drivers.
<br><br>
## Note on the Race-Specific Models
Please be aware that all race-specific models, activated by the -r or --race option (asian, black, hispanic), are experimental features.
These models are primarily based on publicly available population-specific mutation frequency data and have not yet undergone rigorous clinical validation. While our publication may include preliminary analyses using these models, they are intended for research purposes only at this stage.
Therefore, results obtained using any of the race-specific options should be interpreted with significant caution. We are actively working on validating and improving these models with dedicated, diverse datasets.
<br><br>
## Usage

**Input format**
An input for MeTel.py should be a tab-separated text file containing the union set of somatic mutations from two samples of a single patient.
+ **1st column:** Patient ID
+ **2nd column:** Gene
+ **3rd column:** HGVSc 
+ **4th column:** HGVSp
+ **5th column:** A_VAF (Variant Allele Frequency for the first occurring sample)
+ **6th column:** B_VAF (Variant Allele Frequency for the later occurring sample)

**Notes:**
1.	If the temporal order of the samples is unknown (synchronous), the sample order (A vs. B) does not matter.
2.	Enter a VAF of 0 for wild-type positions in a sample.
3.	If a VAF value is not available, we recommend using an estimated value of 0.3, which represents a typical heterozygous somatic mutation.

## Running

**Command line interface**

```
python3 MeTel.py {input.txt} {output.txt} [Options]
```

**Options**
```
-s {syn, meta}, --synmeta {syn, meta}   Synchronocity Information (default : syn)
-r {asian,black,hispanic}, --race {asian,black,hispanic}
                                    Specifies the race-specific model.
                                    *Important: This is an experimental feature. See the note above before using.*
```

**Examples**
- Basic usage (synchronous, default model):
```python3 MeTel.py ./INPUT/patient_1.txt ./OUTPUT/result_1.txt```
- With options (metachronous, Asian-specific model):
```python3 MeTel.py ./INPUT/patient_2.txt ./OUTPUT/result_2.txt -s meta -r asian```

**Output format**

The output file will contain the following key-value pairs.
Example output:
+ **Classification_Score(s):** The log-scale value of the ratio of probability of IPM and MPLC.
+ **Diagnosis_Result:** The final classification. 'IPM' if score > 0, otherwise 'MPLC'.
+ **Confidence_Level:** 'Confident' or 'Likely'.
+ **Race:** The model used for the analysis (asian, black, hispanic, or Unspecified).
