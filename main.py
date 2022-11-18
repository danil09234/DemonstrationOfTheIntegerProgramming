import math
from dataclasses import dataclass
from typing import Callable, NamedTuple


@dataclass
class LimitationsFor2Numbers:
    optimal_a: int | float
    optimal_b: int | float
    numbers_fits_limitation: Callable[[float | int, float | int], bool]
    get_possible_a: Callable[[float | int], list[float | int, float | int]]
    get_possible_b: Callable[[float | int], list[float | int, float | int]]


class Solution(NamedTuple):
    a: float | int
    b: float | int
    result: float | int


def get_all_solutions_for_b(equation: Callable[[float | int, float | int], float | int],
                            limitation: LimitationsFor2Numbers,
                            a: int | float,
                            b: int | float) -> list[Solution | None]:
    solutions = []

    if float(a).is_integer():
        a = int(a)

    if float(b).is_integer():
        b = int(b)

    match b:
        case int():
            if float(a).is_integer():
                if limitation.numbers_fits_limitation(a, b):
                    solutions.append(Solution(
                        a=a,
                        b=b,
                        result=equation(a, b)
                    ))
            else:
                right_a_border = math.ceil(a)
                right_b1, right_b2 = limitation.get_possible_b(right_a_border)
                left_a_border = math.floor(a)
                left_b1, left_b2 = limitation.get_possible_b(left_a_border)

                if float(right_b1).is_integer():
                    if limitation.numbers_fits_limitation(right_a_border, right_b1):
                        solutions.append(Solution(
                            a=right_a_border,
                            b=right_b1,
                            result=equation(right_a_border, right_b1)
                        ))
                    else:
                        branch_solutions = get_all_solutions_for_b(equation, limitation, right_a_border, right_b1)
                        for solution in branch_solutions:
                            solutions.append(solution)
                else:
                    branch_solutions = [
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.ceil(right_b1)),
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.floor(right_b1)),
                    ]
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(right_b2).is_integer():
                    if limitation.numbers_fits_limitation(right_a_border, right_b2):
                        solutions.append(Solution(
                            a=right_a_border,
                            b=right_b2,
                            result=equation(right_a_border, right_b2)
                        ))
                    else:
                        branch_solutions = get_all_solutions_for_b(equation, limitation, right_a_border, right_b2)
                        for solution in branch_solutions:
                            solutions.append(solution)
                else:
                    branch_solutions = [
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.ceil(right_b2)),
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.floor(right_b2)),
                    ]
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(left_b1).is_integer():
                    if limitation.numbers_fits_limitation(left_a_border, left_b1):
                        solutions.append(Solution(
                            a=left_a_border,
                            b=left_b1,
                            result=equation(left_a_border, left_b1)
                        ))
                    else:
                        branch_solutions = get_all_solutions_for_b(equation, limitation, left_a_border, left_b1)
                        for solution in branch_solutions:
                            solutions.append(solution)
                else:
                    branch_solutions = [
                        *get_all_solutions_for_b(equation, limitation, left_a_border, math.ceil(left_b1)),
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.floor(left_b1)),
                    ]
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(left_b2).is_integer():
                    if limitation.numbers_fits_limitation(left_a_border, left_b2):
                        solutions.append(Solution(
                            a=left_a_border,
                            b=left_b2,
                            result=equation(left_a_border, left_b2)
                        ))
                    else:
                        branch_solutions = get_all_solutions_for_b(equation, limitation, left_a_border, left_b2)
                        for solution in branch_solutions:
                            solutions.append(solution)
                else:
                    branch_solutions = [
                        *get_all_solutions_for_b(equation, limitation, left_a_border, math.ceil(left_b2)),
                        *get_all_solutions_for_b(equation, limitation, right_a_border, math.floor(left_b2)),
                    ]
                    for solution in branch_solutions:
                        solutions.append(solution)
        case float():
            right_b_border = math.ceil(b)
            right_a1, right_a2 = limitation.get_possible_a(right_b_border)
            left_b_border = math.floor(b)
            left_a1, left_a2 = limitation.get_possible_a(left_b_border)

            if float(right_a1).is_integer():
                if limitation.numbers_fits_limitation(right_a1, right_b_border):
                    solutions.append(Solution(
                        a=right_a1,
                        b=right_b_border,
                        result=equation(right_a1, right_b_border)
                    ))
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, right_b_border, math.ceil(right_a1)),
                    *get_all_solutions_for_a(equation, limitation, right_b_border, math.floor(right_a1)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(right_a2).is_integer():
                if limitation.numbers_fits_limitation(right_a2, right_b_border):
                    solutions.append(Solution(
                        a=right_a2,
                        b=right_b_border,
                        result=equation(right_a2, right_b_border)
                    ))
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, right_b_border, math.ceil(right_a1)),
                    *get_all_solutions_for_a(equation, limitation, right_b_border, math.floor(right_a1)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(left_a1).is_integer():
                if limitation.numbers_fits_limitation(left_a1, left_b_border):
                    solutions.append(Solution(
                        a=left_a1,
                        b=left_b_border,
                        result=equation(right_a1, left_b_border)
                    ))
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, left_b_border, math.ceil(left_a1)),
                    *get_all_solutions_for_a(equation, limitation, left_b_border, math.floor(left_a1)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(left_a2).is_integer():
                if limitation.numbers_fits_limitation(left_a2, left_b_border):
                    solutions.append(Solution(
                        a=left_a2,
                        b=left_b_border,
                        result=equation(left_a2, left_b_border)
                    ))
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, left_b_border, math.ceil(left_a2)),
                    *get_all_solutions_for_a(equation, limitation, left_b_border, math.floor(left_a2)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

    return solutions


def get_all_solutions_for_a(equation: Callable[[float | int, float | int], float | int],
                            limitation: LimitationsFor2Numbers,
                            a: int | float,
                            b: int | float) -> list[Solution | None]:
    solutions = []

    if float(a).is_integer():
        a = int(a)

    if float(b).is_integer():
        b = int(b)

    match a:
        case int():
            if float(b).is_integer():
                if limitation.numbers_fits_limitation(a, b):
                    solutions.append(Solution(
                        a=a,
                        b=b,
                        result=equation(a, b)
                    ))
            else:
                right_b_border = math.ceil(b)
                right_a1, right_a2 = limitation.get_possible_a(right_b_border)
                left_b_border = math.floor(b)
                left_a1, left_a2 = limitation.get_possible_a(left_b_border)

                if float(right_a1).is_integer():
                    if limitation.numbers_fits_limitation(right_a1, right_b_border):
                        solutions.append(Solution(
                            a=right_a1,
                            b=right_b_border,
                            result=equation(right_a1, right_b_border)
                        ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, right_a1, right_b_border)
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(right_a2).is_integer():
                    if limitation.numbers_fits_limitation(right_a2, right_b_border):
                        solutions.append(Solution(
                            a=right_a2,
                            b=right_b_border,
                            result=equation(right_a2, right_b_border)
                        ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, right_a2, right_b_border)
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(left_a1).is_integer():
                    if limitation.numbers_fits_limitation(left_a1, left_b_border):
                        solutions.append(Solution(
                            a=left_a1,
                            b=left_b_border,
                            result=equation(right_a1, left_b_border)
                        ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, left_a1, left_b_border)
                    for solution in branch_solutions:
                        solutions.append(solution)

                if float(left_a2).is_integer():
                    if limitation.numbers_fits_limitation(left_a2, left_b_border):
                        solutions.append(Solution(
                            a=left_a2,
                            b=left_b_border,
                            result=equation(left_a2, left_b_border)
                        ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, left_a2, left_b_border)
                    for solution in branch_solutions:
                        solutions.append(solution)
        case float():
            right_a_border = math.ceil(a)
            right_b1, right_b2 = limitation.get_possible_b(right_a_border)
            left_a_border = math.floor(a)
            left_b1, left_b2 = limitation.get_possible_b(left_a_border)

            if float(right_b1).is_integer():
                if limitation.numbers_fits_limitation(right_a_border, right_b1):
                    solutions.append(Solution(
                        a=right_a_border,
                        b=right_b1,
                        result=equation(right_a_border, right_b1)
                    ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, right_a_border, right_b1)
                    for solution in branch_solutions:
                        solutions.append(solution)
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, right_a_border, math.ceil(right_b1)),
                    *get_all_solutions_for_a(equation, limitation, right_a_border, math.floor(right_b1)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(right_b2).is_integer():
                if limitation.numbers_fits_limitation(right_a_border, right_b2):
                    solutions.append(Solution(
                        a=right_a_border,
                        b=right_b2,
                        result=equation(right_a_border, right_b2)
                    ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, right_a_border, right_b2)
                    for solution in branch_solutions:
                        solutions.append(solution)
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, right_a_border, math.ceil(right_b2)),
                    *get_all_solutions_for_a(equation, limitation, right_a_border, math.floor(right_b2)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(left_b1).is_integer():
                if limitation.numbers_fits_limitation(left_a_border, left_b1):
                    solutions.append(Solution(
                        a=left_a_border,
                        b=left_b1,
                        result=equation(left_a_border, left_b1)
                    ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, left_a_border, left_b1)
                    for solution in branch_solutions:
                        solutions.append(solution)
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, left_a_border, math.ceil(left_b1)),
                    *get_all_solutions_for_a(equation, limitation, left_a_border, math.floor(left_b1)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)

            if float(left_b2).is_integer():
                if limitation.numbers_fits_limitation(left_a_border, left_b2):
                    solutions.append(Solution(
                        a=left_a_border,
                        b=left_b2,
                        result=equation(left_a_border, left_b2)
                    ))
                else:
                    branch_solutions = get_all_solutions_for_a(equation, limitation, left_a_border, left_b2)
                    for solution in branch_solutions:
                        solutions.append(solution)
            else:
                branch_solutions = [
                    *get_all_solutions_for_a(equation, limitation, left_a_border, math.ceil(left_b2)),
                    *get_all_solutions_for_a(equation, limitation, left_a_border, math.floor(left_b2)),
                ]
                for solution in branch_solutions:
                    solutions.append(solution)
    return solutions


def get_max_solution(solutions: list[Solution]):
    return max(solutions, key=lambda solution: solution.result)


def get_all_solutions(equation: Callable[[float | int, float | int], float | int],
                      limitation: LimitationsFor2Numbers,
                      a: int | float,
                      b: int | float) -> list[Solution | None]:
    return [
        *get_all_solutions_for_a(equation, limitation, a, b),
        *get_all_solutions_for_b(equation, limitation, a, b)
    ]


def integer_division_for_an_equation_with_2_unknowns(
        equation: Callable[[float | int, float | int], float | int],
        limitations: LimitationsFor2Numbers) -> Solution:
    all_solutions = get_all_solutions(equation, limitations, limitations.optimal_a, limitations.optimal_b)

    return get_max_solution(all_solutions)
