from project_base import ProjectBase, ProjectDef


class P116Project(ProjectBase):
    @classmethod
    def define(cls) -> ProjectDef:
        return ProjectDef(
            key="p116",
            name="SaaS-Builder: Autonomous Product & Marketing Strategist",
            desc="An agentic system that transforms raw business ideas into technical architectures and market strategies.",
            student_id="150220747",
            scope=(
                "Implement a multi-agent orchestration that uses Inverse Prompting to refine user intent, "
                "Planning to structure the workflow, and Parallelization to generate technical (JSON) and "
                "marketing (Markdown) assets. A Consistency Agent ensures alignment between tech and business, "
                "while a Reflection loop iteratively improves strategy quality."
            ),
            key_contributions=[
                "Inverse Prompting — Interrogates the user to narrow down SaaS niche and monetization model",
                "Planning & Parallelization — Executes technical architecture and marketing strategy agents concurrently",
                "Consistency Agent — Cross-references technical constraints with marketing promises to avoid hallucinations",
                "Iterative Reflection — A 'Critic Agent' evaluates the final roadmap and refines it for industrial readiness",
            ],
            results=(
                "Produces a professional, internally consistent SaaS launch bundle including an HTML dashboard, "
                "DB schema (JSON), and a 12-week strategic roadmap (Markdown)."
            ),
        )




if __name__ == "__main__":
    P116Project.print_summary()