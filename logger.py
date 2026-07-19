"""
Lightweight, self-contained call logger.

Tracks the sequence of agent calls made during a pipeline run and can
render that sequence as a simple flow-diagram SVG (start -> agent_1 ->
agent_2 -> ... -> end). This is a minimal, dependency-free replacement
for the run-graph logging used during this project's development, so the
repository can be run standalone without any external framework.
"""

import time
import webbrowser
from pathlib import Path


class Logger:
    def __init__(self):
        self.events = []  # [{"name": str, "time": "HH:MM:SS"}, ...]

    def log_agent(self, name, prompt=None):
        """Record that an agent was called."""
        self.events.append({
            "name": name,
            "time": time.strftime("%H:%M:%S"),
        })

    def print_summary(self, compact=False):
        """Print a short summary of all agent calls made so far."""
        print("----- Agent Call Summary -----")
        if not self.events:
            print("(no agent calls recorded)")
            return
        for i, e in enumerate(self.events, start=1):
            if compact:
                print(f"{i}. {e['name']} [{e['time']}]")
            else:
                print(f"{i}. Agent '{e['name']}' called at {e['time']}")

    def render_graph(self, output_path, open_browser=False):
        """
        Render the recorded agent call sequence as a simple vertical
        flow-diagram SVG and save it to '<output_path>.svg'.
        """
        output_path = Path(output_path)
        svg_path = output_path.with_suffix(".svg")

        node_w, node_h = 160, 40
        v_gap = 60
        margin_top = 40
        width = 260

        n = len(self.events)
        height = margin_top * 2 + node_h + n * (node_h + v_gap) + node_h

        def node_y(i):
            return margin_top + node_h + i * (node_h + v_gap)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
        ]

        cx = width / 2

        # start node
        start_y = margin_top
        svg_parts.append(
            f'<circle cx="{cx}" cy="{start_y}" r="14" fill="#2c3e50"/>'
            f'<text x="{cx}" y="{start_y+4}" text-anchor="middle" '
            f'font-size="9" fill="white" font-family="sans-serif">In</text>'
        )

        prev_y = start_y
        for i, e in enumerate(self.events):
            y = node_y(i)
            box_x = cx - node_w / 2
            svg_parts.append(
                f'<rect x="{box_x}" y="{y - node_h/2}" width="{node_w}" '
                f'height="{node_h}" rx="8" fill="white" stroke="#888"/>'
                f'<text x="{cx}" y="{y+4}" text-anchor="middle" font-size="11" '
                f'font-weight="bold" font-family="sans-serif">{e["name"]}</text>'
            )
            svg_parts.append(
                f'<line x1="{cx}" y1="{prev_y + (14 if i == 0 else node_h/2)}" '
                f'x2="{cx}" y2="{y - node_h/2}" stroke="#888" stroke-width="1.5" '
                f'marker-end="url(#arrow)"/>'
                f'<text x="{cx+8}" y="{(prev_y+y)/2}" font-size="8" '
                f'fill="#555" font-family="sans-serif">[{e["time"]}]</text>'
            )
            prev_y = y

        end_y = prev_y + node_h / 2 + v_gap / 2 + 14
        svg_parts.append(
            f'<line x1="{cx}" y1="{prev_y + node_h/2}" x2="{cx}" y2="{end_y-14}" '
            f'stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>'
        )
        svg_parts.append(
            f'<circle cx="{cx}" cy="{end_y}" r="14" fill="#2c3e50"/>'
            f'<text x="{cx}" y="{end_y+4}" text-anchor="middle" '
            f'font-size="9" fill="white" font-family="sans-serif">Out</text>'
        )

        svg_parts.insert(1, (
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
            'refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" '
            'fill="#888"/></marker></defs>'
        ))
        svg_parts.append("</svg>")

        svg_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text("\n".join(svg_parts), encoding="utf-8")

        if open_browser:
            webbrowser.open(svg_path.resolve().as_uri())

        return str(svg_path)
