from manim import *


class TestScene(Scene):
    def construct(self):
        title = Text("Manim is working", font_size=48)
        equation = MathTex(
            r"F_{ij}(\theta)=\mathbb{E}_\theta[\partial_i\log p\,\partial_j\log p]"
        )
        equation.next_to(title, DOWN, buff=0.6)

        self.add(title, equation)
