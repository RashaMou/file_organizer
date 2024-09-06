import os
import hashlib
import shutil
from collections import defaultdict
from typing import List, Dict, Tuple


class FileOrganizer:
    def __init__(self, folder_path: str):
        self.folder_path = os.path.expanduser(folder_path)
        self.duplicates_folder = os.path.join(self.folder_path, "Duplicates")
        self.extension_folders: Dict[str, str] = {}
        self.file_hashes: Dict[str, str] = {}
        self.move_count: Dict[str, int] = defaultdict(int)
        self.report: List[str] = []

    def organize(self) -> Tuple[int, int]:
        os.makedirs(self.duplicates_folder, exist_ok=True)
        total_files = len(
            [
                f
                for f in os.listdir(self.folder_path)
                if os.path.isfile(os.path.join(self.folder_path, f))
            ]
        )
        processed_files = 0

        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path) and not filename.startswith("."):
                self._process_file(filename, file_path)
                processed_files += 1

        return total_files, processed_files

    def _process_file(self, filename: str, file_path: str) -> None:
        ext = self._get_file_extension(filename)
        if ext is None:
            return

        destination_folder = self._get_destination_folder(ext)
        file_hash = self._calculate_file_hash(file_path)

        if file_hash in self.file_hashes:
            self._move_file(file_path, self.duplicates_folder, filename)
        else:
            self.file_hashes[file_hash] = file_path
            if not os.path.exists(os.path.join(destination_folder, filename)):
                self._move_file(file_path, destination_folder, filename)

    def _get_file_extension(self, filename: str) -> str | None:
        _, ext = os.path.splitext(filename)
        if ext == "":
            self.report.append(f"File {filename} doesn't have an extension, skipping.")
            return None
        ext = ext.lstrip(".")
        print(f"EXT: {ext}")
        return ext

    def _get_destination_folder(self, ext: str) -> str:
        if ext not in self.extension_folders:
            folder = os.path.join(self.folder_path, ext)
            os.makedirs(folder, exist_ok=True)
            self.extension_folders[ext] = folder
        return self.extension_folders[ext]

    def _calculate_file_hash(self, file_path: str) -> str:
        md5 = hashlib.md5()
        chunk_size = 8192
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()

    def _move_file(self, source: str, destination_folder: str, filename: str) -> None:
        shutil.move(source, destination_folder)
        self.report.append(f"Moved {filename} to {destination_folder}")
        self.move_count[destination_folder] += 1

    def get_report(self):
        summary = []
        for dir, count in self.move_count.items():
            summary.append(f"Moved {count} file(s) to {dir}")

        return {"summary": summary, "details": self.report}
