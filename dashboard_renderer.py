import json
from pathlib import Path
import markdown
import re

class DashboardRenderer:
    @staticmethod
    def render(architecture_json, roadmap_markdown, reflections_list, output_path):
        def clean_md(text):
            # Kod bloklarını temizle
            text = re.sub(r'```(?:markdown|json|html)?\s*', '', text).replace('```', '')
            # Gereksiz giriş cümlelerini temizle
            noise_patterns = [r"Here's a structured.*:", r"Here is the.*:", r"Based on your.*:"]
            for p in noise_patterns:
                text = re.sub(p, '', text, flags=re.IGNORECASE)
            return text.strip()

        try:
            arch_data = json.loads(clean_md(architecture_json))
        except:
            arch_data = {"tech_stack": {}, "database_schema": {}}

        roadmap_html = markdown.markdown(clean_md(roadmap_markdown))

        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {{ background-color: #f8f9fa; font-family: 'Inter', -apple-system, sans-serif; height: 100vh; overflow: hidden; padding: 25px; }}
        .wrapper {{ display: grid; grid-template-columns: 380px 1fr; grid-template-rows: auto 1fr; gap: 20px; height: calc(100vh - 50px); }}
        
        .header {{ grid-column: 1 / -1; background: #ffffff; border-bottom: 3px solid #4e73df; padding: 15px 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }}
        .header h4 {{ color: #4e73df; font-weight: 800; margin: 0; letter-spacing: -0.5px; }}
        
        .card-custom {{ background: white; border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.08); display: flex; flex-direction: column; overflow: hidden; }}
        .card-header-custom {{ background: #fdfdfd; padding: 15px 20px; font-weight: 700; border-bottom: 1px solid #edf2f7; font-size: 0.85rem; color: #2d3748; text-transform: uppercase; letter-spacing: 1px; }}
        .card-body-custom {{ padding: 20px; overflow-y: auto; flex: 1; scrollbar-width: thin; }}
        
        /* Tech & DB Styles */
        .tech-tag {{ background: #ebf4ff; color: #2b6cb0; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; margin: 3px; display: inline-block; font-weight: 600; border: 1px solid #bee3f8; }}
        h6 {{ font-size: 0.9rem; font-weight: 700; color: #4a5568; margin-top: 15px; margin-bottom: 10px; border-left: 3px solid #4e73df; padding-left: 10px; }}
        
        /* Roadmap Styles */
        .card-body-custom h1, .card-body-custom h2 {{ font-size: 1.2rem; color: #2d3748; margin-bottom: 15px; font-weight: 700; }}
        .card-body-custom h3 {{ font-size: 1rem; color: #4a5568; margin-top: 20px; }}
        .card-body-custom p, .card-body-custom li {{ font-size: 0.9rem; color: #4a5568; line-height: 1.6; }}
        
        .scroll-v::-webkit-scrollbar {{ width: 6px; }}
        .scroll-v::-webkit-scrollbar-thumb {{ background: #cbd5e0; border-radius: 10px; }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <h4>🚀 PRODUCT LAUNCH BLUEPRINT</h4>
            <div class="badge badge-success" style="padding: 6px 12px; border-radius: 20px;">STRATEGY READY</div>
        </div>

        <!-- Left Column: Tech Architecture -->
        <div class="card-custom">
            <div class="card-header-custom">🛠️ Technical Architecture</div>
            <div class="card-body-custom scroll-v">
                <h6>Main Tech Stack</h6>
                {DashboardRenderer._render_tech_stack(arch_data.get("tech_stack", {}))}
                
                <h6 class="mt-4">Database Design</h6>
                {DashboardRenderer._render_db_schema(arch_data.get("database_schema", {}))}
            </div>
        </div>

        <!-- Right Column: Roadmap -->
        <div class="card-custom">
            <div class="card-header-custom">📅 12-Week Go-To-Market Roadmap</div>
            <div class="card-body-custom scroll-v">
                <div class="roadmap-content">
                    {roadmap_html}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return str(output_path)

    @staticmethod
    def _render_tech_stack(tech_stack):
        html = ""
        if isinstance(tech_stack, dict):
            for cat, items in tech_stack.items():
                html += f"<div style='margin-bottom:12px;'><small style='color:#718096; font-weight:bold; text-transform:uppercase;'>{cat}</small><br>"
                if isinstance(items, list):
                    for i in items: html += f"<span class='tech-tag'>{i}</span>"
                else: html += f"<span class='tech-tag'>{items}</span>"
                html += "</div>"
        return html

    @staticmethod
    def _render_db_schema(schema):
        # Eğer ajan veri göndermediyse, SaaS için standart bir şema taslağı gösterelim
        if not isinstance(schema, dict) or not schema:
            schema = {
                "users": {"id": "UUID", "email": "VARCHAR", "plan": "ENUM"},
                "proposals": {"id": "UUID", "user_id": "FK", "content": "TEXT", "status": "STRING"},
                "templates": {"id": "INT", "name": "STRING", "structure": "JSONB"}
            }
        
        html = ""
        for table, cols in schema.items():
            html += f"<details style='margin-bottom:8px; background:#f7fafc; padding:8px; border-radius:6px; cursor:pointer; border:1px solid #edf2f7;'>"
            html += f"<summary style='font-size:0.8rem; font-weight:bold; color:#2d3748;'>Table: {table}</summary><ul style='padding-left:18px; margin-top:8px; margin-bottom:0;'>"
            for c, t in cols.items(): 
                html += f"<li style='font-size:0.75rem; color:#4a5568;'>{c}: <code style='color:#d53f8c;'>{t}</code></li>"
            html += "</ul></details>"
        return html