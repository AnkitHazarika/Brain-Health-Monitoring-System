import os
import random
import shutil
import subprocess
from datetime import datetime, timedelta

# ===== CONFIG =====
SOURCE_DATASET = r"D:\datasets\ISLES-2022"

TARGET_REPO = os.getcwd()
TARGET_DATASET_FOLDER = os.path.join(TARGET_REPO, "Datasets")

START_DATE = datetime(2025, 9, 28)
END_DATE = datetime(2025, 12, 23)

COMMITS = 180
FILES_PER_COMMIT = (3, 8)

PUSH_INTERVAL = 10

PROGRESS_FILE = "progress.txt"

# ==================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_progress(idx):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(idx))

def get_all_files():
    file_list = []
    for root, _, files in os.walk(SOURCE_DATASET):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SOURCE_DATASET)
            file_list.append((full, rel))
    return file_list

def random_date():
    delta = END_DATE - START_DATE
    d = START_DATE + timedelta(days=random.randint(0, delta.days))

    return d.replace(
        hour=random.randint(10, 22),
        minute=random.randint(0, 59)
    )

def copy_file(src, rel):
    dest_path = os.path.join(TARGET_DATASET_FOLDER, rel)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(src, dest_path)

def commit(date, msg):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date.strftime("%Y-%m-%d %H:%M:%S")
    env["GIT_COMMITTER_DATE"] = date.strftime("%Y-%m-%d %H:%M:%S")

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", msg], env=env, check=True)

# ===== MAIN =====

files = get_all_files()
random.shuffle(files)

idx = load_progress()

messages = [
    "Space Station: minor orbit correction applied",
    "Command Center: telemetry drift patched",
    "Astronaut Vega: adjusting solar alignment",
    "Orbital Control: trajectory recalculated",
    "Space Station: stabilizing rotation axis",
    "Commander Orion: signal interference resolved",
    "Ground Control: communication channel secured",
    "Astronaut Nova: sensor calibration updated",
    "Mission Control: propulsion timing refined",
    "Space Station: docking path realigned",

    "Commander Atlas: thruster output balanced",
    "Orbital Control: navigation vectors updated",
    "Astronaut Lyra: thermal system stabilized",
    "Ground Control: telemetry sync restored",
    "Space Station: power grid stabilized",
    "Commander Vega: minor drift corrected",
    "Astronaut Orion: guidance system tuned",
    "Mission Control: signal clarity improved",
    "Space Station: module alignment fixed",
    "Ground Control: relay inconsistencies patched",

    "Astronaut Nova: onboard systems recalibrated",
    "Commander Atlas: fuel flow adjusted",
    "Orbital Control: orbit decay compensated",
    "Space Station: subsystem sync corrected",
    "Mission Control: latency issues resolved",
    "Astronaut Lyra: data relay stabilized",
    "Ground Control: control loop optimized",
    "Commander Orion: navigation glitch fixed",
    "Space Station: structural stress normalized",
    "Orbital Control: trajectory drift minimized",

    "Astronaut Vega: sensor offsets corrected",
    "Mission Control: diagnostics updated",
    "Space Station: timing systems adjusted",
    "Commander Nova: propulsion inconsistency fixed",
    "Ground Control: communication latency reduced",
    "Astronaut Atlas: system thresholds updated",
    "Orbital Control: orbital sync restored",
    "Space Station: energy distribution balanced",
    "Mission Control: telemetry accuracy improved",
    "Commander Lyra: synchronization delay resolved"
]

result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)


commit_count = 0

while commit_count < COMMITS:
    # pick a random day
    base_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))

    # random number of commits that day (max 6)
    commits_today = random.randint(1, 6)

    for _ in range(commits_today):
        if commit_count >= COMMITS or idx >= len(files):
            break

        # random time for each commit
        date = base_date.replace(
            hour=random.randint(10, 22),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        # random files per commit
        n = random.randint(*FILES_PER_COMMIT)

        for _ in range(n):
            if idx >= len(files):
                break
            src, rel = files[idx]
            copy_file(src, rel)
            idx += 1
            save_progress(idx)

        # check if anything to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if result.stdout.strip() == "":
            print("Nothing to commit, skipping...")
            continue

        # commit with random message
        commit(date, random.choice(messages))
        commit_count += 1

        # push periodically
        if commit_count % PUSH_INTERVAL == 0:
            subprocess.run(["git", "push", "origin", "main"])

# final push
subprocess.run(["git", "push", "origin", "main"])