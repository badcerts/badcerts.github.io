"""C08: separated conceptual provenance planes; no physical or causal model."""


def draw_f06(env):
    """Render F06 using the shared builder's Plate, palette and metadata sink."""
    from matplotlib.patches import Polygon

    Plate = env['Plate']
    INK, SECOND, RULE, PAPER = (env[k] for k in ('INK', 'SECOND', 'RULE', 'PAPER'))
    TEAL, BLUE, VIOLET, OCHRE = (env[k] for k in ('TEAL', 'BLUE', 'VIOLET', 'OCHRE'))
    p = Plate('F06', 'Provenance layers and the claim boundary', 408)
    p.text(7, 41, 'At which layer was a property observed, absent or left untested?', 9, color=SECOND)

    # Corresponding vertices align across an exploded stack. No arrowheads:
    # these are assembly-style reading guides, not evidence-transfer edges.
    tops = [67 + 56 * i for i in range(5)]
    for x, offset in ((50, 0), (209, 0), (12, 38), (171, 38)):
        p.line(x, tops[0] + offset, x, tops[-1] + offset, RULE, .7, (0, (2, 3)))

    layers = [
        ('SOURCE BYTES', SECOND,
         'What bytes were retained?',
         'R05: audit output recovered;\noriginal 17 inputs unavailable.\nS-EARLY-AUDITS'),
        ('EXPORT / CONTAINER', BLUE,
         'Which export route?',
         'R12: inspected structures absent.\nR13: word-preserving exports ≠ new samples.\nS-COMPARATIVE / S-CONTRACTS'),
        ('TOKENIZER / PROFILE', VIOLET,
         'What defines the observation unit?',
         'R17/R18: four-token context + target;\nretained known-key scheme/profile.\nS-ENGINEERING / S-RESULTS'),
        ('VERIFIER / CHECK', TEAL,
         'Which operation was performed?',
         'R18: keyed hits; R31: keyless counts.\nExpected output supplied to observer.\nS-RESULTS / S-OBSERVER'),
        ('PERMITTED CLAIM', OCHRE,
         'What may be concluded?',
         'R18/R35: bounded scheme evidence;\nold specimen activation unresolved.\nS-RESULTS / S-HISTORY'),
    ]
    for y, (label, color, question, detail) in zip(tops, layers):
        vertices = [(50, y), (209, y), (171, y + 38), (12, y + 38)]
        p.ax.add_patch(Polygon(vertices, closed=True, facecolor=PAPER,
                               edgecolor=SECOND, linewidth=.7, zorder=2))
        p.line(12, y + 38, 171, y + 38, color, 1.2)
        p.text(110.5, y + 19, label, 9, color=INK, bold=True,
               ha='center', va='center')
        # A short open-ended leader links the plane to its record/source callout.
        p.line(209, y, 220, y, color, .8)
        p.text(226, y - 4, question, 9, bold=True, color=color)
        p.text(226, y + 10, detail, 9, color=SECOND)

    p.line(7, 350, 461, 350, OCHRE, 1.1)
    p.text(7, 360, 'CLAIM BOUNDARY', 9, bold=True, color=OCHRE)
    p.text(111, 360, 'No generic authorship, identity, ownership or truth claim.', 9)
    p.text(7, 382, 'Planes and dotted guides separate questions; depth and spacing encode\nno confidence, physical assembly order or universal causal pipeline.', 9, color=SECOND)
    p.save(
        ['C08'], ['R03', 'R05', 'R12', 'R13', 'R14', 'R17', 'R18', 'R31', 'R35'],
        'Conceptual provenance questions',
        'Five conceptual planes separate retained bytes, export/container, tokenizer/profile, verification and permitted claim. Source-linked callouts keep unavailable inputs, inspected absence and supplied expectations distinct. R14 separately treats model rewriting as a possible marking event.',
        'Planes and guides show conceptual layers, not confidence, physical assembly order or a universal causal pipeline. Export copies add no independent samples.',
        description='Five equal perspective planes are separated by visible gaps and aligned by '
        'dotted, non-directional guides. Each has a short leader to a provenance question and '
        'named research/source records. Source bytes: R05 audit output recovered, original 17 '
        'inputs unavailable. Export/container: R12 inspected metadata structures absent; '
        'R13 word-preserving exports do not add independent samples. Model rewriting is a '
        'separate case retained by R14. Tokenizer/profile: R17/R18 retained known-key '
        'scheme and four-token context plus target. Verifier/check: R18 keyed membership versus '
        'R31 keyless counts with expected output supplied. Permitted claim: R18/R35 bounded '
        'scheme evidence with old specimen activation unresolved.'
    )
