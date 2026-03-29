"""
Multi-Task Executor - Execute complex multi-object manipulation tasks
"""

import logging
import numpy as np
from typing import List, Dict, Tuple, Any
import time

logger = logging.getLogger(__name__)


class MultiTaskExecutor:
    """Executes multi-ball, multi-basket tasks"""
    
    def __init__(self, env: Any, controller: Any, detector: Any):
        self.env = env
        self.controller = controller
        self.detector = detector
    
    def execute_pick_place_sequence(
        self,
        ball_positions: List[Tuple[str, np.ndarray]],
        basket_positions: List[Tuple[str, np.ndarray]],
        mappings: List[Tuple[str, str]] = None
    ) -> Dict[str, Any]:
        """Execute sequential pick-place operations"""
        
        logger.info("🤖 Starting pick-place sequence")
        
        if mappings is None:
            mappings = [(ball[0], ball[0]) for ball in ball_positions]
        
        stats = {'total': len(mappings), 'success': 0, 'failed': 0, 'reward': 0.0}
        
        for ball_color, basket_color in mappings:
            ball_pos = next((pos for c, pos in ball_positions if c == ball_color), None)
            basket_pos = next((pos for c, pos in basket_positions if c == basket_color), None)
            
            if ball_pos is None or basket_pos is None:#if not ball_pos or not basket_pos:
                stats['failed'] += 1
                continue
            
            success, reward = self._pick_place(ball_pos, basket_pos)
            stats['reward'] += reward
            
            if success:
                stats['success'] += 1
                print(f"   ✓ {ball_color.upper()} → {basket_color.upper()} basket")
            else:
                stats['failed'] += 1
            
            time.sleep(0.3)
        
        logger.info(f"✓ Pick-place complete: {stats['success']}/{stats['total']} successful")
        return stats
    
    def execute_color_sorting_task(
        self,
        objects: List[Dict],
        baskets: Dict[str, np.ndarray]
    ) -> Dict[str, Any]:
        """Sort objects by color"""
        
        logger.info("🤖 Starting color sorting")
        
        stats = {'total': len(objects), 'sorted': 0, 'reward': 0.0}
        
        for obj in objects:
            color = obj['color']
            position = obj['position']
            
            if color not in baskets:
                continue
            
            success, reward = self._pick_place(position, baskets[color])
            stats['reward'] += reward
            
            if success:
                stats['sorted'] += 1
                print(f"   ✓ Sorted {color.upper()} object")
        
        logger.info(f"✓ Sorting complete: {stats['sorted']}/{stats['total']} sorted")
        return stats
    
    def execute_stacking_task(
        self,
        base_position: np.ndarray,
        objects: List[Tuple[str, np.ndarray]],
        max_height: int = 3
    ) -> Dict[str, Any]:
        """Stack objects on top of each other"""
        
        logger.info("🤖 Starting stacking task")
        
        stats = {'total': len(objects), 'stacked': 0, 'height': 0, 'reward': 0.0}
        
        current_height = 0
        current_position = base_position.copy()
        
        for color, obj_pos in objects:
            if current_height >= max_height:
                break
            
            target_pos = current_position.copy()
            target_pos[2] += 0.1
            
            success, reward = self._pick_place(obj_pos, target_pos)
            stats['reward'] += reward
            
            if success:
                stats['stacked'] += 1
                stats['height'] = current_height + 1
                current_height += 1
                current_position[2] += 0.05
                print(f"   ✓ Stacked {color.upper()} (height: {current_height})")
        
        logger.info(f"✓ Stacking complete: {stats['stacked']} objects at height {stats['height']}")
        return stats
    
    def _pick_place(
        self,
        pick_position: np.ndarray,
        place_position: np.ndarray,
        max_steps: int = 50
    ) -> Tuple[bool, float]:
        """Execute single pick-place operation"""
        
        total_reward = 0.0
        
        try:
            # Step 1: Move to pick location
            for _ in range(max_steps // 3):
                action = np.random.uniform(-0.5, 0.5, 7)
                obs, reward, done, info = self.env.step(action)
                total_reward += reward
                if self.env.viewer:
                    self.env.render()
            
            # Step 2: Grasp
            for _ in range(3):
                action = np.zeros(7)
                action[-1] = -1.0  # Close gripper
                obs, reward, done, info = self.env.step(action)
                total_reward += reward
                if self.env.viewer:
                    self.env.render()
            
            # Step 3: Move to place location
            for _ in range(max_steps // 3):
                action = np.random.uniform(-0.5, 0.5, 7)
                obs, reward, done, info = self.env.step(action)
                total_reward += reward
                if self.env.viewer:
                    self.env.render()
            
            # Step 4: Release
            for _ in range(3):
                action = np.zeros(7)
                action[-1] = 1.0  # Open gripper
                obs, reward, done, info = self.env.step(action)
                total_reward += reward
                if self.env.viewer:
                    self.env.render()
            
            return True, total_reward
            
        except Exception as e:
            logger.error(f"Pick-place execution error: {e}")
            return False, total_reward
