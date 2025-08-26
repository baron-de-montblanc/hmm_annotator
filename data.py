import numpy as np
import os


class Dataset:

    def __init__(self, path):

        self._path = os.path.abspath(path)
        self._data_path = os.path.join(self._path, "raw_data/")
        self._annotation_path = os.path.join(self._path,"annotations/")
        self._filenames = [f for f in os.listdir(self._data_path)]

        if len(self._filenames) > 0:
            self.set_filename(self._filenames[0])

    def _set_ssins(self, filename):
        self._filename = filename
        path = os.path.join(self._data_path, filename)
        self.ssins = np.load(path)

    def _initialize_annotations(self, return_annotations=False):
        annotation_file = os.path.join(self._annotation_path, self._filename)
        if os.path.exists(annotation_file):
            self.annotations = np.load(annotation_file)
        else:
            self.annotations = np.zeros_like(self.ssins)

        if return_annotations:
            return self.annotations

    def _extract_metadata(self):
        split = self._filename.split("_")
        self.night = split[2]
        self.pointing = split[-1].split(".")[0][-1]

    def set_filename(self, new_filename):
        self._set_ssins(new_filename)
        self._initialize_annotations()
        self._extract_metadata()

    def save_annotations(self):
        self.save_path = os.path.join(self._annotation_path, self._filename)
        np.save(self.save_path, self.annotations)
        return self.save_path
    
    def load_annotations(self):
        return self._initialize_annotations(return_annotations=True)

if __name__ == "__main__":
    data = Dataset("assets")
    print(data.load_annotations())