import pytest
import context
from HexPlant import HexPlant

def test_init_probs_rect():
    hex = HexPlant(3, 5)
    actual_probs = hex.init_probs()
    high_prob = 50
    low_prob= 1
    expected_probs = [
        [
            [high_prob, high_prob, 0, 0, 0, 0],
            [high_prob, high_prob, high_prob, low_prob, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [high_prob, high_prob, high_prob, 0, low_prob, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [high_prob, high_prob, 0, 0, 0, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [0, 0, 0, 0, 0, 0],
        ],
                [
            [high_prob, high_prob, high_prob, 0, low_prob, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    ]
    assert expected_probs == actual_probs

def test_init_probs_square():
    hex = HexPlant(4, 4)
    actual_probs = hex.init_probs()
    high_prob = 50
    low_prob= 1
    expected_probs = [
        [
            [high_prob, high_prob, 0, 0, 0, 0],
            [high_prob, high_prob, high_prob, low_prob, 0, 0],
            [high_prob, high_prob, high_prob, low_prob, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [high_prob, high_prob, high_prob, 0, low_prob, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [high_prob, high_prob, 0, 0, 0, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [high_prob, high_prob, high_prob, low_prob, low_prob, low_prob],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    ]
    assert expected_probs == actual_probs
