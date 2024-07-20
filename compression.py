import gzip
import io


def gzip_compress(data):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(data)
    return out.getvalue()
