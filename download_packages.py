import subprocess
import yaml
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

PACKED_TGZ_DESTINATION = f"tgz-files-{str(uuid.uuid4())}"
os.mkdir(PACKED_TGZ_DESTINATION)

# Thread-safe counter and lock
total_downloaded = 0
total_downloaded_lock = threading.Lock()

def log_progress(package_name: str, total_length: int) -> None:
    global total_downloaded
    with total_downloaded_lock:
        total_downloaded += 1
        percentage_done = (total_downloaded / total_length) * 100
    print(f"{package_name} downloaded ({total_downloaded} / {total_length} - {percentage_done:.4f}% done)")


def download_package(pkg_name_version: str, total_length: int) -> None:
    subprocess.run(
        ["npm", "pack", pkg_name_version, "--pack-destination", PACKED_TGZ_DESTINATION],
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    log_progress(pkg_name_version, total_length)


# Load package names and versions from the lockfile
with open("pnpm-lock.yaml", "r") as file:
    lockfile = yaml.safe_load(file)

packages = lockfile.get("packages", {})
packages_full_names_versions = [t[0] for t in list(packages.items())]
total_packages = len(packages_full_names_versions)

# Use ThreadPoolExecutor to download packages in parallel
with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(download_package, pkg_name_version, total_packages)
        for pkg_name_version in packages_full_names_versions
    ]

    # Ensure progress is logged as tasks complete
    for future in as_completed(futures):
        future.result()  # This will raise any exceptions encountered in the threads

print(f"The packages are all downloaded and can be found in {PACKED_TGZ_DESTINATION}")
