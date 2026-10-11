#!/usr/bin/env python3
"""Check package-local copies of shared readers without coupling leaf Skills."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('xlsx_reader.py', 'api_case_contract.py', 'evidence_scaffold.py', 'parse_api_sources.py', 'check_bruno_report.py')


def main():
    mismatches = []
    count = 0
    for name in NAMES:
        canonical = (ROOT/'scripts/skill_resources'/name).read_bytes()
        copies = list((ROOT/'skills').rglob('scripts/'+name))
        if not copies:
            mismatches.append('missing copies: '+name)
        for path in copies:
            count += 1
            if path.read_bytes() != canonical:
                mismatches.append(str(path.relative_to(ROOT)))
    if mismatches:
        print('Resource copies differ:\n'+'\n'.join(mismatches), file=sys.stderr)
        return 1
    print(f'Standalone resource copies: {count} identical to canonical sources')
    return 0


if __name__ == '__main__':
    sys.exit(main())
