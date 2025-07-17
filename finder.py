from pathlib import Path

class Searcher:
    def __init__(self, directory: str = "", suffix: str = ".txt"):
        if directory:
            self.file_list = [i for i in Path(directory).iterdir() if str(i).endswith(suffix)]
            self.file_set = set([str(i) for i in Path(directory).iterdir() if str(i).endswith(suffix)])
            if not self.file_set:
                raise FileNotFoundError(f"no files in directory {directory} that ends with {suffix}")
        self.match = None

    def update_file(self, path):
        self.file_list = [Path(path)]
        self.file_set = {path}

    def update_dir(self, directory, suffix = ".txt"):
        self.file_list = [i for i in Path(directory).iterdir() if str(i).endswith(suffix)]
        self.file_set = set([str(i) for i in Path(directory).iterdir() if str(i).endswith(suffix)])
        if not self.file_list:
            raise FileNotFoundError(f"no files in directory {directory} that ends with {suffix}")

    def __getitem__(self, item):
        return self.file_list[item]

    def __iter__(self):
        return self.file_list

    def clear(self):
        self.match = Match()

    def read_str(self, file_name: str):
        if file_name in self.file_set:
            return Path(file_name).read_text(encoding="UTF-8")
        else:
            return None

    def read_all(self) -> list[str]:
        content = []
        for file in self.file_list:
            content.append(file.read_text())
        return content

    def search(self, text: str, name: str = None):
        found = defaultdict(list)
        if not name:
            for file_path in self.file_list:
                file = file_path.read_text(encoding="UTF-8")
                if text not in file:
                    found[file_path].append("no matches found")
                    continue
                else:
                    for j in range(len(lines := file.splitlines())):
                        if text in lines[j]:
                            found[file_path].append(j+1)
        elif name:
            if text not in (content := self.read_str(name)):
                found[name].append(f"no matches found")
            else:
                for j in range(len(lines := content.splitlines())):
                    if text in lines[j]:
                        found[name].append(j)
        self.match = Match(found)
        self.genf = self.match.move_f()
        self.genb = self.match.move_b()

    def next(self):
        return next(self.genf)

    def previous(self):
        return next(self.genb)

class Match:
    def __init__(self, matches):
        self.file_invokes = []
        self.curr_pos = 0
        self.cache = 1
        for k, v in dict(matches).items():
            for item in v:
                self.file_invokes.append((k, item))

    def __iter__(self):
        return self.file_invokes

    def __getitem__(self, item):
        return self.file_invokes[item]

    def __len__(self):
        return len(self.file_invokes)

    def move_f(self):
        while True:
            if self.curr_pos != len(self) - 1:
                if self.cache != 1:
                    self.curr_pos += 1
                    yield self.file_invokes[self.curr_pos]
                    continue
                self.cache = 1
                yield self.file_invokes[self.curr_pos]
                if self.curr_pos < len(self) - 1:
                    self.curr_pos += 1
            else:
                self.cache = 1
                yield self.file_invokes[self.curr_pos]
    def move_b(self):
        while True:
            if self.curr_pos != 0:
                if self.cache != -1:
                    self.curr_pos -= 1
                    yield self.file_invokes[self.curr_pos]
                    continue
                self.cache = -1
                yield self.file_invokes[self.curr_pos]
                if self.curr_pos > 0:
                    self.curr_pos -= 1
            else:
                self.cache = -1
                yield self.file_invokes[self.curr_pos]