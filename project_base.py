"""
Minimal project metadata container.

Provides a small dataclass (ProjectDef) and a base class (ProjectBase) so
`main.py` can describe the project (name, scope, key contributions,
results) in a structured, self-contained way, without depending on any
external framework.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ProjectDef:
    key: str
    name: str
    desc: str
    student_id: str = ""
    scope: str = ""
    key_contributions: List[str] = field(default_factory=list)
    results: str = ""


class ProjectBase:
    @classmethod
    def define(cls) -> ProjectDef:
        raise NotImplementedError("Subclasses must implement define()")

    @classmethod
    def summary(cls) -> str:
        d = cls.define()
        lines = [
            f"# {d.name} ({d.key})",
            "",
            d.desc,
            "",
            "## Scope",
            d.scope,
            "",
            "## Key Contributions",
        ]
        lines += [f"- {c}" for c in d.key_contributions]
        lines += ["", "## Results", d.results]
        return "\n".join(lines)

    @classmethod
    def print_summary(cls):
        print(cls.summary())
