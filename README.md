# Package Downloader Using `pnpm-lock.yaml`

This project provides a script to download all the packages specified in your `pnpm-lock.yaml` file and saves them as `.tgz` files in a folder. Each run creates a unique folder named `tgz-files-<uuid>` to store the packages.

## Requirements

Before using the script, ensure you have the following installed:

- **Python 3.x**
- **PNPM** or **NPM** (used to pack the packages)
- **PyYAML** library (for reading the `pnpm-lock.yaml` file)

Install the required Python library by running:

```bash
pip install pyyaml
```

# How to Use

1. Clone the Repository or Download the Script
   Download the download_packages.py script to your local machine.

2. Prepare Your pnpm-lock.yaml File
   Ensure that your pnpm-lock.yaml file is in the same directory as the script.

## You can also make a pnpm-lock file from package.json

Just make sure the package.json file is in the same directory as the script and run:

```bash
pnpm install --lockfile-only
```

this will make a pnpm-lock file without downloading the deps to node_modules

3. Run the Script
   Execute the script using Python:

```bash
python download_packages.py
```

4. Script Execution Details

- The script will create a directory named tgz-files-<uuid>, where <uuid> is a unique identifier generated for each run.
- It reads the pnpm-lock.yaml file and extracts all package names and versions.
- For each package, it runs:

```bash
npm pack <package-name>@<version> --pack-destination tgz-files-<uuid>
```

- The script suppresses the output of the npm pack command to keep the console output clean.
- Progress is logged to the console with the current download status and percentage completed.

5. Completion
   After the script finishes, it will display the location of the downloaded packages:

# Example Output

```
downloading 1 / 25 - 4.0000% done
downloading 2 / 25 - 8.0000% done
...
downloading 25 / 25 - 100.0000% done
The packages are all downloaded and can be found in tgz-files-123e4567-e89b-12d3-a456-426614174000
```
