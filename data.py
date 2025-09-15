import numpy as np
import os


class Dataset:

    def __init__(self, path):

        self._path = os.path.abspath(path)
        self._data_path = os.path.join(self._path, "raw_data/")
        self._annotation_path = os.path.join(self._path,"annotations/")
        self.filenames = sorted([f for f in os.listdir(self._data_path)])

        if len(self.filenames) > 0:
            self.set_filename(self.filenames[0])

        if "bad" in self.filename:
            self.good = False
        else:
            self.good = True

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
        self.night = split[2]
        self.pointing = split[-1].split(".")[0][-1]

    def set_filename(self, new_filename):
        self._set_ssins(new_filename)
        self._initialize_annotations()
        self._extract_metadata()

    def save_annotations(self):
        self.save_path = os.path.join(self._annotation_path, self.filename)
        np.save(self.save_path, self.annotations)
        return self.save_path
    
    def set_pointing(self, pointing):
        _new_filenames = sorted([f for f in os.listdir(self._data_path) if pointing in f])
        self.filenames = _new_filenames
        self.set_filename(self.filenames[0])

    def mark_bad(self):
        self.good = False
        self._rename_filename()

    def mark_good(self):
        self.good = True
        self._rename_filename()

    def _rename_filename(self):

        if self.good:
            if "bad_" in self.filename:
                new_name = self.filename.split("bad_")[1]
            else:
                new_name = self.filename

        else:
            if "bad_" not in self.filename:
                new_name = "bad_" + self.filename
            else:
                new_name = self.filename

        old_name = os.path.join(self._data_path, self.filename)
        new_path = os.path.join(self._data_path, new_name)

        if old_name != new_path:
            os.rename(old_name, new_path)

        self.filename = new_name


    def get_n(self):
        return len(self.filenames)
    
    def load_annotations(self):
        return self._initialize_annotations(return_annotations=True)

if __name__ == "__main__":
    data = Dataset("assets")
    print(data.good)
    data.mark_good()
    print(data.good)

