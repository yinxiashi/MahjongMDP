# Background

Riichi Mahjong (Japanese Mahjong) is widely considered the most strategic and defensive variant of Mahjong. Although it shares the core DNA of traditional Chinese Mahjong—drawing and discarding tiles to complete a hand—it introduces unique rules that turn it into a tense game of probability, risk management, and bluffing.

The core objective is to build a complete hand of 14 tiles before your opponents. A standard winning hand consists of four sets and one pair:

- 4 Sets: These can be Triplets (e.g., 7-7-7) or Sequences (e.g., 2-3-4).
- 1 Pair: Two identical tiles (e.g., 5-5).

Riichi uses 136 tiles (standard sets minus the Flowers/Seasons used in Chinese variants).

- Suits (1-9):
  - Pin (Circles/Dots)
  - Sou (Bamboo/Sticks)
  - Man (Characters/Numbers)
- Honors:
  - Winds: East, South, West, North.
  - Dragons: White, Green, Red.
 
## Existing tool

Currently there are some existing tools available online to help us determine which tiles to discard optimally. For example, [Tenhou](https://tenhou.net/2/?p=11234456677792p) provided a tool to analyze the results for discarding tiles. However, this tool only focus on the speed of improving your hand instead of maximizing the probability of winning. In some case, the option that allow you to improve your hand quickly is not necessarily the best hand that give you the highest chance of winning, because the hand could become slower in later stage.

To fix this issue, we need to use MDP to also consider the game state in later stage to find out the best move in the early game. Later we discovered that in some hand, the MDP actually disagree with Tenhou and the suggested move by MDP are considered suboptimal by Tenhou. A careful inspection shows that the move suggested by Tenhou, will help the hand move to second stage faster, but that stage has less winning chance than the other slower option. Overall, our trained model is highly consistent with Tenhou's result, showing that our model is very likely to be accurate.

# Our focus

Building a complete decision model is too complex and requires an extensive amount of resources to train. For this project, we will focus on one of the most interesting Yakus, Chinitsu (清一色), also known as Full Flush. To win a hand with Chinitsu, you need to form a hand composed exclusively of tiles from a single suit (e.g., only Bamboos). You cannot have any Winds or Dragon tiles in your hand. This makes the discarding decision very difficult, as there are so many ways to improve your hand. So we are trying to build a model that could help us decide which tile to discard to maximize our winning chances.

# Model data

We also pre-trained our simple version and you can download the model data [here](https://drive.google.com/drive/folders/1jh2AEOK2VKHsTjRQebaGAJWqaViUHKnM?usp=sharing).

- The simple version model use 14 tiles as standard game and allow unlimited turns.
- The complex version model use 11 tiles and allow maximum of 3 turns of discarding.
- Both model assume the winning reward being 10000, giveup penalty being 3000 and each turn's discarding penalty being 1000
