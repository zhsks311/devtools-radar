#!/usr/bin/env python3
"""Run the entire validated merge/build/test pipeline without modifying repository data."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]

def run(*args):
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True)

def main():
    run('tools/lint_content.py')
    run('tools/lint_content.py','--data',ROOT/'data/tools.json')
    run('-m','unittest','discover','-s','tests','-v')
    with tempfile.TemporaryDirectory(prefix='radar-check-') as directory:
        base=Path(directory)
        shutil.copytree(ROOT/'content/final',base/'content/final')
        shutil.copytree(ROOT/'data',base/'data')
        # Run merge against a disposable copy, then validate exactly what will render.
        sys.path.insert(0,str(ROOT))
        from content.merge import merge_articles
        merge_articles(base)
        run('tools/lint_content.py','--data',base/'data/tools.json')
        run('build.py','--data',base/'data/tools.json','--output',base/'site',
            '--deals',base/'data/deals.json','--deals-en',base/'data/deals_en.json')
        run('tools/check_site.py','--output',base/'site','--data',base/'data/tools.json')
    print('All checks passed; repository data and dist were not modified.')

if __name__=='__main__':
    try:main()
    except subprocess.CalledProcessError as exc:sys.exit(exc.returncode)
