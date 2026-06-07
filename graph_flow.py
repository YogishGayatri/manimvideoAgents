"""
Graph flow — a ~1 minute Manim Community animation that builds up the graph
data structure from scratch and lands on *why* LangGraph is a graph.

Five short beats (use `--save_sections` to render them separately):
  1. Nodes + edges: the two pieces a graph is made of.
  2. Direction: an edge can point one way (A -> B, not B -> A).
  3. A straight pipeline goes one way and stops.
  4. A graph can branch, merge, and loop back.
  5. LangGraph: your agent *is* a graph — branch to pick a tool, loop until done.

Render (Manim Community / `manim`):
  manim -qh graph_flow.py GraphFlow        # 1080p
  manim -ql graph_flow.py GraphFlow        # fast 480p preview

No LaTeX needed (uses Text only). Needs cairo, pango, ffmpeg.
"""

from manim import *

# ---- palette (shared with agent_flow.py) --------------------------------
USR   = "#4a9eff"   # blue
AST   = "#9d92f0"   # purple
TOOLC = "#33c499"   # teal
LLM   = "#ff7a4d"   # coral
TOK   = "#f0a637"   # amber
INK   = "#ECECEC"   # primary text
MUT   = "#8a8a8a"   # muted text
BG    = "#0e0e12"   # background


