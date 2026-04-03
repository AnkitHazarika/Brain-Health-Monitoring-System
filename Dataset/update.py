import os
import random
import shutil
import subprocess
from datetime import datetime, timedelta

# ===== CONFIG =====
SOURCE_DATASET = r"D:\datasets\ISLES-2022"

TARGET_REPO = os.getcwd()
TARGET_DATASET_FOLDER = os.path.join(TARGET_REPO, "Datasets")

START_DATE = datetime(2025, 8, 14)
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
    "add stroke case data",
    "update FLAIR scans",
    "add DWI images",
    "dataset preprocessing",
    "add ADC maps",
    "update patient samples"
]

result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)


for i in range(COMMITS):
    n = random.randint(*FILES_PER_COMMIT)
    date = random_date()

    for _ in range(n):
        if idx >= len(files):
            break
        src, rel = files[idx]
        copy_file(src, rel)
        idx += 1

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )

    if result.stdout.strip() == "":
        print("Nothing to commit, skipping...")
        continue

    # ✅ Only commit if there are changes
    commit(date, random.choice(messages))

    if i % PUSH_INTERVAL == 0 and i != 0:
        subprocess.run(["git", "push", "origin", "main"])

    if idx >= len(files):
        break

# final push
subprocess.run(["git", "push", "origin", "main"])