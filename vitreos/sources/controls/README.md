# Public control sources

The four membership functions in `membership.py` are extracted from the frozen AxisPL source supplied with the October 7 review packet. Their Python syntax trees match the corresponding canonical functions inspected on October 11. The Apache license notice is retained in `LICENSE.axispl.txt`. Changes are import isolation and formatting; model, NumPy and native key-loading dependencies are absent.

`diagnostics.py` extracts exact-window and multiplicity calculations from the retained trace observer. `experiments.py` retains the three frozen scientific calculations, using the included explicit fixture arrays instead of a private source-loader path. Formatting and imports were adapted for this public package. The key derivation is public and predetermined for all 4,096 trials; no native trace keys are tested.

`../../scripts/reproduce_controls.py` compares every returned field with the original frozen receipt, using exact values except a 1e-12 absolute/relative tolerance for floating arithmetic. It is a read-only calculation. The public fixtures, expected output and research assumptions are supplied together, so successful execution does not imply calibration, provider applicability or independent evidence.
