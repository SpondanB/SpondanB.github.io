---
# hide-toc: true
# hide-navigation: true
myst:
    html_meta:
        "description": "Reinforcement Learning Snake Game: Deep Q-Learning with PyTorch — Spondan Bandyopadhyay"
        "keywords": "projects, games, reinforcement learning, machine learning, AI, Spondan Bandyopadhyay"
--------------------------------------------------------------------------------------------------------

# Reinforcement Learning: Teaching an Agent to Play Snake

**A Deep Q-Learning agent built with PyTorch that learns to play Snake through trial, error, and reward.**

:::{button-link} https://github.com/SpondanB/ReinforecmentLearning-SnakeGame
:color: primary
:outline:
View Source on GitHub
:::
---

## 🎯 The Objective

The goal of this project was to explore **Reinforcement Learning** by building an agent that could learn to play Snake without being explicitly programmed with a strategy.

Rather than telling the Snake exactly what to do, I wanted to create a system where the agent could:

* Observe its current environment.
* Choose an action.
* Receive a reward based on the outcome.
* Learn from that experience.
* Gradually improve its future decisions.

The basic learning loop can be summarized as:

```text
State → Action → Reward → New State → Learning
```

This project uses **Deep Q-Learning (DQN)**, with **PyTorch** handling the neural network and optimization, and **pygame-ce** providing the Snake environment.

---

## 🧠 Reinforcement Learning Formulation

The Snake game can be represented as a classic Reinforcement Learning problem.

There are four fundamental components:

* **Environment:** The Snake game.
* **Agent:** The neural network-controlled Snake.
* **State:** A numerical representation of the current game situation.
* **Action:** The movement selected by the agent.

The environment provides feedback through a **reward function**, allowing the agent to learn which decisions are beneficial.

The interaction between the agent and environment looks like:

```text
                 ┌─────────────────┐
                 │   Snake Game    │
                 │   Environment   │
                 └────────┬────────┘
                          │
                        State
                          │
                          ▼
                 ┌─────────────────┐
                 │      Agent      │
                 │  Neural Network │
                 └────────┬────────┘
                          │
                        Action
                          │
                          ▼
                 ┌─────────────────┐
                 │   Snake Game    │
                 │ Executes Action │
                 └────────┬────────┘
                          │
                    Reward + New State
                          │
                          ▼
                 ┌─────────────────┐
                 │   Train Model   │
                 └─────────────────┘
```

---

## 🎮 The Action Space

The agent only has **three possible actions**:

```text
[1, 0, 0] → Straight
[0, 1, 0] → Right
[0, 0, 1] → Left
```

Instead of predicting an absolute direction such as `UP`, `DOWN`, `LEFT`, or `RIGHT`, the agent makes decisions relative to its current direction.

For example, if the Snake is currently moving upward:

```text
             ↑
             │
             │
           🐍
```

the available actions become:

```text
Straight → ↑
Right    → →
Left     → ←
```

This keeps the action space small while giving the model the information necessary to control the Snake.

---

## 👁️ Designing the Game State

One of the most important design decisions was determining **what information the agent should actually see**.

Instead of giving the model the entire game screen, I created a compact **11-dimensional state representation**:

```text
[
    danger_straight,
    danger_right,
    danger_left,

    direction_left,
    direction_right,
    direction_up,
    direction_down,

    food_left,
    food_right,
    food_up,
    food_down
]
```

The state can be divided into three groups.

### 🚧 Danger Detection

The first three values represent immediate collision risks:

```text
danger_straight
danger_right
danger_left
```

These tell the agent whether moving in a particular direction could result in a collision.

### 🧭 Current Direction

The next four values represent the Snake's current direction:

```text
direction_left
direction_right
direction_up
direction_down
```

This is particularly important because the action space is relative to the Snake's current movement.

### 🍎 Food Location

The final four values describe the position of the food relative to the Snake:

```text
food_left
food_right
food_up
food_down
```

This gives the model enough information to reason about whether the food is generally to its left, right, above, or below.

---

## 🧮 Deep Q-Learning

The agent uses a **Deep Q-Network (DQN)** to estimate the quality of each possible action.

The fundamental idea behind Q-Learning is the function:

$$
Q(s,a)
$$

where:

* **$s$** is the current state.
* **$a$** is an action.
* **$Q(s,a)$** represents the expected quality of taking action $a$ in state $s$.

In simple terms:

> **How good is this action given the current situation?**

The neural network takes the 11-dimensional state and outputs three Q-values:

```text
                  State
                    │
                    ▼
                 11 values
                    │
                    ▼
              ┌───────────┐
              │  11 → 256 │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │  256 → 3  │
              └─────┬─────┘
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Straight   Right      Left
         Q₁        Q₂         Q₃
```

The current architecture is:

$$
11 \rightarrow 256 \rightarrow 3
$$

The three outputs correspond to the estimated value of:

* Going straight.
* Turning right.
* Turning left.

The agent can then select the action with the highest predicted Q-value.

