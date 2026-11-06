import glob
import json
import os

files = glob.glob("data/raw/cricsheet_json/*.json")
print(f"Total JSON files: {len(files)}")

# Check match types across the 3488 files
match_types = {}
for i, f in enumerate(files[:500]): # sample 500
    try:
        with open(f, 'r') as fp:
            d = json.load(fp)
            mtype = d.get("info", {}).get("match_type", "Unknown")
            match_types[mtype] = match_types.get(mtype, 0) + 1
    except Exception as e:
        pass

print("Sample 500 files match types:", match_types)
