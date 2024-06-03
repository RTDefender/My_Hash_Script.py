"""
Name: RTDefender
Date: June 03, 2024

"""

import hashlib
import os
import pyfiglet

def hash_file(filename, algorithm='sha256'):
    """Generate a hash for the given file using the specified algorithm."""
    try:
        h = hashlib.new(algorithm)
        with open(filename, 'rb') as file:
            while chunk := file.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except ValueError:
        print(f"Algorithm {algorithm} is not supported.")
        return None
    except Exception as e:
        print(f"An error occurred while hashing the file: {e}")
        return None

def compare_files(file1, file2, algorithm='sha256'):
    """Compare two files to see if they are identical based on their hash."""
    hash1 = hash_file(file1, algorithm)
    hash2 = hash_file(file2, algorithm)
    if hash1 is None or hash2 is None:
        return False
    return hash1 == hash2

def hash_directory(directory, algorithm='sha256'):
    """Generate hashes for all files in a directory and identify duplicates."""
    file_hashes = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_hash = hash_file(file_path, algorithm)
            if file_hash in file_hashes:
                file_hashes[file_hash].append(file_path)
            else:
                file_hashes[file_hash] = [file_path]
    return file_hashes

def find_duplicates(directory, algorithm='sha256'):
    """Find and print duplicate files in a directory based on their hashes."""
    file_hashes = hash_directory(directory, algorithm)
    duplicates = {hash: paths for hash, paths in file_hashes.items() if len(paths) > 1}
    for hash, paths in duplicates.items():
        print(f"Hash: {hash}")
        for path in paths:
            print(f" - {path}")

def main():
    # Display the banner
    banner = pyfiglet.figlet_format("MY HASH SCRIPT")
    print(banner)
    print("-----------------------------------------------------------------------------")

    print("Select an option:")
    print("1. Hash a file")
    print("2. Compare two files")
    print("3. Find duplicate files in a directory")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        filename = input("Enter the file path: ")
        algorithm = input("Enter the hash algorithm (default is sha256): ") or 'sha256'
        print(f"Using algorithm: {algorithm}")
        hash_result = hash_file(filename, algorithm)
        if hash_result:
            print(f"Hash of {filename}: {hash_result}")
    elif choice == '2':
        file1 = input("Enter the first file path: ")
        file2 = input("Enter the second file path: ")
        algorithm = input("Enter the hash algorithm (default is sha256): ") or 'sha256'
        print(f"Using algorithm: {algorithm}")
        if compare_files(file1, file2, algorithm):
            print("Files are identical.")
        else:
            print("Files are not identical.")
    elif choice == '3':
        directory = input("Enter the directory path: ")
        algorithm = input("Enter the hash algorithm (default is sha256): ") or 'sha256'
        print(f"Using algorithm: {algorithm}")
        find_duplicates(directory, algorithm)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
