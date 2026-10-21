"""Agent Engine (A2A) packaging of the CodeMender analysis agent.

Agent Engine hosts A2A agents through `A2aAgent`: it needs an HTTP+JSON agent card (A2A 1.0) and an executor
builder. The builder runs inside the Agent Engine container, so ADK objects are created lazily there.
"""
from vertexai.agent_engines.templates.a2a import A2aAgent, create_agent_card


def build_executor():
    from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
    from google.adk.artifacts import InMemoryArtifactService
    from google.adk.memory import InMemoryMemoryService
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    from .agent import root_agent

    def make_runner() -> Runner:
        return Runner(app_name=root_agent.name, agent=root_agent, artifact_service=InMemoryArtifactService(),
                      session_service=InMemorySessionService(), memory_service=InMemoryMemoryService())

    return A2aAgentExecutor(runner=make_runner)


def build_a2a_agent() -> A2aAgent:
    from a2a.types import AgentSkill

    skills = [
        AgentSkill(id="analyze_repository", name="Analyse repository for vulnerabilities",
                   description="Clone a git repo, find vulnerabilities (CWE/OWASP mapped), produce fix patches and "
                               "a PDF report attached to the reply.",
                   tags=["security", "code-analysis", "codemender", "sast"],
                   examples=["Analyse https://github.com/org/repo for vulnerabilities"]),
        AgentSkill(id="fix_candidates", name="Provide patches for findings",
                   description="Return unified-diff patches for findings from the last analysis, for a defect-fix agent.",
                   tags=["remediation", "patch"], examples=["Give me the patches for the critical findings"]),
    ]
    card = create_agent_card(agent_name="CodeMender Analysis Agent",
                             description="Security code analysis (CodeMender-style find / verify plan / fix) for a git repository.",
                             skills=skills, streaming=False)
    return A2aAgent(agent_card=card, agent_executor_builder=build_executor)
