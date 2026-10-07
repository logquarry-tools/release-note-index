"""Index release notes by version without duplicate headings."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

def analyze(data):
    versions=[row['version'] for row in data['releases']]
    return {'versions':sorted(set(versions)),'note_counts':{row['version']:len(row.get('notes',[])) for row in data['releases']},'duplicate_versions':sorted(key for key,n in Counter(versions).items() if n>1)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
