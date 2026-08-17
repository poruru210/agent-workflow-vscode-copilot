from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOC_NAME = 'agent-workflow-vscode-copilot-visual-guide-controls-state.html'
DOC = ROOT / 'docs' / DOC_NAME
LEGACY_INDEX = ROOT / 'docs' / 'index.html'


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
    assert DOC.is_file(), f'docs/{DOC_NAME} is missing'
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
        '05 / 作業種別ごとの準備',
        '06 / 動的モデル選択',
        '07 / 証拠の整理',
        'なぜ分岐する？',
        '何をする？',
        'どこへ戻る？',
        '未証明だけの場合',
        '成果鍵 + 独立反証鍵',
    ]
    for marker in required:
        assert marker in visible, f'missing visual-guide marker: {marker}'

    # 02 / 03 / 04 use the same left-basic-flow / right-detail grammar.
    assert text.count('class="flow-diagram"') == 1, 'basic-flow detail diagram must appear once'
    assert text.count('class="branch-diagram"') == 2, 'delegation and failure diagrams must share branch layout'
    assert text.count('class="basic"') >= 3, '02 / 03 / 04 must each show the basic flow on the left'

    # Border colors indicate state only, not phase kind.
    for forbidden in ['.phase.audit{border-color:', '.phase.test{border-color:', '.phase.gate{border-color:']:
        assert forbidden not in text, f'phase-kind border color returned: {forbidden}'

    # Controls are consistent across the three animations.
    for label in ['▶ 再生', 'Ⅱ 停止', '↺ リセット']:
        assert visible.count(label) == 3, f'control label is not consistent: {label}'
    for state in ['再生中', '停止中', 'リセット']:
        assert state in text, f'control state missing: {state}'
    assert 'is-running' in text and 'is-stopped' in text and 'is-reset' in text

    # Playback is intentionally half-speed relative to the previous guide.
    assert 'const STEP_MS=1900' in text, 'main playback is not at 0.5x speed'
    assert 'FLASH_MS=1400' in text, 'branch animation duration is not slowed'

    # Navigation must not contain an animation trigger.
    nav_match = re.search(r'<nav class="nav">(.*?)</nav>', text, flags=re.S | re.I)
    assert nav_match, 'navigation is missing'
    nav = nav_match.group(1)
    assert '再生' not in nav and '<button' not in nav, 'navigation must not contain playback controls'

    # Guide content only; installation and deployment belong in README.
    placement_forbidden = [
        'Repository配置', 'Global配置', 'Installation', 'Actions Artifact',
        'workflow ZIP', '~/.copilot/', '<repo>/.github/'
    ]
    for marker in placement_forbidden:
        assert marker not in visible, f'placement/install content leaked into guide: {marker}'

    # Legacy index is only a compatibility redirect, not the canonical guide.
    assert LEGACY_INDEX.is_file(), 'legacy docs/index.html compatibility redirect is missing'
    legacy = LEGACY_INDEX.read_text(encoding='utf-8')
    assert DOC_NAME in legacy, 'legacy docs/index.html does not point to named guide'
    assert len(legacy) < 2000, 'legacy docs/index.html must remain a small redirect'

    scripts = re.findall(r'<script>(.*?)</script>', text, flags=re.S | re.I)
    assert scripts, 'embedded JavaScript is missing'
    with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as f:
        f.write('\n'.join(scripts))
        js_path = f.name

    result = subprocess.run(['node', '--check', js_path], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr or result.stdout

    print(f'docs/{DOC_NAME} validation PASS')


if __name__ == '__main__':
    main()
