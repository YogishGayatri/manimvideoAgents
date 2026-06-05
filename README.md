# manimvideoAgents

Manim Community animations explaining how AI agents work.

## Setup

System dependencies (Ubuntu/Debian):

```bash
sudo apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev
```

Python environment (a virtualenv is recommended — the system setuptools can
fail to build some transitive deps):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Render

```bash
. .venv/bin/activate
manim -ql agent_flow.py AgentFlow   # fast 480p preview
manim -qh agent_flow.py AgentFlow   # 1080p
```

Add `--save_sections` to render each of the four acts separately. Output lands
in `media/videos/agent_flow/`.
