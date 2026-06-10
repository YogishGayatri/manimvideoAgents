# manimvideoAgents

Manim Community animations explaining how AI agents work.

## Scenes

- **`agent_flow.py` — `AgentFlow`**: how an AI agent works (LLM + tools, the
  chat UI, a web_search call, and messages vs. the raw token stream).
- **`graph_flow.py` — `GraphFlow`**: a ~1 minute, light-on-words intro to the
  graph data structure (nodes, edges, direction, branch/merge/loop) that lands
  on *why* LangGraph models an agent as a graph.
- **`graph_flow_v2.py` — `GraphFlowV2`**: a kinetic alternative to `GraphFlow`
  — a glowing pulse physically traverses the graph; branch / merge / loop are
  shown as tiny live demos, then assembled into an agent answering one
  question end to end.
- **`mcp_flow.py` — `MCPFlow`**: a ~1 minute, visual-first explainer of the
  Model Context Protocol — the N×M → N+M integration problem and the
  Host / Client / Server roles (a "USB-C port for AI").
- **`state_flow.py` — `StateFlow`**: a ~1 minute explainer of LangGraph
  *state* — a card of named fields travels START → END; each node reads it
  and writes into it (two nodes via an LLM call), and the final state is
  the answer.

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

manim -ql graph_flow.py GraphFlow   # fast 480p preview
manim -qh graph_flow.py GraphFlow   # 1080p

manim -ql graph_flow_v2.py GraphFlowV2   # fast 480p preview
manim -qh graph_flow_v2.py GraphFlowV2   # 1080p

manim -ql mcp_flow.py MCPFlow       # fast 480p preview
manim -qh mcp_flow.py MCPFlow       # 1080p

manim -ql state_flow.py StateFlow   # fast 480p preview
manim -qh state_flow.py StateFlow   # 1080p
```

Add `--save_sections` to render each beat/act separately. Output lands in
`media/videos/<file>/`.
