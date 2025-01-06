from typing import Dict, List, Optional
from util import llm_call, extract_xml


def parse_calims(tasks_xml: str) -> List[Dict]:
    """Parse XML tasks into a list of task dictionaries."""
    tasks = []
    current_task = {}

    for line in tasks_xml.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.startswith("<claim>"):
            current_task = {}
        elif line.startswith("<article>"):
            current_task["article"] = line[9:-10].strip()
        elif line.startswith("<outcome>"):
            current_task["outcome"] = line[9:-10].strip()
        elif line.startswith("<description>"):
            current_task["description"] = line[13:-14].strip()
        elif line.startswith("</claim>"):
            if "description" in current_task:
                if "type" not in current_task:
                    current_task["type"] = "default"
                tasks.append(current_task)

    return tasks


class FlexibleOrchestrator:
    """Break down tasks and run them in parallel using worker LLMs."""

    def __init__(
        self,
        claim_decomposer_prompt: str,
        prompt_a: str,
        prompt_b: str,
        prompt_c1: str,
        prompt_c2: str,
        prompt_d1: str,
        case_facts: str,
        case_law: str,
    ):
        """Initialize with prompt templates."""
        self.claim_decomposer_prompt = claim_decomposer_prompt
        self.prompt_a = prompt_a
        self.prompt_b = prompt_b
        self.prompt_c1 = prompt_c1
        self.prompt_c2 = prompt_c2
        self.prompt_d1 = prompt_d1
        self.case_facts = case_facts
        self.case_law = case_law

    def _format_prompt(self, template: str, **kwargs) -> str:
        """Format a prompt template with variables."""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required prompt variable: {e}")

    def process(self, context: Optional[Dict] = None) -> Dict:
        """Process task by breaking it down and running subtasks in parallel - not really parallel for now."""
        context = context or {}
        context.update({"case_facts": self.case_facts})
        context.update({"case_law": self.case_law})

        # Step 1: Get orchestrator response
        decomposer_input = self._format_prompt(self.claim_decomposer_prompt, **context)
        decomposer_response = llm_call(decomposer_input)

        # Parse decomposer response
        claims = parse_calims(decomposer_response)

        print("\n=== CLAIM DECOMPOSER OUTPUT ===")
        claims_articles = [claim["article"] for claim in claims]
        print(f"\nCLAIMs:\n{claims_articles}")

        # Step 2: Process each task
        worker_results = []
        for claim_info in claims:
            print(f'processing claim: {claim_info["article"]} ')
            data = context.copy()
            data.update(claim_info)
            worker_a_input = self._format_prompt(self.prompt_a, **data)
            worker_b_input = self._format_prompt(self.prompt_b, **data)
            worker_c1_input = self._format_prompt(self.prompt_c1, **data)
            worker_c2_input = self._format_prompt(self.prompt_c2, **data)

            # Run worker LLMs
            print(f'running worker A,B,C1,C2 for claim: {claim_info["article"]} ')
            worker_a_response = llm_call(worker_a_input)
            worker_b_response = llm_call(worker_b_input)
            worker_c1_response = llm_call(worker_c1_input)
            worker_c2_response = llm_call(worker_c2_input)

            # Extract worker outputs
            relevant_facts = extract_xml(worker_a_response, "relevant_facts")
            article_cited = extract_xml(worker_b_response, "article_cited")
            applicant_arguments = extract_xml(worker_c1_response, "applicant_arguments")
            respondant_counterarguments = extract_xml(
                worker_c1_response, "respondant_counterarguments"
            )
            court_assessment_analysis = extract_xml(
                worker_c2_response, "court_assessment_analysis"
            )

            # Update data with worker outputs
            data.update({"relevant_facts": relevant_facts})
            data.update({"article_cited": article_cited})
            data.update({"applicant_arguments": applicant_arguments})
            data.update({"respondant_counterarguments": respondant_counterarguments})
            data.update({"court_assessment_analysis": court_assessment_analysis})

            # Run the classifier
            print(f'running classifier D1 for claim: {claim_info["article"]} ')
            classification_input = self._format_prompt(self.prompt_d1, **data)
            classification_response = llm_call(classification_input)

            contemplator = extract_xml(classification_response, "contemplator")
            classification = extract_xml(classification_response, "classification")
            reasoning = extract_xml(classification_response, "reasoning")

            # Update data with classifier outputs
            data.update({"contemplator": contemplator})
            data.update({"classification": classification})
            data.update({"reasoning": reasoning})

            # remomve case facts and case law from data
            data.pop("case_facts", None)
            data.pop("case_law", None)

            # Append worker results
            worker_results.append(data)

        return worker_results
