#! /usr/bin/env python
import yaml
import jinja2


BMI_TEMPLATE = {}
BMI_TEMPLATE["python"] = """\"\"\"The Basic Model Interface for Python\"\"\"
from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class Bmi(ABC):
{% for func in funcs %}
    @abstractmethod
    def {{ func }}(self, ) -> {{ funcs[func].return }}:
        ...
{% endfor %}
"""

TYPE_STRING = {
    "cxx": "std::string",
    "python": "str",
}


def load_bmi(bmi_file="bmi.yaml"):
    with open(bmi_file, "r") as fp:
        bmi = yaml.safe_load(fp)
    return bmi


def render_bmi(bmi, language="python"):
    env = jinja2.Environment()
    template = env.from_string(BMI_TEMPLATE[language])

    funcs = {}
    for func_name in bmi.keys():
        if not func_name.startswith("_"):
            ret_val = bmi[func_name]["return"][language]
            funcs[func_name] = {"return": ret_val}

    return template.render(funcs=funcs)


if __name__ == "__main__":
    bmi = load_bmi("bmi.yaml")
    print(render_bmi(bmi, language="python"))
