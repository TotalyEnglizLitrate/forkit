# TODO: Figure out how to inject the parsed theme into the css, maybe a harcoded tmp file in cache?


from re import compile
from types import SimpleNamespace

from toml import load

from forkit.misc import DefaultPaths, RuntimePaths


patterns: SimpleNamespace = SimpleNamespace(
    till_255=r"(?:[0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])",
    float_0_1=r"(?:0?\\.[0-9][0-9]*|1\\.0[0-9]*)",
    hex_digit=r"[0-9A-Fa-f]",
)
space = compile(r"\s*")

three_tpl_255 = (
    rf"{patterns.till_255}, " rf"{patterns.till_255}, " rf"{patterns.till_255}"
)


rgb = compile(rf"^rgb\({three_tpl_255}\)$")
rgba = compile(rf"^rgba\({three_tpl_255}, {patterns.float_0_1}\)$")
hex = compile(rf"^#(?:{patterns.hex_digit}{{6}}|" rf"{patterns.hex_digit}{{8}})$")
opacity = compile(rf"^{patterns.float_0_1}$")

colours = set()
opacities = set()

types = SimpleNamespace(
    colours=colours | set(x.replace("colour", "color") for x in colours),
    opacities=opacities,
)


class Theme:
    def __init__(self) -> None:
        # TODO: add file.exists() checks and log errors
        self.file = RuntimePaths.theme_file
        self.default_file = DefaultPaths.theme_file

        self.custom = load(self.file)
        self.theme_vals = []
        for k, v in self.custom:
            v = space.sub(v, "").replace(",", ", ")
            if res := self.is_valid(k, v) is not True:
                if res == k:
                    # TODO: Log invalid key and skip custom themeing
                    raise NotImplementedError
                elif res == v:
                    # TODO: Log invalid value and skip custom themeing
                    raise NotImplementedError
            else:
                self.theme_vals.append(f"${k}: {v};")

    @staticmethod
    def is_valid(key: str, value: str):
        if key in types.colours:
            if any(x.fullmatch(value) is not None for x in (rgb, rgba, hex)):
                return True
            else:
                return value
        elif key in opacities:
            if opacity.fullmatch(value) is not None:
                return True
            else:
                return value
        else:
            return key
