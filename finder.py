from pathlib import Path
from collections import namedtuple


path_line = namedtuple("File", ["path", "line"])

class Searcher:
    def __init__(self, directory: str = "", suffix: str = ".txt"):
        if directory:
            self.file_list = [i for i in Path(directory).iterdir() if str(i).endswith(suffix)]
            if not self.file_list:
                raise FileNotFoundError(f"no files in directory {directory} that ends with {suffix}")
        self.found = []
        self.curr_pos = 0


    def update_file(self, path):
        self.file_list = [Path(path)]
    def update_dir(self, directory, suffix = ".txt"):
        self.file_list = [i for i in Path(directory).iterdir() if str(i).endswith(suffix)]
        if not self.file_list:
            raise FileNotFoundError(f"no files in directory {directory} that ends with {suffix}")

    def __getitem__(self, item):
        return self.found[item]

    def __iter__(self):
        return self.found

    def __len__(self):
        return len(self.found)

    def search(self, text: str):
        self.found.clear()
        found = defaultdict(list)
        for file_path in self.file_list:
            file = file_path.read_text(encoding="UTF-8")
            if text not in file:
                found[file_path].append("no matches found")
                continue
            else:
                for j in range(len(lines := file.splitlines())):
                    if text in lines[j]:
                        found[file_path].append(j+1)
        for k, v in found.items():
            for item in v:
                self.found.append((k, item))

        return self.found[0]
    def search1(self, text: str):
        self.found.clear()
        for file_path in self.file_list:
            file = file_path.read_text(encoding="UTF-8")
            lines = file.splitlines()
            if text not in file:
                self.found.append(path_line(file_path, None))
            else:
                for i in range(len(lines)):
                    if text in lines[i]:
                        self.found.append(path_line(file_path, i+1))
        self.curr_pos = 0
        return self.found[0]
    def next(self):
        if self.curr_pos < len(self) - 1:
            self.curr_pos += 1
            return self[self.curr_pos]
        else:
            return self[self.curr_pos]

    def previous(self):
        if self.curr_pos > 0:
            self.curr_pos -= 1
            return self[self.curr_pos]
        else:
            return self[self.curr_pos]