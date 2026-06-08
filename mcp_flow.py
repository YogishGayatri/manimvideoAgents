"""
MCP flow — a ~1 minute Manim Community animation explaining the Model Context
Protocol (MCP) for a slide. Visual-first, light on text.

Beats (use `--save_sections` to render separately):
  0. Title: MCP — an open standard by Anthropic (2024), "a USB-C port for AI".
  1. The problem: N apps × M tools  ->  a tangle of custom integrations.
  2. The fix: drop MCP in the middle  ->  N + M.  One standard port.
  3. The 3 roles: Host (the app), Client (the hidden manager), Server (on the
     tool). A request flows out and data flows back.
  4. Payoff: one protocol, plug in anything.

Render (Manim Community / `manim`):
  manim -qh mcp_flow.py MCPFlow        # 1080p
  manim -ql mcp_flow.py MCPFlow        # fast 480p preview

No LaTeX needed (uses Text only). Needs cairo, pango, ffmpeg.
"""

from manim import *

# ---- palette (shared with the other scenes) -----------------------------
HOST   = "#4a9eff"   # blue   — host / apps
CLIENT = "#9d92f0"   # purple — client
SERVER = "#33c499"   # teal   — server / tools
MCPC   = "#ff7a4d"   # coral  — MCP itself
TOK    = "#f0a637"   # amber  — requests / accents
INK    = "#ECECEC"   # primary text
MUT    = "#8a8a8a"   # muted text
RED    = "#ff6b6b"   # the "messy" number
BG     = "#0e0e12"   # background


# ---- helpers ------------------------------------------------------------
def chip(label, color, w=2.3, h=0.9, fs=24, sub=None):
    """A rounded, soft-filled labelled box."""
    rect = RoundedRectangle(corner_radius=0.14, width=w, height=h, color=color,
                            stroke_width=2.6, fill_color=color, fill_opacity=0.14)
    if sub:
        txt = VGroup(
            Text(label, font_size=fs, color=INK, weight=BOLD),
            Text(sub, font_size=fs - 8, color=MUT),
        ).arrange(DOWN, buff=0.06)
    else:
        txt = Text(label, font_size=fs, color=INK, weight=BOLD)
    if txt.width > w - 0.3:
        txt.scale_to_fit_width(w - 0.3)
    txt.move_to(rect)
    g = VGroup(rect, txt)
    g.rect = rect
    return g


def link(a_pt, b_pt, color=MUT, sw=2.4, op=0.6):
    return Line(a_pt, b_pt, color=color, stroke_width=sw).set_opacity(op)


def caption(s, color=INK, fs=30):
    return Text(s, font_size=fs, color=color).to_edge(DOWN, buff=0.5)


class MCPFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =================================================================
        self.next_section("Beat 0 - title")
        # =================================================================
        big = Text("MCP", font_size=92, color=INK, weight=BOLD)
        full = Text("Model Context Protocol", font_size=34, color=MCPC).next_to(
            big, DOWN, buff=0.35)
        sub = Text("an open standard by Anthropic (2024)",
                   font_size=24, color=MUT).next_to(full, DOWN, buff=0.5)
        tag = Text("a USB-C port for AI", font_size=26, color=TOK).next_to(
            sub, DOWN, buff=0.25)
        self.play(Write(big), run_time=0.9)
        self.play(FadeIn(full, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(tag, shift=UP * 0.2), run_time=0.6)
        self.wait(2.8)
        self.play(FadeOut(VGroup(big, full, sub, tag)), run_time=0.6)

        # =================================================================
        self.next_section("Beat 1 - the N x M problem")
        # =================================================================
        head = Text("Connecting AI to tools — the old way",
                    font_size=34, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.7)

        apps = VGroup(
            chip("Chatbot", HOST), chip("IDE", HOST), chip("Agent", HOST),
        ).arrange(DOWN, buff=0.75).move_to(LEFT * 4.9)
        tools = VGroup(
            chip("Database", SERVER), chip("GitHub", SERVER), chip("Files", SERVER),
        ).arrange(DOWN, buff=0.75).move_to(RIGHT * 4.9)

        side_a = Text("AI apps", font_size=22, color=HOST).next_to(apps, UP, buff=0.3)
        side_t = Text("tools & data", font_size=22, color=SERVER).next_to(tools, UP, buff=0.3)

        self.play(LaggedStartMap(FadeIn, apps, lag_ratio=0.2),
                  FadeIn(side_a), run_time=0.7)
        self.play(LaggedStartMap(FadeIn, tools, lag_ratio=0.2),
                  FadeIn(side_t), run_time=0.7)

        # every app wired to every tool -> a tangle
        mesh = VGroup()
        for a in apps:
            for t in tools:
                mesh.add(link(a.rect.get_right(), t.rect.get_left(), MUT, 2.2, 0.5))
        self.play(LaggedStartMap(Create, mesh, lag_ratio=0.06), run_time=2.0)

        cnt = VGroup(
            Text("3 apps", font_size=30, color=HOST, weight=BOLD),
            Text("×", font_size=30, color=RED, weight=BOLD),
            Text("3 tools", font_size=30, color=SERVER, weight=BOLD),
            Text("=", font_size=30, color=MUT),
            Text("9 custom builds", font_size=30, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cnt), run_time=0.5)
        self.play(Indicate(mesh, color=RED, scale_factor=1.0), run_time=0.8)
        self.wait(1.8)

        # the terminology: in general this is N × M — it explodes
        nm = VGroup(
            Text("N", font_size=34, color=HOST, weight=BOLD),
            Text("apps", font_size=30, color=MUT),
            Text("×", font_size=34, color=RED, weight=BOLD),
            Text("M", font_size=34, color=SERVER, weight=BOLD),
            Text("tools", font_size=30, color=MUT),
            Text("=", font_size=30, color=MUT),
            Text("N × M  builds", font_size=32, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(cnt, nm), run_time=0.7)
        self.wait(2.4)

        # =================================================================
        self.next_section("Beat 2 - N + M with MCP")
        # =================================================================
        new_head = Text("…the MCP way", font_size=34, color=INK).to_edge(UP, buff=0.5)
        self.play(FadeOut(mesh), FadeOut(nm),
                  ReplacementTransform(head, new_head), run_time=0.6)

        mcp = chip("MCP", MCPC, w=2.7, h=1.15, fs=32).move_to(ORIGIN)
        self.play(GrowFromCenter(mcp), run_time=0.6)

        spokes = VGroup()
        for a in apps:
            spokes.add(link(a.rect.get_right(), mcp.rect.get_left(), MCPC, 3.0, 0.85))
        for t in tools:
            spokes.add(link(mcp.rect.get_right(), t.rect.get_left(), MCPC, 3.0, 0.85))
        self.play(LaggedStartMap(Create, spokes, lag_ratio=0.12), run_time=1.6)

        cnt2 = VGroup(
            Text("3 apps", font_size=30, color=HOST, weight=BOLD),
            Text("+", font_size=30, color=SERVER, weight=BOLD),
            Text("3 tools", font_size=30, color=SERVER, weight=BOLD),
            Text("=", font_size=30, color=MUT),
            Text("6 — build it once", font_size=30, color=SERVER, weight=BOLD),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cnt2), run_time=0.5)
        self.play(Indicate(mcp, color=MCPC, scale_factor=1.12), run_time=0.8)
        self.wait(1.4)

        # the terminology: each side speaks MCP once -> N + M
        nm2 = VGroup(
            Text("N", font_size=34, color=HOST, weight=BOLD),
            Text("apps", font_size=30, color=MUT),
            Text("+", font_size=34, color=SERVER, weight=BOLD),
            Text("M", font_size=34, color=SERVER, weight=BOLD),
            Text("tools", font_size=30, color=MUT),
            Text("=", font_size=30, color=MUT),
            Text("N + M  builds", font_size=32, color=SERVER, weight=BOLD),
        ).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(cnt2, nm2), run_time=0.7)
        self.wait(2.6)

        # =================================================================
        self.next_section("Beat 3 - host / client / server")
        # =================================================================
        self.play(
            FadeOut(VGroup(apps, tools, side_a, side_t, spokes, mcp, nm2)),
            FadeOut(new_head), run_time=0.6,
        )
        h3 = Text("Three parts", font_size=36, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(h3), run_time=0.6)

        # Host is a region that contains the Client
        host_box = RoundedRectangle(corner_radius=0.2, width=4.3, height=3.4,
                                    color=HOST, stroke_width=2.6,
                                    fill_color=HOST, fill_opacity=0.06)
        host_box.move_to(LEFT * 3.5 + DOWN * 0.2)
        host_lbl = VGroup(
            Text("Host", font_size=28, color=HOST, weight=BOLD),
            Text("the app you use", font_size=18, color=MUT),
        ).arrange(DOWN, buff=0.06)
        host_lbl.next_to(host_box.get_top(), DOWN, buff=0.22)

        client = chip("Client", CLIENT, w=2.5, h=1.0, fs=24, sub="the manager")
        client.move_to(host_box.get_center() + DOWN * 0.35)

        server = chip("Server", SERVER, w=2.6, h=1.1, fs=24, sub="on the tool")
        server.move_to(RIGHT * 2.3 + DOWN * 0.2)

        data = chip("Data", TOK, w=1.7, h=1.0, fs=22, sub="API · DB")
        data.move_to(RIGHT * 5.3 + DOWN * 0.2)

        self.play(Create(host_box), FadeIn(host_lbl), run_time=0.6)
        self.play(GrowFromCenter(client), run_time=0.5)
        self.play(GrowFromCenter(server), GrowFromCenter(data), run_time=0.6)

        # request out, response back  (two clearly separated arrows)
        cy = client.get_center()[1]
        cxr = client.rect.get_right()[0]
        sxl = server.rect.get_left()[0]
        req = Arrow([cxr, cy + 0.28, 0], [sxl, cy + 0.28, 0], color=TOK,
                    stroke_width=4, tip_length=0.22, buff=0.1)
        resp = Arrow([sxl, cy - 0.32, 0], [cxr, cy - 0.32, 0], color=SERVER,
                     stroke_width=4, tip_length=0.22, buff=0.1)
        mid_x = (cxr + sxl) / 2
        req_l = Text("request", font_size=20, color=TOK).move_to([mid_x, cy + 0.66, 0])
        resp_l = Text("data back", font_size=20, color=SERVER).move_to([mid_x, cy - 0.7, 0])

        fetch = DoubleArrow(server.rect.get_right(), data.rect.get_left(),
                            color=MUT, stroke_width=3.5, tip_length=0.18, buff=0.12)
        fetch_l = Text("fetch", font_size=18, color=MUT).next_to(fetch, UP, buff=0.12)

        self.play(Create(req), FadeIn(req_l), run_time=0.5)
        self.play(Create(fetch), FadeIn(fetch_l), run_time=0.4)
        self.play(Create(resp), FadeIn(resp_l), run_time=0.5)

        # walk through the roles with a moving pulse + a one-line caption
        note = caption("Host — the app you talk to", HOST)
        self.play(FadeIn(note), Indicate(VGroup(host_box, host_lbl), color=HOST,
                                         scale_factor=1.03), run_time=0.9)
        self.wait(1.6)
        note2 = caption("Client — the hidden manager inside", CLIENT)
        self.play(ReplacementTransform(note, note2),
                  Indicate(client, color=CLIENT, scale_factor=1.1), run_time=0.9)
        self.wait(1.6)
        note3 = caption("Server — sits on the tool, fetches the data", SERVER)
        self.play(ReplacementTransform(note2, note3),
                  Indicate(server, color=SERVER, scale_factor=1.1), run_time=0.9)
        self.wait(1.5)

        # pull it together end-to-end, then run the round trip a couple of times
        flow = caption("you ask  →  Client routes  →  Server fetches  →  data returns",
                       INK, fs=24)
        self.play(ReplacementTransform(note3, flow), run_time=0.7)
        self.wait(0.8)
        for _ in range(2):
            dot = Dot(color=TOK, radius=0.1).move_to([cxr, cy + 0.28, 0])
            self.play(FadeIn(dot), run_time=0.2)
            self.play(dot.animate.move_to([sxl, cy + 0.28, 0]), run_time=0.6)
            self.play(Indicate(server, color=SERVER),
                      Indicate(fetch, color=TOK), run_time=0.45)
            self.play(dot.animate.set_color(SERVER).move_to([cxr, cy - 0.32, 0]),
                      run_time=0.6)
            self.play(Indicate(client, color=CLIENT), FadeOut(dot), run_time=0.4)
        self.wait(1.4)

        # =================================================================
        self.next_section("Beat 4 - payoff")
        # =================================================================
        roles = VGroup(h3, host_box, host_lbl, client, server, data,
                       req, resp, req_l, resp_l, fetch, fetch_l, flow)
        self.play(FadeOut(roles), run_time=0.6)

        payoff = VGroup(
            Text("One protocol.", font_size=52, color=INK, weight=BOLD),
            Text("Plug in anything.", font_size=52, color=MCPC, weight=BOLD),
        ).arrange(DOWN, buff=0.25)
        self.play(Write(payoff), run_time=1.1)
        foot = Text("universal compatibility · standardized agent interactions",
                    font_size=24, color=MUT).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(foot, shift=UP * 0.2), run_time=0.6)
        self.wait(3.2)
