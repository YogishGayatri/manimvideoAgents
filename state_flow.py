"""
State flow — a ~1:15 Manim Community animation that makes LangGraph *state*
crystal clear, with almost no prose.

The idea: state is one shared object — a card of key/value fields. It enters
at START, travels along the edges, and every node reads it and writes into it
(two nodes call an LLM to do so). The final state at END *is* the answer.

Beats (use `--save_sections` to render separately):
  0. Title: "State" — the data that travels through your graph.
  1. What is state: a card with fields. A node reads it, writes to it.
  2. The graph: START -> Plan(LLM) -> Search(tool) -> Write(LLM) -> END.
     The card rides the edges; each node fills in one field.
  3. END: the finished state is the answer.

Render (Manim Community / `manim`):
  manim -qh state_flow.py StateFlow        # 1080p
  manim -ql state_flow.py StateFlow        # fast 480p preview

No LaTeX needed (uses Text only). Needs cairo, pango, ffmpeg.
"""

import numpy as np

from manim import *

# ---- palette (shared with the other scenes) -----------------------------
USR   = "#4a9eff"   # blue
AST   = "#9d92f0"   # purple — graph nodes
TOOLC = "#33c499"   # teal   — tool node
LLM   = "#ff7a4d"   # coral  — LLM
TOK   = "#f0a637"   # amber  — the state card / writes
INK   = "#ECECEC"   # primary text
MUT   = "#8a8a8a"   # muted text
BG    = "#0e0e12"   # background

EMPTY = "—"


# ---- helpers ------------------------------------------------------------
def chip(label, color, w=1.9, h=0.8, fs=22):
    rect = RoundedRectangle(corner_radius=0.14, width=w, height=h, color=color,
                            stroke_width=2.6, fill_color=color, fill_opacity=0.14)
    txt = Text(label, font_size=fs, color=INK, weight=BOLD)
    if txt.width > w - 0.3:
        txt.scale_to_fit_width(w - 0.3)
    txt.move_to(rect)
    g = VGroup(rect, txt)
    g.rect = rect
    return g


def edge(a, b, color=MUT, sw=3.5):
    return Arrow(a.rect.get_right(), b.rect.get_left(), buff=0.12, color=color,
                 stroke_width=sw, tip_length=0.2)


def caption(s, color=INK, fs=28):
    return Text(s, font_size=fs, color=color).to_edge(DOWN, buff=0.45)


class StateFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =================================================================
        self.next_section("Beat 0 - title")
        # =================================================================
        big = Text("State", font_size=92, color=TOK, weight=BOLD)
        sub = Text("the data that travels through your graph",
                   font_size=28, color=MUT).next_to(big, DOWN, buff=0.4)
        self.play(Write(big), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.6)
        self.wait(2.4)
        self.play(FadeOut(VGroup(big, sub)), run_time=0.5)

        # =================================================================
        self.next_section("Beat 1 - what is state")
        # =================================================================
        # the state card: a small set of named fields
        keys = ["question", "plan", "result", "answer"]
        key_mobs, val_mobs, rows = [], [], VGroup()
        for k in keys:
            km = Text(k, font_size=22, color=MUT)
            vm = Text(EMPTY, font_size=22, color=MUT)
            key_mobs.append(km)
            val_mobs.append(vm)
            rows.add(VGroup(km, vm))
        # column-align: keys at x=0, values at a fixed x offset, fixed row pitch
        kw = max(km.width for km in key_mobs)
        for i, (km, vm) in enumerate(zip(key_mobs, val_mobs)):
            km.move_to(ORIGIN, aligned_edge=LEFT).shift(DOWN * i * 0.6)
            vm.move_to(km.get_left() + RIGHT * (kw + 0.5), aligned_edge=LEFT)

        card_rect = RoundedRectangle(
            corner_radius=0.18, width=6.0, height=rows.height + 1.5,
            color=TOK, stroke_width=2.8, fill_color=TOK, fill_opacity=0.07,
        )
        card_title = Text("state", font_size=24, color=TOK, weight=BOLD)
        rows.move_to(card_rect.get_center() + DOWN * 0.25)
        rows.align_to(card_rect.get_left() + RIGHT * 0.5, LEFT)
        card_title.next_to(card_rect.get_top(), DOWN, buff=0.18)
        card = VGroup(card_rect, card_title, rows).move_to(ORIGIN + DOWN * 0.3)

        h1 = Text("State is just this", font_size=36, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(h1), run_time=0.6)
        self.play(Create(card_rect), FadeIn(card_title), run_time=0.7)
        self.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.2), run_time=0.9)

        cap1 = caption("a few named fields — what we know so far", MUT)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(2.2)

        # a node reads it and writes to it
        self.play(card.animate.shift(LEFT * 2.0), FadeOut(cap1), run_time=0.6)
        demo = chip("node", AST, w=2.0, h=0.85, fs=24).next_to(card, RIGHT, buff=1.8)
        r_arrow = Arrow(card_rect.get_right() + UP * 0.5, demo.rect.get_left() + UP * 0.35,
                        color=USR, stroke_width=3.5, tip_length=0.2, buff=0.15)
        w_arrow = Arrow(demo.rect.get_left() + DOWN * 0.35, card_rect.get_right() + DOWN * 0.5,
                        color=TOK, stroke_width=3.5, tip_length=0.2, buff=0.15)
        r_lbl = Text("reads", font_size=20, color=USR).next_to(r_arrow, UP, buff=0.1)
        w_lbl = Text("writes", font_size=20, color=TOK).next_to(w_arrow, DOWN, buff=0.1)
        self.play(GrowFromCenter(demo), run_time=0.5)
        self.play(Create(r_arrow), FadeIn(r_lbl), run_time=0.6)
        self.play(Create(w_arrow), FadeIn(w_lbl), run_time=0.6)

        cap2 = caption("every node reads the state, then writes to it", INK)
        self.play(FadeIn(cap2), run_time=0.5)
        self.wait(2.6)

        # =================================================================
        self.next_section("Beat 2 - the journey")
        # =================================================================
        self.play(FadeOut(VGroup(demo, r_arrow, w_arrow, r_lbl, w_lbl, cap2, h1)),
                  run_time=0.5)

        # the graph across the top
        n_start = chip("START", MUT, w=1.7, h=0.75, fs=18)
        n_plan = chip("Plan", AST)
        n_search = chip("Search", TOOLC)
        n_write = chip("Write", AST)
        n_end = chip("END", USR, w=1.7, h=0.75, fs=18)
        nodes = VGroup(n_start, n_plan, n_search, n_write, n_end).arrange(
            RIGHT, buff=1.05).move_to(UP * 2.5)

        # LLM badges on the two thinking nodes
        b1 = chip("LLM", LLM, w=1.0, h=0.5, fs=16).next_to(n_plan, UP, buff=0.2)
        b2 = chip("LLM", LLM, w=1.0, h=0.5, fs=16).next_to(n_write, UP, buff=0.2)
        t_badge = chip("tool", TOOLC, w=1.0, h=0.5, fs=16).next_to(n_search, UP, buff=0.2)

        edges = VGroup(*[edge(a, b) for a, b in zip(nodes[:-1], nodes[1:])])

        self.play(card.animate.scale(0.85).move_to(DOWN * 1.5 + LEFT * 4.3),
                  run_time=0.7)
        self.play(LaggedStartMap(FadeIn, nodes, lag_ratio=0.15),
                  LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.15),
                  run_time=1.2)
        self.play(FadeIn(b1, shift=DOWN * 0.15), FadeIn(b2, shift=DOWN * 0.15),
                  FadeIn(t_badge, shift=DOWN * 0.15), run_time=0.6)
        self.wait(1.2)

        # -- a helper to rewrite one field of the card --------------------
        def write_field(idx, new_text, color=INK):
            old = val_mobs[idx]
            new = Text(new_text, font_size=22, color=color)
            new.scale(0.85)  # match the card's current scale
            new.move_to(old, aligned_edge=LEFT)
            max_w = card_rect.get_right()[0] - old.get_left()[0] - 0.35
            if new.width > max_w:
                new.scale_to_fit_width(max_w)
                new.move_to(old, aligned_edge=LEFT)
            val_mobs[idx] = new
            rows[idx].remove(old)
            rows[idx].add(new)
            return old, new

        def card_under(n):
            # follow the node, but keep the card fully on screen
            x = float(np.clip(n.rect.get_center()[0], -4.3, 4.3))
            return x * RIGHT + DOWN * 1.5

        def travel(to_node, e):
            self.play(card.animate.move_to(card_under(to_node)),
                      ShowPassingFlash(e.copy().set_color(TOK).set_stroke(width=6),
                                       time_width=0.6),
                      run_time=1.1)

        # reads: a copy of a field flies up into the node's badge
        def read_into(badge, *idxs):
            ghosts = VGroup(*[val_mobs[i].copy() for i in idxs])
            self.play(*[g.animate.scale(0.5).set_opacity(0.55)
                        .move_to(badge.rect.get_center()) for g in ghosts],
                      run_time=1.0)
            self.play(Indicate(badge, color=badge.rect.get_color(),
                               scale_factor=1.3), FadeOut(ghosts), run_time=0.5)

        # writes: the new value drops out of the badge into the card
        def write_from(badge, idx, text, color):
            old, new = write_field(idx, text, color)
            spawn = new.copy().scale(0.5).move_to(badge.rect.get_center())
            self.play(FadeOut(old, run_time=0.3),
                      ReplacementTransform(spawn, new),
                      Flash(new, color=color, flash_radius=0.7), run_time=0.8)
            self.remove(old)

        # START: the user's question enters the state
        self.play(card.animate.move_to(card_under(n_start)), run_time=0.7)
        self.play(Indicate(n_start, color=INK, scale_factor=1.1), run_time=0.5)
        old, new = write_field(0, '"weather in Paris?"', USR)
        self.play(Transform(old, new), run_time=0.5)
        self.remove(old)
        self.add(new)
        cap = caption("the question goes into the state…", USR, fs=24)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(1.8)

        # PLAN: reads the question, the LLM writes a plan
        travel(n_plan, edges[0])
        cap2 = caption("Plan: LLM reads the question → writes a plan", LLM, fs=24)
        self.play(ReplacementTransform(cap, cap2), run_time=0.4)
        read_into(b1, 0)
        write_from(b1, 1, '"search the web"', INK)
        self.wait(2.2)

        # SEARCH: reads the plan, the tool writes the result
        travel(n_search, edges[1])
        cap3 = caption("Search: tool reads the plan → writes the result", TOOLC, fs=24)
        self.play(ReplacementTransform(cap2, cap3), run_time=0.4)
        read_into(t_badge, 1)
        write_from(t_badge, 2, '"18°C, sunny"', TOOLC)
        self.wait(2.2)

        # WRITE: reads question + result, the LLM writes the answer
        travel(n_write, edges[2])
        cap4 = caption("Write: LLM reads question + result → writes the answer",
                       LLM, fs=24)
        self.play(ReplacementTransform(cap3, cap4), run_time=0.4)
        read_into(b2, 0, 2)
        write_from(b2, 3, '"Paris: 18°C and sunny"', TOK)
        self.wait(2.2)

        # END: the state arrives complete
        travel(n_end, edges[3])
        self.play(Indicate(n_end, color=USR, scale_factor=1.12), run_time=0.6)
        self.wait(1.4)

        # =================================================================
        self.next_section("Beat 3 - the payoff")
        # =================================================================
        self.play(FadeOut(VGroup(nodes, edges, b1, b2, t_badge, cap4)), run_time=0.6)
        self.play(card.animate.scale(1.15).move_to(UP * 0.9), run_time=0.8)
        self.play(Indicate(rows[3], color=TOK, scale_factor=1.12), run_time=0.8)
        self.wait(0.4)

        # the answer field leaves the state and becomes the user's reply
        reply_txt = Text("Paris: 18°C and sunny", font_size=26, color=INK)
        reply_rect = RoundedRectangle(
            corner_radius=0.22, width=reply_txt.width + 0.6,
            height=reply_txt.height + 0.45, color=USR, stroke_width=2.5,
            fill_color=USR, fill_opacity=0.18,
        )
        reply_txt.move_to(reply_rect)
        reply = VGroup(reply_rect, reply_txt).next_to(card, DOWN, buff=0.55)
        self.play(ReplacementTransform(rows[3].copy(), reply), run_time=0.9)
        self.wait(2.0)

        k1 = Text("Same card in, fuller card out.", font_size=30, color=INK)
        k2 = Text("Nodes change the state. Edges carry it.",
                  font_size=30, color=TOK, weight=BOLD)
        ks = VGroup(k1, k2).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        self.play(Write(k1), run_time=0.8)
        self.wait(0.6)
        self.play(Write(k2), run_time=0.9)
        self.wait(3.6)
