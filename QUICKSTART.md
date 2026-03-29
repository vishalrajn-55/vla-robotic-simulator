# 🚀 QUICKSTART - Get Running in 10 Minutes

## What You're Building

A system where you can say:
> **"Pick up the red ball and put it in the blue basket"**

And a robot in simulation DOES IT. Using AI to understand your command.

---

## Prerequisites

✅ Windows 10/11  
✅ Python 3.8+  
✅ 16GB RAM  
✅ Internet (for first-time setup only)  

---

## Step 1: Install Ollama (2 minutes)

This is your **local AI brain** that understands commands.

1. Go to https://ollama.com/download/windows
2. Download and run installer (standard Windows installer)
3. Once installed, open **Command Prompt** and run:
   ```bash
   ollama run llama2
   ```

**First time takes 5-10 minutes** (downloading 4GB model)

After that, you should see:
```
>>> (ready for input)
```

**Leave this terminal open** while you run the demo.

---

## Step 2: Clone Repository (1 minute)

```bash
# In a NEW Command Prompt, go to where you want the project
cd Desktop  # or wherever

# Clone the repository
git clone https://github.com/vishalrajn-55/vla-robotic-simulator.git

# Go into folder
cd vla-robotic-simulator
```

---

## Step 3: Install Python Packages (3 minutes)

```bash
# In same Command Prompt
pip install -r requirements.txt
```

This installs:
- robosuite (robot simulator)
- mujoco (physics engine)
- openai (LLM communication)
- And dependencies

---

## Step 4: Run the Demo (3 minutes)

```bash
# Make sure you still have Ollama running in first terminal!
# Then run this in your current terminal:

python main_multi_task.py --mode demo
```

**You should see:**

```
======================================================================
VLA-ROBOTICS MULTI-TASK ORCHESTRATOR
Using: MuJoCo Physics + Franka Panda + Natural Language
======================================================================

📦 Initializing MuJoCo Environment...
   Robot: Franka Panda
   Task: PickPlace
✓ Environment ready!

🔍 Scanning environment for objects...
✓ Objects detected

======================================================================
COMMAND 1/5
======================================================================

💬 COMMAND: "Pick up the red ball and put it in the red basket"

📋 Interpreted 6 actions from command

🤖 Starting pick-place sequence
   ✓ RED → RED basket

✓ Pick-place complete: 1/1 successful
```

**Then a window opens showing:**
- Franka Panda robot arm
- Red, blue, green balls on table
- Red, blue, green baskets
- Robot picks up balls and places them in baskets
- Different commands execute for each "COMMAND" section

---

## What Each Command Does

### Command 1: Single Pick-Place
**"Pick up the red ball and put it in the red basket"**
- Robot picks red ball from [0.30, 0.20]
- Places in red basket at [0.60, 0.00]

### Command 2: Color Sorting
**"Sort all colored balls into their matching color baskets"**
- Robot processes all 3 balls:
  - Red → Red basket
  - Blue → Blue basket
  - Green → Green basket

### Command 3: Stacking
**"Stack the blue ball on top of the red ball, then green on top"**
- Builds a 3-ball tower:
  ```
     GREEN
       BLUE
       RED
  ```

### Commands 4-5: More complex sequences
- Sequential movement
- Multi-object organization

---

## Try Interactive Mode

Once demo completes, try:

```bash
python main_multi_task.py --mode interactive
```

Then type your own commands:
```
💬 Command: Pick up the blue ball
💬 Command: Sort all objects
💬 Command: Create a stack
```

Type `quit` to exit.

---

## Files Overview

| File | Purpose |
|------|---------|
| `main_multi_task.py` | 🎯 Main script you run |
| `config_multi_task.yaml` | Settings for robots, balls, commands |
| `vla_interface.py` | Talks to Ollama LLM |
| `task_interpreter.py` | Converts text to actions |
| `multi_task_executor.py` | Executes multi-object tasks |
| `robot_controller.py` | Controls robot arm |
| `object_detector.py` | Detects balls and baskets |

---

## Configuration: Add More Objects

Want to add a **yellow ball** and **yellow basket**?

Edit `config_multi_task.yaml`:

