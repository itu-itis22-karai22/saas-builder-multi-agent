from pathlib import Path
from llm import call_llm
from metrics import Metrics
from logger import Logger

logger = Logger()

# --------------------------
# Agent Fonksiyonları
# --------------------------

def inverse_prompting_agent(idea, metrics):
    prompt = f"""
User business idea:
{idea}

Ask clarifying questions to narrow the SaaS niche,
target users and monetization model.
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("InversePromptingAgent", prompt)
    return text


def planning_agent(intent, metrics):
    prompt = f"""
Create a workflow plan for building a SaaS product from this idea:

{intent}

Output a structured plan.
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("PlanningAgent", prompt)
    return text


def technical_agent(plan, metrics):
    prompt = f"""
Generate a SaaS technical architecture.

Return JSON including:
- services
- database schema
- tech stack

Plan:
{plan}
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("TechnicalAgent", prompt)
    return text


def marketing_agent(plan, metrics):
    prompt = f"""
Generate a 12 week go-to-market strategy.

Plan:
{plan}

Output markdown roadmap.
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("MarketingAgent", prompt)
    return text


def consistency_agent(tech, marketing, metrics):
    prompt = f"""
Check consistency between:

Technical architecture:
{tech}

Marketing roadmap:
{marketing}

Identify conflicts and fix them.
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("ConsistencyAgent", prompt)
    return text


def critic_agent(bundle, metrics):
    prompt = f"""
Evaluate this SaaS launch strategy.

{bundle}

Suggest improvements for industrial readiness.
"""
    text, tokens, time = call_llm(prompt)
    metrics.log(tokens, time)
    logger.log_agent("CriticAgent", prompt)
    return text

def get_clarifying_questions(user_idea):
    prompt = f"""
User business idea:
{user_idea}

Ask 3 clarifying questions to narrow the SaaS niche,
target users and monetization model.

Return ONLY the questions.
"""

    logger.log_agent("InversePromptingAgent", prompt)
    questions, tokens, latency = call_llm(prompt)
    return questions

# --------------------------
# Test / Standalone Run
# --------------------------

def run():
    """Pipeline çalıştırır ve logger üzerinden lastrun.svg üretir"""
    idea = "Freelancer Proposal Generator"  # test amacıyla default fikir
    metrics = Metrics()

    intent = inverse_prompting_agent(idea, metrics)
    plan = planning_agent(intent, metrics)
    tech = technical_agent(plan, metrics)
    marketing = marketing_agent(plan, metrics)
    aligned = consistency_agent(tech, marketing, metrics)
    critique = critic_agent(aligned, metrics)

    plan_with_feedback = f"{plan}\n# Critique:\n{critique}"

    logger.print_summary(compact=True)

    # Output klasörünü otomatik oluştur
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # lastrun.svg oluştur
    logger.render_graph(output_path=output_dir / "lastrun", open_browser=False)

    return {
        "architecture": tech,
        "roadmap": marketing,
        "critique": critique,
        "plan_with_feedback": plan_with_feedback
    }


if __name__ == "__main__":
    result = run()
    print("\n--- Final Output ---")
    print(result)
    input("\nPress Enter to exit...")