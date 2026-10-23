import time
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from backend.agents.resume_agent import resume_agent
from backend.agents.matching_agent import matching_agent
from backend.agents.recommendation_agent import recommendation_agent
from backend.agents.interview_agent import interview_agent

def track_time(agent_name, start_time):
    elapsed = time.perf_counter() - start_time
    print(f"[PERFORMANCE] {agent_name}: {elapsed:.2f} seconds")
    

class HireSenseState(TypedDict, total=False):

    resume_path: str
    job_description: str

    resume_text: str
    resume_skills: dict

    match_results: dict
    recommendations: str
    interview_questions: str

    errors: list


def analyze_resume_node(state: HireSenseState):
    start_time = time.perf_counter()

    try:
        result = resume_agent(state["resume_path"])

        return {
            "resume_text": result["resume_text"],
            "resume_skills": result["resume_skills"]
        }

    except Exception as error:
        return {"errors": [str(error)]}

    finally:
        track_time("Resume Analysis", start_time)


def matching_node(state: HireSenseState):
    if state.get("errors"):
        return {}

    start_time = time.perf_counter()

    try:
        result = matching_agent(
            state["resume_text"],
            state["job_description"]
        )

        return {
            "match_results": result["match_results"]
        }

    except Exception as error:
        return {"errors": [str(error)]}

    finally:
        track_time("Job Matching", start_time)

def recommendation_node(state: HireSenseState):
    if state.get("errors"):
        return {}

    start_time = time.perf_counter()

    try:
        result = recommendation_agent(
            state["resume_text"],
            state["job_description"],
            state["match_results"]
        )

        return {
            "recommendations": result["recommendations"]
        }

    except Exception as error:
        return {"errors": [str(error)]}

    finally:
        track_time("Recommendations", start_time)

def interview_node(state: HireSenseState):
    if state.get("errors"):
        return {}

    start_time = time.perf_counter()

    try:
        result = interview_agent(
            state["resume_text"],
            state["job_description"],
            state["match_results"]
        )

        return {
            "interview_questions": result["interview_questions"]
        }

    except Exception as error:
        return {"errors": [str(error)]}

    finally:
        track_time("Interview Preparation", start_time)

# Build LangGraph workflow

workflow = StateGraph(HireSenseState)

workflow.add_node("resume_analysis", analyze_resume_node)
workflow.add_node("job_matching", matching_node)
workflow.add_node("recommendations", recommendation_node)
workflow.add_node("interview_preparation", interview_node)

workflow.add_edge(START, "resume_analysis")
workflow.add_edge("resume_analysis", "job_matching")
workflow.add_edge("job_matching", "recommendations")
workflow.add_edge("recommendations", "interview_preparation")
workflow.add_edge("interview_preparation", END)

hire_graph = workflow.compile()


def run_hiresense(resume_path: str, job_description: str):

    print("[PERFORMANCE] HireSense workflow started", flush=True)

    initial_state = {
        "resume_path": resume_path,
        "job_description": job_description,
        "errors": []
    }

    result = hire_graph.invoke(initial_state)

    print("[PERFORMANCE] HireSense workflow completed", flush=True)

    return result
