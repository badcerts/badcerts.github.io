#!/usr/bin/env python3
"""Package the manifest-listed payload once; write separate archive checksums."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    files = [row['path'] for row in manifest['files']] + ['PUBLIC_MANIFEST.json','receipts/SHA256SUMS']
    destination = ROOT/'downloads'
    destination.mkdir(exist_ok=True)
    archive = destination/'complete-public-package.zip'
    temporary = destination/'complete-public-package.zip.tmp'
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zipped:
        for name in sorted(files):
            path = ROOT/name
            if path.is_symlink() or not path.resolve().is_relative_to(ROOT) or not path.is_file():
                raise ValueError('Unsafe payload path: '+name)
            member = zipfile.ZipInfo(manifest['candidate']+'/'+name,date_time=(2026,10,11,0,0,0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            zipped.writestr(member,path.read_bytes())
    os.replace(temporary,archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination/'SHA256SUMS').write_text(digest+'  '+archive.name+'\n')
    print(json.dumps({'archive':archive.name,'bytes':archive.stat().st_size,'sha256':digest,'payload_files':len(files)}))


if __name__=='__main__':
    main()
