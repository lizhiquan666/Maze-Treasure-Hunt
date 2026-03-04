# 🐧 Maze Treasure Hunt (迷宫寻宝)

⭐ If this project is helpful to you, please give it a Star! 

## 📖 Introduction
**Maze Treasure Hunt** is a fun and interactive 2D maze navigation game built with Python and the `pygame` library. Players control a little penguin navigating through a dynamically generated maze, aiming to collect scattered gold coins while avoiding static obstacles. The game ends when the penguin successfully reaches the target (a 520 rose 🌹) at the bottom-right corner!

## ✨ Key Features
- **Dynamic Maze Generation**: Generates a randomized maze layout layout using graph traversal algorithms. no two games are exactly the same!
- **Smooth Animations**: Enjoy silky-smooth pixel-based movement mechanics and rotating coin animations.
- **State Machine Architecture**: Clean transitions between "Instructions", "Playing", and "Game Over" screens.
- **Audio Experience**: Includes togglable background funk music and celebratory win sounds.
- **Dynamic Game Over Screen**: Features a shrinking/expanding penguin animation upon successfully completing the maze.

## 🚀 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/lizhiquan666/Maze-Treasure-Hunt.git
   ```
2. **Install dependencies**:
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install pygame numpy
   ```
3. **Run the game**:
   Navigate to the game directory and execute the main Python script:
   ```bash
   cd pygame
   python python源程序.py
   ```
   
## 🎮 Game Controls
- **Arrow Keys (`←`, `→`, `↑`, `↓`)**: Move the penguin across the maze.
- **`R` Key**: Instantly reset the game (creates a new maze and resets the score).
- **`M` Key**: Toggle background music on / off.

## 🛠️ Project Structure
```text
Maze-Treasure-Hunt/
├── pygame/                     # Main game directory
│   ├── python源程序.py          # Main game script & logic
│   ├── Funky Town.mp3          # Background music(not included)
│   ├── Wang Fei.mp3            # Victory music(not included)
│   ├── *.png / *.jpg           # Image assets (penguin, coins, obstacles, etc.)
├── README.md                   # This documentation file
└── LICENSE                     # Apache 2.0 License file
```

## 📄 License
This project is licensed under the Apache License 2.0. You can freely use, modify, and distribute this code, with patent rights protection.

Please refer to the [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) file for more details.

## 🙏 Acknowledgments
Special thanks to the following students for their contributions to the development of this project:
- **Gao Ruihan**
- **Li Zhiquan** 
- **Zheng Dengyuan**

We would also like to extend our sincere gratitude to **Zhang Xueli** for her support to this project.
```bibtex
@misc{zhang2026motionlora,
  author       = {Xueli Zhang},
  title        = {AnimateDiff Motion Module LoRA for Slow Motion Generation},
  year         = {2026},
  howpublished = {\url{https://github.com/Shelly-icecream/AnimateDiff-Motion-Module-LoRA}},
  note         = {GitHub repository}
}
```

## 📚 References
If you use this project for your own research or coursework, please cite the following work:
```bibtex
@misc{lizhiquan2026mazetreasurehunt,
  author       = {Li Zhiquan},
  title        = {Maze Treasure Hunt Game},
  year         = {2026},
  howpublished = {\url{https://github.com/lizhiquan666/Maze-Treasure-Hunt.git}},
  note         = {GitHub repository}
}
```

## ⚠️ Disclaimer
This repository is provided for academic, recreational, and research purposes only. Use it in accordance with the Apache 2.0 License.