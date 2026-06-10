"""
Graph flow v2 — a fresh ~1 minute Manim take on the graph data structure and
why LangGraph uses one. Distinct from graph_flow.py: this version is kinetic —
a glowing pulse physically *traverses* the graph, and branch / merge / loop are
each shown as a tiny live example before they're assembled into an agent.

Beats (use `--save_sections` to render separately):
  0. Title.
  1. Vocabulary, fast: node, edge, directed (A → B, not B → A).
  2. A straight line only goes forward — and falls off the end.
  3. Three superpowers a line doesn't have: branch, merge, loop (live demos).
  4. Assemble them: a LangGraph agent answering one question, end to end.
  5. Payoff: branch = decide, loop = keep trying — that's why agents are graphs.

Render (Manim Community / `manim`):
  manim -qh graph_flow_v2.py GraphFlowV2        # 1080p
  manim -ql graph_flow_v2.py GraphFlowV2        # fast 480p preview

No LaTeX needed (uses Text only). Needs cairo, pango, ffmpeg.
"""

import numpy as np

from manim import *

# ---- palette (shared with the other scenes) -----------------------------
USR   = "#4a9eff"   # blue
AST   = "#9d92f0"   # purple
TOOLC = "#33c499"   # teal
LLM   = "#ff7a4d"   # coral
TOK   = "#f0a637"   # amber — the travelling pulse
INK   = "#ECECEC"   # primary text
MUT   = "#8a8a8a"   # muted text
BG    = "#0e0e12"   # background


