
import json
import os
from pathlib import Path
from docent import Docent


# CONFIG 
# Update your API key here
API_KEY       = "Docent_API_Key" 
# Collection ID for each model
COLLECTIONS = {
    "claude-4-5-opus-high": "b038912e-0133-4594-b093-92806f8ffb17",
    "gemini-3-flash-high": "1ebbdd7a-55b3-4015-9b83-5978cc7fb618",
    "minimax-m2-5-high": "5b77e003-7328-4003-879e-9b55dd3a0b6f",
    "claude-opus-4-6": "9243cc78-d399-402f-be97-e366ff63282c",
    "gpt5-2-codex": "fb22a2e4-0a41-4d41-8e1e-388d4cb50d80",
}
MODEL = "gpt5-2-codex"
COLLECTION_ID = COLLECTIONS[MODEL]
OUTPUT_DIR = Path(f"trajectories/{MODEL}")

def download_all(client: Docent, collection_id: str, output_dir: Path):
    '''
    Download all json file for each model(collection_id) from Docent and save it in the output_dir path.
    '''
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching agent run list from collection: {collection_id}")

    page_size = 1000
    offset    = 0
    all_runs  = []

    while True:
        result = client.execute_dql(
            collection_id,
            f"""
            SELECT
                ar.id              AS run_id,
                ar.name            AS run_name,
                ar.metadata_json   AS metadata
            FROM agent_runs ar
            ORDER BY ar.id
            LIMIT {page_size} OFFSET {offset}
            """
        )
        rows = client.dql_result_to_dicts(result)
        if not rows:
            break
        all_runs.extend(rows)
        offset += page_size
        print(f"  Fetched {len(all_runs)} runs so far...")

    print(f"Total runs found: {len(all_runs)}")

    saved = 0
    skipped = 0

    for run in all_runs:
        run_id   = run["run_id"]
        run_name = run.get("run_name") or run_id  

        safe_name = run_name.replace("/", "_").replace(" ", "_")
        out_path  = output_dir / f"{safe_name}.json"

        if out_path.exists():
            skipped += 1
            continue   

        # Fetch the transcript (messages) for this run
        result = client.execute_dql(
            collection_id,
            f"""
            SELECT
                t.messages
            FROM transcripts t
            JOIN agent_runs ar ON ar.id = t.agent_run_id
            WHERE ar.id = '{run_id}'
            LIMIT 1
            """
        )
        rows = client.dql_result_to_dicts(result)

        if not rows:
            print(f"  WARNING: no transcript found for run {run_name}")
            continue

        # parsing the messages
        messages = rows[0]["messages"]
        if isinstance(messages, str):
            messages = json.loads(messages)

        # Save to file
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        saved += 1
        if saved % 50 == 0:
            print(f"  Saved {saved} trajectories...")

    print(f"\nDone! Saved {saved} new files, skipped {skipped} already existing.")
    print(f"Files are in: {output_dir.resolve()}")

if __name__ == "__main__":
    if API_KEY == "Docent_API_Key":
        print("ERROR: Please replace YOUR_API_KEY with your actual Docent API key.")
        print("Get it from: https://docent.transluce.org → Settings → API Keys")
        exit(1)

    client = Docent(api_key=API_KEY)
    download_all(client, COLLECTION_ID, OUTPUT_DIR)