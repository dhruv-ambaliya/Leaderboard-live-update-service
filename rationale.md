# Leaderboard Ranking Rationale

## Tiebreaker Logic

The leaderboard is sorted based on the following criteria, in order of priority:

1.  **Total Points (Descending)**: The primary ranking criterion. Players with higher total points are ranked higher.
    *   *Note*: "D$Q" (Disqualified) and "-" (Did not participate/finish) are treated as 0 points.

2.  **Total Spending (Ascending)**: If two or more players have the same Total Points, the player with the **lower** Total Spending is ranked higher.
    *   *Reasoning*: Efficiency is rewarded. Achieving the same points with less investment is considered superior performance.

3.  **Countback System (Descending)**: If players are tied on both Total Points and Total Spending, a "countback" is performed.
    *   This compares the highest individual event score for each player. The player with the higher single event score is ranked higher.
    *   If the highest scores are identical, the number of times that score was achieved is compared (more is better).
    *   If still tied, the second highest score is compared, and so on.
    *   *Implementation*: This is achieved by creating a list of all event scores for each player, sorting them in descending order, and comparing these lists lexicographically.

4.  **Alphabetical Order (Ascending)**: If all the above criteria are identical, players are sorted alphabetically by their name.
    *   *Highlighting*: In this case, the players are considered truly tied, and their names are highlighted in **Red** in the output.

## Further Tiebreaker Suggestions

If the current criteria fail to resolve a tie (i.e., players have identical points, spending, and exact same distribution of event scores), the following additional criteria could be considered:

1.  **Most Recent Form**: Compare scores starting from the most recent event (R24) backwards. The player who performed better in the most recent event is ranked higher. This rewards current form over historical performance.
2.  **Best Finish Position**: If event position data is available (not just points), the player with the highest individual race finish (e.g., 1st place, 2nd place) is ranked higher.
3.  **Fewest Disqualifications (D$Q)**: The player with fewer disqualifications is ranked higher, rewarding consistency and fair play.
4.  **Head-to-Head**: If only two players are tied, compare their scores in events where they both competed.
