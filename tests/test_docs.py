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
        '02 / Main Trunk',
        '03 / Orchestration',
        '04 / Failure & Correction',
        '委譲は「主幹のphaseから呼び、結果を同じphaseへ返す」',
        'FAIL時だけ主幹から一時離脱する',
        'Dynamic Model Routing',
        '成果鍵',
        '独立反証鍵',
    ]
    for marker in required:
        assert marker in text, f'missing visual-guide marker: {marker}'

    # The visual guide explains runtime motion only. Installation, deployment,
    # repository/global placement, CI packaging, and artifact acquisition belong
    # in README and must not drift back into docs/index.html.
    placement_forbidden = [
        'Repository配置',
        'Global配置',
        'Installation',
        'Actions Artifact',
        'workflow ZIP',
        '~/.copilot/',
        '<repo>/.github/',
    ]
    for marker in placement_forbidden:
        assert marker not in text, f'placement/install content leaked into motion guide: {marker}'

    # Prevent the previous visually ambiguous three-lane/Z-style main-flow layout
    # and decorative sweep animations from returning.
    layout_forbidden = [
        'flow-layout',
        'Orchestration Sidecar',
        'NORMAL SUCCESS PATH',
        'FAIL / CORRECTION LOOP',
        'phase:nth-child(n+7)',
        'grid-column:6',
        'grid-column:5',
        'grid-column:4',
        'animation:sweep',
    ]
    for marker in layout_forbidden:
        assert marker not in text, f'legacy/ambiguous visual marker remains: {marker}'

    scripts = re.findall(r'<script>(.*?)</script>', text, flags=re.S | re.I)
    assert scripts, 'embedded JavaScript is missing'
    js = '\n'.join(scripts)
    with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as f:
        f.write(js)
        js_path = f.name

    result = subprocess.run(['node', '--check', js_path], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr or result.stdout

    print('docs/index.html motion-guide validation PASS')


if __name__ == '__main__':
    main()
