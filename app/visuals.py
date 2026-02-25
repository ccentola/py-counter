SQUARE_SIZE = 20
GAP = 2
STICK_GAP = 8
GROUP_GAP = 16
COLOR = "#e803fc"
SVG_HEIGHT = 10 * (SQUARE_SIZE + GAP)


def build_unit(x: int, y: int) -> str:
    return f'<rect x="{x}" y="{y}" width="{SQUARE_SIZE}" height="{SQUARE_SIZE}" fill="{COLOR}"/>'


def build_ten_stick(x: int) -> str:
    rects = []
    for i in range(10):
        y = i * (SQUARE_SIZE + GAP)
        rects.append(build_unit(x, y))
    return "".join(rects)


def build_hundreds_block(x: int) -> str:
    sticks = []
    for i in range(10):
        sticks.append(build_ten_stick(x + i * (SQUARE_SIZE + GAP)))
    return "".join(sticks)


def build_thousands_label(x: int, value: int) -> str:
    thousands = (value // 1000) * 1000
    formatted = f"{thousands:,}"
    return f'<text x="{x}" y="{SVG_HEIGHT // 2}" font-size="48" fill="{COLOR}" dominant-baseline="middle">{formatted}</text>'


def build_svg(value: int) -> str:
    parts = []
    x = 0

    if value < 100:
        tens = value // 10
        units = value % 10
        for i in range(tens):
            parts.append(build_ten_stick(x))
            x += SQUARE_SIZE + STICK_GAP
        if tens > 0 and units > 0:
            x += GROUP_GAP - STICK_GAP
        for i in range(units):
            parts.append(build_unit(x, 0))
            x += SQUARE_SIZE + GAP

    elif value < 1000:
        hundreds = value // 100
        tens = (value % 100) // 10
        units = value % 10
        for i in range(hundreds):
            parts.append(build_hundreds_block(x))
            x += 10 * (SQUARE_SIZE + GAP) + STICK_GAP
        if hundreds > 0 and tens > 0:
            x += GROUP_GAP - STICK_GAP
        for i in range(tens):
            parts.append(build_ten_stick(x))
            x += SQUARE_SIZE + STICK_GAP
        if (hundreds > 0 or tens > 0) and units > 0:
            x += GROUP_GAP - STICK_GAP
        for i in range(units):
            parts.append(build_unit(x, 0))
            x += SQUARE_SIZE + GAP

    else:
        hundreds = (value % 1000) // 100
        parts.append(build_thousands_label(x, value))
        x += 120 + GROUP_GAP
        for i in range(hundreds):
            parts.append(build_hundreds_block(x))
            x += 10 * (SQUARE_SIZE + GAP) + STICK_GAP

    width = max(x, 1)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{SVG_HEIGHT}">{"".join(parts)}</svg>'
