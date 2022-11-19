from unittest import TestCase
from typing import Callable, NamedTuple

from main import LimitationsFor2Numbers, integer_division_for_an_equation_with_2_unknowns, Solution


class TestTask(NamedTuple):
    equation: Callable[[float | int, float | int], float | int]
    limitations: LimitationsFor2Numbers
    expected_result: Solution


EXAMPLE_TASKS = [
    TestTask(
        equation=lambda a, b: 5 * a + 4 * b,
        limitations=LimitationsFor2Numbers(
            optimal_a=3.75,
            optimal_b=1.25,
            numbers_fits_limitation=lambda a, b: (10 * a + 6 * b <= 45) and (a + b <= 5),
            get_possible_a=lambda b: [(45 - 6 * b) / 10, 5 - b],
            get_possible_b=lambda a: [(45 - 10 * a) / 6, 5 - a]
        ),
        expected_result=Solution(a=3, b=2, result=23)
    ),
    TestTask(
        equation=lambda a, b: 2 * a + 4 * b,
        limitations=LimitationsFor2Numbers(
            optimal_a=(9 / 5),
            optimal_b=(41 / 15),
            numbers_fits_limitation=lambda a, b: (2 * a + b <= (19 / 3)) and (a + 3 * b <= 10),
            get_possible_a=lambda b: [10 - 3 * b, ((19 / 3) - b) / 2],
            get_possible_b=lambda a: [(19 / 3) / (2 * a), (10 - a) / 3]
        ),
        expected_result=Solution(a=1, b=3, result=14)
    ),
    TestTask(
        equation=lambda a, b: 3 * a + b,
        limitations=LimitationsFor2Numbers(
            optimal_a=6,
            optimal_b=(1 / 5),
            numbers_fits_limitation=lambda a, b: (2 * a + 5 * b <= 13) and (a <= 6),
            get_possible_a=lambda b: [(13 - 5 * b) / 2, (13 - 5 * b) / 2],
            get_possible_b=lambda a: [(13 - 2 * a) / 5, 6]
        ),
        expected_result=Solution(a=6, b=0, result=18)
    ),
    TestTask(
        equation=lambda a, b: 3 * a + b,
        limitations=LimitationsFor2Numbers(
            optimal_a=(9/4),
            optimal_b=(1/2),
            numbers_fits_limitation=lambda a, b: (2 * a + 3 * b <= 6) and (2 * a - 3 * b <= 3),
            get_possible_a=lambda b: [(6 - 3 * b) / 2, (3 + 3 * b) / 2],
            get_possible_b=lambda a: [(6 - 2 * a) / 3, (3 - 2 * a) / (-3)]
        ),
        expected_result=Solution(a=1, b=1, result=4)
    ),
    TestTask(
        equation=lambda a, b: a + 2 * b,
        limitations=LimitationsFor2Numbers(
            optimal_a=(7/22),
            optimal_b=(61/22),
            numbers_fits_limitation=lambda a, b: (5 * a + 7 * b <= 21) and ((-a) + 3 * b <= 8),
            get_possible_a=lambda b: [(21 - 7 * b) / 5, (-8) + 3 * b],
            get_possible_b=lambda a: [(21 - 5 * a) / 7, (8 + a) / 3]
        ),
        expected_result=Solution(a=1, b=2, result=5)
    )
]


class TestIntegerDivisionMethod(TestCase):
    def example(self, task: TestTask):
        result = integer_division_for_an_equation_with_2_unknowns(
            equation=task.equation,
            limitations=task.limitations
        )

        self.assertEqual(task.expected_result, result)

    def test_example_1(self):
        self.example(EXAMPLE_TASKS[0])

    def test_example_2(self):
        self.example(EXAMPLE_TASKS[1])

    def test_example_3(self):
        self.example(EXAMPLE_TASKS[2])

    def test_example_4(self):
        self.example(EXAMPLE_TASKS[3])

    def test_example_5(self):
        self.example(EXAMPLE_TASKS[4])
