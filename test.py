import pytest
from unittest import mock
from io import StringIO
import os
from Bio import SeqIO

# Mock Streamlit components for testing
@pytest.fixture
def mock_st():
    with mock.patch('streamlit.title'), mock.patch('streamlit.file_uploader'), \
         mock.patch('streamlit.info'), mock.patch('streamlit.markdown'), \
         mock.patch('streamlit.pyplot'):
        yield

# Test for padding function
def test_pad_fasta_sequences():
    input_fasta = "test_input.fasta"
    output_fasta = "test_output.fasta"
    
    # Sample input sequence data
    sample_fasta = """>seq1
    ATGC
    >seq2
    ATG
    >seq3
    ATGCG"""
    
    # Write the sample data to a file
    with open(input_fasta, 'w') as f:
        f.write(sample_fasta)
    
    # Run the padding function
    pad_fasta_sequences(input_fasta, output_fasta)
    
    # Read back the padded sequences and verify
    with open(output_fasta, 'r') as f:
        output_lines = f.readlines()
    
    assert len(output_lines) == 6  # 3 sequences, each with header and sequence
    assert output_lines[1].strip() == "ATGC-"  # seq1 padded to length 5
    assert output_lines[3].strip() == "ATG--"  # seq2 padded to length 5
    assert output_lines[5].strip() == "ATGCG"  # seq3 remains unchanged
    
    # Clean up the files
    os.remove(input_fasta)
    os.remove(output_fasta)

# Test for conservation calculation
def test_calculate_conservation():
    # Sample aligned sequences (this could be an output from the pad_fasta_sequences function)
    aligned_fasta = """>seq1
    ATGC-
    >seq2
    ATG--
    >seq3
    ATGCG"""
    
    # Write the sample alignment to a file
    aligned_file = "aligned.fasta"
    with open(aligned_file, 'w') as f:
        f.write(aligned_fasta)
    
    # Calculate conservation scores
    scores, consensus = calculate_conservation(aligned_file, tie_strategy="mark_as_X")
    
    # Check the consensus sequence
    assert consensus == "ATGC-"  # The consensus should match the most common residues at each position
    
    # Check the conservation scores (should be a list of scores for each position)
    assert len(scores) == 5  # Should match the length of the longest sequence
    
    # Clean up the file
    os.remove(aligned_file)

# Test for Streamlit plot
def test_plot_conservation(mock_st):
    # Mock conservation scores
    scores = [0.9, 0.8, 0.95, 0.85, 0.9]
    
    # Run the plot function
    plot_conservation(scores)
    
    # Check if the plot was generated
    mock_st.pyplot.assert_called_once()

# Test the complete process
def test_complete_process(mock_st):
    # Test complete process of uploading a file and running all functions
    # Prepare a mock for the file uploader
    with mock.patch("streamlit.file_uploader") as mock_file_uploader:
        # Simulate file upload by returning a StringIO object with FASTA content
        mock_file_uploader.return_value = StringIO(">seq1\nATGC\n>seq2\nATG\n>seq3\nATGCG")
        
        # Execute the main Streamlit workflow
        uploaded_file = mock_file_uploader.return_value
        fasta_content = uploaded_file.getvalue().decode("utf-8")
        
        # Use a temporary path for this test
        fasta_path = "input.fasta"
        with open(fasta_path, "w") as f:
            f.write(fasta_content)
        
        # Align sequences, calculate conservation, and plot
        aligned_file = "aligned.fasta"
        pad_fasta_sequences(fasta_path, aligned_file)
        scores, consensus = calculate_conservation(aligned_file, tie_strategy="mark_as_X")
        plot_conservation(scores)
        
        # Verify the consensus sequence
        assert consensus == "ATGC-"  # Expected consensus
        
        # Clean up files
        os.remove(fasta_path)
        os.remove(aligned_file)
