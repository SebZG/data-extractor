# Data Extractor

A simple Python script that scans one or more text files for emails, phone numbers, and website URLs, then saves the results into a single CSV file.

## What it does

Given a file or folder containing `.txt` files, the script:

- finds email addresses
- finds phone numbers
- finds website URLs
- removes duplicates while keeping the first occurrence
- writes all matches to `contacts.csv` by default

## Requirements

- Python 3.6 or newer
- A text file or a folder of text files to scan

## Usage

From the project directory, run:

```bash
python3 extractor.py example-email.txt
```

This scans the example file and saves results to a file named `contacts.csv` in the current folder.

To scan a folder of text files and choose the output name:

```bash
python3 extractor.py path/to/folder -o contacts.csv
```

You can also point directly to a text file with a custom output path:

```bash
python3 extractor.py /path/to/file.txt -o extracted_contacts.csv
```

## Command-line arguments

- `input`: a single `.txt` file or a directory of `.txt` files
- `-o, --output`: output CSV file path (default: `contacts.csv`)

## Output format

The CSV contains three columns:

- `Type` — either `Email`, `Phone`, or `Website`
- `Value` — the extracted contact detail
- `Source file` — the file where it was found

Example:

```csv
Type,Value,Source file
Email,hello@example.com,example-email.txt
Phone,(555) 123-4567,example-email.txt
Website,www.example.com,example-email.txt
```

## Example

```bash
python3 extractor.py example-email.txt -o my_contacts.csv
```

After running this command, open `my_contacts.csv` in Excel, Google Sheets, or any CSV viewer to review the extracted contacts.

