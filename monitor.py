import time
from monitor_engine import check_once

if __name__ == "__main__":
    print("Starting monitor (CLI mode). Press Ctrl+C to stop.")
    try:
        while True:
            new = check_once()
            if new:
                print(f"New alerts: {len(new)}")
            time.sleep(30)  # run every 30s in CLI mode
    except KeyboardInterrupt:
        print("Stopped.")
