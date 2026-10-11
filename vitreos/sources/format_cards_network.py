"""F05 categorical artifact exchanges and shared-input bonds; no new measurement."""


def draw_f05(env):
    from matplotlib.patches import FancyArrowPatch, Polygon
    from matplotlib.path import Path

    Plate = env['Plate']
    INK, SECOND, RULE, TEAL, BLUE, OCHRE, VIOLET, PAPER = (
        env[k] for k in ('INK', 'SECOND', 'RULE', 'TEAL', 'BLUE', 'OCHRE', 'VIOLET', 'PAPER')
    )
    p = Plate('F05', 'Shared inputs, different operations', 417)

    def artifact(x, y, w, h, text, color=INK):
        p.rect(x, y, w, h, fill=PAPER, edge=color)
        p.text(x + w / 2, y + 6, text, 9, color=color, ha='center')

    def event(x, y, color=TEAL):
        p.ax.add_patch(Polygon([(x, y-6), (x+6, y), (x, y+6), (x-6, y)],
                              closed=True, facecolor=color, edgecolor=color, linewidth=.9, zorder=5))

    def exchange(start, end, color=SECOND, reused=False, rad=0):
        edge = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=8,
                               connectionstyle=f'arc3,rad={rad}', linewidth=1.0,
                               linestyle=(0, (3, 2)) if reused else '-',
                               color=color, shrinkA=0, shrinkB=0, zorder=2)
        p.ax.add_patch(edge)

    def edge_label(x, y, text, color=SECOND, ha='center'):
        a = p.text(x, y, text, 9, color=color, ha=ha)
        a.set_bbox(dict(facecolor='white', edgecolor='none', pad=.6))
        a.set_zorder(6)

    # A categorical legend: shape and line pattern survive grayscale printing.
    p.rect(7, 42, 12, 8, fill=PAPER, edge=INK)
    p.text(24, 39, 'Artifact', 9)
    event(93, 46, SECOND)
    p.text(106, 39, 'Analysis event', 9)
    exchange((215, 46), (234, 46))
    p.text(240, 39, 'Exchange', 9)
    exchange((320, 46), (342, 46), TEAL, reused=True)
    p.text(349, 39, 'Reused input', 9)
    p.text(7, 60, 'One retained clean/marked pair; checks share the material below.', 9, color=SECOND)

    # Artifacts and operation vertices form a non-lane network. The dashed
    # fixture bond fans to all three operations; it is not a common bus.
    artifact(7, 88, 102, 30, 'Original keys', OCHRE)
    artifact(176, 83, 116, 38, 'Fixed IDs + profile\nONE PAIR · R18', TEAL)
    artifact(176, 149, 116, 42, 'Reported result rows\nKey-holder aggregates', INK)
    artifact(334, 246, 127, 36, 'Code + expected output\nSupplied with request', VIOLET)

    holder = (62, 171)
    review = (408, 171)
    observer = (234, 264)

    # Original keys go only to the key-holder event. No public-reader,
    # analytical-review or observer edge carries native membership labels.
    exchange((58, 118), (62, 164), OCHRE)
    edge_label(34, 137, 'keys', OCHRE)
    exchange((176, 104), (68, 167), TEAL, reused=True)
    edge_label(120, 118, 'IDs + profile', TEAL)
    exchange((292, 104), (402, 167), TEAL, reused=True)
    edge_label(351, 118, 'IDs + profile', TEAL)

    # Holder creates the aggregate artifact; the two other events consume it.
    exchange((69, 171), (176, 171))
    edge_label(123, 155, 'keyed totals')
    exchange((292, 171), (401, 171))
    edge_label(347, 155, 'reported totals')
    exchange((234, 191), (234, 257))
    edge_label(248, 209, 'reported\ncounts', ha='left')

    # The bowed bond is the same fixture/profile reused by the keyless event.
    # Its crossing with the aggregate-exchange edge is not a junction. A white
    # under-stroke makes the crossing visually explicit without extra vertices.
    curve = Path([(208, 121), (132, 129), (134, 220), (228, 258)],
                 [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    bridge = FancyArrowPatch(path=curve, arrowstyle='-', linewidth=3.5,
                             color='white', zorder=3)
    p.ax.add_patch(bridge)
    shared = FancyArrowPatch(path=curve, arrowstyle='-|>', linewidth=1.1,
                             linestyle=(0, (3, 2)), color=TEAL,
                             mutation_scale=8, zorder=4)
    p.ax.add_patch(shared)
    edge_label(153, 237, 'same IDs / profile', TEAL, ha='right')

    exchange((334, 265), (241, 264), VIOLET)
    edge_label(291, 248, 'supplied', VIOLET)

    event(*holder, TEAL)
    event(*review, BLUE)
    event(*observer, VIOLET)
    p.text(7, 185, 'Original-key holder', 9, bold=True, color=TEAL)
    p.text(7, 199, 'Only membership measure\n7 Oct, 23:26 UTC · R18', 9)
    p.text(316, 185, 'Analytical review', 9, bold=True, color=BLUE)
    p.text(316, 199, 'Recount + arithmetic\nR18 / R38', 9)
    p.text(234, 279, 'Keyless observer · R31', 9, bold=True, color=VIOLET, ha='center')
    p.text(234, 293, 'Counts / arithmetic only; no model or keys', 9, ha='center')
    p.text(234, 307, 'Execution peer-reported · 8 Oct return/review', 9, ha='center')

    # A disconnected component preserves older field activity without making
    # it an input to, or proof of, the October keyless observer result.
    p.line(7, 328, 461, 328, RULE)
    p.text(7, 338, 'Separate historical branch', 9, bold=True)
    p.text(7, 353, 'Field inference', 9)
    event(127, 358, SECOND)
    exchange((134, 358), (225, 358))
    edge_label(177, 343, 'rows')
    artifact(225, 337, 236, 40, 'Historical rows · R27 / R32\nClean exporter source unavailable', OCHRE)

    p.text(7, 391, 'Categorical links: no time scale, physics, weights or covariance.', 9, color=SECOND)
    p.text(7, 405, 'Shared inputs do not create independent scientific samples.', 9, color=SECOND)

    p.save(
        ['C06', 'C07', 'C19'], ['R18', 'R27', 'R31', 'R32', 'R38'],
        'Categorical artifact nodes, analysis-event vertices and labeled exchange/reuse edges',
        'Boxes are artifacts; diamonds are analysis events. Dashed bonds expose reuse of one '
        'pair; solid arrows label exchanges. Only the key holder measures membership. Observer code and expected '
        'output are supplied to the keyless observer, whose execution is peer-reported. The '
        'disconnected branch preserves earlier field work.',
        'Categorical geometry only: no time scale, amplitudes, tensor operation, edge weights or '
        'measured covariance. A line crossing is not an event. Shared inputs do not add independent '
        'samples or authenticate execution.',
        description='In the main component, four artifact nodes and three analysis-event vertices expose which materials '
        'are exchanged and reused. Dashed connections identify the shared fixed IDs/profile; '
        'solid arrows carry keys, measured aggregates or supplied observer code and expected output. A separate '
        'historical field component prevents the older inference evidence from being conflated '
        'with the October keyless observer.'
    )
    return p
