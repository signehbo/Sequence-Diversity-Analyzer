# MOL3022

# De Novo Transcription Factor Binding Site Prediction

## Overview
This project provides a Streamlit-based web application for de novo motif discovery in transcription factor binding sites. It uses MEME Suite to identify motifs in DNA sequences uploaded in FASTA format.

## Prerequisites
Before running the application, ensure you have the following installed:

- Python 3.x
- Required Python packages:
  ```bash
  pip install streamlit biopython
  ```
- MEME Suite installed and accessible from the command line. Follow installation instructions [here](http://meme-suite.org/doc/install.html).

## Usage
### Running the Application
1. Clone or download the repository.
2. Navigate to the directory where the script is located.
3. Run the following command to start the Streamlit application:
   ```bash
   streamlit run tf_motif_finder.py
   ```
4. The application will open in a web browser.

### Using the Application
1. Upload a FASTA file containing DNA sequences.
2. Adjust motif search parameters (minimum and maximum motif width).
3. Click the "Run MEME for Motif Discovery" button.
4. Once MEME completes the analysis, a link to the results will be displayed.

### Example Test Data
You can test the application using the example dataset from MEME Suite:
[crp0.fna](http://meme-suite.org/meme-software/example-datasets/crp0.fna).

## Troubleshooting
- If MEME is not found, ensure it is installed and added to the system path.
- If Streamlit does not start, try running:
  ```bash
  python -m streamlit run tf_motif_finder.py
  ```
- Check the logs if MEME analysis fails.

## License
This project is released under an open-source license. 

