from os import chdir
from pathlib import Path
from sys import argv
from typing import Iterable

COLEMAK = {
    "p": ";",
    "t": "b",
    "x": "c",
    "c": "d",
    "k": "e",
    "e": "f",
    "m": "h",
    "l": "i",
    "y": "j",
    "n": "k",
    "u": "l",
    "h": "m",
    "j": "n",
    ";": "o",
    "r": "p",
    "s": "r",
    "d": "s",
    "f": "t",
    "i": "u",
    "z": "x",
    "o": "y",
    "b": "z",
}


def to_colemak(ch: str) -> str:
    if ch.isupper():
        return COLEMAK[ch.lower()].upper()
    else:
        return COLEMAK[ch]


REMAPPED = {}


def make_map(mode: str, lhs: str, rhs: str) -> str:
    if mode not in REMAPPED.keys():
        REMAPPED[mode] = []

    s = "    {}noremap {} {}\n".format(mode, lhs, rhs)
    if rhs not in REMAPPED[mode]:
        s += "    {}noremap {} <Nop>\n".format(mode, rhs)

    REMAPPED[mode].append(lhs)

    return s


def gen_mappings(mode: str, mapping, set: Iterable[str]) -> Iterable[str]:
    if type(mapping) == str:
        for k in set:
            yield make_map(
                mode, mapping.format(to_colemak(k)), mapping.format(k)
            )
    else:
        for k in set:
            lhs, rhs = mapping(to_colemak(k), k)
            yield make_map(mode, lhs, rhs)


def main():
    modes = {
        "": [
            lambda lhs, rhs: (lhs.upper(), rhs.upper()),
            "{}",
            "<C-{}>",
            "<C-W>{}",
            lambda lhs, rhs: ("<C-W>" + lhs.upper(), "<C-W>" + rhs.upper()),
            "<C-W><C-{}>",
            "[{}",
            "]{}",
            lambda lhs, rhs: ("g" + lhs.upper(), "g" + rhs.upper()),
            "g{}",
            lambda lhs, rhs: ("x" + lhs.upper(), "z" + rhs.upper()),
            lambda lhs, rhs: ("x" + lhs, "z" + rhs),
            ("<C-W>g{}", ["f", "F", "t", "T"]),
            ("<C-\\><C-{}>", ["n"]),
            ("[<C-{}>", ["D", "I"]),
            ("]<C-{}>", ["D", "I"]),
            ("[{}", ["D", "I", "P"]),
            ("]{}", ["D", "I", "P"]),
            ("g<C-{}>", ["h"]),
            # TODO: zuw, zug, zuW, zuG not tested
        ],
        "i": [
            ("<C-G>{}", ["j", "k", "u"]),
            ("<C-G><C-{}>", ["j", "k", "u"]),
            lambda lhs, rhs: (
                "<C-C><C-" + lhs + ">",
                "<C-X><C-" + rhs + ">",
            ),
            lambda lhs, rhs: (
                "<C-P><C-" + lhs + ">",
                "<C-R><C-" + rhs + ">",
            ),
            "<C-{}>",
            ("<C-\\><C-{}>", ["n"]),
        ],
        "c": ["<C-{}>", ("<C-\\><C-{}>", ["n"])],
        "v": [
            ("a{}", ["B", "b", "p", "s", "t"]),
            lambda lhs, rhs: ("u" + lhs, "i" + rhs),
        ],
        "o": [
            ("a{}", ["B", "b", "p", "s", "t"]),
            lambda lhs, rhs: ("u" + lhs, "i" + rhs),
        ],
        "t": [("<C-\\><C-{}>", ["n", "o"])],
    }

    outfile = Path("./autoload/colemak_dh.vim")
    outfile.parent.mkdir(exist_ok=True)

    contents = "function colemak_dh#setup()\n"

    for mode in modes:
        for mapping in modes[mode]:
            if type(mapping) == tuple:
                set = mapping[1]
                mapping = mapping[0]
            else:
                set = list(COLEMAK.keys())
            set.sort()
            contents += "".join(gen_mappings(mode, mapping, set))

    for ch in ["'", '"', "(", ")", "<", ">", "[", "]", "`", "{", "}"]:
        contents += make_map("v", "u" + ch, "i" + ch)
        contents += make_map("v", "u" + ch, "i" + ch)

    contents += """    inoremap <C-i> <C-i>
    cnoremap <C-i> <C-i>
    inoremap <C-m> <C-m>
    cnoremap <C-m> <C-m>
    nnoremap XX ZZ
    vnoremap <nowait> i l
    nnoremap <nowait> z b
    vnoremap <nowait> z b
    noremap <nowait> z b
endfunction
"""

    outfile.write_text(contents)


if __name__ == "__main__":
    chdir(Path(argv[0]).parent)
    main()
