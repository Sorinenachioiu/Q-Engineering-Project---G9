import base64
import json
import numpy as np
from collections import Counter
import os
from surface_codes.four_two_two import *

def decode_measurement_data(file_name):
    # Load the JSON data from the file
    with open(file_name, 'r') as f:
        data = json.load(f)

    # Extract Base64 encoded data for stabilizer_c and logical_c
    stabilizer_encoded_data = data['__value__']['pub_results'][0]['__value__']['data']['__value__']['fields']['stabilizer_c']['__value__']['array']['__value__']
    logical_encoded_data = data['__value__']['pub_results'][0]['__value__']['data']['__value__']['fields']['logical_c']['__value__']['array']['__value__']
    
    # Decode the Base64 string for stabilizer_c
    stabilizer_decoded_bytes = base64.b64decode(stabilizer_encoded_data)
    logical_decoded_bytes = base64.b64decode(logical_encoded_data)
    
    # Get the number of bits per measurement
    stabilizer_num_bits = data['__value__']['pub_results'][0]['__value__']['data']['__value__']['fields']['stabilizer_c']['__value__']['num_bits']
    logical_num_bits = data['__value__']['pub_results'][0]['__value__']['data']['__value__']['fields']['logical_c']['__value__']['num_bits']
    
    # Convert to binary representation (each measurement is stabilizer_num_bits or logical_num_bits bits here)
    stabilizer_measurements = np.unpackbits(np.frombuffer(stabilizer_decoded_bytes, dtype=np.uint8))
    logical_measurements = np.unpackbits(np.frombuffer(logical_decoded_bytes, dtype=np.uint8))
    
    # Reshape the results to match the number of bits per shot
    stabilizer_reshaped_measurements = stabilizer_measurements.reshape(-1, stabilizer_num_bits)
    logical_reshaped_measurements = logical_measurements.reshape(-1, logical_num_bits)
    
    # Handle arrays with different lengths by trimming or padding
    num_stabilizer_measurements = stabilizer_reshaped_measurements.shape[0]
    num_logical_measurements = logical_reshaped_measurements.shape[0]
    
    if num_stabilizer_measurements < num_logical_measurements:
        # Trim logical measurements to match the stabilizer
        logical_reshaped_measurements = logical_reshaped_measurements[:num_stabilizer_measurements]
    elif num_stabilizer_measurements > num_logical_measurements:
        # Trim stabilizer measurements to match the logical
        stabilizer_reshaped_measurements = stabilizer_reshaped_measurements[:num_logical_measurements]

    # Combine both sets of measurements
    combined_measurements = np.concatenate((stabilizer_reshaped_measurements, logical_reshaped_measurements), axis=1)
    
    # Convert binary measurements to strings
    combined_bitstrings = [''.join(map(str, row)) for row in combined_measurements]
    
    # Count occurrences of each outcome
    combined_counts = Counter(combined_bitstrings)

    # Print results
    print("Combined Measurement Results (Counts):")
    for bitstring, count in combined_counts.items():
        print(f"{bitstring}: {count}")
    
    # Now pass the counts to the next function as needed
    results = analyze_four_two_two_logical_state(combined_counts)
    pretty_print_four_two_two_results(results)

def decode_measurement_results():
    file_name = os.path.join(os.getcwd(), "src", "run_ibm", "four_two_two", "results", "00", "job-cy8w818nrmz00085y3xg-result.json")
    decode_measurement_data(file_name)

# Example usage
decode_measurement_results()
