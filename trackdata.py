"""
trackdata.py
Traverses the specific trajectories folder and counts roles in each message 
(system, user, assistant, tool) for each trajectory JSON file. Also checks for unknown role entries

Usage:
    python trackdata.py --dir trajectories/claude-4-5-opus-high

"""

import json
import argparse
import csv
from pathlib import Path


def count_roles(messages: list) -> dict:
    '''
    Function to count all the roles in list of messages(singe json file)
    :params: messages: list of messages for which roles need to be counted
    '''
    counts = {"system": 0, "user": 0, "assistant": 0, "tool": 0, "unknown": 0}
    for msg in messages:
        role = msg.get("role", "").lower().strip()
        # If role is not part of the asked categories, it is counted as unknown. This ensures all messages with role are counted.
        if role in counts:
            counts[role] += 1
        else:
            counts["unknown"] += 1
    return counts


def process_folder(folder: Path, csv_path: Path):
    '''
    Function to process the messages in each foldedr. 
    Calls the count_roles function for each JSON files found.
    :params: folder: path to the folder where the JSON files are present.
           : csv_path: path to the folder where the final counts are to be saved.
    '''
    files = sorted(folder.glob("*.json"))
 
    if not files:
        print(f"No JSON files found in {folder}")
        return
 
    print(f"Found {len(files)} trajectory files in {folder}\n")
 
    rows = []
    grand = {"system": 0, "user": 0, "assistant": 0, "tool": 0, "unknown": 0}
 
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
 
            # Handle both bare list and wrapped {"messages": [...]}
            if isinstance(data, dict):
                data = data.get("messages") or data.get("trajectory") or []
 
            counts = count_roles(data)
            total  = sum(counts.values())
 
            for key in grand:
                grand[key] += counts[key]
 
            rows.append({
                "file":      path.name,
                "system":    counts["system"],
                "user":      counts["user"],
                "assistant": counts["assistant"],
                "tool":      counts["tool"],
                "unknown":   counts["unknown"],
                "total":     total,
            })

            # additional print
            # print(
            #     f"{path.name} "
            #     f"{counts['system']} "
            #     f"{counts['user']} "
            #     f"{counts['assistant']} "
            #     f"{counts['tool']} "
            #     f"{counts['unknown']} "
            #     f"{total}"
            # )
 
        except Exception as e:
            print(f"{path.name:} ERROR: {e}")
 
    # Print grand total
    grand_total = sum(grand.values())
    # print(
    #     f"{'TOTAL'} "
    #     f"{grand['system']} "
    #     f"{grand['user']} "
    #     f"{grand['assistant']} "
    #     f"{grand['tool']} "
    #     f"{grand['unknown']} "
    #     f"{grand_total}"
    # )
    print(f"\nAverage messages per trajectory: {grand_total / len(files):.1f}")
 
    # Save to CSV
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "system", "user", "assistant", "tool", "unknown", "total"])
        writer.writeheader()
        writer.writerows(rows)
        # Add a totals row at the bottom of the csv file 
        writer.writerow({
            "file":      "TOTAL",
            "system":    grand["system"],
            "user":      grand["user"],
            "assistant": grand["assistant"],
            "tool":      grand["tool"],
            "unknown":   grand["unknown"],
            "total":     grand_total,
        })
 
    print(f"\nCSV saved to: {csv_path.resolve()}")
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="trajectories", help="Folder to scan")
    parser.add_argument("--out", default=None, help="Output CSV filename (default: <folder-name>_counts.csv)")
    args = parser.parse_args()
 
    folder = Path(args.dir)
    csv_path = Path(args.out) if args.out else Path(f"{folder.name}_counts.csv")
 
    process_folder(folder, csv_path)