# 🚀 Space Invaders: A Pygame Classic Remastered!

Welcome to my take on the timeless arcade classic, Space Invaders, built entirely with Python and Pygame! Relive the nostalgia with modern twists and challenging gameplay.

## ✨ Features

* **Classic Gameplay:** Experience the core mechanics of the original Space Invaders.
* **Multiple Enemy Types:** Face off against different alien invaders, each with varying points.
* **Defensive Shields:** Strategically use destructible shields to protect your spaceship.
* **Dynamic Power-ups:** Grab power-ups like:
    * **Double Bullet:** Unleash a twin stream of fire!
    * **Speed Boost:** Outmaneuver your foes with increased agility.
* **Challenging Boss Fights:** Prepare for intense encounters with powerful bosses that appear every 5 levels!
* **Two Exciting Game Modes:**
    * **Classic Mode:** Conquer 5 progressively harder levels, culminating in a final boss battle, to achieve victory!
    * **Unlimited Mode:** See how long you can survive and how high you can score against endless waves of increasingly difficult enemies.
* **Immersive Audio:** Engage your senses with classic arcade sound effects and a looping background music track.
* **Robust Asset Loading:** Includes error handling for missing image/sound files, falling back to colored shapes if assets aren't found.

## 🕹️ How to Play

* **Movement:** Use the **Left Arrow** and **Right Arrow** keys to move your spaceship horizontally.
* **Shoot:** Press the **Spacebar** to fire bullets at the incoming alien horde.
* **Menu Navigation:** Use your mouse to click on game mode selections.
* **Game Over/Victory:** Press **'R'** to Restart (same mode) or **'M'** to return to the Main Menu.

## 🛠️ Technologies Used

* **Python 3.x**
* **Pygame Library**

## 📦 Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/SpaceInvadersGame.git](https://github.com/YourUsername/SpaceInvadersGame.git)
    ```
    (Replace `YourUsername` and `SpaceInvadersGame` with your actual GitHub details)
2.  **Navigate to the Project Directory:**
    ```bash
    cd SpaceInvadersGame
    ```
3.  **Install Pygame:**
    ```bash
    pip install pygame
    ```
4.  **Place Assets:** Ensure your `player_ship.png`, `enemy1.png`, `background.png`, `laser.wav`, etc., are all located in the folder specified by the `image_folder` variable in `SpaceInvaders.py`. **Remember to update this path in the code if your assets are in a different location!**
    ```python
    # In SpaceInvaders.py, update this line with your asset path:
    image_folder = "C:\\Users\\mathe\\Desktop\\New folder" # <--- YOUR ASSET PATH HERE
    ```
5.  **Run the Game:**
    ```bash
    python SpaceInvaders.py
    ```

## 🙏 Feedback and Contributions

Feel free to open an issue or submit a pull request if you have suggestions, bug reports, or want to contribute to this project!

---