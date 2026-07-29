#!/opt/homebrew/bin/python3
"""Regression guard for get_new_pairs() vs the ~2026-06-11 transcript format.

WHAT BROKE: Claude Code began interleaving non-message entries
(attachment / system / mode / ai-title / last-prompt / queue-operation) into the
parentUuid chain — ~93 per session. parse_line() returns None for those, so they
never entered uuid_map, and find_real_user() dead-ended at the first one. Result:
get_new_pairs() returned ZERO pairs on every modern transcript, silently, for
seven weeks. Nothing raised; the memory pipeline just stopped capturing.

WHY A FIXTURE AND NOT A LIVE TRANSCRIPT: a live-transcript assertion passes for
the wrong reason the moment the newest session happens to have a short chain.
fixtures/attachment_chain.jsonl is a real chain SHAPE — 30 consecutive lines of a
live transcript with type/uuid/parentUuid/isMeta preserved verbatim — and all text
synthesized, so it ships no conversation content and never changes underfoot.

The fixture was CHOSEN by measurement, not by eye: it is the first window found
that yields 0 pairs unpatched and >0 patched. An earlier hand-picked window
looked identical (same interleaved attachment types) yet passed unpatched — its
assistant's parent pointed straight at a real user, so it never exercised the
traversal. Sanitizing must therefore preserve the three properties find_real_user
branches on — raw content str vs list, isMeta, and a leading '<' — because
replacing an empty-text tool_result user with clean synthetic text silently
turned the fixture back into a non-reproducer.

MUTATION-TESTED: with the else-branch stub in get_new_pairs removed, both
assertions below fail (0 pairs). A test that still passes without the fix is not
a test.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_transcript import get_new_pairs

FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'fixtures', 'attachment_chain.jsonl')


class TestChainTraversal(unittest.TestCase):

    def test_fixture_has_interleaved_chain_nodes(self):
        """Guard the guard: if the fixture loses its non-message entries it
        stops exercising the bug and would pass unpatched."""
        import json
        with open(FIXTURE) as f:
            types = [json.loads(line)['type'] for line in f]
        self.assertIn('attachment', types)
        self.assertTrue(
            any(t not in ('user', 'assistant') for t in types),
            'fixture must interleave non-message entries in the parent chain')

    def test_fixture_still_forces_traversal(self):
        """The property that makes this fixture a falsifier: at least one user
        entry between the assistant and its real user contributes NO text
        (tool_result list content). Replace those with plain strings and the
        chain resolves without the fix — the test would pass unpatched."""
        import json
        with open(FIXTURE) as f:
            entries = [json.loads(line) for line in f]
        empty_users = [e for e in entries
                       if e['type'] == 'user'
                       and isinstance(e.get('message', {}).get('content'), list)]
        self.assertTrue(
            empty_users,
            'fixture no longer contains text-less user entries — it would pass '
            'without the chain-node fix and prove nothing')

    def test_pairs_survive_interleaved_chain_nodes(self):
        """THE regression: assistant messages whose parent chain passes through
        attachment/system/mode nodes must still resolve to their real user."""
        pairs, _ = get_new_pairs(FIXTURE, 0)
        self.assertTrue(
            pairs,
            'get_new_pairs returned 0 pairs — find_real_user is dead-ending on '
            'chain nodes again (the 2026-06-11 format regression)')

    def test_pairs_carry_real_text_both_sides(self):
        """A pair with an empty side would satisfy a naive non-empty assertion
        while still being useless to the memory pipeline."""
        pairs, _ = get_new_pairs(FIXTURE, 0)
        for user_msg, asst_msg in pairs:
            self.assertEqual(user_msg['type'], 'user')
            self.assertEqual(asst_msg['type'], 'assistant')
            self.assertTrue(user_msg['content'].strip())
            self.assertTrue(asst_msg['content'].strip())

    def test_offset_advances_to_end_of_file(self):
        """The stub branch must not disturb offset bookkeeping — a short offset
        would re-process bytes forever."""
        _, new_offset = get_new_pairs(FIXTURE, 0)
        self.assertEqual(new_offset, os.path.getsize(FIXTURE))


if __name__ == '__main__':
    unittest.main(verbosity=2)
