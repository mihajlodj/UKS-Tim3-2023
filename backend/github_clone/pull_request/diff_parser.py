from unidiff import PatchSet
from io import StringIO

def parse_diff(diff_text):
    print(diff_text)
    patch_set = PatchSet(StringIO(diff_text))
    diff = []
    overall_additions = 0
    overall_deletions = 0
    for patched_file in patch_set:
        file_path = patched_file.path
        overall_additions += patched_file.added
        overall_deletions += patched_file.removed
        diff.append({ 'file_path': file_path, 'content': _get_lines(patched_file), 'additions': patched_file.added, 'deletions': patched_file.removed, 'mode': _get_mode(patched_file) })
    return diff, overall_additions, overall_deletions


def _get_lines(patched_file):
    lines = []
    for hunk in patched_file:
        for line in hunk:
            lines.append(str(line))
    return lines


def _get_mode(patched_file):
    if patched_file.is_added_file:
        return 'add'
    elif patched_file.is_removed_file:
        return 'delete'
    return 'update'