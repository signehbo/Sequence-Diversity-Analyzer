import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from Bio import AlignIO
from Bio.Align import AlignInfo
from io import StringIO
import subprocess
from collections import Counter

def run_mafft(fasta_file, output_file="aligned.fasta"):
    # Run MAFFT to align the protein sequences.
    cmd = ["mafft", "--auto", fasta_file]
    with open(output_file, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    return output_file

def calculate_conservation(alignment_file, tie_strategy="mark_as_X"):
    alignment = AlignIO.read(alignment_file, "fasta")
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


def plot_conservation(scores):
    """Plot conservation scores along the sequence."""
    plt.figure(figsize=(12, 4))
    plt.plot(scores, marker='o', linestyle='-', color='b')
    plt.xlabel("Position")
    plt.ylabel("Conservation Score")
    plt.title("Sequence Conservation Analysis")
    plt.ylim(0, 1)
    st.pyplot(plt)

# Streamlit UI
st.title("Sequence Diversity Analyzer")
uploaded_file = st.file_uploader("Upload a FASTA file with multiple sequences", type=["fasta"])

if uploaded_file:
    tie_strategy = st.radio(
        "Choose tie-breaking strategy for consensus calculation:",
        ("Mark ties as X", "Choose first winner")
    )

    st.info("""
    **When to use:**
    - *Mark ties as X:*  
    Use this if you want to visualize positions where multiple residues are equally common.  
    Ideal for reporting, visualization, or further analysis that tolerates ambiguity.
    
    - *Choose first winner:*  
    Use this if you need a clean, unambiguous consensus sequence for downstream tasks like primer design, modeling, or automated pipelines.
    """)

    # Map user choice to argument value
    tie_strategy_arg = "mark_as_X" if tie_strategy == "Mark ties as X" else "first_winner"

    fasta_content = uploaded_file.getvalue().decode("utf-8")
    fasta_path = "input.fasta"
    with open(fasta_path, "w") as f:
        f.write(fasta_content)
    
    st.markdown("**Running MAFFT for alignment...**")
    aligned_file = run_mafft(fasta_path)
    st.markdown("**Calculating conservation scores...**")
    scores, consensus = calculate_conservation(aligned_file, tie_strategy=tie_strategy_arg)
    st.markdown(f"**Consensus Sequence:** `{consensus}`")
    plot_conservation(scores)
