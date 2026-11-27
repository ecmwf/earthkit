"""Generate the SVG dependency graphs used by the earthkit documentation.

Run it from the root of this repository::

    python docs/concepts/make_dependency_graphs.py

It rewrites the four graphs used by the "Dependencies between earthkit
components" page, in ``docs/concepts/images/``.

Only the standard library is used, and every node position is fixed, so no
Graphviz is needed and repeated runs write byte-identical files: there are no
timestamps, no random identifiers and nothing taken from the environment.

The data to edit is ``EDGE_DATA`` (which component depends on which, how
strongly, and where that comes from) and ``GRAPHS`` (which edge kinds each of
the four pictures shows).  The drawing is derived from it: nodes are boxes on
four layers, an edge is a cubic curve between the two boxes, and an edge label
is put at the first free spot of its curve.  Before anything is written the
layout of every graph is checked (see ``_check``): an edge may not cross a box
it is not attached to, labels may not overlap boxes, arrowheads, other labels
or other edges, and nothing may leave the canvas.  A check that fails prints
every problem and writes nothing, so an edit of the data below cannot quietly
produce an unreadable picture.

Arrow direction: ``A -> B`` means that A depends on B.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------------
# canvas, fonts, colours
# --------------------------------------------------------------------------------

WIDTH = 1040.0
HEIGHT = 790.0
MARGIN = 24.0

NODE_W = 172.0
NODE_H = 44.0

FONT_FAMILY = "Helvetica, Arial, sans-serif"
NODE_FS = 15.0
TITLE_FS = 19.0
CAPTION_FS = 13.5
LABEL_FS = 13.0
LEGEND_FS = 13.0

# average advance width of a glyph, as a fraction of the font size; used only
# to estimate the size of a text bounding box for the overlap checks
TEXT_FACTOR = 0.54

INK = "#1f2937"
FAINT = "#4b5563"
BOX_FILL = "#f8fafc"
BOX_STROKE = "#64748b"
PLATE_FILL = "#ffffff"

# padding used by the overlap checks
PAD_NODE = 6.0
PAD_LABEL = 5.0

SVG_NS = "http://www.w3.org/2000/svg"

# --------------------------------------------------------------------------------
# the components and their fixed positions (centre of the box)
#
# four layers: the applications on top, then earthkit-data, then earthkit-geo
# (data -> geo is a hard dependency, so data sits above geo) and earthkit-utils
# at the bottom, because almost everything depends on it.
# --------------------------------------------------------------------------------

COMPONENTS = ("data", "plots", "geo", "meteo", "transforms", "hydro", "utils")

# size of the box of every component.  earthkit-utils is drawn as a wide band:
# six of the seven components depend on it, and a band gives every one of them
# an anchor directly below its own box, so that those edges are straight lines.
SIZES: dict[str, tuple[float, float]] = {name: (NODE_W, NODE_H) for name in COMPONENTS}
SIZES["utils"] = (920.0, NODE_H)

# nodes whose anchors follow the x of the node at the other end of the edge
WIDE = {"utils"}
BAND_INSET = 40.0
BAND_PITCH = 26.0
# nodes whose anchors are spread along the side of their box
BOX_INSET = 22.0
# room kept free of spread anchors on each side of a vertical one
BOX_KEEP = 14.0

POSITIONS: dict[str, tuple[float, float]] = {
    "plots": (140.0, 112.0),
    "meteo": (380.0, 112.0),
    "transforms": (620.0, 112.0),
    "hydro": (860.0, 112.0),
    "data": (740.0, 320.0),
    "geo": (260.0, 480.0),
    "utils": (520.0, 610.0),
}

TITLE_OF = {name: f"earthkit-{name}" for name in COMPONENTS}

# --------------------------------------------------------------------------------
# the edge kinds and how they are drawn
# --------------------------------------------------------------------------------

KIND_ORDER = ("hard", "optional", "undeclared", "future")

KIND_STYLE: dict[str, dict[str, object]] = {
    "hard": {
        "stroke": "#3f3f46",
        "width": 1.9,
        "dash": "",
        "legend": "required dependency",
        "phrase": "required",
    },
    "optional": {
        "stroke": "#1d6fb8",
        "width": 1.9,
        "dash": "7 5",
        "legend": "optional dependency (extra in label)",
        "phrase": "optional",
    },
    "undeclared": {
        "stroke": "#d97706",
        "width": 2.3,
        "dash": "0.1 6.5",
        "cap": "round",
        "legend": "used but not declared",
        "phrase": "used but not declared",
    },
    "future": {
        "stroke": "#15803d",
        "width": 3.2,
        "dash": "",
        "legend": "planned dependency, not released",
        "phrase": "planned",
    },
}

KIND_HEAD: dict[str, tuple[float, float]] = {
    "hard": (11.0, 4.6),
    "optional": (11.0, 4.6),
    "undeclared": (10.5, 4.8),
    "future": (13.0, 5.8),
}

# --------------------------------------------------------------------------------
# the dependency data
#
# (source, target, kind, label, source of the information)
#
# Test, CI and documentation only extras are deliberately not listed: they are
# not dependencies of a user installed release.
# --------------------------------------------------------------------------------

EDGE_DATA: list[tuple[str, str, str, str, str]] = [
    # hard runtime dependencies, declared in the [project].dependencies list
    ("data", "geo", "hard", "", "earthkit-data pyproject.toml:25"),
    ("data", "utils", "hard", "", "earthkit-data pyproject.toml:26 (>=1.0.3)"),
    ("plots", "utils", "hard", "", "earthkit-plots pyproject.toml:25 (>=1.0.4,<2)"),
    ("plots", "data", "hard", "", "earthkit-plots pyproject.toml:26 (~=1.0)"),
    ("geo", "utils", "hard", "", "earthkit-geo pyproject.toml:22 (>=1.0.3)"),
    ("meteo", "utils", "hard", "", "earthkit-meteo pyproject.toml:26 (~=1.0)"),
    ("transforms", "utils", "hard", "", "earthkit-transforms pyproject.toml:26 (~=1.0)"),
    ("hydro", "utils", "hard", "", "earthkit-hydro pyproject.toml:27 (~=1.0)"),
    # optional dependencies: an extra pulls in the component
    ("plots", "geo", "optional", "regridding", "earthkit-plots pyproject.toml:49-50, extra 'regridding'"),
    ("meteo", "geo", "optional", "regimes", "earthkit-meteo pyproject.toml:65-66, extra 'regimes'"),
    ("transforms", "data", "optional", "all", "earthkit-transforms pyproject.toml:37-38, extra 'all'"),
    (
        "hydro",
        "data",
        "optional",
        "readers / all",
        "earthkit-hydro pyproject.toml:41-42 and 63-64, extras 'readers' and 'all'",
    ),
    # used by the library code but missing from the runtime dependencies
    (
        "meteo",
        "data",
        "undeclared",
        "",
        "earthkit-meteo src/earthkit/meteo/utils/fieldlist.py:14; only in the test extra",
    ),
    (
        "geo",
        "data",
        "undeclared",
        "",
        "earthkit-geo src/earthkit/geo/grids/_regrid/data/fieldlist/handler.py:25-31; only in test/ci extras",
    ),
    (
        "utils",
        "data",
        "undeclared",
        "",
        "earthkit-utils src/earthkit/utils/decorators/_dispatch.py:45-52; only in docs/test extras",
    ),
    (
        "data",
        "meteo",
        "undeclared",
        "",
        "earthkit-data src/earthkit/data/utils/meteo/registry.py:37-39; soft importlib use, with a fallback",
    ),
    # planned, not released yet
    (
        "transforms",
        "geo",
        "future",
        "future",
        "planned hard dependency of earthkit-transforms on earthkit-geo, not released",
    ),
]

# --------------------------------------------------------------------------------
# the four graphs: file name, edge kinds, title, caption, number of edges
# --------------------------------------------------------------------------------


@dataclass
class Graph:
    """One SVG file."""

    stem: str
    kinds: tuple[str, ...]
    title: str
    caption: str
    expected: int


GRAPHS = [
    Graph(
        "deps-hard",
        ("hard",),
        "Required dependencies between earthkit components",
        "Only the dependencies declared in the 'dependencies' list of the develop branch of a component.",
        8,
    ),
    Graph(
        "deps-optional",
        ("hard", "optional"),
        "Required and optional dependencies between earthkit components",
        "A dashed blue arrow is only followed when the extra named in its label is installed.",
        12,
    ),
    Graph(
        "deps-all",
        ("hard", "optional", "undeclared"),
        "All dependencies between earthkit components",
        "A dotted orange arrow is used by the code but missing from the runtime dependencies: it may "
        "only be pulled in by an optional, test or documentation extra.",
        16,
    ),
    Graph(
        "deps-future",
        KIND_ORDER,
        "Current and planned dependencies between earthkit components",
        "The thick green arrow is a dependency that is planned but not released yet.",
        17,
    ),
]

# a label is tried at these fractions of the curve, at these distances along the
# normal of the curve, on both sides; the first position that does not collide
# with anything wins (see _place_labels)
LABEL_TS = (0.5, 0.4, 0.6, 0.3, 0.7, 0.22, 0.78)
LABEL_D = (18.0, 32.0, 46.0)


@dataclass
class Edge:
    """A dependency between two components."""

    src: str
    dst: str
    kind: str
    label: str = ""
    note: str = ""


@dataclass
class Placed:
    """An edge with its geometry: a cubic curve, an arrowhead and a label."""

    edge: Edge
    cubic: tuple[tuple[float, float], ...] = ()
    curve: tuple[tuple[float, float], ...] = ()
    head: tuple[tuple[float, float], ...] = ()
    samples: list[tuple[float, float]] = field(default_factory=list)
    box: tuple[float, float, float, float] = ()
    label_pos: tuple[float, float] | None = None
    label_rect: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


# --------------------------------------------------------------------------------
# small geometry helpers
# --------------------------------------------------------------------------------


def _node_rect(name: str, pad: float = 0.0) -> tuple[float, float, float, float]:
    cx, cy = POSITIONS[name]
    width, height = SIZES[name]
    return (cx - width / 2 - pad, cy - height / 2 - pad, cx + width / 2 + pad, cy + height / 2 + pad)


def _intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float], pad: float = 0.0) -> bool:
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def _text_width(text: str, size: float) -> float:
    return len(text) * TEXT_FACTOR * size


def _label_rect(text: str, cx: float, cy: float, size: float) -> tuple[float, float, float, float]:
    """Bounding box of a text drawn with ``text-anchor: middle`` centred on (cx, cy)."""
    half_w = _text_width(text, size) / 2 + PAD_LABEL
    half_h = size / 2 + PAD_LABEL
    return (cx - half_w, cy - half_h, cx + half_w, cy + half_h)


def _lerp(p: tuple[float, float], q: tuple[float, float], t: float) -> tuple[float, float]:
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _bezier(pts: tuple[tuple[float, float], ...], t: float) -> tuple[float, float]:
    p0, p1, p2, p3 = pts
    u = 1.0 - t
    a = u * u * u
    b = 3 * u * u * t
    c = 3 * u * t * t
    d = t * t * t
    return (
        a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
        a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1],
    )


def _split(pts: tuple[tuple[float, float], ...], t: float) -> tuple:
    """De Casteljau: split a cubic at t and return both halves."""
    p0, p1, p2, p3 = pts
    q0 = _lerp(p0, p1, t)
    q1 = _lerp(p1, p2, t)
    q2 = _lerp(p2, p3, t)
    r0 = _lerp(q0, q1, t)
    r1 = _lerp(q1, q2, t)
    s = _lerp(r0, r1, t)
    return (p0, q0, r0, s), (s, r1, q2, p3)


# --------------------------------------------------------------------------------
# layout: anchors, curves, arrowheads and labels
# --------------------------------------------------------------------------------

SAMPLES = 200
CURVE_K = 0.55


def _band_anchors(node: str, entries: list[tuple[float, int, str]]) -> dict[int, float]:
    """The x of the anchors of a wide band, one per edge.

    A band is wide enough to give every edge the anchor directly above or below
    the node at the other end, so that the edge is a straight vertical line.
    Edges that share the x of their node, or that are pushed together by the
    edges of a neighbour, are spread by one pitch.
    """
    cx, _ = POSITIONS[node]
    width = SIZES[node][0]
    low, high = cx - width / 2 + BAND_INSET, cx + width / 2 - BAND_INSET
    groups: dict[float, list[int]] = {}
    for other_cx, i, _which in entries:
        groups.setdefault(min(max(other_cx, low), high), []).append(i)

    out: dict[int, float] = {}
    last: float | None = None
    for base in sorted(groups):
        indices = groups[base]
        for j, i in enumerate(indices):
            x = base + (j - (len(indices) - 1) / 2) * BAND_PITCH
            if last is not None and x < last + BAND_PITCH:
                x = last + BAND_PITCH
            out[i] = x
            last = x
    return out


def _spread(count: int, low: float, high: float) -> list[float]:
    if count <= 0:
        return []
    if count == 1:
        return [(low + high) / 2]
    return [low + (high - low) * j / (count - 1) for j in range(count)]


def _slot_xs(node: str, entries: list[tuple[float, int, str]], aligned: dict[int, float]) -> list[float]:
    """The x positions of the anchors collected on one side of a box, in order.

    The edges that end on a wide band keep the x of the band, so that they are
    vertical.  The remaining edges are spread on the free part of the side, on
    the left or on the right of the band edges, sorted by the x of the node at
    the other end, so that they neither overlap each other nor cross close to
    the box.
    """
    cx, _ = POSITIONS[node]
    half = SIZES[node][0] / 2 - BOX_INSET
    fixed = sorted({aligned[i] for _other_cx, i, _which in entries if i in aligned})
    if not fixed:
        return _spread(len(entries), cx - half, cx + half)
    if len(fixed) == len(entries):
        return [aligned[i] for _other_cx, i, _which in entries]

    middle = sum(fixed) / len(fixed)
    free = [e for e in entries if e[1] not in aligned]
    left = [e for e in free if e[0] < middle]
    right = [e for e in free if e[0] >= middle]

    xs: dict[tuple[int, str], float] = {}
    for e, x in zip(left, _spread(len(left), cx - half, max(cx - half, fixed[0] - BOX_KEEP)), strict=True):
        xs[(e[1], e[2])] = x
    for e, x in zip(right, _spread(len(right), min(cx + half, fixed[-1] + BOX_KEEP), cx + half), strict=True):
        xs[(e[1], e[2])] = x
    for _other_cx, i, which in entries:
        if i in aligned:
            xs[(i, which)] = aligned[i]
    return [xs[(i, which)] for _other_cx, i, which in entries]


def _anchors(edges: list[Edge]) -> dict[int, tuple[tuple[float, float], tuple[float, float], bool]]:
    """Work out where every edge leaves and enters its node box.

    The wide bands decide the x of their anchors first; the boxes follow them for
    those edges and spread the remaining ones along their side, sorted by the x
    of the node at the other end, so that edges neither overlap each other nor
    cross each other close to a box.
    """
    sides: dict[tuple[str, str], list[tuple[float, int, str]]] = defaultdict(list)
    down: dict[int, bool] = {}
    for i, e in enumerate(edges):
        is_down = POSITIONS[e.dst][1] > POSITIONS[e.src][1]
        down[i] = is_down
        src_side, dst_side = ("bottom", "top") if is_down else ("top", "bottom")
        for node, side, other, which in (
            (e.src, src_side, e.dst, "src"),
            (e.dst, dst_side, e.src, "dst"),
        ):
            sides[(node, side)].append((POSITIONS[other][0], i, which))
    for entries in sides.values():
        entries.sort()

    aligned: dict[int, float] = {}
    for (node, _side), entries in sides.items():
        if node in WIDE:
            aligned.update(_band_anchors(node, entries))

    out: dict[int, tuple[tuple[float, float], tuple[float, float], bool]] = {}
    for (node, side), entries in sorted(sides.items()):
        _, cy = POSITIONS[node]
        height = SIZES[node][1]
        y = cy + height / 2 if side == "bottom" else cy - height / 2
        for x, (_other_cx, i, which) in zip(_slot_xs(node, entries, aligned), entries, strict=True):
            end0, end1, _ = out.get(i, ((0.0, 0.0), (0.0, 0.0), down[i]))
            if which == "src":
                end0 = (x, y)
            else:
                end1 = (x, y)
            out[i] = (end0, end1, down[i])
    return out


def _place(edge: Edge, placed: tuple[tuple[float, float], tuple[float, float], bool]) -> Placed:
    """Build the curve and the arrowhead of one edge."""
    (x0, y0), (x1, y1), is_down = placed
    sign = 1.0 if is_down else -1.0
    k = CURVE_K * abs(y1 - y0)
    cubic = ((x0, y0), (x0, y0 + sign * k), (x1, y1 - sign * k), (x1, y1))

    head_len, head_w = KIND_HEAD[edge.kind]
    ts = [i / SAMPLES for i in range(SAMPLES + 1)]
    pts = [_bezier(cubic, t) for t in ts]
    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    # find the point of the curve that is head_len away from the end, so that
    # the line stops where the arrowhead starts
    run = 0.0
    cut = 0
    for i in range(1, len(pts)):
        run += math.dist(pts[i - 1], pts[i])
        if total - run <= head_len:
            cut = i - 1
            break
    t_cut = ts[cut] if cut > 0 else ts[1]
    prefix, suffix = _split(cubic, t_cut)
    tip = cubic[3]
    back = prefix[3]
    dirx, diry = suffix[1][0] - suffix[0][0], suffix[1][1] - suffix[0][1]
    norm = math.hypot(dirx, diry) or 1.0
    ux, uy = dirx / norm, diry / norm
    head = (tip, (back[0] - uy * head_w, back[1] + ux * head_w), (back[0] + uy * head_w, back[1] - ux * head_w))

    xs = [q[0] for q in pts] + [q[0] for q in head]
    ys = [q[1] for q in pts] + [q[1] for q in head]
    box = (min(xs), min(ys), max(xs), max(ys))
    return Placed(edge=edge, cubic=cubic, curve=prefix, head=head, samples=list(pts), box=box)


def _tangent(pts: tuple[tuple[float, float], ...], t: float) -> tuple[float, float]:
    p0, p1, p2, p3 = pts
    u = 1.0 - t
    return (
        3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
        3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]),
    )


def _head_box(p: Placed) -> tuple[float, float, float, float]:
    xs = [q[0] for q in p.head]
    ys = [q[1] for q in p.head]
    return (min(xs), min(ys), max(xs), max(ys))


def _label_candidates(p: Placed):
    """Positions to try for a label: along the curve, off the curve on both sides."""
    for t in LABEL_TS:
        x, y = _bezier(p.cubic, t)
        tx, ty = _tangent(p.cubic, t)
        norm = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / norm, tx / norm
        for d in LABEL_D:
            yield (x + nx * d, y + ny * d)
            yield (x - nx * d, y - ny * d)


def _label_free(rect: tuple[float, float, float, float], p: Placed, placed: list[Placed]) -> bool:
    """Check whether a label rectangle is free of boxes, arrowheads, other labels and other lines."""
    if rect[0] < MARGIN or rect[2] > WIDTH - MARGIN or rect[1] < MARGIN or rect[3] > HEIGHT - MARGIN:
        return False
    for node in COMPONENTS:
        if _intersects(rect, _node_rect(node), 2.0):
            return False
    for other in placed:
        if other.label_pos is not None and other is not p and _intersects(rect, other.label_rect, 3.0):
            return False
        if _intersects(rect, _head_box(other), PAD_LABEL):
            return False
        if other is not p and any(
            _intersects(rect, (q[0] - 1.0, q[1] - 1.0, q[0] + 1.0, q[1] + 1.0), 1.0) for q in other.samples
        ):
            return False
    return True


def _place_labels(placed: list[Placed]) -> None:
    """Give every labelled edge the first free position of its candidates."""
    for p in placed:
        if not p.edge.label:
            continue
        for cx, cy in _label_candidates(p):
            rect = _label_rect(p.edge.label, cx, cy, LABEL_FS)
            if _label_free(rect, p, placed):
                p.label_pos = (cx, cy)
                p.label_rect = rect
                break
        else:
            # nowhere free: keep the middle of the curve and let the checks report it
            cx, cy = _bezier(p.cubic, 0.5)
            p.label_pos = (cx, cy)
            p.label_rect = _label_rect(p.edge.label, cx, cy, LABEL_FS)


def _layout(edges: list[Edge]) -> list[Placed]:
    anchors = _anchors(edges)
    placed = [_place(e, anchors[i]) for i, e in enumerate(edges)]
    _place_labels(placed)
    return placed


# --------------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------------


def _check(name: str, edges: list[Edge], placed: list[Placed]) -> list[str]:
    """Return a list of layout problems; the graph is only written when it is empty."""
    problems: list[str] = []

    if len(edges) != next(g.expected for g in GRAPHS if g.stem == name):
        problems.append(f"{name}: {len(edges)} edges, expected {next(g.expected for g in GRAPHS if g.stem == name)}")

    for a in COMPONENTS:
        for b in COMPONENTS:
            if a < b and _intersects(_node_rect(a), _node_rect(b)):
                problems.append(f"{name}: node boxes {a} and {b} overlap")

    for p in placed:
        for node, (ax, ay) in ((p.edge.src, p.cubic[0]), (p.edge.dst, p.cubic[3])):
            left, _top, right, _bottom = _node_rect(node)
            if not left - 0.5 <= ax <= right + 0.5:
                problems.append(
                    f"{name}: the anchor of {TITLE_OF[p.edge.src]} -> {TITLE_OF[p.edge.dst]} is not on the box of "
                    f"{TITLE_OF[node]}",
                )

    for p in placed:
        for node in COMPONENTS:
            if node in (p.edge.src, p.edge.dst):
                continue
            left, top, right, bottom = _node_rect(node, PAD_NODE)
            if not _intersects(p.box, (left, top, right, bottom)):
                continue
            hits = [q for q in p.samples if left < q[0] < right and top < q[1] < bottom]
            if hits:
                problems.append(
                    f"{name}: edge {TITLE_OF[p.edge.src]} -> {TITLE_OF[p.edge.dst]} ({p.edge.kind}) crosses "
                    f"the box of {TITLE_OF[node]} at ({hits[0][0]:.0f}, {hits[0][1]:.0f})",
                )

    for p in placed:
        if p.label_pos is None:
            continue
        if not _label_free(p.label_rect, p, placed):
            problems.append(
                f"{name}: the label '{p.edge.label}' of {TITLE_OF[p.edge.src]} -> {TITLE_OF[p.edge.dst]} "
                f"has no free position",
            )

    for p in placed:
        for px, py in p.samples + list(p.head):
            if px < MARGIN or px > WIDTH - MARGIN or py < MARGIN or py > HEIGHT - MARGIN:
                problems.append(f"{name}: edge {p.edge.src} -> {p.edge.dst} leaves the canvas")
                break

    return problems


# --------------------------------------------------------------------------------
# svg writing
# --------------------------------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _f(value: float) -> str:
    return f"{value:.1f}"


def _n(value: float) -> str:
    text = f"{value:.1f}"
    return text[:-2] if text.endswith(".0") else text


def _curve_path(pts: tuple[tuple[float, float], ...]) -> str:
    p0, p1, p2, p3 = pts
    return f"M {_f(p0[0])} {_f(p0[1])} C {_f(p1[0])} {_f(p1[1])}, {_f(p2[0])} {_f(p2[1])}, {_f(p3[0])} {_f(p3[1])}"


def _polygon(pts: tuple[tuple[float, float], ...]) -> str:
    return " ".join(f"{_f(x)},{_f(y)}" for x, y in pts)


def _style_attrs(kind: str) -> str:
    """The inline drawing attributes of an edge of this kind.

    They are written on every element instead of in a ``<style>`` block: the
    converters used for the print and PDF formats of the documentation (and the
    internal renderer of ImageMagick) ignore css, and the colours are chosen for
    the white background that every graph draws.
    """
    style = KIND_STYLE[kind]
    attrs = [
        'fill="none"',
        f'stroke="{style["stroke"]}"',
        f'stroke-width="{style["width"]}"',
    ]
    if style.get("cap"):
        attrs.append(f'stroke-linecap="{style["cap"]}"')
    if style["dash"]:
        attrs.append(f'stroke-dasharray="{style["dash"]}"')
    return " ".join(attrs)


LEGEND_SAMPLE = 52.0
LEGEND_GAP = 9.0
LEGEND_PAD = 32.0
LEGEND_ROW_H = 26.0


def _legend_rows(kinds: list[str]) -> list[str]:
    """Lay the legend out in one or more rows and return the svg lines."""
    items = [(kind, str(KIND_STYLE[kind]["legend"])) for kind in kinds]
    widths = [LEGEND_SAMPLE + LEGEND_GAP + _text_width(text, LEGEND_FS) for _kind, text in items]

    rows: list[list[int]] = []
    row: list[int] = []
    x = MARGIN
    for i, width in enumerate(widths):
        if row and x + LEGEND_PAD + width > WIDTH - MARGIN:
            rows.append(row)
            row = []
            x = MARGIN
        row.append(i)
        x += LEGEND_PAD + width
    if row:
        rows.append(row)

    out: list[str] = []
    y = HEIGHT - 62.0 - LEGEND_ROW_H * (len(rows) - 1)
    for row in rows:
        x = MARGIN
        for i in row:
            kind, text = items[i]
            out.append(
                f'    <path d="M {_f(x)} {_f(y)} L {_f(x + LEGEND_SAMPLE)} {_f(y)}" {_style_attrs(kind)}/>',
            )
            head = (
                (x + LEGEND_SAMPLE, y),
                (x + LEGEND_SAMPLE - 8.0, y - 4.0),
                (x + LEGEND_SAMPLE - 8.0, y + 4.0),
            )
            out.append(f'    <polygon points="{_polygon(head)}" fill="{KIND_STYLE[kind]["stroke"]}"/>')
            out.append(
                f'    <text x="{_f(x + LEGEND_SAMPLE + LEGEND_GAP)}" y="{_f(y + LEGEND_FS * 0.36)}" '
                f'font-size="{_n(LEGEND_FS)}" fill="{FAINT}">{_esc(text)}</text>',
            )
            x += widths[i] + LEGEND_PAD
        y += LEGEND_ROW_H
    out.append(
        f'    <text x="{_f(WIDTH - MARGIN)}" y="{_f(HEIGHT - 28.0)}" text-anchor="end" '
        f'font-size="{_n(CAPTION_FS)}" fill="{FAINT}">arrow: A &#8594; B means A depends on B</text>',
    )
    return out


def _render(graph: Graph, edges: list[Edge], placed: list[Placed]) -> str:
    kinds = [kind for kind in KIND_ORDER if kind in graph.kinds]
    counts = {kind: sum(1 for e in edges if e.kind == kind) for kind in kinds}
    listing = ", ".join(f"{counts[kind]} {KIND_STYLE[kind]['phrase']}" for kind in kinds)
    desc = (
        f"Directed graph of the dependencies between the seven earthkit components. "
        f"Nodes: {', '.join(TITLE_OF[name] for name in COMPONENTS)}. "
        f"{len(edges)} arrows: {listing}. An arrow from A to B means that A depends on B."
    )

    out: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="{SVG_NS}" width="{_n(WIDTH)}" height="{_n(HEIGHT)}" '
            f'viewBox="0 0 {_n(WIDTH)} {_n(HEIGHT)}" role="img" '
            f'aria-labelledby="{graph.stem}-title {graph.stem}-desc">'
        ),
        f'  <title id="{graph.stem}-title">{_esc(graph.title)}</title>',
        f'  <desc id="{graph.stem}-desc">{_esc(desc)}</desc>',
        f'  <rect x="0" y="0" width="{_n(WIDTH)}" height="{_n(HEIGHT)}" fill="{PLATE_FILL}"/>',
        f'  <g font-family="{FONT_FAMILY}">',
        f'    <text x="{_n(MARGIN)}" y="{_n(MARGIN + TITLE_FS)}" font-size="{_n(TITLE_FS)}" '
        f'font-weight="600" fill="{INK}">{_esc(graph.title)}</text>',
    ]
    for i, line in enumerate(_wrap(graph.caption, 104)):
        out.append(
            f'    <text x="{_n(MARGIN)}" y="{_n(MARGIN + TITLE_FS + 21.0 + 17.0 * i)}" '
            f'font-size="{_n(CAPTION_FS)}" fill="{FAINT}">{_esc(line)}</text>',
        )

    out.append('    <g data-role="edges">')
    for p in placed:
        out.append(f'    <path d="{_curve_path(p.curve)}" {_style_attrs(p.edge.kind)}/>')
    for p in placed:
        out.append(f'    <polygon points="{_polygon(p.head)}" fill="{KIND_STYLE[p.edge.kind]["stroke"]}"/>')
    out.append("    </g>")

    out.append('    <g data-role="edge-labels">')
    for p in placed:
        if not p.label_pos:
            continue
        cx, cy = p.label_pos
        left, top, right, bottom = p.label_rect
        colour = str(KIND_STYLE[p.edge.kind]["stroke"])
        out.append(
            f'    <rect x="{_f(left)}" y="{_f(top)}" width="{_f(right - left)}" height="{_f(bottom - top)}" '
            f'rx="4" fill="{PLATE_FILL}" stroke="{colour}" stroke-opacity="0.35"/>',
        )
        out.append(
            f'    <text x="{_f(cx)}" y="{_f(cy + LABEL_FS * 0.36)}" text-anchor="middle" '
            f'font-size="{_n(LABEL_FS)}" fill="{colour}">{_esc(p.edge.label)}</text>',
        )
    out.append("    </g>")

    out.append('    <g data-role="nodes">')
    for name in COMPONENTS:
        left, top, right, bottom = _node_rect(name)
        width, height = SIZES[name]
        text = TITLE_OF[name]
        out.append(
            f'    <rect x="{_f(left)}" y="{_f(top)}" width="{_n(width)}" height="{_n(height)}" rx="8" '
            f'fill="{BOX_FILL}" stroke="{BOX_STROKE}" stroke-width="1.4"/>',
        )
        out.append(
            f'    <text x="{_f((left + right) / 2)}" y="{_f((top + bottom) / 2 + NODE_FS * 0.36)}" '
            f'text-anchor="middle" font-size="{_n(NODE_FS)}" font-weight="600" fill="{INK}">{_esc(text)}</text>',
        )
    out.append("    </g>")

    out.append('    <g data-role="legend">')
    out.extend(_legend_rows(kinds))
    out.append("    </g>")

    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line: list[str] = []
    for word in words:
        if line and len(" ".join(line)) + 1 + len(word) > width:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return lines


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------


def _selected(kinds: tuple[str, ...]) -> list[Edge]:
    return [Edge(src, dst, kind, label, note) for (src, dst, kind, label, note) in EDGE_DATA if kind in kinds]


def main() -> int:
    out_dir = Path(__file__).resolve().parent / "images"
    pages: list[tuple[Path, list[Edge], str]] = []
    problems: list[str] = []

    for graph in GRAPHS:
        edges = _selected(graph.kinds)
        placed = _layout(edges)
        problems += _check(graph.stem, edges, placed)
        pages.append((out_dir / f"{graph.stem}.svg", edges, _render(graph, edges, placed)))

    if problems:
        print("layout problems:")
        for line in problems:
            print(f"  - {line}")
        return 1

    for path, _edges, text in pages:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    root = Path(__file__).resolve().parents[2]
    print(f"wrote {len(pages)} graphs to {out_dir.relative_to(root)}")
    for graph, (_path, edges, _text) in zip(GRAPHS, pages, strict=True):
        counts = {kind: sum(1 for e in edges if e.kind == kind) for kind in KIND_ORDER}
        detail = ", ".join(f"{counts[kind]} {kind}" for kind in KIND_ORDER if counts[kind])
        assert len(edges) == graph.expected, (graph.stem, len(edges), graph.expected)
        print(f"  {graph.stem}.svg: {len(edges)} edges ({detail})")

    print("\nedge sources:")
    for src, dst, kind, label, note in EDGE_DATA:
        flag = f" [{label}]" if label else ""
        print(f"  {TITLE_OF[src]:<18} -> {TITLE_OF[dst]:<18} {kind:<10}{flag:<18} {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