# ---- helpers ------------------------------------------------------------
def cnode(label, color, r=0.55, fs=26):
    c = Circle(radius=r, color=color, stroke_width=3.5,
               fill_color=color, fill_opacity=0.18)
    t = Text(label, font_size=fs, color=INK, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.circle = c
    return g


def darrow(a, b, color=MUT, sw=4):
    return Arrow(a.get_center(), b.get_center(), buff=a.circle.radius + 0.06,
                 color=color, stroke_width=sw, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.4)


def caption(s, color=INK, fs=30):
    return Text(s, font_size=fs, color=color).to_edge(DOWN, buff=0.55)


class GraphFlowV2(Scene):
    def construct(self):
        self.camera.background_color = BG

        # convenience: a glowing pulse and the act of sending it down an edge
        def pulse_at(node):
            d = Dot(color=TOK, radius=0.14).move_to(node.get_center())
            d.set_z_index(10)
            return d

        def send(dot, target, edge, rt=0.75):
            self.play(
                dot.animate.move_to(target.get_center()),
                ShowPassingFlash(edge.copy().set_color(TOK).set_stroke(width=7),
                                 time_width=0.6),
                run_time=rt,
            )
            self.play(Indicate(target, color=target.circle.get_color(),
                               scale_factor=1.12), run_time=0.4)

        # =================================================================
        self.next_section("Beat 0 - title")
        # =================================================================
        big = Text("Graphs", font_size=92, color=INK, weight=BOLD)
        sub = Text("the shape of every LangGraph agent",
                   font_size=30, color=MUT).next_to(big, DOWN, buff=0.4)
        self.play(Write(big), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(VGroup(big, sub)), run_time=0.5)

        # =================================================================
        self.next_section("Beat 1 - vocabulary")
        # =================================================================
        a = cnode("A", USR).move_to(LEFT * 2.6)
        b = cnode("B", AST).move_to(RIGHT * 2.6)
        self.play(FadeIn(a, scale=0.6), FadeIn(b, scale=0.6), run_time=0.6)
        nl = Text("nodes", font_size=26, color=MUT).next_to(
            VGroup(a, b), UP, buff=0.9)
        self.play(FadeIn(nl, shift=UP * 0.2), run_time=0.4)

        line = Line(a.get_center(), b.get_center(), color=MUT, stroke_width=4,
                    buff=a.circle.radius + 0.06)
        el = Text("edge", font_size=26, color=MUT).next_to(line, DOWN, buff=0.25)
        self.play(Create(line), FadeIn(el), run_time=0.6)
        self.wait(0.6)

        # the edge gains a direction
        arr = darrow(a, b, color=USR, sw=5)
        self.play(ReplacementTransform(line, arr),
                  FadeOut(el), FadeOut(nl), run_time=0.6)
        dl = caption("directed:  A → B", USR)
        self.play(FadeIn(dl), run_time=0.4)
        # a pulse runs A -> B fine...
        d = pulse_at(a)
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        self.play(d.animate.move_to(b.get_center()),
                  ShowPassingFlash(arr.copy().set_color(TOK).set_stroke(width=7),
                                   time_width=0.6), run_time=0.7)
        # ...but not back the other way
        ghost = darrow(b, a, color=MUT, sw=4).shift(DOWN * 1.0)
        cross = Cross(ghost, stroke_color=LLM, stroke_width=6).scale(0.55)
        nb = Text("not  B → A", font_size=26, color=LLM).next_to(ghost, DOWN, buff=0.15)
        self.play(Create(ghost), run_time=0.35)
        self.play(Create(cross), FadeIn(nb), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(VGroup(a, b, arr, d, dl, ghost, cross, nb)), run_time=0.5)

        # =================================================================
        self.next_section("Beat 2 - a line only goes forward")
        # =================================================================
        th = Text("A line only goes one way", font_size=36, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(th), run_time=0.6)

        p = VGroup(*[cnode(s, MUT, r=0.45, fs=22) for s in ["1", "2", "3", "4"]])
        p.arrange(RIGHT, buff=1.6).move_to(ORIGIN)
        pe = VGroup(*[darrow(p[i], p[i + 1]) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in p],
                              *[GrowArrow(e) for e in pe], lag_ratio=0.16),
                  run_time=1.2)

        # a pulse rolls through and drops off the end
        d = pulse_at(p[0])
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        for i in range(3):
            self.play(d.animate.move_to(p[i + 1].get_center()),
                      ShowPassingFlash(pe[i].copy().set_color(TOK).set_stroke(width=7),
                                       time_width=0.6), run_time=0.55)
        self.play(d.animate.shift(RIGHT * 1.6).set_opacity(0.0), run_time=0.6)
        cl = caption("forward, then it stops.  No choices, no second tries.", MUT)
        self.play(FadeIn(cl), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(VGroup(th, p, pe, cl)), run_time=0.5)

        # =================================================================
        self.next_section("Beat 3 - branch, merge, loop")
        # =================================================================
        th = Text("A graph can do three more things", font_size=36, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(th), run_time=0.6)

        # --- BRANCH ---------------------------------------------------
        x = cnode("", USR, r=0.45).move_to(LEFT * 3.2)
        top = cnode("", AST, r=0.45).move_to(RIGHT * 2.2 + UP * 1.4)
        bot = cnode("", TOOLC, r=0.45).move_to(RIGHT * 2.2 + DOWN * 1.4)
        e_top = darrow(x, top, color=MUT)
        e_bot = darrow(x, bot, color=MUT)
        self.play(FadeIn(x, scale=0.6), FadeIn(top, scale=0.6), FadeIn(bot, scale=0.6),
                  GrowArrow(e_top), GrowArrow(e_bot), run_time=0.7)
        lbl = caption("branch — one node, a choice of paths", USR)
        self.play(FadeIn(lbl), run_time=0.4)
        d = pulse_at(x)
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        # it picks the top path
        self.play(d.animate.move_to(top.get_center()),
                  e_top.animate.set_color(USR).set_stroke(width=6),
                  ShowPassingFlash(e_top.copy().set_color(TOK).set_stroke(width=7),
                                   time_width=0.6), run_time=0.7)
        self.play(Indicate(top, color=AST, scale_factor=1.15), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(VGroup(x, top, bot, e_top, e_bot, d)), run_time=0.4)

        # --- MERGE ----------------------------------------------------
        l1 = cnode("", USR, r=0.45).move_to(LEFT * 3.2 + UP * 1.4)
        l2 = cnode("", AST, r=0.45).move_to(LEFT * 3.2 + DOWN * 1.4)
        m = cnode("", LLM, r=0.45).move_to(RIGHT * 2.2)
        e1 = darrow(l1, m, color=MUT)
        e2 = darrow(l2, m, color=MUT)
        self.play(FadeIn(l1, scale=0.6), FadeIn(l2, scale=0.6), FadeIn(m, scale=0.6),
                  GrowArrow(e1), GrowArrow(e2), run_time=0.7)
        lbl2 = caption("merge — separate paths rejoin", LLM)
        self.play(ReplacementTransform(lbl, lbl2), run_time=0.4)
        d1 = pulse_at(l1)
        d2 = pulse_at(l2)
        self.play(FadeIn(d1, scale=0.5), FadeIn(d2, scale=0.5), run_time=0.25)
        self.play(d1.animate.move_to(m.get_center()),
                  d2.animate.move_to(m.get_center()),
                  ShowPassingFlash(e1.copy().set_color(TOK).set_stroke(width=7), time_width=0.6),
                  ShowPassingFlash(e2.copy().set_color(TOK).set_stroke(width=7), time_width=0.6),
                  run_time=0.7)
        self.play(Indicate(m, color=LLM, scale_factor=1.18), FadeOut(d2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(VGroup(l1, l2, m, e1, e2, d1)), run_time=0.4)

        # --- LOOP -----------------------------------------------------
        pnode = cnode("", AST, r=0.5).move_to(LEFT * 1.9)
        qnode = cnode("", TOOLC, r=0.5).move_to(RIGHT * 1.9)
        e_fwd = darrow(pnode, qnode, color=MUT)
        back = CurvedArrow(qnode.get_top() + UP * 0.05, pnode.get_top() + UP * 0.05,
                           angle=PI / 2.2, color=TOK, stroke_width=4, tip_length=0.22)
        self.play(FadeIn(pnode, scale=0.6), FadeIn(qnode, scale=0.6),
                  GrowArrow(e_fwd), Create(back), run_time=0.8)
        lbl3 = caption("loop — go around again until it's ready", TOK)
        self.play(ReplacementTransform(lbl2, lbl3), run_time=0.4)
        cnt = Text("0", font_size=26, color=TOK).next_to(back, UP, buff=0.1)
        self.play(FadeIn(cnt), run_time=0.3)
        d = pulse_at(pnode)
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        for i in (1, 2):
            self.play(d.animate.move_to(qnode.get_center()),
                      ShowPassingFlash(e_fwd.copy().set_color(TOK).set_stroke(width=7),
                                       time_width=0.6), run_time=0.55)
            new_cnt = Text(str(i), font_size=26, color=TOK).move_to(cnt)
            self.play(MoveAlongPath(d, back.copy().reverse_direction()),
                      Transform(cnt, new_cnt), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(VGroup(pnode, qnode, e_fwd, back, cnt, d, lbl3, th)),
                  run_time=0.5)

        # =================================================================
        self.next_section("Beat 4 - the agent, end to end")
        # =================================================================
        th = Text("So a LangGraph agent looks like this", font_size=34,
                  color=INK).to_edge(UP, buff=0.5)
        self.play(Write(th), run_time=0.7)

        g_start = cnode("START", MUT, r=0.6, fs=18).move_to(LEFT * 5.0 + UP * 0.4)
        g_agent = cnode("Agent", LLM, r=0.78, fs=22).move_to(LEFT * 1.2 + UP * 0.4)
        g_tool = cnode("Tool", TOOLC, r=0.66, fs=20).move_to(RIGHT * 3.0 + UP * 1.9)
        g_end = cnode("END", USR, r=0.6, fs=20).move_to(RIGHT * 3.0 + DOWN * 1.7)

        e_sa = darrow(g_start, g_agent, color=MUT)
        e_at = darrow(g_agent, g_tool, color=TOK)
        e_ae = darrow(g_agent, g_end, color=USR)
        loop_back = CurvedArrow(
            g_tool.get_left() + LEFT * 0.04, g_agent.get_top() + RIGHT * 0.15,
            angle=PI / 2.4, color=TOOLC, stroke_width=4, tip_length=0.22)

        l_at = Text("need info", font_size=20, color=TOK).next_to(e_at, DOWN, buff=0.12).shift(RIGHT*0.1)
        l_back = Text("result back", font_size=18, color=TOOLC).next_to(loop_back, UP, buff=0.06)
        l_ae = Text("done", font_size=20, color=USR).next_to(e_ae, RIGHT, buff=0.15)

        self.play(FadeIn(g_start, scale=0.6), FadeIn(g_agent, scale=0.6),
                  GrowArrow(e_sa), run_time=0.6)
        self.play(FadeIn(g_tool, scale=0.6), FadeIn(g_end, scale=0.6),
                  GrowArrow(e_at), GrowArrow(e_ae), Create(loop_back), run_time=0.8)
        self.play(FadeIn(l_at), FadeIn(l_back), FadeIn(l_ae), run_time=0.5)

        q = Text('"is it raining in Paris?"', font_size=22, color=USR).next_to(
            g_start, DOWN, buff=0.5).shift(RIGHT * 0.3)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.5)
        self.wait(0.9)

        # run it end to end: start -> agent -(branch: need info)-> tool -(loop)-> agent -> end
        d = pulse_at(g_start)
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        send(d, g_agent, e_sa, rt=0.7)
        cap = caption("the agent decides: it needs a tool…", LLM, fs=26)
        self.play(FadeIn(cap), run_time=0.4)
        send(d, g_tool, e_at, rt=0.7)              # branch -> tool
        # loop the result back to the agent
        self.play(MoveAlongPath(d, loop_back), run_time=0.8)
        self.play(Indicate(g_agent, color=LLM, scale_factor=1.12), run_time=0.4)
        cap2 = caption("…gets the result, loops back, now it can answer", TOOLC, fs=26)
        self.play(ReplacementTransform(cap, cap2), run_time=0.4)
        send(d, g_end, e_ae, rt=0.7)               # branch -> done
        self.play(d.animate.set_opacity(0.0), run_time=0.3)
        self.wait(2.0)

        # =================================================================
        self.next_section("Beat 5 - payoff")
        # =================================================================
        self.play(FadeOut(VGroup(th, g_start, g_agent, g_tool, g_end, e_sa, e_at,
                                 e_ae, loop_back, l_at, l_back, l_ae, q, cap2)),
                  run_time=0.6)
        k1 = Text("Branch to decide.   Loop to keep trying.",
                  font_size=38, color=INK, weight=BOLD)
        k2 = Text("That's why an agent is a graph — not a line.",
                  font_size=32, color=TOK)
        ks = VGroup(k1, k2).arrange(DOWN, buff=0.45)
        self.play(Write(k1), run_time=1.0)
        self.play(FadeIn(k2, shift=UP * 0.2), run_time=0.7)
        self.wait(3.0)
