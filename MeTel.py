import argparse
import math

# Constants
DEFAULT_DIVISOR = 14906 ##samples in ./GENIE/data_NSCLC_all.txt (GENIE v15)
ASIAN_DIVISOR = 1069 ##samples in ./GENIE/data_NSCLC_asian.txt (GENIE v15)
NON_ASIAN_DIVISOR = 13837 ##samples in ./GENIE/data_NSCLC_nonasian.txt (GENIE v15)
DEFAULT_MUTATION_FREQUENCY = 10**-6
IPM_PRIOR = 0.29
MPLC_PRIOR = 0.71

# Function to read mutation frequencies
def read_mutation_frequencies(filename, divisor):
    mutation_frequencies = {}
    with open(filename, 'r') as file:
        for line in file:
            gene, hgvsc, count = line.split('\t')
            ID = f'{gene}\t{hgvsc}'
            mutation_frequencies[ID] = float(count) / divisor
    return mutation_frequencies

# Function to parse a line of input file
def parse_line(line):
    fields = line.split('\t')
    gene, hgvsp, avaf, bvaf = fields[1], fields[3], float(fields[4]), float(fields[5])
    return gene, hgvsp, avaf, bvaf

# Function to calculate the probability
def calculate_probability(avaf, bvaf, mutation_frequency):
    if avaf != 0 and bvaf != 0:
        return math.log10((2 * avaf + (1 - 2 * avaf) * mutation_frequency) / mutation_frequency)
    elif avaf != 0 and bvaf == 0:
        return math.log10(1 - 2 * (avaf))
    else:
        return 0  # Log(1) is 0

# Function to calculate score and confidence level
def calculate_score_and_confidence(prob_list, mutation_prior_ratio, max_mutation_count):
    score = sum(prob_list) + math.log10(mutation_prior_ratio)
    classification = 'IPM' if score > 0 else 'MPLC'
    confidence_level = get_confidence_level(max_mutation_count)
    return score, classification, confidence_level

# Function to determine confidence level based on maximum mutation count
def get_confidence_level(max_mutation_count):
    if max_mutation_count <= 2:
        return 'Likely'
    else:
        return 'Confident'


# Main processing function
def process_metel(input_file, mutation_frequencies, mode, race):
    with open(input_file, 'r') as file:
        ab_list, ba_list = [], []
        a_mutation_count, b_mutation_count = 0, 0  

        for line in file:
            gene, hgvsp, avaf, bvaf = parse_line(line)
            mutation_frequency = mutation_frequencies.get(f'{gene}\t{hgvsp}', DEFAULT_MUTATION_FREQUENCY)
            ab_list.append(calculate_probability(avaf, bvaf, mutation_frequency))
            
            # Update mutation counts for A and B
            if avaf != 0:
                a_mutation_count += 1
            if bvaf != 0:
                b_mutation_count += 1

            if mode == 'syn':
                ba_list.append(calculate_probability(bvaf, avaf, mutation_frequency))

        max_mutation_count = max(a_mutation_count, b_mutation_count)
        mutation_prior_ratio = IPM_PRIOR / MPLC_PRIOR

        score_ab, classification_ab, confidence_ab = calculate_score_and_confidence(ab_list, mutation_prior_ratio, max_mutation_count)
        score_ba, classification_ba, confidence_ba = calculate_score_and_confidence(ba_list, mutation_prior_ratio, max_mutation_count)

        # Selecting the result with the higher absolute score
        final_score, final_classification, final_confidence = (score_ab, classification_ab, confidence_ab) \
            if abs(score_ab) > abs(score_ba) else (score_ba, classification_ba, confidence_ba)
        return final_score, final_classification, final_confidence, race

# Setup argument parser
parser = argparse.ArgumentParser(description='Process VAF data for MeTel algorithm.')
parser.add_argument('input_file', type=str, help='Input file name')
parser.add_argument('-s', '--synmeta', type=str, default='syn', choices=['syn', 'meta'], help='Synchronicity mode')
parser.add_argument('-r', '--race', type=str, choices=['asian', 'non-asian'], help='Race mode')
parser.add_argument('output_file', type=str, help='Output file name')

# Parse arguments
args = parser.parse_args()

# Determine mutation frequency file and divisor based on race option
mutation_freq_file = './GENIE/data_mutations_c.txt'  # Default file
divisor = DEFAULT_DIVISOR

if args.race == 'asian':
    mutation_freq_file = './GENIE/data_mutations_c_asian.txt'
    divisor = ASIAN_DIVISOR
elif args.race == 'non-asian':
    mutation_freq_file = './GENIE/data_mutations_c_nonasian.txt'
    divisor = NON_ASIAN_DIVISOR

# Read mutation frequencies
mutation_frequencies = read_mutation_frequencies(mutation_freq_file, divisor)

# Determine race value for output
race_value = 'Unspecified'
if args.race:
    race_value = args.race

# Process input file
result = process_metel(args.input_file, mutation_frequencies, args.synmeta, race_value)

# Write the result to output file
with open(args.output_file, 'w') as out:
    out.write('Classification_Score(s)\tDiagnosis_Result\tConfidence_Level\tRace\n')
    out.write('\t'.join(map(str, result)) + '\n')
