import numpy as np
import os
from pathlib import Path


class Dataset:

    def __init__(self, path):

        self._path = os.path.abspath(path)
        self._data_path = os.path.join(self._path, "raw_data/")
        self._annotation_path = os.path.join(self._path,"annotations/")
        self.filenames = self._sorted_files()

        if len(self.filenames) > 0:
            self.set_filename(self.filenames[0])
        self._set_goodness()

    def _set_goodness(self):
        self.good = bool(self.filename) and not self.filename.startswith("bad_")

    def _set_ssins(self, filename):
        self.filename = filename
        path = os.path.join(self._data_path, filename)
        self.ssins = np.load(path)

    def _initialize_annotations(self, return_annotations=False):
        annotation_file = os.path.join(self._annotation_path, self.filename)
        if os.path.exists(annotation_file):
            self.annotations = np.load(annotation_file)
        else:
            self.annotations = np.zeros_like(self.ssins)

        if return_annotations:
            return self.annotations

    def _extract_metadata(self):
        split = self.filename.split("_")
        self.night = split[-2]
        self.pointing = split[-1].split(".")[0][-1]

    def set_filename(self, new_filename):
        self._set_ssins(new_filename)
        self._initialize_annotations()
        self._extract_metadata()
        self._set_goodness()

    def save_annotations(self):
        self.save_path = os.path.join(self._annotation_path, self.filename)
        np.save(self.save_path, self.annotations)
        return self.save_path
    
    def set_pointing(self, pointing):
        self.filenames = self._sorted_files(p=pointing)
        self.set_filename(self.filenames[0])

    def mark_bad(self):
        self.good = False
        self._rename_filename()

    def mark_good(self):
        self.good = True
        self._rename_filename()

    def _rename_filename(self):
        old_base = self.filename
        new_base = (old_base if self.good else f"bad_{old_base}")
        if self.good and old_base.startswith("bad_"):
            new_base = old_base[4:]

        if new_base == old_base:
            return

        old_data = Path(self._data_path) / old_base
        new_data = Path(self._data_path) / new_base
        old_ann  = Path(self._annotation_path) / old_base
        new_ann  = Path(self._annotation_path) / new_base

        # data file
        new_data.parent.mkdir(parents=True, exist_ok=True)
        os.replace(old_data, new_data)

        # annotation file (if present)
        if old_ann.exists():
            new_ann.parent.mkdir(parents=True, exist_ok=True)
            os.replace(old_ann, new_ann)

        self.filename = new_base
        self.filenames = self._sorted_files()

    def count_bad(self):
        return sum(1 for f in self.filenames if f.startswith("bad_"))

    def get_n(self):
        return len(self.filenames)
    
    def load_annotations(self):
        return self._initialize_annotations(return_annotations=True)
    
    def _canonical(self, name):
        return name[4:] if name.startswith("bad_") else name

    def _sorted_files(self, p=""):
        files = [f for f in os.listdir(self._data_path)
                if f.endswith(".npy") and (Path(self._data_path)/f).is_file() and p in f]
        # sort by canonical name, with good first then bad (stable)
        return sorted(files, key=lambda f: (self._canonical(f), f.startswith("bad_")))


if __name__ == "__main__":
    data = Dataset("assets")

