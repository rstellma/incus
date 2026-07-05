#!/usr/bin/env python3

"""
Was diff.py eigentlich tun würde
Es vergleicht zwei Welten:

Incus Live State   ↔   YAML Spec

Also konkret:

Welche Instances existieren im System, aber nicht im Spec?
Welche sind im Spec, aber nicht im System?
Welche Configs unterscheiden sich?
Welche Profile fehlen / sind zusätzlich?

Beispiel-Ausgabe (konzeptionell)
INSTANCE desktop:
  - profile mismatch: 10-Env_Desktop missing
  - extra profile: debug

INSTANCE yt-dlp:
  - OK

MISSING IN INCUS:
  - dev-container

MISSING IN SPEC:
  - temp-test

==> für den Moment zurückgestellt, bis das System soweit "erwachsen" ist, dass man sich über neue/mehr Features Gedanken machen kann.
"""
