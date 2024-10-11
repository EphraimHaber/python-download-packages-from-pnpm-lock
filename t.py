import subprocess
import yaml
import os
import uuid

PACKED_TGZ_DESTINATION = f"tgz-files-{str(uuid.uuid4())}"
os.mkdir(PACKED_TGZ_DESTINATION)


def log_progress(curr: int, total_length: int) -> None:
    percentage_done = ((curr + 1) / (total_length)) * 100
    print(f"downloading {curr + 1} / {total_length} - {percentage_done:.4f}% done")


with open("pnpm-lock.yaml", "r") as file:
    lockfile = yaml.safe_load(file)

packages = lockfile.get("packages", {})
packages_full_names_versions = [t[0] for t in list(packages.items())]
for i, pkg_name_version in enumerate(packages_full_names_versions):
    subprocess.run(
        ["npm", "pack", pkg_name_version, "--pack-destination", PACKED_TGZ_DESTINATION],
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    log_progress(i, len(packages_full_names_versions))


print(f"The packages are all downloaded and can be found in {PACKED_TGZ_DESTINATION}")
