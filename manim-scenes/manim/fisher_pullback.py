from manim import *


class FisherPullback(Scene):
    def construct(self):
        title = Text("Fisher Information as a Pullback Metric", font_size=36)
        title.to_edge(UP)

        M = RoundedRectangle(width=4.3, height=2.5, corner_radius=0.2)
        M.set_stroke(BLUE, 2)
        M.set_fill(BLUE_E, opacity=0.12)
        M.shift(LEFT * 3.2)

        P = RoundedRectangle(width=4.3, height=2.5, corner_radius=0.2)
        P.set_stroke(GREEN, 2)
        P.set_fill(GREEN_E, opacity=0.12)
        P.shift(RIGHT * 3.2)

        M_label = MathTex(r"\mathcal{M}", font_size=42).move_to(
            M.get_top() + DOWN * 0.45
        )
        P_label = MathTex(r"\mathcal{P}", font_size=42).move_to(
            P.get_top() + DOWN * 0.45
        )

        M_sub = Text("parameter space", font_size=22).next_to(M, DOWN, buff=0.2)
        P_sub = Text("distribution space", font_size=22).next_to(P, DOWN, buff=0.2)

        theta = Dot(M.get_center() + LEFT * 0.45 + DOWN * 0.05, color=BLUE)
        theta_label = MathTex(r"\theta", font_size=30).next_to(theta, DOWN, buff=0.12)

        ptheta = Dot(P.get_center() + LEFT * 0.35 + DOWN * 0.05, color=GREEN)
        ptheta_label = MathTex(r"p(\cdot;\theta)", font_size=30).next_to(
            ptheta, DOWN, buff=0.12
        )

        map_arrow = Arrow(M.get_right(), P.get_left(), buff=0.25, color=BLUE)
        map_label = MathTex(r"f:\theta\mapsto p(\cdot;\theta)", font_size=28)
        map_label.next_to(map_arrow, UP, buff=0.15)

        tangent = Arrow(
            theta.get_center(),
            theta.get_center() + UP * 0.8 + RIGHT * 0.55,
            buff=0,
            color=YELLOW,
        )
        tangent_label = MathTex(r"\partial_i", font_size=28).next_to(
            tangent.get_end(), UP, buff=0.1
        )

        score = Arrow(
            ptheta.get_center(),
            ptheta.get_center() + UP * 0.8 + RIGHT * 0.55,
            buff=0,
            color=YELLOW,
        )
        score_label = MathTex(r"\partial_i \log p", font_size=28).next_to(
            score.get_end(), UP, buff=0.1
        )

        df_arrow = Arrow(
            tangent.get_end() + DOWN * 1.55,
            score.get_end() + DOWN * 1.55,
            buff=0.15,
            color=GRAY,
        )
        df_label = MathTex(r"df_\theta", font_size=28).next_to(df_arrow, DOWN, buff=0.1)

        metric_p = MathTex(r"\langle u,v\rangle_p = \mathbb{E}_p[uv]", font_size=30)
        metric_p.move_to(P.get_bottom() + UP * 0.45)

        metric_m = MathTex(
            r"F_{ij}(\theta)=\mathbb{E}_\theta[\partial_i\log p\,\partial_j\log p]",
            font_size=30,
        )
        metric_m.move_to(DOWN * 2.75)

        pullback = CurvedArrow(
            P.get_bottom() + DOWN * 0.25,
            M.get_bottom() + DOWN * 0.25,
            angle=-TAU / 5,
            color=YELLOW,
        )
        pullback_label = MathTex(r"f^\ast g_{\mathcal{P}}", font_size=30)
        pullback_label.next_to(pullback, DOWN, buff=0.15)

        self.play(Write(title))
        self.play(
            FadeIn(M),
            FadeIn(P),
            Write(M_label),
            Write(P_label),
            Write(M_sub),
            Write(P_sub),
        )
        self.play(FadeIn(theta), Write(theta_label))
        self.play(GrowArrow(map_arrow), Write(map_label))
        self.play(TransformFromCopy(theta, ptheta), Write(ptheta_label))
        self.play(GrowArrow(tangent), Write(tangent_label))
        self.play(
            GrowArrow(score), Write(score_label), GrowArrow(df_arrow), Write(df_label)
        )
        self.play(Write(metric_p))
        self.play(GrowArrow(pullback), Write(pullback_label))
        self.play(Write(metric_m))
        self.wait(2)
