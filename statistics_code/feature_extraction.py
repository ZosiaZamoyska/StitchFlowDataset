import numpy as np
from scipy import signal
from scipy.stats import skew, kurtosis

def analyze_stitch_characteristics(sequence):
    """Analyze key characteristics of a stitch sequence."""
    first_derivative, second_derivative = compute_derivatives(sequence)
    
    # Movement range analysis
    ypr_range = np.ptp(sequence, axis=0)
    
    # Speed analysis (using first derivative)
    max_speeds = np.max(np.abs(first_derivative), axis=0)
    avg_speeds = np.mean(np.abs(first_derivative), axis=0)
    
    # Direction changes
    direction_changes = [count_zero_crossings(sequence[:, i]) for i in range(3)]
    
    # Movement complexity (using acceleration peaks)
    complexity = [count_acceleration_peaks(second_derivative[:, i]) for i in range(3)]
    
    analysis = {
        'duration': len(sequence) * (1000 / 119),  # Convert frames to milliseconds using 119 Hz sampling rate
        'yaw_range': ypr_range[0],
        'pitch_range': ypr_range[1],
        'roll_range': ypr_range[2],
        'max_yaw_speed': max_speeds[0],
        'max_pitch_speed': max_speeds[1],
        'max_roll_speed': max_speeds[2],
        'avg_yaw_speed': avg_speeds[0],
        'avg_pitch_speed': avg_speeds[1],
        'avg_roll_speed': avg_speeds[2],
        'yaw_direction_changes': direction_changes[0],
        'pitch_direction_changes': direction_changes[1],
        'roll_direction_changes': direction_changes[2],
        'yaw_complexity': complexity[0],
        'pitch_complexity': complexity[1],
        'roll_complexity': complexity[2]
    }
    
    return analysis

def compute_derivatives(ypr_data, time_step=1):
    first_derivative = np.gradient(ypr_data, time_step, axis=0)
    second_derivative = np.gradient(first_derivative, time_step, axis=0)
    return first_derivative, second_derivative

def count_zero_crossings(signal):
    return np.sum(np.diff(np.sign(signal)) != 0)

def count_acceleration_peaks(acceleration, threshold_factor=2):
    threshold = np.mean(acceleration) + threshold_factor * np.std(acceleration)
    return np.sum(acceleration > threshold)

def extract_features(sequence, time_step=1):
    """Extract features from YPR sequence data."""
    first_derivative, second_derivative = compute_derivatives(sequence, time_step)
    feature_values = []

    # Raw Yaw, Pitch, Roll Statistics
    stats = [np.mean, np.std, np.min, np.max]
    for func in stats:
        feature_values.extend(func(sequence, axis=0))

    # Velocity (First Derivative)
    for func in stats:
        feature_values.extend(func(first_derivative, axis=0))

    # Acceleration (Second Derivative)
    for func in stats:
        feature_values.extend(func(second_derivative, axis=0))

    # Zero Crossings & Peaks
    for data in first_derivative.T:
        feature_values.append(count_zero_crossings(data))
    for data in second_derivative.T:
        feature_values.append(count_acceleration_peaks(data))

    return np.array(feature_values)

def get_feature_names():
    """Return the names of all features in order."""
    axes = ['yaw', 'pitch', 'roll']
    stats = ['mean', 'std', 'min', 'max']
    
    feature_names = []
    
    # Raw YPR Statistics
    for stat in stats:
        for axis in axes:
            feature_names.append(f'{axis}_{stat}')
    
    # Velocity Statistics
    for stat in stats:
        for axis in axes:
            feature_names.append(f'{axis}_velocity_{stat}')
    
    # Acceleration Statistics
    for stat in stats:
        for axis in axes:
            feature_names.append(f'{axis}_acceleration_{stat}')
    
    # Zero Crossings
    for axis in axes:
        feature_names.append(f'{axis}_zero_crossings')
    
    # Acceleration Peaks
    for axis in axes:
        feature_names.append(f'{axis}_acceleration_peaks')
    
    return feature_names
