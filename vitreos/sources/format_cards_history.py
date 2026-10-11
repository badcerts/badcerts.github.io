"""Categorical history lanes and explicit Toulmin geometry; no new measurements."""


def draw_f02(env):
    P = env['Plate']
    teal, blue, ochre, violet, second, rule = [env[k] for k in ('TEAL', 'BLUE', 'OCHRE', 'VIOLET', 'SECOND', 'RULE')]
    from matplotlib.patches import FancyArrowPatch

    p = P('F02', 'Hypothesis episodes and revisions', 420)
    p.text(7, 40, 'Reading order within each lane; positions are ordinal, never duration.', 9, color=second)
    styles = {
        'proposal': ('^', violet, False),
        'test': ('o', teal, True),
        'correction': ('D', blue, True),
        'open': ('o', violet, False),
        'excluded': ('x', ochre, True),
        'retained': ('s', second, True),
    }
    for x, name in [(12, 'proposal'), (94, 'test'), (153, 'correction'), (249, 'open'), (317, 'excluded'), (399, 'retained')]:
        marker, color, fill = styles[name]
        p.dot(x, 64, color, marker, fill)
        p.text(x + 8, 59, name.capitalize(), 9, color=second)

    def event(x, y, kind, label):
        marker, color, fill = styles[kind]
        p.dot(x, y, color, marker, fill)
        p.text(x, y + 10, label, 9, ha='center')

    def arc(x1, x2, y, label):
        # The curve relates claims within one history; it is not a time scale.
        p.ax.add_patch(FancyArrowPatch((x1, y - 4), (x2, y - 4),
                       connectionstyle='arc3,rad=-.30', arrowstyle='-|>',
                       mutation_scale=7, lw=.8, color=blue))
        p.text((x1 + x2) / 2, y - 39, label, 9, color=blue, ha='center')

    lanes = [
        ('Byte carriers\nR03 / R05', 119,
         [(148, 'test', 'Scanned classes\nreported absent'),
          (277, 'correction', 'Scope\ncorrected'),
          (408, 'open', 'Ordinary-space\nquestion open')]),
        ('Keyed excess\nR18', 198,
         [(155, 'retained', '39-75 hits:\nfeasible bound'),
          (290, 'test', 'Keyed count:\n60/93'),
          (421, 'retained', 'Bounded result;\nno calibration')]),
        ('Tokenizer\nR21 / R22', 247,
         [(146, 'proposal', 'Keyed coupling\nproposed'),
          (267, 'test', '24 relabelings:\nidentity-only null'),
          (411, 'open', 'Output-changing\ncoupling untested')]),
        ('Interaction\nfingerprint\nR23 / R38', 296,
         [(174, 'proposal', 'Mirroring\nproposed'),
          (305, 'correction', 'Shared-context\nconfound retained'),
          (425, 'open', 'Blind study\noptional')]),
        ('Field lineage\nR27 / R32', 345,
         [(151, 'retained', 'Historical rows\nretained'),
          (284, 'open', 'Clean source\nnot returned'),
          (416, 'excluded', 'Stronger claim\nexcluded')]),
    ]
    for label, y, events in lanes:
        p.text(7, y - 8, label, 9, bold=True)
        end = 447 if events[-1][1] == 'excluded' else events[-1][0] + 22
        p.line(events[0][0] - 9, y, end, y, rule)
        for x, kind, text in events:
            event(x, y, kind, text)
        if events[-1][1] == 'open':
            p.arrow(events[-1][0] + 7, y, 455, y, violet)
        elif events[-1][1] == 'excluded':
            p.line(447, y - 5, 447, y + 5, ochre, 1.2)
    arc(148, 277, 119, 'narrows claim')
    arc(277, 408, 119, 'retains alternative')
    arc(155, 290, 198, 'resolves bound')
    p.note(392, 'Markers name event types; arcs name corrections, not evidence strength.\nOpen endpoints are unresolved or optional, not assignments to run a study.')
    p.save(['C02', 'C12', 'C16'],
           ['R03', 'R05', 'R18', 'R21', 'R22', 'R23', 'R27', 'R32', 'R38'],
           'Five categorical hypothesis lanes; labeled events and within-history correction arcs',
           'Hypothesis lanes preserve proposals, tests, corrections and retained endpoints. Labeled arcs narrow the byte-scan claim while retaining ordinary-space alternatives, and connect the earlier 39-75 feasible bound to the measured 60/93 keyed count. Shapes identify event types; open and excluded endpoints remain distinct.',
           'Positions and lane lengths are ordinal layout only, not duration, credibility, probability or statistical survival. Arcs document interpretive relationships, not independent evidence. Open endpoints do not initiate experiments.')


