# Baseball Performance Prediction

## Overview

The **Baseball Performance Prediction** project predicts the likelihood of a baseball team winning a game based on various game-specific and team factors. The model calculates a performance score between 0 and 1, with 1 indicating a high likelihood of winning. This score is derived from a combination of team performance metrics and contextual game factors.

## Key Features

- **Performance Score Calculation**: 
  - The prediction score is based on weighted factors, including:
    - **Team Stats**: Average runs scored and allowed, as well as win/loss records.
    - **Opponent Matchup**: Head-to-head team performance and recent form.
    - **Game Context**: Location (home vs. away), rest days, and weather conditions.
  
- **Simple Statistical Model**: 
  - The prediction model uses straightforward calculations involving key team and game factors to generate the performance score.
  
- **Game-Specific Factors**: 
  - The prediction accounts for contextual elements like team location (home/away), rest days, and weather, ensuring a more accurate outcome prediction.
