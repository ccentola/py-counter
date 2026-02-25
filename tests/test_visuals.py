from app.visuals import (
    build_svg,
    build_unit,
    build_ten_stick,
    build_hundreds_block,
    build_thousands_label,
)


# UNIT TESTS: build_unit =======================================================
def test_build_unit_returns_single_rect():
    result = build_unit(0, 0)
    assert result.count("<rect") == 1


def test_build_unit_uses_correct_color():
    result = build_unit(0, 0)
    assert "#e803fc" in result


def test_build_unit_uses_correct_position():
    result = build_unit(10, 20)
    assert 'x="10"' in result
    assert 'y="20"' in result


# UNIT TESTS: build_ten_stick ==================================================
def test_build_ten_stick_returns_ten_rects():
    result = build_ten_stick(0)
    assert result.count("<rect") == 10


def test_build_ten_stick_uses_correct_color():
    result = build_ten_stick(0)
    assert "#e803fc" in result


def test_build_ten_stick_stacks_vertically():
    result = build_ten_stick(0)
    assert 'y="0"' in result
    assert 'y="22"' in result  # SQUARE_SIZE(20) + GAP(2)


# UNIT TESTS: build_hundreds_block =============================================
def test_build_hundreds_block_returns_hundred_rects():
    result = build_hundreds_block(0)
    assert result.count("<rect") == 100


def test_build_hundreds_block_uses_correct_color():
    result = build_hundreds_block(0)
    assert "#e803fc" in result


# UNIT TESTS: build_thousands_label ============================================
def test_build_thousands_label_returns_text_element():
    result = build_thousands_label(0, 1000)
    assert "<text" in result


def test_build_thousands_label_formats_number():
    result = build_thousands_label(0, 3000)
    assert "3,000" in result


def test_build_thousands_label_uses_correct_color():
    result = build_thousands_label(0, 1000)
    assert "#e803fc" in result


# UNIT TESTS: build_svg ========================================================
def test_returns_svg_string():
    result = build_svg(0)
    assert "<svg" in result


def test_zero_renders_no_shapes():
    result = build_svg(0)
    assert "<rect" not in result


def test_five_renders_five_unit_squares():
    result = build_svg(5)
    assert result.count("<rect") == 5


def test_ten_renders_one_ten_stick():
    result = build_svg(10)
    assert result.count("<rect") == 10


def test_twenty_three_renders_two_sticks_and_three_units():
    result = build_svg(23)
    assert result.count("<rect") == 23


def test_ninety_nine_renders_nine_sticks_and_nine_units():
    result = build_svg(99)
    assert result.count("<rect") == 99


def test_one_hundred_renders_one_hundreds_block():
    result = build_svg(100)
    assert result.count("<rect") == 100


def test_two_fifty_renders_two_hundreds_and_five_tens():
    result = build_svg(250)
    assert result.count("<rect") == 250


def test_nine_ninety_nine():
    result = build_svg(999)
    assert result.count("<rect") == 999


def test_hundreds_drops_leftover_units():
    result = build_svg(150)
    assert result.count("<rect") == 150


def test_one_thousand_renders_label():
    result = build_svg(1000)
    assert "1,000" in result


def test_thousands_label_shows_correct_value():
    result = build_svg(3000)
    assert "3,000" in result


def test_thousands_with_leftover_hundreds():
    result = build_svg(2300)
    assert "2,000" in result
    assert result.count("<rect") == 300


def test_thousands_drops_leftover_tens():
    result = build_svg(1250)
    assert "1,000" in result
    assert result.count("<rect") == 200


def test_nine_thousand_nine_hundred():
    result = build_svg(9900)
    assert "9,000" in result
    assert result.count("<rect") == 900
