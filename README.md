# Crochet movement dataset — release notes

This data includes recorded sequence movement of chain, single crochet, and double crochet stitches used in StitchFlow. 

---

## Contents of this release

This archive includes:

- **Raw sensor recordings** from crochet stitch movements, organized so each file is one labeled stitch sequence (see [Directory layout](#directory-layout)).
- **Participants:** anonymous identifiers **P0** through **P7**, plus **user1** (researcher).
- **Optional bundled materials** 
  - `statistics/` — aggregated tables (per-participant summaries, sequence-level metrics).
  - Scripts used to generate those statistics and features (see [Provenance and reproducibility](#provenance-and-reproducibility)).

---

## Directory layout

Top-level folders are **stitch labels**; each file is one sequence from a given participant.

```text
data_archive/
  ch/          # chain — one .txt file per sequence
  sc/          # single crochet
  dc/          # double crochet
```

**Naming convention:** `[participant]_[sequence_id].txt`

- Participants: `P0` … `P7`, `user1`
- Example: `ch/P3_14.txt` — chain stitch, participant P3, sequence 14  
- Example: `sc/user1_36.txt` — single crochet, user1 (researcher), sequence 36

---

## File format

Each `.txt` file is a time-series of the IMU orientation.

- **Delimiter:** tab-separated values (`\t`)  
- **Columns / fields:** yaw, pitch, roll in degrees
- **Sampling rate:** 119Hz
- **Preprocessing in released files:** sequences are relative to the initialization orientation

---

## Labels (stitch types)

| Code | Meaning        | Notes |
|------|----------------|-------|
| `ch` | Chain          | 260 entries  |
| `sc` | Single crochet | 260 entries  |
| `dc` | Double crochet | 260 entries  |

---

## Dataset statistics

- **`all_participants_summary.csv`** — aggregated counts and summary metrics per participant and stitch type.
- **`sequences_[participant].csv`** — per-sequence metrics for that participant.
- **`summary_[participant].csv`** — summary for that participant.

### Statistics CSV format

All files in `statistics/` are comma-separated (`.csv`) and use the participant naming pattern `user1_`, `P0_` ... `P7_`.

- **`sequences_[participant].csv` columns**
  - `participant`, `stitch_type`, `sequence_id`
  - `duration` (ms at 119 Hz), `yaw_range`, `pitch_range`, `roll_range`
  - `max_yaw_speed`, `max_pitch_speed`, `max_roll_speed`
  - `avg_yaw_speed`, `avg_pitch_speed`, `avg_roll_speed`
  - `yaw_direction_changes`, `pitch_direction_changes`, `roll_direction_changes`
  - `yaw_complexity`, `pitch_complexity`, `roll_complexity`
- **`summary_[participant].csv` and `all_participants_summary.csv` columns**
  - `participant`, `stitch_type`, `count`
  - `avg_duration`, `std_duration`
  - `avg_yaw_range`, `std_yaw_range`
  - `avg_pitch_range`, `std_pitch_range`
  - `avg_roll_range`, `std_roll_range`

---

## Provenance and reproducibility

Statistics and features in this project were produced with code under `statistics_code/`. This release includes the processed subset needed to reproduce `statistics/`.

Typical entry points:

- **`analyze_data.py`** — loads participant-prefixed files from the stitch-type folders (`ch`, `sc`, `dc`), computes movement characteristics, and writes CSVs under `statistics/`.
- **`feature_extraction.py`** — feature definitions used by the analysis scripts.

**Dependencies**

- Python 3.9+
- `numpy`, `pandas`, `scipy`, `scikit-learn`

Install dependencies:

```bash
pip install numpy pandas scipy scikit-learn
```

**To reproduce** summary tables from this archive:

1. Ensure `data_archive/` is at repository root.
2. Run: `python statistics_code/analyze_data.py`
3. Confirm outputs match the bundled `statistics/` files (within floating-point tolerance).

---

## Suggested citation

```bibtex
@inproceedings{10.1145/3746059.3747715,
author = {Marciniak, Zofia and Lertjaturaphat, Punn and Bianchi, Andrea},
title = {StitchFlow: Enabling In-Situ Creative Explorations of Crochet Patterns With Stitch Tracking and Process Sharing},
year = {2025},
isbn = {9798400720376},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3746059.3747715},
doi = {10.1145/3746059.3747715},
booktitle = {Proceedings of the 38th Annual ACM Symposium on User Interface Software and Technology},
articleno = {7},
numpages = {15},
keywords = {Digital Fabrication, Crochet Patterns, Design Tools},
location = {
},
series = {UIST '25}
}
```

---

## Changelog

| Version | Date       | Changes |
|---------|------------|---------|
| 1.0.0   | 2026-05-13 | Initial public release |