def draw_f03(env):
    P = env['Plate']
    teal, blue, ochre, second, rule, paper = [env[k] for k in ('TEAL', 'BLUE', 'OCHRE', 'SECOND', 'RULE', 'PAPER')]
    from matplotlib.patches import FancyArrowPatch

    p = P('F03', 'Two arguments with visible limits', 422)

    def card(x, y, w, h, title, body, color, fill='white'):
        p.rect(x, y, w, h, fill=fill, edge=rule)
        p.line(x, y, x + w, y, color, 1.3)
        p.text(x + 6, y + 5, title, 9, color=color, bold=True)
        p.text(x + 6, y + 19, body, 9)

    def limited_link(x, y1, y2):
        p.ax.add_patch(FancyArrowPatch((x, y1), (x, y2),
                       arrowstyle='-|>', mutation_scale=7,
                       lw=.8, linestyle=':', color=ochre))

    arguments = [
        (44, 'R05  /  Negative byte audit',
         '17 files; scanned hidden,\nformat and whitespace\nclasses reported absent.',
         'Named unusual-byte features\nnot observed in the\nchecked copies.',
         'A specified-feature check\nconstrains that feature in\nthe inspected copy.',
         'Audit output recovered;\n17 original inputs\nunavailable.',
         'Ordinary separators / export\nmay evade the checks;\nno universal sensitivity.'),
        (226, 'R18  /  Positive keyed excess',
         'Primary key: 168/252 raw;\n60/93 distinct-window hits.',
         'Keyed excess remains after\nexact-repeat removal;\nno authorship verdict.',
         'Under retained construction,\ncompare hits with registered\ngamma = 0.25.',
         'Original-key local rescore;\none pair; public replay\nhas no secret keys.',
         'Repeat removal is not\nindependence; nominal z is\nnot a calibrated error rate.'),
    ]
    for top, title, data, claim, warrant, custody, rebuttal in arguments:
        p.text(7, top, title, 10, bold=True)
        y = top + 20
        card(7, y, 174, 60, 'DATA', data, blue, paper)
        card(287, y, 174, 60, 'BOUNDED CLAIM', claim, teal, paper)
        p.arrow(185, y + 29, 282, y + 29, second)
        p.text(234, y + 12, 'supports', 9, color=second, ha='center')
        lower = top + 96
        card(7, lower, 142, 64, 'QUALIFIER / CUSTODY', custody, ochre)
        card(160, lower, 147, 64, 'WARRANT', warrant, teal)
        card(318, lower, 143, 64, 'REBUTTAL / LIMIT', rebuttal, ochre)
        # Warrant supplies the inference edge, rather than another observation.
        p.arrow(234, lower - 3, 234, y + 32, teal)
        limited_link(78, lower - 3, y + 62)
        limited_link(389, lower - 3, y + 62)
    p.note(396, 'Solid arrows connect data, warrant and claim; dotted links constrain scope.\nGeometry encodes reasoning roles, not evidence strength or authentication.')
    p.save(['C03'], ['R05', 'R18', 'R20', 'R33'],
           'Two documented Toulmin arguments; data, warrant, bounded claim, qualifier and rebuttal',
           'Each argument connects data to a bounded claim horizontally. A separate warrant enters that inference from below; custody qualifications attach to the observation and rebuttals limit the claim. The negative byte audit and positive keyed excess therefore receive the same explicit inferential treatment. Neither warrants generic authorship attribution.',
           'Solid arrows express documented reasoning and dotted links its scope conditions, not proof of premises or source authentication. Spatial position and box area are categorical, with no numerical evidence-strength scale.')
