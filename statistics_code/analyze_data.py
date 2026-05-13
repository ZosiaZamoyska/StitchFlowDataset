import numpy as np
import logging
import os
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from feature_extraction import extract_features, analyze_stitch_characteristics, get_feature_names

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_participant_data(base_folder, prefix):
    """Load data for a specific participant."""
    data = []
    labels = []
    
    for stitch_type in ['ch', 'sc', 'dc']:  # chain, single crochet, double crochet
        stitch_folder = os.path.join(base_folder, stitch_type)
        if os.path.exists(stitch_folder):
            for file_name in os.listdir(stitch_folder):
                if file_name.startswith(prefix):
                    file_path = os.path.join(stitch_folder, file_name)
                    try:
                        ypr_data = np.loadtxt(file_path, delimiter='\t')
                        if ypr_data.shape[0] > 0:
                            initial_position = ypr_data[0]
                            ypr_data = ypr_data - initial_position
                            data.append(ypr_data)
                            labels.append(stitch_type)
                    except Exception as e:
                        logger.warning(f"Problem loading {file_path}: {str(e)}")
    
    return data, labels

def analyze_participant_data(data, labels, participant_id):
    """Analyze movement characteristics for a specific participant."""
    logger.info(f"\n=== Dataset Statistics for {participant_id} ===")
    
    # Initialize statistics containers
    stats_list = []
    summary_stats = []
    
    # Collect statistics for each sequence
    for i, sequence in enumerate(data):
        characteristics = analyze_stitch_characteristics(sequence)
        
        # Store individual sequence data
        stats_list.append({
            'participant': participant_id,
            'stitch_type': labels[i],
            'sequence_id': i,
            'duration': characteristics['duration'],
            'yaw_range': characteristics['yaw_range'],
            'pitch_range': characteristics['pitch_range'],
            'roll_range': characteristics['roll_range'],
            'max_yaw_speed': characteristics['max_yaw_speed'],
            'max_pitch_speed': characteristics['max_pitch_speed'],
            'max_roll_speed': characteristics['max_roll_speed'],
            'avg_yaw_speed': characteristics['avg_yaw_speed'],
            'avg_pitch_speed': characteristics['avg_pitch_speed'],
            'avg_roll_speed': characteristics['avg_roll_speed'],
            'yaw_direction_changes': characteristics['yaw_direction_changes'],
            'pitch_direction_changes': characteristics['pitch_direction_changes'],
            'roll_direction_changes': characteristics['roll_direction_changes'],
            'yaw_complexity': characteristics['yaw_complexity'],
            'pitch_complexity': characteristics['pitch_complexity'],
            'roll_complexity': characteristics['roll_complexity']
        })
    
    # Calculate statistics per stitch type
    unique_labels = set(labels)
    for stitch_type in unique_labels:
        stitch_indices = [i for i, label in enumerate(labels) if label == stitch_type]
        stitch_data = [stats_list[i] for i in stitch_indices]
        
        # Calculate means and stds for this stitch type
        summary = {
            'participant': participant_id,
            'stitch_type': stitch_type,
            'count': len(stitch_indices),
            'avg_duration': np.mean([d['duration'] for d in stitch_data]),
            'std_duration': np.std([d['duration'] for d in stitch_data]),
            'avg_yaw_range': np.mean([d['yaw_range'] for d in stitch_data]),
            'std_yaw_range': np.std([d['yaw_range'] for d in stitch_data]),
            'avg_pitch_range': np.mean([d['pitch_range'] for d in stitch_data]),
            'std_pitch_range': np.std([d['pitch_range'] for d in stitch_data]),
            'avg_roll_range': np.mean([d['roll_range'] for d in stitch_data]),
            'std_roll_range': np.std([d['roll_range'] for d in stitch_data])
        }
        summary_stats.append(summary)
    
    # Create DataFrames
    df_sequences = pd.DataFrame(stats_list)
    df_summary = pd.DataFrame(summary_stats)
    
    # Save to CSV
    os.makedirs("statistics", exist_ok=True)
    df_sequences.to_csv(f"statistics/sequences_{participant_id}.csv", index=False)
    df_summary.to_csv(f"statistics/summary_{participant_id}.csv", index=False)
    
    return df_sequences, df_summary

def main():
    base_folder = "data_archive"
    prefixes = ['user1_', 'P0_', 'P1_', 'P2_', 'P3_', 'P4_', 'P5_', 'P6_', 'P7_']
    
    # Print model features
    print("\nFeatures used by the model:")
    features = get_feature_names()
    for f in features:
        print("-", f)
    print("\n")
    
    # Analyze data for each participant
    all_summaries = []
    for prefix in prefixes:
        print(f"\nAnalyzing data for {prefix}")
        data, labels = load_participant_data(base_folder, prefix)
        if data:  # Only analyze if we found data
            df_sequences, df_summary = analyze_participant_data(data, labels, prefix)
            all_summaries.append(df_summary)
            print(f"Found {len(data)} sequences")
            print(f"Stitch type distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")
        else:
            print(f"No data found for {prefix}")
    
    # Combine all summaries
    if all_summaries:
        combined_summary = pd.concat(all_summaries, ignore_index=True)
        combined_summary.to_csv("statistics/all_participants_summary.csv", index=False)
        print("\nCombined summary saved to statistics/all_participants_summary.csv")

if __name__ == "__main__":
    main() 