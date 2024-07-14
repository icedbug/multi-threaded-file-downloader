import os
import threading
import requests
from tqdm import tqdm
import time

# Define the URL and the number of threads
url = "https://samples.vx-underground.org/tmp/Families.7z"
num_threads = 4
download_dir = "E:\\downloaded_files"

# Create a directory for downloads if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Get the file size
response = requests.head(url)
file_size = int(response.headers['Content-Length'])

# Define the size of each chunk
chunk_size = file_size // num_threads

# Create a list to store the start and end byte positions for each chunk
chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads)]
# Adjust the last chunk to include any remaining bytes
chunks[-1] = (chunks[-1][0], file_size - 1)

# Initialize a global progress bar
progress = tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading')

def download_chunk(url, start, end, index):
    headers = {'Range': f'bytes={start}-{end}'}
    part_file_path = os.path.join(download_dir, f"part_{index}")
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        total_downloaded = 0
        start_time = time.time()
        with open(part_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_downloaded += len(chunk)
                    progress.update(len(chunk))
        end_time = time.time()
        download_speed = total_downloaded / (end_time - start_time)
        print(f"Thread {index}: Completed downloading chunk {index} at {download_speed / 1024:.2f} KB/s")
    except requests.RequestException as e:
        print(f"Thread {index}: Error downloading chunk {index} - {e}")
    except Exception as e:
        print(f"Thread {index}: Unexpected error - {e}")

# Create and start threads for downloading chunks
threads = []
for i, (start, end) in enumerate(chunks):
    thread = threading.Thread(target=download_chunk, args=(url, start, end, i))
    threads.append(thread)
    thread.start()
    print(f"Thread {i}: Started downloading chunk {i}")

# Wait for all download threads to finish
for thread in threads:
    thread.join()

# Combine the chunks into a single file
output_file_path = os.path.join(download_dir, "Families.7z")
try:
    with open(output_file_path, "wb") as f, tqdm(total=file_size, unit='B', unit_scale=True, desc='Combining') as progress_bar:
        for i in range(num_threads):
            part_file_path = os.path.join(download_dir, f"part_{i}")
            if os.path.exists(part_file_path):
                with open(part_file_path, "rb") as part_file:
                    while True:
                        data = part_file.read(1024 * 1024)  # Read in 1 MB chunks
                        if not data:
                            break
                        f.write(data)
                        progress_bar.update(len(data))
                os.remove(part_file_path)
            else:
                print(f"Warning: {part_file_path} does not exist.")
    print("Files combined successfully!")
except OSError as e:
    print(f"Error combining files: {e}")
except Exception as e:
    print(f"Unexpected error during file combination: {e}")

progress.close()
print("Download completed!")
