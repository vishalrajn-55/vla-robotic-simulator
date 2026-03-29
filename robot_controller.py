"""
Robot Controller - Control robot in MuJoCo simulation
"""

import logging
import numpy as np
from typing import Any, Tuple

logger = logging.getLogger(__name__)


class RobotController:
    """Controls Franka Panda robot in MuJoCo"""
    
    def __init__(self, env: Any):
        self.env = env
        self.action_space = env.action_space
    
    def execute_action(self, action_desc: str) -> Tuple[Any, float, bool]:
        """Execute action from description"""
        logger.debug(f"Executing: {action_desc}")
        
        action_vec = self._interpret_action(action_desc)
        obs, reward, done, info = self.env.step(action_vec)
        
        return obs, reward, done
    
    def _interpret_action(self, desc: str) -> np.ndarray:
        """Map description to control vector (7D for Panda: x,y,z,rx,ry,rz,gripper)"""
        desc_lower = desc.lower()
        
        # 7D action: [x, y, z, rx, ry, rz, gripper]
        if any(w in desc_lower for w in ["close", "grasp", "pick", "grab"]):
            action = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0])
        elif any(w in desc_lower for w in ["open", "release", "drop", "place"]):
            action = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        elif any(w in desc_lower for w in ["up", "lift", "raise"]):
            action = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
        elif any(w in desc_lower for w in ["down", "lower"]):
            action = np.array([0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0])
        elif any(w in desc_lower for w in ["left"]):
            action = np.array([-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        elif any(w in desc_lower for w in ["right"]):
            action = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        else:
            action = np.random.uniform(-0.1, 0.1, self.action_space.shape)
        
        return action
    
    def reset(self) -> Any:
        """Reset environment"""
        return self.env.reset()
