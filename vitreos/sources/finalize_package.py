#!/usr/bin/env python3
"""Explicitly write the output inventory/ledger after a reviewed build.

This writer is separate from the read-only verifier. Rebuilding changes artifact
identity and does not transfer prior visual, security or publication acceptance.
"""
from pathlib import Path
import argparse,hashlib,json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();root=args.root.resolve()
    excluded={'PUBLIC_MANIFEST.json','receipts/SHA256SUMS','downloads/complete-public-package.zip','downloads/SHA256SUMS'}
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_symlink():raise ValueError('No symlinks in public package')
        if not p.is_file():continue
        name=p.relative_to(root).as_posix()
        if name in excluded:continue
        files.append({'path':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    manifest={'schema':'axispl.public-product-manifest.v1','candidate':'Vitreos_AxisPL_Evidence_Atlas_20261011_purpose_context','files':files,'self_hash_rule':'This manifest and receipts/SHA256SUMS are excluded from this files array. The checksum ledger covers payload files plus this manifest. Optional distribution sidecars downloads/complete-public-package.zip and downloads/SHA256SUMS are produced afterwards, excluded from the payload and never embedded recursively in the archive. The public verifier checks their checksum and exact payload correspondence when present.','scope':'Byte inventory, not authenticity or scientific certification.'}
    m=root/'PUBLIC_MANIFEST.json';m.write_text(json.dumps(manifest,indent=2)+'\n')
    sums=files+[{'path':'PUBLIC_MANIFEST.json','sha256':hashlib.sha256(m.read_bytes()).hexdigest()}]
    (root/'receipts/SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in sorted(sums,key=lambda r:r['path'])))
    print(json.dumps({'payload_files':len(files),'manifest_sha256':hashlib.sha256(m.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
