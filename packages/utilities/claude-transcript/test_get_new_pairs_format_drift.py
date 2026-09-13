#!/opt/homebrew/bin/python3
"""Regression guard for get_new_pairs() vs machine-envelope user text.

WHAT BROKE (2026-08-27): find_real_user rejected ANY user message whose
extracted text started with '<', intending to skip <command-name> echoes,
<local-command-caveat> wrappers and <system-reminder> injections. A real prompt
whose text is pasted markup — '<section ...><style>...</style> swap this badge'
plus an image block — was rejected too, so every assistant turn in that session
segment dead-ended its parent chain at it. Result: 18 text-bearing assistant
turns, 0 pairs even from offset 0 — the memory_sweep drift alarm.

SECOND BUG SAME FUNCTION: find_real_user recursed once per ancestor. Modern
chains run thousands deep through attachment stubs (2044 measured live), past
the interpreter limit — sweep_one raised RecursionError and the transcript was
skipped every run, never even reaching the alarm. The walk is iterative now.

FIXTURE: fixtures/format_drift_markup_prompt.jsonl mirrors the live shape —
attachment/system/mode/queue-operation chain nodes, user content as str and as
[{text|tool_result|image}] blocks, two real prompts that both start with '<',
and one '[Request interrupted by user]' leaf (kept OUT of every assistant's
ancestry on purpose: the old predicate ACCEPTS it — it doesn't start with '<' —
so reachable placement would give old-logic 1 pair and mask the regression).
All strings synthesized.

MUTATION-TESTED: _pairs_under_old_predicate below is a copy of the pre-fix
pairing (the literal startswith('<') rejection). It returns 0 on this fixture;
the fixed get_new_pairs returns 2. A test that passes without the fix is not
a test.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import claude_transcript as ct  # noqa: E402

get_new_pairs = ct.get_new_pairs
parse_line = ct.parse_line

FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'fixtures', 'format_drift_markup_prompt.jsonl')


def _pairs_under_old_predicate(filepath):
    """Copy of the pre-fix get_new_pairs pairing logic: same uuid_map +
    stub-node construction, same chain walk, but the OLD broken predicate —
    reject any user text starting with '<'. Deliberately not imported."""
    messages, uuid_map = [], {}
    with open(filepath) as f:
        for line in f:
            msg = parse_line(line)
            if msg:
                messages.append(msg)
                uuid_map[msg['uuid']] = msg
            else:
                stripped = line.strip()
                if stripped and '"uuid"' in stripped:
                    try:
                        obj = json.loads(stripped)
                    except json.JSONDecodeError:
                        continue
                    if obj and obj.get('uuid') and obj['uuid'] not in uuid_map:
                        uuid_map[obj['uuid']] = {
                            'type': obj.get('type', 'chain'), 'uuid': obj['uuid'],
                            'parent': obj.get('parentUuid'), 'content': '',
                            'raw_content': '', 'timestamp': '', 'is_meta': True,
                        }

    def find_real_user(uuid):
        seen = set()
        while uuid and uuid not in seen:
            seen.add(uuid)
            node = uuid_map.get(uuid)
            if not node:
                return None
            if (node['type'] == 'user' and node['content']
                    and not node['is_meta']
                    and not node['content'].startswith('<')):  # the old bug
                return node
            uuid = node.get('parent')
        return None

    pairs = {}
    for msg in messages:
        if msg['type'] == 'assistant' and msg['content']:
            user = find_real_user(msg['parent'])
            if user:
                pairs[user['uuid']] = (user, msg)
    return list(pairs.values())


class TestFormatDrift(unittest.TestCase):

    def test_fixture_falsifies_old_predicate(self):
        """Guard the guard: the pre-fix startswith('<') predicate must return
        ZERO pairs on this fixture, or the fixture no longer exercises the bug."""
        old = _pairs_under_old_predicate(FIXTURE)
        self.assertEqual(
            len(old), 0,
            'old predicate returned pairs — fixture lost its falsifying shape')

    def test_fixture_has_text_bearing_assistant_turns(self):
        """The alarm signature needs >= 3 assistant turns carrying text."""
        n = 0
        with open(FIXTURE) as f:
            for line in f:
                msg = parse_line(line)
                if msg and msg['type'] == 'assistant' and msg['content']:
                    n += 1
        self.assertGreaterEqual(n, 3)

    def test_pasted_markup_prompts_pair(self):
        """THE regression: real prompts whose text starts with '<' must pair."""
        pairs, _ = get_new_pairs(FIXTURE, 0)
        self.assertEqual(len(pairs), 2)
        users = {u['uuid'] for u, _ in pairs}
        self.assertEqual(users, {'usr-paste', 'usr-svg'})

    def test_pairs_carry_real_text_both_sides(self):
        pairs, _ = get_new_pairs(FIXTURE, 0)
        for user_msg, asst_msg in pairs:
            self.assertEqual(user_msg['type'], 'user')
            self.assertEqual(asst_msg['type'], 'assistant')
            self.assertTrue(user_msg['content'].strip())
            self.assertTrue(asst_msg['content'].strip())

    def test_noise_still_rejected(self):
        """Envelopes, meta, tool_results and interrupt notes are not prompts;
        the two pasted-markup prompts are."""
        expect_real = {
            'usr-paste': True, 'usr-svg': True,
            'usr-caveat': False, 'usr-cmd': False, 'usr-imgnote': False,
            'usr-tr1': False, 'usr-interrupt': False,
        }
        expect_machine_text = {
            'usr-caveat': True, 'usr-cmd': True, 'usr-interrupt': True,
            'usr-imgnote': False,  # '[Image: ...]' — rejected via isMeta, not text
            'usr-tr1': False,    # tool_result-only: '', never reaches text check
            'usr-paste': False, 'usr-svg': False,
        }
        machine_fn = getattr(ct, '_is_machine_user_text', None)
        self.assertIsNotNone(machine_fn, 'pre-fix module has no shared '
                                   'machine-envelope predicate')
        seen = set()
        with open(FIXTURE) as f:
            for line in f:
                msg = parse_line(line)
                if not msg or msg['type'] != 'user' or msg['uuid'] not in expect_real:
                    continue
                seen.add(msg['uuid'])
                self.assertEqual(
                    ct._is_real_user_message(msg), expect_real[msg['uuid']],
                    msg['uuid'])
                if msg['content']:
                    self.assertEqual(
                        machine_fn(msg['content']),
                        expect_machine_text[msg['uuid']], msg['uuid'])
        self.assertEqual(seen, set(expect_real))

    def test_tool_only_assistant_turn_never_pairs(self):
        """asst-0002 is tool_use-only — it must not anchor a pair nor break
        the chain for the text turn above it."""
        pairs, _ = get_new_pairs(FIXTURE, 0)
        self.assertNotIn('asst-0002', {a['uuid'] for _, a in pairs})


if __name__ == '__main__':
    unittest.main(verbosity=2)
