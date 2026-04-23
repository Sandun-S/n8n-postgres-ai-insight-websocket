import psycopg2
import json
from datetime import datetime

# 1. Load the file you saved
with open('kva_dump.json') as f: #kva_dump.json   , pf_dump.json,  grafana_dump.json
    raw_data = json.load(f)

# 2. Connect to Docker Postgres (Host is localhost if running on same machine)
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="qube_password" # Matches your docker-compose
    )
    cur = conn.cursor()

    results = raw_data['response']['results']

    for ref_id in results:
        print(f"Processing RefID: {ref_id}")
        frames = results[ref_id].get('frames', [])
        for frame in frames:
            # Extract labels (Device Name)
            device = frame['schema']['fields'][1]['labels']['device']
            resource = frame['schema']['fields'][1]['labels']['resource_name']
            
            # Extract Data
            timestamps = frame['data']['values'][0]
            values = frame['data']['values'][1]

            for ts, val in zip(timestamps, values):
                if val is None: continue # Skip nulls
                
                # Convert ms timestamp to readable datetime
                dt = datetime.fromtimestamp(ts / 1000.0)
                
                cur.execute(
                    "INSERT INTO telemetry (time, device, resource_name, value) VALUES (%s, %s, %s, %s)",
                    (dt, device, resource, val)
                )
    
    conn.commit()
    print("Migration successful! Data is now in qube_timescale.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        cur.close()
        conn.close()