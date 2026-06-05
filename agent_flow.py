"""
Agent flow — a Manim Community animation for teaching how an AI agent works.

Four acts (use `--save_sections` to render them separately):
  1. The agent architecture: Mistral (LLM) + web_search + get_datetime, wired up.
  2. The UI: user says "hey", a reply comes back.
  3. A current-event question -> web_search is called -> small result -> answer.
  4. The payoff: the 4 messages + the tool call on the left, and Mistral's
     actual token stream (chat template) growing one step at a time on the right.

Render (Manim Community / `manim`):
  manim -qh agent_flow.py AgentFlow        # 1080p
  manim -ql agent_flow.py AgentFlow        # fast 480p preview

No LaTeX needed (uses Text/Paragraph only). Needs cairo, pango, ffmpeg.
Swap any text strings freely; layout auto-fits.
"""

from manim import *

# ---- palette -------------------------------------------------------------
SYS   = "#9a9a93"   # system  (gray)
USR   = "#4a9eff"   # user    (blue)
AST   = "#9d92f0"   # assistant (purple)
TOOLC = "#33c499"   # tool    (teal)
LLM   = "#ff7a4d"   # Mistral brain (coral)
TOK   = "#f0a637"   # special / control tokens (amber)
INK   = "#ECECEC"   # primary text
MUT   = "#8a8a8a"   # muted text
BG    = "#0e0e12"   # background


# ---- helpers -------------------------------------------------------------
def mtext(s, **kw):
    """Text, or Paragraph if the string contains explicit newlines."""
    if "\n" in s:
        return Paragraph(*s.split("\n"), line_spacing=0.6, **kw)
    return Text(s, **kw)


def boxed(mob, color, buff=0.22, radius=0.16, fo=0.12, sw=2.0):
    rect = RoundedRectangle(
        corner_radius=radius, width=mob.width + 2 * buff, height=mob.height + 2 * buff,
        color=color, stroke_width=sw, fill_color=color, fill_opacity=fo,
    ).move_to(mob)
    return VGroup(rect, mob)


def label_box(title, subtitle=None, color=INK, w=2.6, h=1.1, fs=28):
    rect = RoundedRectangle(
        corner_radius=0.16, width=w, height=h, color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.12,
    )
    if subtitle:
        txt = VGroup(
            Text(title, font_size=fs, color=INK, weight=BOLD),
            Text(subtitle, font_size=fs - 8, color=MUT),
        ).arrange(DOWN, buff=0.08)
    else:
        txt = Text(title, font_size=fs, color=INK, weight=BOLD)
    txt.move_to(rect)
    return VGroup(rect, txt)


def bubble(text, color, fs=22):
    return boxed(mtext(text, font_size=fs, color=INK), color, buff=0.2, radius=0.22, fo=0.18)


def role_card(role, content, color, fs=22):
    g = VGroup(
        Text(role, font_size=fs - 4, color=color, weight=BOLD),
        mtext(content, font_size=fs, color=INK),
    ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    return boxed(g, color, buff=0.2, radius=0.14, fo=0.1)


def wire_line(segments, fs=18):
    pieces = [Text(s, font="monospace", font_size=fs, color=col) for s, col in segments]
    return VGroup(*pieces).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)


class AgentFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =================================================================
        self.next_section("Act 1 - architecture")
        # =================================================================
        title = Text("How an AI agent works", font_size=40, color=INK).to_edge(UP, buff=0.45)
        self.play(Write(title))

        llm = label_box("Mistral", "LLM", color=LLM, w=2.7, h=1.25, fs=30)
        web = label_box("web_search", "tool", color=TOOLC, w=2.7, h=1.0, fs=24)
        clk = label_box("get_datetime", "tool", color=TOOLC, w=2.9, h=1.0, fs=24)
        tools = VGroup(web, clk).arrange(RIGHT, buff=0.55).next_to(llm, DOWN, buff=1.05)

        a1 = DoubleArrow(llm.get_bottom(), web.get_top(), buff=0.12, color=MUT, stroke_width=3, tip_length=0.2)
        a2 = DoubleArrow(llm.get_bottom(), clk.get_top(), buff=0.12, color=MUT, stroke_width=3, tip_length=0.2)

        core = VGroup(llm, tools)
        boundary = DashedVMobject(
            SurroundingRectangle(core, color=AST, buff=0.55, stroke_width=2.5), num_dashes=64
        )
        agent_lbl = Text("Agent", font_size=24, color=AST).next_to(boundary, UP, buff=0.12).align_to(boundary, LEFT).shift(RIGHT * 0.15)

        user = label_box("User", color=USR, w=1.9, h=1.05, fs=26).next_to(boundary, LEFT, buff=1.0)
        ua = DoubleArrow(user.get_right(), boundary.get_left(), buff=0.12, color=USR, stroke_width=3, tip_length=0.2)

        self.play(FadeIn(llm, scale=0.8))
        self.play(FadeIn(web, shift=UP * 0.3), FadeIn(clk, shift=UP * 0.3))
        self.play(Create(a1), Create(a2))
        self.play(Create(boundary), FadeIn(agent_lbl))
        self.play(FadeIn(user, shift=RIGHT * 0.3), Create(ua))
        self.wait(0.8)

        # =================================================================
        self.next_section("Act 2 - the UI")
        # =================================================================
        self.play(FadeOut(title))
        arch = VGroup(llm, tools, a1, a2, boundary, agent_lbl, user, ua)
        self.play(arch.animate.scale(0.62).to_edge(LEFT, buff=0.5))

        phone = RoundedRectangle(
            corner_radius=0.3, width=5.0, height=6.7, color=MUT, stroke_width=2.5,
            fill_color="#16161c", fill_opacity=1.0,
        ).to_edge(RIGHT, buff=0.6)
        hbar = RoundedRectangle(
            corner_radius=0.18, width=4.7, height=0.7, color=AST, stroke_width=1.5,
            fill_color=AST, fill_opacity=0.2,
        ).move_to(phone.get_top() + DOWN * 0.55)
        htxt = Text("Mistral Agent", font_size=22, color=INK).move_to(hbar)
        self.play(Create(phone), FadeIn(hbar), Write(htxt))

        cursor = []

        def add_bubble(text, color, side, fs=22):
            b = bubble(text, color, fs=fs)
            if b.width > 3.95:
                b.scale_to_fit_width(3.95)
            anchor = cursor[-1] if cursor else hbar
            b.next_to(anchor, DOWN, buff=0.3)
            if side == "r":
                b.align_to(phone, RIGHT).shift(LEFT * 0.28)
            else:
                b.align_to(phone, LEFT).shift(RIGHT * 0.28)
            cursor.append(b)
            return b

        u1 = add_bubble("hey", USR, "r")
        self.play(FadeIn(u1, shift=UP * 0.3))
        self.play(Indicate(user, color=USR), run_time=0.6)
        self.play(Indicate(boundary, color=AST, scale_factor=1.04), run_time=0.6)
        self.play(Indicate(llm, color=LLM), run_time=0.6)
        r1 = add_bubble("Hey! How can I help?", AST, "l")
        self.play(FadeIn(r1, shift=UP * 0.3))
        self.wait(0.8)

        # =================================================================
        self.next_section("Act 3 - current event + web_search")
        # =================================================================
        self.play(FadeOut(VGroup(u1, r1)))
        cursor.clear()

        q = add_bubble("What's the latest on Artemis II?", USR, "r")
        self.play(FadeIn(q, shift=UP * 0.3))

        self.play(Indicate(user, color=USR), run_time=0.5)
        self.play(Indicate(llm, color=LLM), run_time=0.6)
        think = Text("...deciding", font_size=20, color=MUT).next_to(llm, UP, buff=0.18)
        self.play(FadeIn(think)); self.wait(0.3); self.play(FadeOut(think))

        self.play(Indicate(a1, color=TOK), run_time=0.6)
        self.play(Indicate(web, color=TOK, scale_factor=1.12), run_time=0.6)
        searching = Text("searching the web...", font_size=18, color=TOK).next_to(web, DOWN, buff=0.25)
        self.play(FadeIn(searching)); self.wait(0.5)

        res = boxed(Text("flyby on track", font="monospace", font_size=16, color=TOOLC),
                    TOOLC, buff=0.12, radius=0.1, fo=0.18).move_to(web)
        self.play(FadeOut(searching), FadeIn(res))
        self.play(res.animate.move_to(llm))
        self.play(Indicate(llm, color=LLM), FadeOut(res))

        ans = add_bubble(
            "The latest: Artemis II's crewed\nMoon flyby is on track, with the\nlaunch window confirmed.",
            AST, "l", fs=20,
        )
        self.play(FadeIn(ans, shift=UP * 0.3))
        self.wait(1.0)

        # =================================================================
        self.next_section("Act 4 - messages vs the template")
        # =================================================================
        self.play(FadeOut(arch), FadeOut(VGroup(phone, hbar, htxt, q, ans)))

        t4 = Text("The same conversation, two views", font_size=34, color=INK).to_edge(UP, buff=0.45)
        self.play(Write(t4))

        items = [
            ("system",               "You are a helpful assistant.",  SYS),
            ("available tools",      "web_search, get_datetime",      TOK),
            ("user",                 "What's the latest on Artemis II?", USR),
            ("assistant - tool call", 'web_search("Artemis II ...")',  AST),
            ("tool - result",        "flyby on track; window confirmed.", TOOLC),
            ("assistant - answer",   "The latest: flyby is on track...", AST),
        ]
        cards = VGroup(*[role_card(r, c, col) for r, c, col in items]).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT
        )
        cards.scale_to_fit_height(5.0).to_edge(LEFT, buff=0.55)

        wsegs = [
            [("<s>", TOK), ("[SYSTEM_PROMPT]", TOK), ("You are a helpful assistant.", INK), ("[/SYSTEM_PROMPT]", TOK)],
            [("[AVAILABLE_TOOLS]", TOK), ("[ web_search, get_datetime ]", INK), ("[/AVAILABLE_TOOLS]", TOK)],
            [("[INST]", TOK), ("What's the latest on Artemis II?", INK), ("[/INST]", TOK)],
            [("[TOOL_CALLS]", TOK), ('[{"name":"web_search", ...}]', INK), ("</s>", TOK)],
            [("[TOOL_RESULTS]", TOK), ("flyby on track; window confirmed.", INK), ("[/TOOL_RESULTS]", TOK)],
            [("The latest: flyby is on track...", INK), ("</s>", TOK)],
        ]
        lines = [wire_line(seg, fs=18) for seg in wsegs]
        wire = VGroup(*lines).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        wire.scale_to_fit_width(6.1)
        if wire.height > 5.0:
            wire.scale_to_fit_height(5.0)
        wire.to_edge(RIGHT, buff=0.45).set_y(cards.get_y())

        lh = Text("Messages - what you write", font_size=22, color=USR).next_to(cards, UP, buff=0.25).align_to(cards, LEFT)
        rh = Text("Tokens - what Mistral sees", font_size=22, color=TOK).next_to(wire, UP, buff=0.25).align_to(wire, LEFT)
        self.play(FadeIn(lh), FadeIn(rh))

        for i in range(len(items)):
            self.play(FadeIn(cards[i], shift=RIGHT * 0.3), run_time=0.45)
            self.play(FadeIn(lines[i], shift=LEFT * 0.3), run_time=0.45)
            toks = VGroup(*[p for p, (s, c) in zip(lines[i], wsegs[i]) if c == TOK])
            if len(toks) > 0:
                self.play(Indicate(toks, color=TOK, scale_factor=1.18), run_time=0.45)

        self.wait(0.8)
        note = Text("Roles are for you. On the wire, it's one token stream.",
                    font_size=24, color=INK).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(2)
