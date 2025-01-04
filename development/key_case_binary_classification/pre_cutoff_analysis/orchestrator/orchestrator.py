from typing import Dict, List, Optional
from util import llm_call, extract_xml, text_to_json


def parse_tasks(tasks_xml: str) -> List[Dict]:
    """Parse XML tasks into a list of task dictionaries."""
    tasks = []
    current_task = {}

    for line in tasks_xml.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.startswith("<task>"):
            current_task = {}
        elif line.startswith("<name>"):
            current_task["name"] = line[6:-7].strip()
        elif line.startswith("<goal>"):
            current_task["goal"] = line[6:-7].strip()
        elif line.startswith("<description>"):
            current_task["description"] = line[13:-14].strip()
        elif line.startswith("</task>"):
            if "description" in current_task:
                if "type" not in current_task:
                    current_task["type"] = "default"
                tasks.append(current_task)

    return tasks


class FlexibleOrchestrator:
    """Break down tasks and run them in parallel using worker LLMs."""

    def __init__(
        self,
        orchestrator_prompt: str,
        synthetizer_prompt: str,
        worker_prompt: str,
        case_facts: str,
        # case_law: str
    ):
        """Initialize with prompt templates."""
        self.orchestrator_prompt = orchestrator_prompt
        self.worker_prompt = worker_prompt
        self.synthetizer_prompt = synthetizer_prompt
        self.case_facts = case_facts
        # self.case_law = case_law

    def _format_prompt(self, template: str, **kwargs) -> str:
        """Format a prompt template with variables."""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required prompt variable: {e}")

    def process(self, task: str, context: Optional[Dict] = None) -> Dict:
        """Process task by breaking it down and running subtasks in parallel."""
        context = context or {}

        # Step 1: Get orchestrator response
        orchestrator_input = self._format_prompt(
            self.orchestrator_prompt, task=task, **context
        )
        orchestrator_response = llm_call(orchestrator_input)

        # Parse orchestrator response
        analysis = extract_xml(orchestrator_response, "analysis")
        tasks_xml = extract_xml(orchestrator_response, "tasks")
        tasks = parse_tasks(tasks_xml)

        print("\n=== ORCHESTRATOR OUTPUT ===")
        print(f"\nANALYSIS:\n{analysis}")
        print(f"\nTASKS:\n{tasks}")

        # Step 2: Process each task
        worker_results = []
        for task_info in tasks:
            worker_input = self._format_prompt(
                self.worker_prompt,
                task_name=task_info["name"],
                task_goal=task_info["goal"],
                task_description=task_info["description"],
                case_facts=self.case_facts,
                # case_law = self.case_law
                # **context
            )

            worker_response = llm_call(worker_input)
            result = extract_xml(worker_response, "response")

            worker_results.append(
                {
                    "name": task_info["name"],
                    "goal": task_info["goal"],
                    "description": task_info["description"],
                    "result": result,
                }
            )

            print(f"\n=== WORKER RESULT ({task_info['name']}) ===\n{result}\n")

        tasks_data = {
            "analysis": analysis,
            "worker_results": worker_results,
        }

        sythnsizer_input = self._format_prompt(
            self.synthetizer_prompt,
            original_task=task,
            subtasks=worker_results,
            **context,
        )
        print("\n=== SYNTHNESIZER OUTPUT ===")
        sythnsizer_response = llm_call(sythnsizer_input)
        print("OUTPUT:", sythnsizer_response)
        sythnsizer_response_parsed = text_to_json(sythnsizer_response)

        return {
            "orchestrator_response": orchestrator_response,
            "tasks_data": tasks_data,
            "synthetizer_response": sythnsizer_response_parsed,
        }
