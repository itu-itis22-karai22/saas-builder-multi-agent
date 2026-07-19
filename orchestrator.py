from agent import *
from agent import get_clarifying_questions
from metrics import Metrics
import threading

from dashboard_renderer import DashboardRenderer
from pathlib import Path 

# 5️⃣ Critic Agent (Reflection) - 2 iterasyon
REFLECTION_ITERATIONS = 2
    
def run_system(idea):
    metrics = Metrics()

    # 1️⃣ Inverse Prompting
    intent = inverse_prompting_agent(idea, metrics)

    # 2️⃣ Planning
    plan = planning_agent(intent, metrics)

    # 3️⃣ Parallel Technical & Marketing
    tech = None
    marketing = None

    def tech_task():
        nonlocal tech
        tech = technical_agent(plan, metrics)

    def marketing_task():
        nonlocal marketing
        marketing = marketing_agent(plan, metrics)

    t1 = threading.Thread(target=tech_task)
    t2 = threading.Thread(target=marketing_task)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # 4️⃣ Consistency check
    aligned = consistency_agent(tech, marketing, metrics)


    for i in range(REFLECTION_ITERATIONS):
        critique = critic_agent(aligned, metrics)
        plan += f"\n# Feedback from Critic (Iteration {i+1}):\n" + critique
        metrics.print()

    return {
        "architecture": tech,
        "roadmap": marketing,
        "critique": critique,
        "plan_with_feedback": plan
    }
    
def generate_questions(user_idea):
    return get_clarifying_questions(user_idea)


def run_pipeline(user_idea, answers):

    metrics = Metrics()

    enriched_input = f"""
Business Idea:
{user_idea}

User Answers to Clarifying Questions:
{answers}
"""

    plan = planning_agent(enriched_input, metrics)

    tech = technical_agent(plan, metrics)
    marketing = marketing_agent(plan, metrics)


    consistency = consistency_agent(tech, marketing, metrics)


    reflection_outputs = []
    current_input = consistency

    for i in range(REFLECTION_ITERATIONS):
        critique = critic_agent(current_input, metrics)
        reflection_outputs.append(critique)
        current_input = critique

    

    # Metrics sözlüğünü burada oluşturuyoruz
    metrics_dict = {
        "LLM Calls": metrics.calls,
        "Tokens Used": metrics.tokens,
        "Total Latency (s)": round(sum(metrics.times), 2)
    }

    # 6️⃣ Render Dashboard (Metrikler kaldırıldı)
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    dashboard_path = output_dir / "saas_bundle_dashboard.html"

    DashboardRenderer.render(
        architecture_json=tech, 
        roadmap_markdown=marketing, 
        reflections_list=reflection_outputs,
        output_path=dashboard_path
    )


    return {
        "plan": plan,
        "architecture": tech,
        "roadmap": marketing,
        "reflections": reflection_outputs,
        "metrics": metrics,
        "metrics_dict": metrics_dict, # Bunu da ekleyelim ki Streamlit'e gitsin
        "dashboard_html_path": str(dashboard_path)
    }

