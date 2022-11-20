import math
from dataclasses import dataclass
from typing import Callable, NamedTuple


@dataclass
class LimitationsFor2Numbers:
    """
    Limitations for an equation with two arguments
    """
    # Optimal "a" argument, which fits limitations
    optimal_a: int | float
    # Optimal "b" argument, which fits limitations
    optimal_b: int | float
    # Function to get if an argument pairs fits limitations
    numbers_fits_limitation: Callable[[float | int, float | int], bool]
    # Function to get a list of 2 possible a by putting b into an equation
    get_possible_a: Callable[[float | int], list[float | int, float | int]]
    # Function to get a list of 2 possible b by putting a into an equation
    get_possible_b: Callable[[float | int], list[float | int, float | int]]


class Solution(NamedTuple):
    """
    Solution of an equation
    """
    a: float | int  # Equation argument "a"
    b: float | int  # Equation argument "b"
    result: float | int  # Result of equation with arguments "a" and "b"


class NumbersPair(NamedTuple):
    """
    Pairs of equation arguments
    """
    a: float | int
    b: float | int


def get_all_solutions_for_side(equation: Callable[[float | int, float | int], float | int],
                               limitation: LimitationsFor2Numbers,
                               a: int | float,
                               b: int | float,
                               side_a: bool = True) -> list[Solution]:
    """
    Function to get a list of all solutions of an equation by a certain side.
    Each solution will be of an integer "a", integer "b" and integer "result".
    Warning: integer means a number, not a type
    :param equation: Equation to work with
    :param limitation: Limitations for the equation arguments
    :param a: Optimal a for the equation, which fits limitations
    :param b: Optimal b for the equation, which fits limitations
    :param side_a: If True, function will work with a side in a priority. Else b side in a priority
    :return: List of Solutions
    """
    if float(a).is_integer():
        a = int(a)
    if float(b).is_integer():
        b = int(b)

    a_in_priority = None
    solutions = []

    match a, b:
        case int(), int() if limitation.numbers_fits_limitation(a, b):
            solutions.append(Solution(
                a=a,
                b=b,
                result=equation(a, b)
            ))
        case int(), float() if side_a:
            a_in_priority = True
        case float(), int() if not side_a:
            a_in_priority = False
        case float(), _ if side_a:
            a_in_priority = False
        case _, float() if not side_a:
            a_in_priority = True

    if a_in_priority is None:
        return solutions
    elif a_in_priority:
        right_b_border = math.ceil(b)
        right_a1, right_a2 = limitation.get_possible_a(right_b_border)
        left_b_border = math.floor(b)
        left_a1, left_a2 = limitation.get_possible_a(left_b_border)

        number_pairs = [
            NumbersPair(a=right_a1, b=right_b_border),
            NumbersPair(a=right_a2, b=right_b_border),
            NumbersPair(a=left_a1, b=left_b_border),
            NumbersPair(a=left_a2, b=left_b_border)
        ]
    else:
        right_a_border = math.ceil(a)
        right_b1, right_b2 = limitation.get_possible_b(right_a_border)
        left_a_border = math.floor(a)
        left_b1, left_b2 = limitation.get_possible_b(left_a_border)

        number_pairs = [
            NumbersPair(a=right_a_border, b=right_b1),
            NumbersPair(a=right_a_border, b=right_b2),
            NumbersPair(a=left_a_border, b=left_b1),
            NumbersPair(a=left_a_border, b=left_b2)
        ]

    for number_a, number_b in number_pairs:
        if float(number_a if a_in_priority else number_b).is_integer():
            if limitation.numbers_fits_limitation(number_a, number_b):
                solutions.append(Solution(
                    a=number_a,
                    b=number_b,
                    result=equation(number_a, number_b)
                ))
            else:
                solutions += get_all_solutions(equation, limitation, number_a, number_b)
        else:
            solutions += get_all_solutions(equation, limitation, number_a,
                                           math.ceil(number_a if a_in_priority else number_b))
            solutions += get_all_solutions(equation, limitation, number_a,
                                           math.floor(number_a if a_in_priority else number_b))
    return solutions


def get_max_solution(solutions: list[Solution]):
    """
    Get max Solution object by result key
    :param solutions: A list to find max
    :return: Solution with a max result
    """
    return max(solutions, key=lambda solution: solution.result)


def get_all_solutions(equation: Callable[[float | int, float | int], float | int],
                      limitation: LimitationsFor2Numbers,
                      a: int | float,
                      b: int | float) -> list[Solution | None]:
    """
    Function to get a list of all solutions of an equation by each side.
    Each solution will be of an integer "a", integer "b" and integer "result".
    Warning: integer means a number, not a type
    :param equation: Equation to work with
    :param limitation: Limitations for the equation arguments
    :param a: Optimal a for the equation, which fits limitations
    :param b: Optimal b for the equation, which fits limitations
    :return: A list of all equation solutions
    """
    return [
        *get_all_solutions_for_side(equation, limitation, a, b, True),
        *get_all_solutions_for_side(equation, limitation, a, b, False)
    ]


def integer_division_for_an_equation_with_2_unknowns(
        equation: Callable[[float | int, float | int], float | int],
        limitations: LimitationsFor2Numbers) -> Solution:
    """
    Function to find a maximal integer solution with integer "a" and "b" arguments for a given equation
    Arguments pair will fit limitations
    :param equation: Equation to find an integer solution
    :param limitations: Limitations for the equation arguments
    :return: Maximal integer solution
    """
    all_solutions = get_all_solutions(equation, limitations, limitations.optimal_a, limitations.optimal_b)

    return get_max_solution(all_solutions)
