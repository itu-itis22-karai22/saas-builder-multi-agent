import streamlit as st
import streamlit.components.v1 as components
from orchestrator import generate_questions, run_pipeline
from dashboard_renderer import DashboardRenderer

st.title("SaaS Builder Agentic System")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = None

idea = st.text_input("Enter your SaaS idea")

if idea == "":
    st.stop()

# Generate clarifying questions
if st.button("Generate Questions"):
    st.session_state.questions = generate_questions(idea)

# Show questions and collect answers
if st.session_state.questions:
    st.subheader("Clarifying Questions (Inverse Prompting)")
    st.write(st.session_state.questions)

    answers = st.text_area("Your Answers")

    if st.button("Generate Strategy"):

        # Run the pipeline
        result = run_pipeline(idea, answers)

        # Display main outputs
        st.subheader("Product Plan")
        st.write(result["plan"])

        st.subheader("Technical Architecture")
        st.write(result["architecture"])

        st.subheader("Marketing Roadmap")
        st.write(result["roadmap"])

        # Reflections
        st.subheader("Reflection Process")
        reflections = result.get("reflections", [])
        for i, reflection in enumerate(reflections):
            st.write(f"Reflection Round {i+1}")
            st.write(reflection)
        st.info(f"Total Reflection Iterations: {len(reflections)}")

        # System Metrics
        st.subheader("System Metrics")
        metrics = result.get("metrics", None)
        metrics_dict = {}
        if metrics is not None:
            st.metric("LLM Calls", metrics.calls)
            st.metric("Tokens Used", metrics.tokens)
            total_time = sum(metrics.times)
            st.metric("Total Latency (s)", round(total_time, 2))
            mean_time = round(total_time / metrics.calls if metrics.calls > 0 else 0, 2)
            # Metrics dictionary for DashboardRenderer
            metrics_dict = {
                "LLM Calls": metrics.calls,
                "Tokens Used": metrics.tokens,
                "Total Latency (s)": round(total_time, 2),
                "Mean Response Time (s)": mean_time
            }
        else:
            st.write("No metrics available.")

        

        st.success("SaaS Bundle Generated Successfully!")
        
        # Render dashboard (Metrikler kaldırılmış haliyle)
        dashboard_html_path = DashboardRenderer.render(
            architecture_json=result.get("architecture", "{}"), 
            roadmap_markdown=result.get("roadmap", ""),
            reflections_list=reflections,
            output_path="dashboard_temp.html"
        )

        # Dashboard Görüntüleme
        with open(dashboard_html_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        
        # Yüksekliği biraz artırdım ki scroll rahat olsun
        components.html(html_code, height=1200, scrolling=True)

        