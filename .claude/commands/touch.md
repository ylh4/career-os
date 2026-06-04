---
description: Log an interaction with a contact and set the next suggested touch.
argument-hint: "<contact-slug-or-name>  [note]"
---

Log a networking interaction with the contact `$ARGUMENTS`.

1. Resolve the contact: find `contacts/<slug>.md` (match the slug or name). If none exists,
   create one with `# Name`, role/email fields, and an `## Interactions` section.
2. Append a dated entry to the contact's `## Interactions` log:
   `- <today> — <what happened / the note from $ARGUMENTS>`. Never rewrite past entries.
3. Set the **next suggested touch**: add/update a `**Next touch:** <date> — <reason>` line
   (a sensible cadence, e.g. ~3–4 weeks out unless the note implies sooner).
4. If this contact is tied to a pipeline opportunity, make sure that opportunity's
   `next_action` reflects any follow-up the interaction created.

PROVENANCE: log only what actually happened; don't invent commitments. Report the logged
interaction and the next suggested touch date.
