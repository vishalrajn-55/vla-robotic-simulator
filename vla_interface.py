"""
VLA Interface Module - Handles LLM communication
"""

import logging
from typing import List, Optional
import json

logger = logging.getLogger(__name__)


class VLAInterface:
    """Interface for VLA model communication"""
    
    def __init__(
        self,
        model: str = "llama2",
        api_base: str = "http://localhost:11434/v1",
        use_local: bool = True
    ):
        self.model = model
        self.api_base = api_base
        self.use_local = use_local
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client for local Ollama"""
        try:
            from openai import OpenAI
            if self.use_local:
                self.client = OpenAI(api_key="ollama", base_url=self.api_base)
                logger.info(f"✓ Connected to local LLM at {self.api_base}")
            else:
                self.client = OpenAI()
                logger.info("✓ Using OpenAI API")
        except ImportError:
            logger.warning("OpenAI not available. Using mock responses.")
            self.client = None
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:
        """Query the VLA model"""
        
        if not self.client:
            return self._mock_response(prompt)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"VLA query error: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """Generate mock response for testing"""
        if "red ball" in prompt.lower():
            return '["locate red ball", "move to ball", "grasp ball", "lift", "move to basket", "release"]'
        elif "green" in prompt.lower():
            return '["locate green", "approach", "grasp", "lift", "move right", "release"]'
        elif "stack" in prompt.lower():
            return '["locate first ball", "pick up", "place base", "locate second", "stack", "locate third", "stack"]'
        elif "sort" in prompt.lower():
            return '["scan environment", "identify colors", "pick red", "place red basket", "pick blue", "place blue basket", "pick green", "place green basket"]'
        else:
            return '["assess", "plan", "execute", "verify"]'


class TaskPlanner:
    """Task planning using VLA"""
    
    SYSTEM_PROMPT = """You are a robot task planner. Convert natural language commands into atomic robot actions.
Return ONLY a JSON array. Example: ["locate target", "move to target", "grasp", "lift", "move away", "release"]
Do NOT include explanations."""
    
    def __init__(self, vla: VLAInterface):
        self.vla = vla
    
    def plan(self, command: str) -> List[str]:
        """Generate action sequence from command"""
        logger.info(f"Planning: {command}")
        
        prompt = f"Robot command: {command}"
        
        try:
            response = self.vla.query(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.2,
                max_tokens=300
            )
            
            # Parse JSON
            actions = json.loads(response)
            if isinstance(actions, list):
                logger.info(f"✓ Generated {len(actions)} actions")
                return actions
        except json.JSONDecodeError:
            logger.warning("Parsing error, extracting fallback")
            return self._extract_fallback(response)
        except Exception as e:
            logger.error(f"Planning error: {e}")
        
        return []
    
    def _extract_fallback(self, response: str) -> List[str]:
        """Fallback action extraction"""
        actions = [a.strip().strip('•-•').strip('"\'')
                  for a in response.split('\n')
                  if a.strip() and len(a.strip()) > 3]
        return actions[:10]
