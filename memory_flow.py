"""
Memory flow — a ~1:15 Manim Community animation on the three things that let a
LangGraph agent "remember" and stay safe:

  short-term memory  (Checkpointer)  — the current conversation, saved per turn
  long-term memory   (Store)         — facts that outlive the chat
  human-in-the-loop                  — pause before risky steps: approve / edit / reject

It follows the user's slide layout (short-term left, long-term right, both
feeding the LLM) and then adds the human-in-the-loop beat. Visual-first.

Render (Manim Community / `manim`):
  manim -qh memory_flow.py MemoryFlow        # 1080p
  manim -ql memory_flow.py MemoryFlow        # fast 480p preview

No LaTeX needed (uses Text only). Needs cairo, pango, ffmpeg.
"""

import numpy as np

from manim import *

# ---- palette (slide semantics, repo tones) ------------------------------
HUMAN = "#e0524a"   # red   — human message / reject
AI    = "#3aaf57"   # green — AI message / approve
BLUE  = "#4a9eff"   # blue  — checkpointer / store outlines
TOK   = "#f0a637"   # amber — the LLM and the flow arrows
LLMc  = "#f0a637"   # amber — LLM ellipse
INK   = "#ECECEC"   # primary text
MUT   = "#8a8a8a"   # muted text / neutral outlines
BG    = "#0e0e12"   # background


# ---- helpers ------------------------------------------------------------
def bubble(text, color, w=3.3, h=0.6, fs=20):
    rect = RoundedRectangle(corner_radius=0.18, width=w, height=h, color=color,
                            stroke_width=2.6, fill_opacity=0.0)
    t = Text(text, font_size=fs, color=color, weight=BOLD)
    if t.width > w - 0.4:
        t.scale_to_fit_width(w - 0.4)
    t.move_to(rect)
    return VGroup(rect, t)


def heading(text, color=INK, fs=32):
    return Text(text, font_size=fs, color=color, weight=BOLD)


def caption(s, color=INK, fs=26):
    return Text(s, font_size=fs, color=color).to_edge(DOWN, buff=0.4)


def flow_arrow(p1, p2, color=TOK, sw=5, angle=-PI / 8):
    return CurvedArrow(p1, p2, color=color, stroke_width=sw, tip_length=0.25,
                       angle=angle)


class MemoryFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # the LLM lives at the bottom-centre throughout the first half
        llm = VGroup(
            Ellipse(width=3.0, height=1.15, color=LLMc, stroke_width=3.5),
            Text("LLM", font_size=26, color=LLMc, weight=BOLD),
        )
        llm[1].move_to(llm[0])
        llm.move_to(DOWN * 2.5)

        # =================================================================
        self.next_section("Beat 0 - title")
        # =================================================================
        t0 = VGroup(
            Text("How an agent remembers", font_size=44, color=INK, weight=BOLD),
            Text("short-term · long-term · human-in-the-loop",
                 font_size=26, color=MUT),
        ).arrange(DOWN, buff=0.4)
        self.play(Write(t0[0]), run_time=0.9)
        self.play(FadeIn(t0[1], shift=UP * 0.2), run_time=0.6)
        self.wait(2.6)
        self.play(FadeOut(t0), run_time=0.5)

        # =================================================================
        self.next_section("Beat 1 - short-term memory (Checkpointer)")
        # =================================================================
        h_l = heading("Short-term memory", BLUE).move_to(LEFT * 3.7 + UP * 3.35)
        self.play(Write(h_l), run_time=0.6)

        msgs = VGroup(
            bubble("Human message", HUMAN),
            bubble("AI message", AI),
            bubble("Human message", HUMAN),
            bubble("AI message", AI),
            bubble("Human message", HUMAN),
        )
        for i, m in enumerate(msgs):
            m.move_to(LEFT * 3.9 + UP * (1.85 - i * 0.72))
            if i % 2 == 1:                       # indent the AI replies
                m.shift(RIGHT * 0.55)
        cp_box = SurroundingRectangle(msgs, color=BLUE, corner_radius=0.22,
                                      buff=0.3, stroke_width=3)
        cp_lbl = Text("Checkpointer", font_size=26, color=BLUE).next_to(
            cp_box, DOWN, buff=0.22)

        self.play(Create(cp_box), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.25) for m in msgs],
                              lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(cp_lbl, shift=UP * 0.15), run_time=0.4)
        cap = caption("the current conversation — saved turn by turn", BLUE)
        self.play(FadeIn(cap), run_time=0.5)
        # sweep through the saved turns
        self.play(LaggedStart(*[Indicate(m, color=m[0].get_color(),
                                         scale_factor=1.06) for m in msgs],
                              lag_ratio=0.22), run_time=1.8)
        self.wait(2.6)
        self.play(FadeOut(cap), run_time=0.4)

        # =================================================================
        self.next_section("Beat 2 - long-term memory (Store)")
        # =================================================================
        h_r = heading("Long-term memory", AI).move_to(RIGHT * 3.7 + UP * 3.35)
        self.play(Write(h_r), run_time=0.6)

        grid = VGroup()
        for r in range(4):
            for c in range(4):
                col = HUMAN if (r + c) % 2 == 0 else AI
                grid.add(RoundedRectangle(corner_radius=0.05, width=0.6, height=0.22,
                                          color=col, stroke_width=2.2, fill_opacity=0.0))
        grid.arrange_in_grid(rows=4, cols=4, buff=(0.2, 0.18))
        grid.move_to(RIGHT * 3.7 + UP * 1.7)
        mem_box = SurroundingRectangle(grid, color=MUT, corner_radius=0.16,
                                       buff=0.28, stroke_width=3)

        diamond = Polygon([1.2, 0, 0], [0, 0.62, 0], [-1.2, 0, 0], [0, -0.62, 0],
                          color=BLUE, stroke_width=3).move_to(RIGHT * 3.7 + DOWN * 0.55)
        store_lbl = Text("Store", font_size=26, color=BLUE).next_to(
            diamond, DOWN, buff=0.2)
        a_d1 = Arrow(mem_box.get_corner(DL) + RIGHT * 0.5, diamond.get_left() + UP * 0.25,
                     color=INK, stroke_width=3, tip_length=0.2, buff=0.15)
        a_d2 = Arrow(mem_box.get_corner(DR) + LEFT * 0.5, diamond.get_right() + UP * 0.25,
                     color=INK, stroke_width=3, tip_length=0.2, buff=0.15)

        self.play(Create(mem_box), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in grid],
                              lag_ratio=0.04), run_time=1.4)
        self.play(GrowArrow(a_d1), GrowArrow(a_d2), run_time=0.5)
        self.play(Create(diamond), FadeIn(store_lbl, shift=UP * 0.15), run_time=0.6)
        cap = caption("facts that outlive the chat — saved and looked up", AI)
        self.play(FadeIn(cap), run_time=0.5)
        # look up a relevant fact: it drops down into the Store
        self.play(Indicate(grid[6], color=AI, scale_factor=1.6), run_time=0.5)
        fact = grid[6].copy().set_stroke(width=4)
        self.play(fact.animate.move_to(diamond.get_center()), run_time=0.8)
        self.play(Indicate(diamond, color=BLUE, scale_factor=1.12),
                  FadeOut(fact), run_time=0.5)
        self.wait(3.4)
        self.play(FadeOut(cap), run_time=0.4)

        # =================================================================
        self.next_section("Beat 3 - both feed the LLM")
        # =================================================================
        divider = DashedLine(UP * 3.7, DOWN * 1.7, color=MUT, stroke_width=2.5,
                             dash_length=0.18)
        self.play(Create(divider), run_time=0.5)
        self.play(FadeIn(llm, scale=0.85), run_time=0.6)

        a_cp = flow_arrow(cp_box.get_bottom() + DOWN * 0.05,
                          llm[0].get_left() + LEFT * 0.05, color=TOK, angle=PI / 8)
        a_st = flow_arrow(diamond.get_bottom() + DOWN * 0.05,
                          llm[0].get_right() + RIGHT * 0.05, color=TOK, angle=-PI / 8)
        self.play(Create(a_cp), Create(a_st), run_time=0.8)

        cap = caption("every turn, the LLM reads both", INK)
        self.play(FadeIn(cap), run_time=0.5)
        # a pulse from each memory down into the LLM
        d1 = Dot(color=TOK, radius=0.12).move_to(cp_box.get_bottom())
        d2 = Dot(color=TOK, radius=0.12).move_to(diamond.get_bottom())
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.2)
        self.play(MoveAlongPath(d1, a_cp.copy()), MoveAlongPath(d2, a_st.copy()),
                  run_time=1.0)
        self.play(Indicate(llm, color=LLMc, scale_factor=1.12),
                  FadeOut(d1), FadeOut(d2), run_time=0.6)
        self.wait(3.0)

        # bridge into human-in-the-loop
        bridge = caption("…but some actions shouldn't run on their own", HUMAN)
        self.play(ReplacementTransform(cap, bridge), run_time=0.5)
        self.wait(2.0)

        # =================================================================
        self.next_section("Beat 4 - human-in-the-loop")
        # =================================================================
        slide = VGroup(h_l, msgs, cp_box, cp_lbl, h_r, grid, mem_box, diamond,
                       store_lbl, a_d1, a_d2, divider, a_cp, a_st, bridge)
        self.play(FadeOut(slide), llm.animate.move_to(LEFT * 4.3 + UP * 0.3),
                  run_time=0.8)
        h_hitl = heading("Human-in-the-loop", TOK).to_edge(UP, buff=0.5)
        self.play(Write(h_hitl), run_time=0.6)

        # the LLM proposes a risky action
        action = bubble("send email", HUMAN, w=2.6, h=0.8, fs=22)
        action.move_to(LEFT * 0.2 + UP * 0.3)
        a_propose = Arrow(llm[0].get_right(), action.get_left(), color=TOK,
                          stroke_width=4, tip_length=0.22, buff=0.2)
        self.play(GrowArrow(a_propose), FadeIn(action, shift=RIGHT * 0.2), run_time=0.7)

        # an interrupt gate stops the flow
        gate = DashedLine(action.get_right() + RIGHT * 0.5 + UP * 0.7,
                          action.get_right() + RIGHT * 0.5 + DOWN * 0.7,
                          color=HUMAN, stroke_width=4, dash_length=0.14)
        gate_lbl = Text("interrupt", font_size=20, color=HUMAN).next_to(gate, UP, buff=0.12)
        d = Dot(color=TOK, radius=0.13).move_to(action.get_right())
        self.play(FadeIn(d, scale=0.5), run_time=0.2)
        self.play(d.animate.move_to(gate.get_center() + LEFT * 0.2),
                  Create(gate), FadeIn(gate_lbl), run_time=0.6)
        self.play(Wiggle(d), run_time=0.6)          # blocked, waiting
        cap = caption("before a risky step, the graph pauses…", HUMAN)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(2.2)

        # a human reviews: approve / edit / reject
        person = VGroup(
            Circle(radius=0.22, color=INK, stroke_width=3),
            Arc(radius=0.5, start_angle=PI * 0.15, angle=PI * 0.7, color=INK,
                stroke_width=3),
        )
        person[0].next_to(person[1], UP, buff=-0.05)
        person.move_to(RIGHT * 4.7 + UP * 1.3)
        p_lbl = Text("you", font_size=20, color=INK).next_to(person, DOWN, buff=0.12)

        opts = VGroup(
            bubble("approve", AI, w=2.2, h=0.6, fs=20),
            bubble("edit", TOK, w=2.2, h=0.6, fs=20),
            bubble("reject", HUMAN, w=2.2, h=0.6, fs=20),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 4.7 + DOWN * 0.9)

        self.play(FadeIn(person, shift=DOWN * 0.2), FadeIn(p_lbl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in opts],
                              lag_ratio=0.2), run_time=0.9)
        cap2 = caption("…and waits for you: approve, edit, or reject", INK)
        self.play(ReplacementTransform(cap, cap2), run_time=0.4)
        self.wait(2.0)

        # you approve -> the approval reaches the gate, which opens
        self.play(Indicate(opts[0], color=AI, scale_factor=1.15), run_time=0.6)
        a_ok = Arrow(opts[0].get_left(), gate.get_center() + RIGHT * 0.2,
                     color=AI, stroke_width=3.5, tip_length=0.2, buff=0.2)
        self.play(GrowArrow(a_ok), run_time=0.5)
        self.play(gate.animate.set_opacity(0.2),
                  gate_lbl.animate.set_opacity(0.2), run_time=0.5)
        # gate open -> the agent's pending action now runs (it sends the email)
        self.play(d.animate.move_to(action.get_right() + LEFT * 0.15), run_time=0.6)
        sent = Text("sent", font_size=22, color=AI, weight=BOLD).next_to(
            action, DOWN, buff=0.22)
        self.play(action[0].animate.set_color(AI), action[1].animate.set_color(AI),
                  FadeOut(d), FadeIn(sent, shift=UP * 0.15),
                  Flash(action, color=AI, flash_radius=1.0), run_time=0.7)
        cap3 = caption("only after you approve does the agent act", AI)
        self.play(ReplacementTransform(cap2, cap3), run_time=0.4)
        self.wait(4.4)

        # =================================================================
        self.next_section("Beat 5 - payoff")
        # =================================================================
        stage = VGroup(h_hitl, llm, action, a_propose, gate, gate_lbl, person,
                       p_lbl, opts, a_ok, sent, cap3)
        self.play(FadeOut(stage), run_time=0.6)

        rows = VGroup(
            VGroup(Text("Checkpointer", font_size=30, color=BLUE, weight=BOLD),
                   Text("— this conversation", font_size=28, color=INK)),
            VGroup(Text("Store", font_size=30, color=AI, weight=BOLD),
                   Text("— what to remember", font_size=28, color=INK)),
            VGroup(Text("Human-in-the-loop", font_size=30, color=TOK, weight=BOLD),
                   Text("— when to ask you", font_size=28, color=INK)),
        )
        for row in rows:
            row.arrange(RIGHT, buff=0.25)
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(ORIGIN)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(1.4)
        self.wait(5.0)
