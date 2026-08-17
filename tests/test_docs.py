from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'index.html'


class StrictEnoughHTMLParser(HTMLParser):
    pass


def main() -> None:
    assert DOC.is_file(), 'docs/index.html is missing'
    text = DOC.read_text(encoding='utf-8')

    parser = StrictEnoughHTMLParser()
    parser.feed(text)
    parser.close()

    required = [
        'NORMAL SUCCESS PATH',
        'Orchestration Sidecar',
        'FAIL / CORRECTION LOOP',
        'Dynamic Model Routing',
        'Repository配置',
        'Global配置',
    ]
    for marker in required:
        assert marker in text, f'missing visual-guide marker: {marker}'

    forbidden = [
        'phase:nth-child(n+7)',
        'grid-column:6',
        'grid-column:5',
        'grid-column:4',
    ]
    for marker in forbidden:
        assert marker not in text, f'legacy serpentine layout marker remains: {marker}'

    scripts = re.findall(r'<script>(.*?)</script>', text, flags=re.S | re.I)
    assert scripts, 'embedded JavaScript is missing'
    js = '\n'.join(scripts)
    with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as f:
        f.write(js)
        js_path = f.name

    result = subprocess.run(['node', '--check', js_path], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr or result.stdout

    print('docs/index.html validation PASS')


if __name__ == '__main__':
    main()
