import pytest

from suggestedimages.constants import *
from suggestedimages.search import *


def test_GetColorClass():
    get_color_class = GetColorClass()

    assert get_color_class('a') == 'color-1'
    assert get_color_class('b') == 'color-2'
    assert get_color_class('b') == 'color-2'
    assert get_color_class('c') == 'color-3'


    get_color_class = GetColorClass()

    for id in range(0, 2*NUM_COLORS):
        get_color_class(id)

    assert get_color_class(2) == get_color_class(NUM_COLORS + 2)
