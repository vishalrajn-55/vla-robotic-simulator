"""
Object Detector - Detect colored objects in simulation
"""

import logging
import numpy as np
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class ObjectDetector:
    """Detects colored objects (balls, baskets)"""
    
    COLOR_RANGES = {
        'red': {'min': np.array([0.8, 0.0, 0.0]), 'max': np.array([1.0, 0.3, 0.3])},
        'blue': {'min': np.array([0.0, 0.0, 0.8]), 'max': np.array([0.3, 0.3, 1.0])},
        'green': {'min': np.array([0.0, 0.8, 0.0]), 'max': np.array([0.3, 1.0, 0.3])},
    }
    
    def __init__(self, env: Any):
        self.env = env
        self.detected_objects = {}
    
    def detect_objects(self, camera_obs: Optional[np.ndarray] = None) -> Dict:
        """Detect all colored objects"""
        logger.info("Scanning environment...")
        
        detected = {color: [] for color in self.COLOR_RANGES.keys()}
        
        try:
            for body_id in range(len(self.env.model.body_names)):
                body_name = self.env.model.body_names[body_id].decode('utf-8')
                position = self.env.data.body_xpos[body_id].copy()
                
                color = self._classify_by_name(body_name)
                if color and color in detected:
                    detected[color].append({
                        'name': body_name,
                        'position': position,
                        'body_id': body_id
                    })
        except Exception as e:
            logger.warning(f"Detection error: {e}")
        
        self.detected_objects = detected
        return detected
    
    def get_object_position(self, color: str, index: int = 0) -> Optional[np.ndarray]:
        """Get position of colored object"""
        objects = self.detected_objects.get(color, [])
        if index < len(objects):
            return objects[index]['position']
        return None
    
    def _classify_by_name(self, name: str) -> Optional[str]:
        """Classify object by name"""
        name_lower = name.lower()
        for color in self.COLOR_RANGES.keys():
            if color in name_lower:
                return color
        return None