---

## 📈 Reward Function

The reward function determines how the environment communicates success or failure to the agent.

For this project, I kept the reward system deliberately simple:

| Event            | Reward |
| ---------------- | -----: |
| 🍎 Eat food      |  `+10` |
| 💀 Die / collide |  `-10` |
| Normal movement  |    `0` |

Conceptually:

```text
                    Action
                       │
                       ▼
                  ┌─────────┐
                  │  Snake  │
                  └────┬────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        Food         Nothing       Death
          │            │            │
         +10            0          -10
```

The agent isn't explicitly told:

> "Move toward the food."

Instead, it learns that states and actions leading to food tend to produce positive rewards, while actions leading to death produce negative rewards.

---

## 📐 The Bellman Equation

The core of Q-Learning is the **Bellman equation**.

The Q-value can be updated using:

$$
Q_{new}(s,a)
=
Q(s,a)
+
\alpha
\left[
R(s,a)
+
\gamma \max_{a'}Q(s',a')
-
Q(s,a)
\right]
$$

Where:

* **$Q(s,a)$**: Current estimate of the action's value.
* **$R(s,a)$**: Reward received after taking the action.
* **$\alpha$**: Learning rate.
* **$\gamma$**: Discount factor.
* **$s'$**: New state after taking the action.
* **$\max Q(s',a')$**: Best estimated future value from the new state.

The parameters used in this project are:

$$
\alpha = 0.001
$$

$$
\gamma = 0.9
$$

The discount factor allows the agent to consider not only the immediate reward but also the potential rewards that may occur in future states.

---

## 🎯 From Bellman Equation to Neural Network Loss

With a traditional Q-Learning implementation, Q-values can be stored in a table.

With Deep Q-Learning, the neural network approximates the Q-function instead.

For a given state:

$$
Q(s) = [Q(s,a_1), Q(s,a_2), Q(s,a_3)]
$$

After taking an action, the agent receives a reward and observes the next state.

The target value can then be calculated as:

$$
Q_{target}
=
R
+
\gamma \max_{a'}Q(s',a')
$$

The network is trained to make its prediction closer to this target.

The loss can be represented as:

$$
Loss =
(Q_{target}-Q_{predicted})^2
$$

which corresponds to the **Mean Squared Error (MSE)** formulation.

The learning process therefore becomes:

```text
Current State
      │
      ▼
Neural Network
      │
      ▼
Predicted Q-values
      │
      ▼
Choose Action
      │
      ▼
Environment
      │
      ├──── Reward
      │
      └──── New State
               │
               ▼
        Calculate Target
               │
               ▼
            Loss
               │
               ▼
        Backpropagation
               │
               ▼
        Update Network
```

---

## 🎲 Exploration vs Exploitation

Another challenge is deciding whether the agent should:

1. **Exploit** what it already believes is the best action.
2. **Explore** and try something new.

If the agent always chooses the action with the highest predicted Q-value, it may never discover better strategies.

For this project, the exploration parameter is:

$$
\epsilon = 0.2
$$

Conceptually:

```text
                 Choose Action
                      │
             ┌────────┴────────┐
             │                 │
         Explore            Exploit
             │                 │
       Random Action      Best Q-value
```

This allows the agent to occasionally take a less certain action and gather new information about the environment.

---

## 🔄 The Training Loop

The complete training process is built around a simple interaction loop:

```python
state = get_state(game)

action = get_move(state)

reward, game_over, score = game.play_step(action)

new_state = get_state(game)

remember(
    state,
    action,
    reward,
    new_state,
    game_over
)

train_model()
```

Repeated over many iterations, this becomes:

```text
Get State
   ↓
Predict Q-values
   ↓
Choose Action
   ↓
Play Action
   ↓
Receive Reward
   ↓
Get New State
   ↓
Calculate Target
   ↓
Calculate Loss
   ↓
Backpropagation
   ↓
Update Model
   ↓
Repeat
```

The agent essentially learns by repeatedly asking:

> **"What happened when I did that?"**

and using the answer to adjust its future decisions.

---

## 🧪 Training Results

After approximately **15 minutes of training** and around **100 generations**, the agent achieved a highest observed score of: 🏆 89

The training configuration was approximately:

| Parameter       |       Value |
| --------------- | ----------: |
| State size      |        `11` |
| Hidden layer    |       `256` |
| Output size     |         `3` |
| Learning rate   |     `0.001` |
| Discount factor |       `0.9` |
| Exploration     |       `0.2` |
| Training time   | ~15 minutes |
| Generations     |        ~100 |
| Highest score   |      **89** |

For me, the interesting part wasn't simply reaching a score of 89.

It was seeing the agent improve through interaction with the environment rather than through explicitly programmed Snake-playing rules.

---

## 🛠️ Technical Challenges

### **State Representation**

One of the biggest design decisions was deciding how much information to expose to the agent.

Giving it the entire game screen would create a much more complicated learning problem.

Instead, I chose an 11-dimensional representation containing:

* Immediate dangers.
* Current direction.
* Food direction.

This makes the environment much easier to learn while still retaining the information needed for basic decision-making.

The trade-off is that the agent cannot reason about information that isn't represented in the state.

---

### **Learning From Future Rewards**

A particularly interesting aspect of Q-Learning is that the quality of an action isn't necessarily determined by its immediate result.

An action can appear good now but create a bad state several moves later.

The discount factor:

$$
\gamma = 0.9
$$

allows the model to incorporate these future rewards into its Q-value estimates.

This is what makes the problem more than simply:

```text
Food nearby → move toward food
```

The agent has to learn:

```text
Current Action
      ↓
Future State
      ↓
Future Consequences
      ↓
Expected Return
```

---

### **Exploration**

Early in training, the network's predictions are essentially meaningless.

There is no reason for the model to initially believe that turning left is better than turning right.

Exploration allows it to collect experiences that can eventually change those estimates.

This creates an interesting feedback loop:

```text
Explore
   ↓
Collect Experience
   ↓
Update Q-values
   ↓
Better Decisions
   ↓
Explore Better States
   ↓
Learn More
```

---

## 🧰 Tech Stack

* **Language:** Python
* **Deep Learning:** PyTorch
* **Game Environment:** pygame-ce
* **Algorithm:** Deep Q-Learning
* **State Space:** 11-dimensional
* **Action Space:** 3 actions
* **Neural Network:** `11 → 256 → 3`
* **Data Representation:** Numerical state vectors

---

## 🚀 Running the Project

Clone the repository and install the required dependencies.

Then run:

```bash
python agent.py
```

The agent will begin interacting with the Snake environment and training the neural network.

---

## 🔮 Future Improvements

This implementation is intentionally simple, which leaves a lot of room for experimentation.

### **Experience Replay**

Store previous experiences:

```text
(state, action, reward, next_state, done)
```

and sample batches of experiences during training.

This can reduce the correlation between consecutive training samples and make learning more stable.

---

### **Target Networks**

Introduce a separate target network to make the Q-learning target more stable.

```text
             Online Network
                   │
                   ▼
              Prediction
                   │
                   ▼
                 Loss
                   ▲
                   │
              Target Network
```

This is one of the standard improvements to a basic DQN implementation.

---

### **Double DQN**

Experiment with **Double DQN** to reduce the overestimation of action values that can occur with standard Q-learning.

---

### **A Better State Representation**

The current agent receives an engineered 11-dimensional state.

A natural next step would be to give the model more information about the actual game board:

```text
Game Grid
    ↓
Tensor Representation
    ↓
Convolutional Neural Network
    ↓
Q-values
    ↓
Action
```

This would allow the neural network to learn spatial representations instead of relying entirely on manually engineered features.

---

### **Learning Directly From Pixels**

The most ambitious direction would be to remove the manually constructed state representation completely.

Instead:

```text
Game Screen
     ↓
     CNN
     ↓
Learned Features
     ↓
  Q-values
     ↓
   Action
```

This would turn the project into a much more interesting experiment in visual reinforcement learning.

---

## 💭 Why This Project Matters to Me

This project started as a relatively simple experiment: **can I teach an AI to play Snake?**

But while building it, I became more interested in the underlying idea.

In traditional programming, I would explicitly define the behavior:

```text
IF food is left:
    turn left

IF wall is ahead:
    turn right
```

With reinforcement learning, I instead define the environment, the actions, and the consequences.

The agent has to discover useful behavior through interaction.

That distinction is what makes RL particularly interesting to me.

I'm increasingly interested in AI systems that go beyond simply mapping an input to an output.

Systems that can:

```text
Observe
   ↓
Reason
   ↓
Act
   ↓
Receive Feedback
   ↓
Learn
   ↓
Act Better
```

The Snake agent is obviously a very small version of this idea.

But it provides a useful environment for understanding the fundamental loop behind **sequential decision-making and autonomous agents**.

---

## 🧩 Final Thoughts

The most interesting moment in this project wasn't when the Snake reached a score of **89**.

It was realizing that the agent had no explicit concept of *how to play Snake*.

It wasn't given a strategy.

It wasn't told:

> "Food is good."

It wasn't given a predefined path.

Instead, it repeatedly interacted with the environment:

$$
State
\rightarrow
Action
\rightarrow
Reward
\rightarrow
New\ State
\rightarrow
Learning
$$

and gradually adjusted its behavior.

At the beginning, the agent is effectively guessing.

Over time, those guesses become informed by experience.

That transition—from **random actions to learned behavior**—is what made this project particularly interesting to me.

There is still a lot I want to explore: better DQN architectures, experience replay, target networks, Double DQN, richer state representations, and eventually learning directly from visual input.

For now, however, this small Snake game has given me a practical way to understand one of the fundamental ideas behind reinforcement learning:

> **An agent can learn what to do by interacting with the world and learning from the consequences of its actions.**
