# MOL3022 - Sequence Diversity Analyzer

The Sequence Diversity Analyzer is a tool designed to analyze sequence conservation and diversity across multiple protein sequences. It aligns the sequences, calculates conservation scores, and visualizes sequence variability.

The project is developed for the course [MOL3022 - Bioinformatics - Method Oriented Project](https://www.ntnu.edu/studies/courses/MOL3022#tab=omEmnet) and consists of a Python script with a Streamlit-based front-end.

## How to run the project

1. **Download a protein sequence dataset in FASTA format.**
   - You can obtain protein sequences from [UniProt KnowledgeBase](https://www.uniprot.org/uniprotkb?query=reviewed:true) by clicking the "Download" button.
   - Ensure the file is in uncompressed FASTA format before proceeding.

2. **Install the necessary dependencies.**
   - Open a terminal and navigate to the project folder.
   - Run the command:
     ```
     pip install -r requirements.txt
     ```

3. **Run the project using Streamlit.**
   - Execute the following command in the terminal:
     ```
     streamlit run main.py
     ```

## Expected results

When you run the tool, your browser will open and connect to the Streamlit application. You will see an interface allowing you to upload a FASTA file containing multiple sequences.

### **Features:**
- **Upload a FASTA file**: The tool accepts a multi-sequence FASTA file as input.
- **Padding and sanitizing sequences**: The tool pads and sanitizes sequences to ensure that they are the same length and dont contain dots or spaces.
- **Compute conservation scores**: Each position in the alignment receives a conservation score, indicating how conserved the residue is across sequences.
- **View a consensus sequence**: The most common residues at each position are displayed. The user can choose between two tie-breaking strategies for consensus calculation.
Mark ties as X: If multiple residues have the same frequency, they are marked as 'X'.
Choose first winner: The first most common residue found in the alignment column is chosen.
- **Visualize conservation**: A graph plots conservation scores across the sequence, highlighting conserved and variable regions.

### **Sample interface:**

#### Uploading a FASTA file:
![Upload Page](docs/Upload_Page.png)

#### Chossing tie breaking method:
![Choosing tie breaking](docs/Choosing_tiebreaking.png)


#### Consensus sequence and conservation plot:
![Consensus sequence and conservation plot](docs/conservation_and_consensus.png)

## Scoring Method

The conservation score is calculated as:
  ```
  Score = (Most frequent residue count) / (Total number of residues at position)

  ```
A score of **1.0** indicates complete conservation at that position (all residues are identical across sequences), while lower scores indicate more variability.

---
This tool provides a way to analyze protein sequence conservation and generate a consensus sequence.

