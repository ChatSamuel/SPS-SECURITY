import hashlib


class Fingerprint:

    def __init__(self, sha256):
        self.sha256 = sha256


def compute_fingerprint(file_path):

    h = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)

    return Fingerprint(h.hexdigest())
