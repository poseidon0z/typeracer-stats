import requests
import json
import time
import os


def fetch_all_races(player_id, universe="play"):
    last_time = int(time.time())  # Start from the latest timestamp
    all_races = []
    backup_file = f"type_data_{universe}.json"

    # Load existing backup if available
    if os.path.exists(backup_file):
        with open(backup_file, "r") as infile:
            try:
                existing_data = json.load(infile)
                if existing_data:
                    last_time = int(
                        existing_data[-1]["t"]
                    )  # Use the oldest race timestamp
                    all_races = existing_data
            except json.JSONDecodeError:
                print("Backup file is empty or corrupted, starting fresh.")

    new_races = []
    while True:
        end_time = last_time  # Adjust end_time dynamically
        start_time = 0  # Fetch all races up to the oldest available
        url = f"https://data.typeracer.com/games?playerId=tr:{player_id}&universe={universe}&startDate={start_time}&endDate={end_time}"
        response = requests.get(url)
        data_json = response.json()

        if len(data_json) <= 1:
            print("No more races to fetch!")
            break

        data_json = data_json[:-1]  # Remove last element (likely metadata or duplicate)
        new_races.extend(data_json)

        last_time = int(data_json[-1]["t"])  # Update last_time for pagination

        print(f"Fetched {len(new_races)} new races so far...")

        time.sleep(1)  # Avoid hitting API rate limits

    # Append new races to maintain chronological order
    all_races.extend(new_races)

    # Save updated data
    with open(backup_file, "w") as outfile:
        json.dump(all_races, outfile, indent=4)

    return all_races


if __name__ == "__main__":
    player_id = "adi_idgaf"
    universe = "play"
    races = fetch_all_races(player_id, universe)

    print(f"Saved {len(races)} races to type_data_{universe}.json!")
