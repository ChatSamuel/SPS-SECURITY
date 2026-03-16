import hashlib

def get_hash(file):

    sha256 = hashlib.sha256()

    try:

        with open(file, "rb") as f:

            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except:
        return None
