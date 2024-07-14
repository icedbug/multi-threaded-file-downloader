# Multi-Threaded File Downloader

This repository contains a Python script for efficiently downloading large files by splitting the download into multiple chunks and using multi-threading. The script also combines the downloaded chunks into a single file and provides progress bars for both the downloading and combining processes.

## Features

- **Multi-threaded downloading**: Downloads file chunks in parallel to speed up the download process.
- **Progress bars**: Displays progress bars for both downloading and combining file chunks.
- **Error handling**: Handles errors during downloading and combining, and logs detailed messages.
- **Flexible configuration**: Easily configurable for different file URLs and number of threads.

## Requirements

- Python 3.6+
- `requests` library
- `tqdm` library

You can install the required libraries using:
```bash
pip install requests tqdm