# ---- helpers ------------------------------------------------------------
def node(label, color=USR, r=0.55, fs=28):
    """A graph node: a soft-filled circle with a centered label."""
    c = Circle(radius=r, color=color, stroke_width=3,
               fill_color=color, fill_opacity=0.18)
    t = Text(label, font_size=fs, color=INK, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.circle = c
    return g


def directed(n1, n2, color=MUT, sw=4):
    """A straight arrow from the rim of n1 to the rim of n2."""
    r = n1.circle.radius
    return Arrow(n1.get_center(), n2.get_center(), buff=r + 0.05,
                 color=color, stroke_width=sw, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.35)


def caption(s, color=INK, fs=30):
    return Text(s, font_size=fs, color=color).to_edge(DOWN, buff=0.55)


class GraphFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =================================================================
        self.next_section("Beat 0 - title card")
        # =================================================================
        big = Text("Graphs", font_size=88, color=INK, weight=BOLD)
        sub = Text("…and why LangGraph is built on them",
                   font_size=30, color=MUT).next_to(big, DOWN, buff=0.4)
        # a tiny three-node graph as a flourish under the title
        d1 = Dot(LEFT * 1.2, color=USR, radius=0.1)
        d2 = Dot(RIGHT * 1.2 + UP * 0.1, color=AST, radius=0.1)
        d3 = Dot(DOWN * 1.0, color=TOOLC, radius=0.1)
        flourish = VGroup(
            Line(d1.get_center(), d2.get_center(), color=MUT, stroke_width=2),
            Line(d1.get_center(), d3.get_center(), color=MUT, stroke_width=2),
            Line(d2.get_center(), d3.get_center(), color=MUT, stroke_width=2),
            d1, d2, d3,
        ).scale(0.9).next_to(sub, DOWN, buff=0.7)
        self.play(Write(big), run_time=1.0)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.play(LaggedStartMap(GrowFromCenter, VGroup(d1, d2, d3), lag_ratio=0.3),
                  Create(flourish[:3]), run_time=1.0)
        self.wait(1.4)
        self.play(FadeOut(VGroup(big, sub, flourish)), run_time=0.6)

        # =================================================================
        self.next_section("Beat 1 - nodes + edges")
        # =================================================================
        title = Text("What is a graph?", font_size=44, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        a = node("A", USR).move_to(LEFT * 3.2 + UP * 0.3)
        b = node("B", AST).move_to(RIGHT * 3.2 + UP * 0.3)
        c = node("C", TOOLC).move_to(DOWN * 2.3)

        # nodes
        self.play(GrowFromCenter(a), GrowFromCenter(b), run_time=0.7)
        nlabel = Text("nodes", font_size=26, color=MUT).next_to(a, UP, buff=0.3)
        self.play(FadeIn(nlabel, shift=UP * 0.2), run_time=0.5)

        # an edge between them
        e_ab = Line(a.get_center(), b.get_center(), color=MUT, stroke_width=4,
                    buff=a.circle.radius + 0.05)
        elabel = Text("edge", font_size=26, color=MUT).next_to(e_ab, UP, buff=0.18)
        self.play(Create(e_ab), FadeIn(elabel, shift=UP * 0.2), run_time=0.7)

        # grow into a little graph
        self.play(GrowFromCenter(c), run_time=0.5)
        e_ac = Line(a.get_center(), c.get_center(), color=MUT, stroke_width=4,
                    buff=a.circle.radius + 0.05)
        e_bc = Line(b.get_center(), c.get_center(), color=MUT, stroke_width=4,
                    buff=a.circle.radius + 0.05)
        self.play(Create(e_ac), Create(e_bc), run_time=0.7)

        cap = caption("Dots connected by lines.", INK)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.6)

        # =================================================================
        self.next_section("Beat 2 - direction")
        # =================================================================
        self.play(
            FadeOut(VGroup(c, e_ac, e_bc, nlabel, elabel, cap)),
            run_time=0.5,
        )
        self.play(
            a.animate.move_to(LEFT * 2.6),
            b.animate.move_to(RIGHT * 2.6),
            run_time=0.5,
        )

        # replace the plain line with a one-way arrow
        arr_ab = directed(a, b, color=USR, sw=5)
        self.play(ReplacementTransform(e_ab, arr_ab), run_time=0.7)
        cap = caption("Edges can point one way:  A → B", USR)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(0.4)

        # ...not the other way
        ghost = directed(b, a, color=MUT, sw=4).shift(DOWN * 0.55)
        cross = Cross(ghost, stroke_color=LLM, stroke_width=5).scale(0.5)
        nope = Text("not B → A", font_size=26, color=LLM).next_to(ghost, DOWN, buff=0.15)
        self.play(Create(ghost), run_time=0.4)
        self.play(Create(cross), FadeIn(nope), run_time=0.5)
        self.wait(1.8)

        # =================================================================
        self.next_section("Beat 3 - a straight pipeline")
        # =================================================================
        self.play(
            FadeOut(VGroup(a, b, arr_ab, ghost, cross, nope, cap, title)),
            run_time=0.5,
        )
        title2 = Text("Why a graph?", font_size=44, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title2), run_time=0.6)

        # a straight pipeline: 1 -> 2 -> 3
        p1 = node("1", MUT).move_to(LEFT * 4.2)
        p2 = node("2", MUT).move_to(LEFT * 0.0)
        p3 = node("3", MUT).move_to(RIGHT * 4.2)
        pa = directed(p1, p2, color=MUT)
        pb = directed(p2, p3, color=MUT)
        pipe = VGroup(p1, pa, p2, pb, p3)
        self.play(LaggedStart(
            GrowFromCenter(p1), Create(pa), GrowFromCenter(p2),
            Create(pb), GrowFromCenter(p3), lag_ratio=0.4, run_time=1.6,
        ))
        cap = caption("A pipeline runs one way, then stops.", MUT)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.8)

        # =================================================================
        self.next_section("Beat 4 - branch, merge, loop")
        # =================================================================
        self.play(FadeOut(cap), pipe.animate.scale(0.7).to_edge(UP, buff=1.4),
                  run_time=0.6)

        # rebuild a richer graph: a branches to b & c, they merge to d,
        # and d loops back to a.
        g_a = node("A", USR).move_to(LEFT * 4.0 + DOWN * 0.4)
        g_b = node("B", AST).move_to(LEFT * 0.5 + UP * 1.4)
        g_c = node("C", TOOLC).move_to(LEFT * 0.5 + DOWN * 2.2)
        g_d = node("D", LLM).move_to(RIGHT * 3.6 + DOWN * 0.4)

        self.play(GrowFromCenter(g_a), GrowFromCenter(g_b),
                  GrowFromCenter(g_c), GrowFromCenter(g_d), run_time=0.6)

        # branch: A -> B and A -> C
        br1 = directed(g_a, g_b, color=USR)
        br2 = directed(g_a, g_c, color=USR)
        self.play(Create(br1), Create(br2), run_time=0.6)
        tag_branch = Text("branch", font_size=26, color=USR).next_to(g_a, UP, buff=0.25)
        self.play(FadeIn(tag_branch, shift=UP * 0.2), run_time=0.4)
        self.wait(0.6)

        # merge: B -> D and C -> D
        mg1 = directed(g_b, g_d, color=AST)
        mg2 = directed(g_c, g_d, color=TOOLC)
        self.play(Create(mg1), Create(mg2), run_time=0.6)
        tag_merge = Text("merge", font_size=26, color=INK).next_to(g_d, UP, buff=0.25)
        self.play(FadeIn(tag_merge, shift=UP * 0.2), run_time=0.4)
        self.wait(0.6)

        # loop: D -> A (curved arc back over the top)
        loop = CurvedArrow(
            g_d.get_top() + UP * 0.05, g_a.get_top() + UP * 0.05,
            angle=-PI / 2.2, color=TOK, stroke_width=4, tip_length=0.24,
        )
        tag_loop = Text("loop back", font_size=26, color=TOK).next_to(loop, UP, buff=0.05)
        self.play(Create(loop), FadeIn(tag_loop), run_time=0.7)

        cap = caption("A graph can branch, merge, and loop.", INK)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(2.0)

        # =================================================================
        self.next_section("Beat 5 - LangGraph")
        # =================================================================
        self.play(
            FadeOut(VGroup(pipe, g_a, g_b, g_c, g_d, br1, br2, mg1, mg2,
                           loop, tag_branch, tag_merge, tag_loop, cap, title2)),
            run_time=0.6,
        )
        t3 = Text("This is LangGraph", font_size=44, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(t3), run_time=0.7)

        # the agent graph
        start = node("START", MUT, r=0.62, fs=20).move_to(LEFT * 4.6 + UP * 1.3)
        agent = node("Agent", LLM, r=0.78, fs=24).move_to(LEFT * 0.6)
        tools = node("Tools", TOOLC, r=0.72, fs=22).move_to(RIGHT * 4.2 + UP * 1.0)
        end   = node("END", USR, r=0.62, fs=22).move_to(LEFT * 0.6 + DOWN * 2.4)

        self.play(GrowFromCenter(start), GrowFromCenter(agent), run_time=0.5)
        e_start = directed(start, agent, color=MUT)
        self.play(Create(e_start), run_time=0.4)

        # agent decides: call a tool, or finish  ->  the branch
        self.play(GrowFromCenter(tools), GrowFromCenter(end), run_time=0.5)
        e_call = directed(agent, tools, color=TOK)
        lbl_call = Text("call a tool", font_size=22, color=TOK).next_to(
            e_call, DOWN, buff=0.12).shift(RIGHT * 0.1)
        e_done = directed(agent, end, color=USR)
        lbl_done = Text("done", font_size=22, color=USR).next_to(e_done, RIGHT, buff=0.15)
        self.play(Create(e_call), FadeIn(lbl_call), run_time=0.6)
        self.play(Create(e_done), FadeIn(lbl_done), run_time=0.6)

        # tools loop back to the agent
        loop2 = CurvedArrow(
            tools.get_left() + LEFT * 0.05, agent.get_right() + UP * 0.35,
            angle=PI / 2.6, color=TOOLC, stroke_width=4, tip_length=0.24,
        )
        lbl_loop = Text("result goes back", font_size=20, color=TOOLC).next_to(
            loop2, UP, buff=0.08)
        self.play(Create(loop2), FadeIn(lbl_loop), run_time=0.7)

        # show the loop "running": pulse around agent -> tools -> back
        self.wait(0.5)
        for _ in range(3):
            self.play(Indicate(agent, color=LLM, scale_factor=1.12), run_time=0.45)
            self.play(Indicate(e_call, color=TOK), run_time=0.35)
            self.play(Indicate(tools, color=TOOLC, scale_factor=1.12), run_time=0.45)
            self.play(Indicate(loop2, color=TOOLC), run_time=0.35)
        # ...then it finishes
        self.play(Indicate(agent, color=LLM, scale_factor=1.12), run_time=0.45)
        self.play(Indicate(e_done, color=USR), Indicate(end, color=USR, scale_factor=1.15),
                  run_time=0.6)

        cap = caption("Branch to pick a tool. Loop until it's done.", INK)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(2.2)

        # =================================================================
        self.next_section("Beat 6 - the mapping")
        # =================================================================
        agent_graph = VGroup(t3, start, agent, tools, end, e_start, e_call,
                             lbl_call, e_done, lbl_done, loop2, lbl_loop, cap)
        self.play(FadeOut(agent_graph), run_time=0.6)

        head = Text("So, in LangGraph:", font_size=40, color=INK).to_edge(UP, buff=0.7)
        self.play(Write(head), run_time=0.7)

        rows = [
            ("nodes", "=", "your steps  (call the LLM, run a tool)", USR),
            ("edges", "=", "what happens next", AST),
            ("loops", "=", "keep going until the answer is ready", TOK),
        ]
        line_mobs = VGroup()
        for left, eq, right, col in rows:
            lm = Text(left, font_size=34, color=col, weight=BOLD)
            em = Text(eq, font_size=34, color=MUT)
            rm = Text(right, font_size=30, color=INK)
            row = VGroup(lm, em, rm).arrange(RIGHT, buff=0.35)
            line_mobs.add(row)
        line_mobs.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(ORIGIN + DOWN * 0.3)
        for row in line_mobs:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.7)
        self.wait(0.8)

        kicker = Text("Your agent, drawn as a graph.",
                      font_size=32, color=INK).to_edge(DOWN, buff=0.55)
        self.play(Write(kicker), run_time=0.9)
        self.wait(2.0)
