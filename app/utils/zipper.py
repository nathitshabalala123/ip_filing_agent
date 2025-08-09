import os
import zipfile
from typing import List


def zip_files(file_paths: List[str], zip_filename: str) -> str:
    os.makedirs(os.path.dirname(zip_filename) or ".", exist_ok=True)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in file_paths:
            arcname = os.path.basename(path)
            zf.write(path, arcname)
    return zip_filename 