import streamlit as st
import matplotlib.pyplot as plt
from Bio import AlignIO
from collections import Counter

def pad_fasta_sequences(input_fasta, output_fasta):
    sequences = []
    headers = []
    
    # Parse FASTA
    with open(input_fasta, "r") as f:
        current_header = None
        current_seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_header is not None:
                    sequences.append(current_seq)
                    headers.append(current_header)
                current_header = line
                current_seq = ""
            else:
                current_seq += line.replace(" ", "").replace(".", "")  # Clean up
        # Add the last sequence
        if current_header is not None:
            sequences.append(current_seq)
            headers.append(current_header)
    
    # Pad sequences
    max_len = max(len(seq) for seq in sequences)
    padded_sequences = [seq.ljust(max_len, "-") for seq in sequences]
    
    # Write output
    with open(output_fasta, "w") as f:
        for h, s in zip(headers, padded_sequences):
            f.write(f"{h}\n{s}\n")
    return output_fasta 

#Helper function to calculate conservation scores
def calculate_conservation(alignment_file, tie_strategy="mark_as_X"):
    alignment = AlignIO.read(alignment_file, "fasta")
    print(alignment)
    scores = []
    consensus_list = []
    
    for i in range(len(alignment[0])):  
        column = [alignment[j].seq[i] for j in range(len(alignment))]
        column_no_gaps = [residue for residue in column if residue != "-"]
        
        if column_no_gaps:
            counts = Counter(column_no_gaps)
            max_count = max(counts.values())
            most_common_residues = [residue for residue, count in counts.items() if count == max_count]
            
            if len(most_common_residues) > 1:
                if tie_strategy == "mark_as_X":
                    consensus_residue = 'X'
                else:  # tie_strategy == "first_winner"
                    # Pick the residue that appears first in the alignment column
                    for residue in column_no_gaps:
                        if residue in most_common_residues:
                            consensus_residue = residue
                            break
            else:
                consensus_residue = most_common_residues[0]
                
            score = max_count / len(column_no_gaps)
        else:
            consensus_residue = "-"  
            score = 0
        
        scores.append(score)
        consensus_list.append(consensus_residue)
    
    consensus = "".join(consensus_list)
    return scores, consensus

#Helper function to plot conservation scores
def plot_conservation(scores):
    """Plot conservation scores along the sequence."""
    plt.figure(figsize=(12, 4))
    plt.plot(scores, marker='o', linestyle='-', color='b')
    plt.xlabel("Position")
    plt.ylabel("Conservation Score")
    plt.title("Sequence Conservation Analysis")
    plt.ylim(0, 1)
    st.pyplot(plt)

#Main function run when user runs streamlit run main.py in terminal
# Streamlit UI
st.title("Sequence Diversity Analyzer")
uploaded_file = st.file_uploader("Upload a FASTA file with multiple sequences, from for example UniProt", type=["fasta"])

if uploaded_file:
    tie_strategy = st.radio(
        "Choose tie-breaking strategy for consensus calculation:",
        ("Mark ties as X", "Choose first winner")
    )

    st.info("""
    **When to use:**
    - *Mark ties as X:*  
    Shows an 'X' where multiple residues are equally common.  
    Good for visual analysis and identifying uncertain positions.
    
    - *Choose first winner:*  
    Picks the first most common residue found.  
    Best for creating a clear consensus sequence for further use
    """)

    # Map user choice to argument value
    tie_strategy_arg = "mark_as_X" if tie_strategy == "Mark ties as X" else "first_winner"

    fasta_content = uploaded_file.getvalue().decode("utf-8")
    fasta_path = "input.fasta"
    with open(fasta_path, "w") as f:
        f.write(fasta_content)
    
    st.markdown("**Aligning by padding sequences to the longest length...**")
    aligned_file = "aligned.fasta"
    pad_fasta_sequences(fasta_path, aligned_file)
    st.markdown("**Calculating conservation scores...**")
    scores, consensus = calculate_conservation(aligned_file, tie_strategy=tie_strategy_arg)
    st.markdown(f"**Consensus Sequence:** `{consensus}`")
    plot_conservation(scores)
