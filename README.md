# SnakeGameAI

This project is a Snake game developed using Pygame, where an AI is trained to play the game using Reinforcement Learning with PyTorch.

This project uses Pygame for the graphical interface of the Snake game and PyTorch for implementing and training the reinforcement learning model. The goal of the project is to create an AI that can learn to play the Snake game efficiently through trial and error, using reinforcement learning techniques.

The AI is trained using the Deep Q-Learning (DQN) algorithm. The training process involves:
- State Representation: The state of the game (position of the snake, food, and direction) is represented as input to the neural network.
- Action Selection: The AI selects an action (move up, down, left, right) based on the current state using an epsilon-greedy policy.
- Reward System: The AI receives a reward based on its actions (e.g., +10 for eating food, -10 for hitting the wall or itself).
- Network Training: The neural network is trained to minimize the difference between the predicted Q-values and the target Q-values.

When the game is started, a graph plots the score and mean score v/s the number of games, to show the model learning to play the game in real time.

https://github.com/user-attachments/assets/11b1a0b1-42d5-42e9-a199-1bb531950e82
