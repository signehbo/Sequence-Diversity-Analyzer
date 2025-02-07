import streamlit as st
from Bio import SeqIO
import subprocess
import os

# Set page config
st.set_page_config(layout="wide")

# Function to write sequences to a temporary file
def write_fasta(sequences, filename):
    with open(filename, "w") as f:
        for i, seq in enumerate(sequences):
            f.write(f">seq{i}\n{seq}\n")

# Function to run MEME for motif discovery
def run_meme(input_fasta, output_dir, minw=6, maxw=20):
    cmd = [
        "meme", input_fasta,
        "-oc", output_dir,
        "-minw", str(minw),
        "-maxw", str(maxw),
        "-mod", "zoops",
        "-nmotifs", "3"
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Streamlit UI
st.title("De Novo Transcription Factor Binding Site Prediction")
st.markdown("*Find motifs for transcription factor binding sites using MEME.*")

# File uploader
uploaded_file = st.file_uploader("Upload a FASTA file", type=["fna", "fa", "fasta"])
if uploaded_file:
    sequences = [str(record.seq) for record in SeqIO.parse(uploaded_file, "fasta")]
    st.write(f"Loaded {len(sequences)} sequences.")
    
    # Set motif search parameters
    min_width = st.slider("Minimum motif width", 6, 15, 6)
    max_width = st.slider("Maximum motif width", 15, 30, 20)
    
    # Run MEME button
    if st.button("Run MEME for Motif Discovery"):
        fasta_filename = "temp_sequences.fasta"
        output_dir = "meme_output"
        
        write_fasta(sequences, fasta_filename)
        run_meme(fasta_filename, output_dir, min_width, max_width)
        
        if os.path.exists(os.path.join(output_dir, "meme.html")):
            st.markdown(f"[View MEME results](./{output_dir}/meme.html)", unsafe_allow_html=True)
        else:
            st.error("MEME analysis failed. Check the logs.")
