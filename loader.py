import os
import zipfile
from dataclasses import dataclass
from typing import List, Dict, Optional

import pandas as pd


@dataclass
class Session:
    folder: str
    session_key: str
    files: List[str]
    pos: Optional[pd.DataFrame]
    accel: Optional[pd.DataFrame]
    orient: Optional[pd.DataFrame]
    angvel: Optional[pd.DataFrame]
    magfield: Optional[pd.DataFrame]


def _ensure_unzipped(folder: str) -> None:
    """Extract zip files and also extract zips found in subdirectories"""
    zip_files = []
    # Find all zip files recursively
    for dirpath, dirnames, filenames in os.walk(folder):
        for name in filenames:
            if name.lower().endswith('.zip'):
                zip_files.append((dirpath, name))
    
    for dirpath, name in zip_files:
        zip_path = os.path.join(dirpath, name)
        out_dir = os.path.join(dirpath, f"{name}_unzipped")
        if not os.path.isdir(out_dir):
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    zf.extractall(out_dir)
            except Exception:
                pass


def _has_gps_columns(csv_path: str) -> bool:
    """Check if CSV has GPS columns (latitude, longitude, timestamp)"""
    try:
        df = pd.read_csv(csv_path, nrows=1)
        cols_lower = [c.lower() for c in df.columns]
        has_lat = any('lat' in c for c in cols_lower)
        has_lon = any('lon' in c for c in cols_lower)
        has_ts = any('timestamp' in c or 'time' in c for c in cols_lower)
        return has_lat and has_lon and has_ts
    except Exception:
        return False


def _collect_csvs(roots: List[str]) -> List[str]:
    csvs: List[str] = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        # Recursively search for sensorlog_*.csv files in all subdirectories
        # Also accept variations like SensorLog_*.csv or any CSV with GPS columns
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                name_lower = name.lower()
                if name_lower.endswith('.csv'):
                    csv_path = os.path.join(dirpath, name)
                    # Match sensorlog_*.csv or SensorLog_*.csv or similar patterns
                    # OR accept any CSV that has GPS columns (latitude, longitude, timestamp)
                    if 'sensorlog' in name_lower or 'sensor_log' in name_lower or _has_gps_columns(csv_path):
                        csvs.append(csv_path)
    # Deduplicate paths
    unique = sorted(set(csvs))
    return unique


def _group_by_session(csvs: List[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for path in csvs:
        base = os.path.basename(path)
        stem = os.path.splitext(base)[0]
        parts = stem.split('_')
        if len(parts) < 3:
            key = stem
        else:
            key = f"{parts[-2]}_{parts[-1]}"
        groups.setdefault(key, []).append(path)
    return groups


def _read_if_exists(files: List[str], kind: str) -> Optional[pd.DataFrame]:
    for path in files:
        basename_lower = os.path.basename(path).lower()
        # Match patterns like: sensorlog_pos_*.csv, SensorLog_pos_*.csv, *_pos_*.csv, etc.
        matches_pattern = f"_{kind}_" in basename_lower or f"sensorlog_{kind}_" in basename_lower or f"sensor_log_{kind}_" in basename_lower
        
        # For 'pos' type, also accept any CSV with GPS columns as fallback
        if kind == 'pos' and not matches_pattern:
            matches_pattern = _has_gps_columns(path)
        
        if matches_pattern:
            try:
                return pd.read_csv(path)
            except Exception:
                return None
    return None


def load_sessions(input_folders: List[str]) -> List[Session]:
    sessions: List[Session] = []
    seen_keys: Dict[str, bool] = {}
    for folder in input_folders:
        if not os.path.isdir(folder):
            continue
        _ensure_unzipped(folder)
        # Collect all root directories: main folder + all _unzipped folders recursively
        roots = [folder]
        for dirpath, dirnames, filenames in os.walk(folder):
            for d in dirnames:
                if d.endswith('_unzipped'):
                    roots.append(os.path.join(dirpath, d))
        csvs = _collect_csvs(roots)
        if not csvs:
            continue
        groups = _group_by_session(csvs)
        for key, files in groups.items():
            sess_key = f"{folder} | {key}"
            if seen_keys.get(sess_key):
                continue
            seen_keys[sess_key] = True
            sess = Session(
                folder=folder,
                session_key=sess_key,
                files=files,
                pos=_read_if_exists(files, 'pos'),
                accel=_read_if_exists(files, 'accel'),
                orient=_read_if_exists(files, 'orient'),
                angvel=_read_if_exists(files, 'angvel'),
                magfield=_read_if_exists(files, 'magfield'),
            )
            sessions.append(sess)
    return sessions


