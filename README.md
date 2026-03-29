# VLA-Robotics Simulator: Multi-Task Robotic Manipulation with Natural Language

🤖 **Franka Panda Robot** + 🧠 **LLM VLA** + 🌐 **MuJoCo Physics** + 🎯 **Multi-Task Manipulation**

**Connect any VLA application with a robotic simulator to demonstrate multi-task pick-and-place operations using natural language commands.**

---

## Features

✅ **Natural Language Commands** - "Pick up the red ball and put it in the blue basket"  
✅ **Multi-Object Manipulation** - 3 balls, 3 baskets, complex task sequences  
✅ **VLA Integration** - All commands processed through local LLM (Ollama)  
✅ **No Hardcoded Actions** - 7+ dynamic commands interpreted at runtime  
✅ **Windows Compatible** - 16GB RAM, native Python, MuJoCo physics  
✅ **MuJoCo Simulation** - Realistic physics, high-speed inference  

---

## Quick Start (Windows 16GB Laptop)

### 1. Install Ollama (Local LLM)
- Download: https://ollama.com/download/windows
- Run installer
- Open Command Prompt:
  ```bash
  ollama run llama2
  ```
  (Keep this terminal open)

### 2. Clone & Install
```bash
git clone https://github.com/vishalrajn-55/vla-robotic-simulator.git
cd vla-robotic-simulator
pip install -r requirements.txt
```

### 3. Run Demo
```bash
# In new Command Prompt (Ollama running in first one)
python main_multi_task.py --mode demo
```

---

## What You See

✅ MuJoCo 3D window with Franka Panda robot  
✅ 3 colored balls (red, blue, green) on table  
✅ 3 matching colored baskets  
✅ Robot picks up balls and places them in baskets  
✅ 5 different natural language commands execute automatically  

---

## Example Commands Executed

1. **"Pick up the red ball and put it in the red basket"**
2. **"Sort all colored balls into their matching color baskets"**
3. **"Stack the blue ball on top of the red ball, then green on top"**
4. **"Move all balls to the right side of the table in order"**
5. **"Create a tower by stacking red, blue, and green balls"**

---

## Technology Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **Simulator** | MuJoCo | Native Windows, fast physics |
| **Robot** | Franka Panda | Professional arm, perfect for manipulation |
| **VLA** | Ollama + Llama2 | Local, private, free, easy setup |
| **Framework** | robosuite | Pre-built tasks, pick-place ready |

---

## Repository Structure

```
vla-robotic-simulator/
├── main_multi_task.py       # Main orchestrator
├── config_multi_task.yaml   # Configuration
├── vla_interface.py         # VLA communication
├── task_interpreter.py      # NLP → Actions
├── robot_controller.py      # Robot control
├── object_detector.py       # Object detection
├── multi_task_executor.py   # Multi-task execution
├── requirements.txt         # Dependencies
└── README.md               # This file
```

---

## Interactive Mode

Run custom commands:
```bash
python main_multi_task.py --mode interactive
```

Type: "Pick up the blue ball", "Stack all objects", etc.

---

## Why MuJoCo (Not Gazebo)?

- ✅ Native Windows support (no WSL needed)
- ✅ Lighter on 16GB RAM
- ✅ Better for multi-object tasks
- ✅ Faster setup and execution
- ✅ Better Python integration

---

## License

MIT License

---

**Ready to run on your Windows 16GB laptop! 🚀**
