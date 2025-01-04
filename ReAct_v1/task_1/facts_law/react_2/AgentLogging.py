from typing import Dict, Any, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
import json
from datetime import datetime
from langchain.tools import BaseTool


class AgentLoggingCallback(BaseCallbackHandler):
    def __init__(self, log_file_path: str = None):
        """Initialize the callback handler with an optional log file path."""
        self.log_file_path = (
            log_file_path
            or f"agent_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        self.logs = {
            "thoughts": [],
            "actions": [],
            "tool_outputs": [],
            "final_output": None,
            "errors": [],
        }
        self.current_action = None

    def on_agent_action(self, action: AgentAction, **kwargs) -> Any:
        """Log agent actions and thoughts."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "thought": action.log,
            "action": action.tool,
            "action_input": action.tool_input,
        }
        self.logs["thoughts"].append(log_entry)
        self.logs["actions"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "tool": action.tool,
                "input": action.tool_input,
            }
        )
        self.current_action = {  # Update current_action here
            "tool": action.tool,
            "input": action.tool_input,
        }
        # self._save_logs()

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs
    ) -> Any:
        print(f"Tool started: {serialized.get('name')} with input: {input_str}")
        self.current_action = {"tool": serialized.get("name"), "input": input_str}

    def on_tool_end(
        self, output: str, run_id: str = None, parent_run_id: str = None, **kwargs
    ):
        """Log tool outputs."""
        if self.current_action:
            tool_output = {
                "timestamp": datetime.now().isoformat(),
                "tool": self.current_action.get("tool"),
                "input": self.current_action.get("input"),
                "output": output,
            }
        else:
            tool_output = {"timestamp": datetime.now().isoformat(), "output": output}

        self.logs["tool_outputs"].append(tool_output)
        print(
            f"Tool output logged: {output[:100]}..."
        )  # Debug print, truncated for readability
        # self._save_logs()
        self.current_action = None

    def on_tool_error(self, error: Exception, **kwargs) -> Any:
        """Log tool errors."""
        self.logs["errors"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "error": str(error),
                "error_type": error.__class__.__name__,
                "tool": (
                    self.current_action.get("tool") if self.current_action else None
                ),
            }
        )
        print(f"Tool error logged: {str(error)}")  # Debug print
        # self._save_logs()

    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> Any:
        """Log the final output."""
        self.logs["final_output"] = {
            "timestamp": datetime.now().isoformat(),
            "output": finish.return_values,
            "log": finish.log,
        }
        # self._save_logs()

    def on_error(self, error: Exception, **kwargs) -> Any:
        """Log any errors that occur."""
        self.logs["errors"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "error": str(error),
                "error_type": error.__class__.__name__,
            }
        )
        # self._save_logs()

    def _save_logs(self):
        """Save logs to file."""
        with open(self.log_file_path, "w") as f:
            json.dump(self.logs, f, indent=2)
