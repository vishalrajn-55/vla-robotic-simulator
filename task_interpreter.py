"""
Task Interpreter - NLP to Robot Actions
"""

import logging
from typing import List
from vla_interface import VLAInterface, TaskPlanner

logger = logging.getLogger(__name__)


class TaskInterpreter:
    """Converts natural language to robot actions"""
    
    def __init__(self, vla: VLAInterface):
        self.vla = vla
        self.planner = TaskPlanner(vla)
    
    def interpret(self, command: str) -> List[str]:
        """Interpret natural language command"""
        logger.info(f"Interpreting: {command}")
        
        actions = self.planner.plan(command)
        
        if not actions:
            logger.warning("No actions generated")
            actions = self._default_sequence(command)
        
        return actions
    
    def _default_sequence(self, command: str) -> List[str]:
        """Default action sequence"""
        return [
            "assess environment",
            "identify target",
            "move to target",
            "interact",
            "verify completion"
        ]
