from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'index.html'


class MotionGuideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip_depth = 0
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {'script', 'style'}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {'script', 'style'} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and data.strip():
            self.text.append(data.strip())


def main() -> None:
    assert DOC.is_file(), 'docs/index.html is missing'
    text = DOC.read_text(encoding='utf-8')

    parser = MotionGuideParser()
    parser.feed(text)
    parser.close()
    visible = ' '.join(parser.text)

    required = [
        '全体像',
        '02 / 基本フロー',
        '03 / Subagent委譲',
        '04 / 失敗時の診断・修正',
        '復帰先は変更内容で決まる',
        '候補成果物を変更した',
        'テスト計画だけを変更した',
        '追加証拠だけで再判定できる',
        '外部操作の計画・対象・権限が変わった',
        '06 / 動的モデル選択',
        '成果鍵',
        '独立反証鍵',
    ]
    for marker in required:
        assert marker in visible, f'missing visual-guide marker: {marker}'

    # User-facing Japanese should not regress to the previous literal or mixed wording.
    language_forbidden = [
        '主幹',
        'phaseから',
        'phase内',
        'candidate固定',
        'material risk',
        'freshnessだけ',
        'job requirements',
        'minimum sufficient model',
        '#workflowモデル選択s',
        'モデル選択 Selection',
    ]
    for marker in language_forbidden:
        assert marker not in visible, f'awkward/mixed user-facing wording remains: {marker}'

    # The visual guide explains workflow motion only. Installation/deployment belongs in README.
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
        assert marker not in visible, f'placement/install content leaked into motion guide: {marker}'

    # Prevent the old three-lane/Z layout and meaningless sweep decoration from returning.
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

    assert text.index('id="overview"') < text.index('id="bootstrap"'), 'overview must precede detailed flows'

    scripts = re.findall(r'<script>(.*?)</script>', text, flags=re.S | re.I)
    assert scripts, 'embedded JavaScript is missing'
    js = '\n'.join(scripts)
    with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as f:
        f.write(js)
        js_path = f.name

    result = subprocess.run(['node', '--check', js_path], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr or result.stdout

    print('docs/index.html language/motion validation PASS')


if __name__ == '__main__':
    main()
