from helpers import *
from ..basic_codes import *


def basic_examples_simple_codes(backend):
    bit_flip_examples(backend)


def bit_flip_examples(backend):
    errors = [("x", 0)]
    perform_experiment(backend, bit_flip_code(errors, True), "errors/bit_flip0")

    errors = [("x", 1)]
    perform_experiment(backend, bit_flip_code(errors, True), "errors/bit_flip1")

    errors = [("x", 1), ("x", 0)]
    perform_experiment(backend, bit_flip_code(errors, True), "errors/bit_flip_0_1")

    errors = [("z", 1)]
    perform_experiment(backend, bit_flip_code(errors, True), "errors/phase_flip")

    errors = [("y", 2)]
    perform_experiment(backend, bit_flip_code(errors, True), "errors/bit_phase_flip")