```yaml
multi_task:
  balls:
    - {color: "red", position: [0.30, 0.20, 0.82]}
    - {color: "blue", position: [0.40, 0.30, 0.82]}
    - {color: "green", position: [0.50, 0.20, 0.82]}
    - {color: "yellow", position: [0.55, 0.15, 0.82]}  # NEW!
  
  baskets:
    - {color: "red", position: [0.60, 0.00, 0.82]}
    - {color: "blue", position: [0.70, 0.10, 0.82]}
    - {color: "green", position: [0.80, 0.00, 0.82]}
    - {color: "yellow", position: [0.90, 0.05, 0.82]}  # NEW!

  commands:
    - "Sort all colored balls into their matching baskets"
    # Will now handle 4 colors!
```

Then run again: `python main_multi_task.py --mode demo`

---

## Troubleshooting

### Error: "Connection refused"
**Problem:** Ollama not running

**Fix:** Go back to Step 1, open new terminal, run:
```bash
ollama run llama2
```
Keep this terminal open.

### Error: "Import Error: No module named 'robosuite'"
**Problem:** Packages not installed

**Fix:**
```bash
pip install --upgrade -r requirements.txt
```

### Error: "Out of memory"
**Problem:** 16GB not enough for Llama2

**Fix:** Use lighter model. In first terminal, press Ctrl+C to stop, then:
```bash
ollama run mistral    # Much lighter
```
Or `ollama run phi3` (even lighter)

### Slow performance
**Problem:** Rendering enabled on slow CPU

**Fix:** Edit `config_multi_task.yaml`:
```yaml
simulation:
  render: false   # Disable visualization
```

---

## System Architecture

```
Your Command (Text Input)
           ↓
    Ollama LLM (Local, on your laptop)
    - Understands natural language
    - Breaks command into steps
           ↓
    Task Interpreter
    - Converts to robot actions
           ↓
    Multi-Task Executor
    - Plans sequence for multiple objects
           ↓
    MuJoCo Physics Engine
    - Realistic robot simulation
    - Collision detection
    - Physics accuracy
           ↓
    Franka Panda Robot (Simulated)
    - 7-DOF manipulator arm
    - Gripper (grasp/release)
    - Joint control
           ↓
    Visual Output
    - Real-time 3D rendering
    - Shows robot and objects
```

---

## Why MuJoCo (not Gazebo)?

| Feature | MuJoCo | Gazebo |
|---------|--------|--------|
| Windows support | ✅ Native | ❌ Needs WSL |
| Setup complexity | ⭐ Simple | ⭐⭐⭐ Complex |
| Memory usage | 💾 Light | 💾💾💾 Heavy |
| Multi-object tasks | ✅ Excellent | ⚠️ OK |
| Installation time | 5 min | 30 min |

**Result:** MuJoCo is better for your Windows 16GB laptop.

---

## Next: Advanced Features

- 🤖 **More robots**: Fetch, KUKA, etc.
- 🎯 **More tasks**: Push, lift, stack, throw
- 🧠 **Different LLMs**: Mistral, Phi, GPT-4
- 🌍 **Real robot**: Connect to actual Franka Panda via ROS
- 📸 **Vision**: Add camera input for real-time detection

---

## Getting Help

1. Check error message - usually tells what's wrong
2. Verify Ollama running: `ollama run llama2` in separate terminal
3. Reinstall packages: `pip install --upgrade -r requirements.txt`
4. Check repository issues: https://github.com/vishalrajn-55/vla-robotic-simulator/issues

---

## Success Indicators

✅ Ollama running (command prompt shows `>>>`)  
✅ Python packages installed (no import errors)  
✅ MuJoCo window opens  
✅ Franka Panda robot visible  
✅ Balls and baskets spawn  
✅ Robot picks up ball and places in basket  
✅ 5 commands execute automatically  

---

## Performance Specs

- **First command interpretation:** ~2-3 seconds
- **Subsequent commands:** ~1-2 seconds  
- **Pick-place action:** ~5-10 seconds simulated
- **Rendering:** 60 FPS (if enabled)
- **Memory usage:** ~4-6GB while running

---

**You're all set! Enjoy controlling robots with natural language! 🚀**
