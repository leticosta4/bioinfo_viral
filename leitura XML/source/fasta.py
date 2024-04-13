import pandas as pd
from source.utils import Setup_filesystem

def slicing_genome(seq_especifica):
    nucleotides_slices = []
    for j in range(0, len(seq_especifica), 60):
        nucleotides_slices.append(seq_especifica[j:j+60])
    return nucleotides_slices    

def slicing_locus_and_sequence(locus_list, nuc_list):
    maximum_locus = []
    maximum_nuc = []

    for ln in range(0, len(locus_list), 2000):
        maximum_locus.append(locus_list[ln:ln+2000])
        maximum_nuc.append(nuc_list[ln:ln+2000])
    return zip(maximum_locus, maximum_nuc)

def generate_fasta(df):
    locus_list = df['Locus'].tolist()
    nuc_list = df['Nucleotide_Sequence'].tolist()

    first_line = True
    index = 1

    lists_of_lists = slicing_locus_and_sequence(locus_list, nuc_list)

    for locus_portion, seq_portion in lists_of_lists:
        with open(f"data/processed/fasta_files/genome{index}.fasta", "w") as fasta_file:

            for locus, seq in zip(locus_portion, seq_portion):
                genome = slicing_genome(seq)

                if(first_line):
                    fasta_file.write(">" + locus + "\n")
                    first_line = False
                else:
                    fasta_file.write("\n>" + locus + "\n")

                for genome_slice in genome:        
                    fasta_file.write(genome_slice + "\n" )
            first_line = True
        fasta_file.close()
        index += 1