"""
VLA-Robotics Multi-Task Orchestrator
Connect natural language commands to multi-object robotic manipulation
Using MuJoCo physics engine with Franka Panda robot
"""

import os
import sys
import yaml
import numpy as np
import logging
import time
from pathlib import Path
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import robosuite as suite
    from robosuite.controllers import load_controller_config
    import mujoco
except ImportError as e:
    logger.error(f"❌ Missing package: {e}")
    logger.error("Install with: pip install -r requirements.txt")
    sys.exit(1)

from vla_interface import VLAInterface
from task_interpreter import TaskInterpreter
from robot_controller import RobotController
from multi_task_executor import MultiTaskExecutor
from object_detector import ObjectDetector


class VLARoboticsOrchestrator:
    """Main orchestrator for VLA-based multi-task robotics"""
    
    def __init__(self, config_path: str = "config_multi_task.yaml"):
        logger.info("="*70)
        logger.info("VLA-ROBOTICS MULTI-TASK ORCHESTRATOR")
        logger.info("Using: MuJoCo Physics + Franka Panda + Natural Language")
        logger.info("="*70)
        
        self.config = self._load_config(config_path)
        
        # Initialize VLA
        self.vla = VLAInterface(
            model=self.config['vla']['model'],
            api_base=self.config['vla']['api_base'],
            use_local=self.config['vla']['use_local']
        )
        
        self.interpreter = TaskInterpreter(vla=self.vla)
        self.env = None
        self.controller = None
        self.detector = None
        self.executor = None
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration from YAML"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"❌ Config file not found: {path}")
            sys.exit(1)
    
    def initialize_environment(self):
        """Initialize MuJoCo environment"""
        logger.info("\n📦 Initializing MuJoCo Environment...")
        logger.info("   Robot: Franka Panda")
        logger.info("   Task: PickPlace")
        
        sim_cfg = self.config['simulation']
        
        self.env = suite.make(
            env_name=sim_cfg['task'],
            robots=sim_cfg['robot'],
            use_camera_obs=False,
            has_renderer=sim_cfg['render'],
            has_offscreen_renderer=False,
            render_camera="frontview",
            reward_shaping=True,
            horizon=sim_cfg['horizon'],
            control_freq=int(1.0 / sim_cfg['timestep']),
        )
        
        self.controller = RobotController(self.env)
        self.detector = ObjectDetector(self.env)
        self.executor = MultiTaskExecutor(self.env, self.controller, self.detector)
        
        logger.info("✓ Environment ready!\n")
    
    def run_demo(self):
        """Run multi-task demonstration"""
        
        self.initialize_environment()
        self.env.reset()
        
        # Detect objects
        logger.info("🔍 Scanning environment for objects...")
        self.detector.detect_objects()
        logger.info("✓ Objects detected\n")
        
        commands = self.config['commands']
        mt_cfg = self.config['multi_task']
        
        for idx, command in enumerate(commands[:5], 1):
            logger.info("="*70)
            logger.info(f"COMMAND {idx}/5")
            logger.info("="*70)
            print(f"\n💬 COMMAND: \"{command}\"\n")
            
            # Process through VLA
            actions = self.interpreter.interpret(command)
            logger.info(f"📋 Interpreted {len(actions)} actions from command\n")
            
            # Execute based on command type
            cmd_lower = command.lower()
            
            if "sort" in cmd_lower:
                balls = [{'color': b['color'], 'position': np.array(b['position'])}
                        for b in mt_cfg['balls']]
                baskets = {b['color']: np.array(b['position']) for b in mt_cfg['baskets']}
                self.executor.execute_color_sorting_task(balls, baskets)
                
            elif "stack" in cmd_lower:
                balls = [(b['color'], np.array(b['position'])) for b in mt_cfg['balls']]
                base = np.array(mt_cfg['stacking']['base_position'])
                self.executor.execute_stacking_task(base, balls, max_height=3)
                
            else:
                balls = [(b['color'], np.array(b['position'])) for b in mt_cfg['balls']]
                baskets = [(b['color'], np.array(b['position'])) for b in mt_cfg['baskets']]
                self.executor.execute_pick_place_sequence(balls, baskets)
            
            time.sleep(1)
        
        self.env.close()
        logger.info("\n" + "="*70)
        logger.info("✓ DEMONSTRATION COMPLETE!")
        logger.info("="*70)
    
    def run_interactive(self):
        """Run interactive mode"""
        
        self.initialize_environment()
        self.env.reset()
        self.detector.detect_objects()
        
        logger.info("📝 Interactive Mode - Enter custom commands")
        logger.info("   Type 'quit' to exit\n")
        
        mt_cfg = self.config['multi_task']
        
        while True:
            try:
                command = input("\n💬 Command: ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not command:
                    continue
                
                actions = self.interpreter.interpret(command)
                
                cmd_lower = command.lower()
                if "sort" in cmd_lower:
                    balls = [{'color': b['color'], 'position': np.array(b['position'])}
                            for b in mt_cfg['balls']]
                    baskets = {b['color']: np.array(b['position']) for b in mt_cfg['baskets']}
                    self.executor.execute_color_sorting_task(balls, baskets)
                elif "stack" in cmd_lower:
                    balls = [(b['color'], np.array(b['position'])) for b in mt_cfg['balls']]
                    base = np.array(mt_cfg['stacking']['base_position'])
                    self.executor.execute_stacking_task(base, balls)
                else:
                    balls = [(b['color'], np.array(b['position'])) for b in mt_cfg['balls']]
                    baskets = [(b['color'], np.array(b['position'])) for b in mt_cfg['baskets']]
                    self.executor.execute_pick_place_sequence(balls, baskets)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
        
        self.env.close()
        logger.info("\n✓ Goodbye!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="VLA-Robotics: Multi-task robotic manipulation with natural language"
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'interactive'],
        default='demo',
        help='Run mode: demo (5 predefined commands) or interactive (user input)'
    )
    parser.add_argument(
        '--config',
        default='config_multi_task.yaml',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    orchestrator = VLARoboticsOrchestrator(config_path=args.config)
    
    if args.mode == 'demo':
        orchestrator.run_demo()
    else:
        orchestrator.run_interactive()


if __name__ == "__main__":
    main()
