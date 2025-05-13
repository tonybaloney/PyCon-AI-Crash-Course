# PyCon US 2025 Tutorial - AI Crash Course for Python developers

This repo contains the exercises for Anthony Shaw's PyCon US Tutorial **AI Crash Course for Python Devs**

## Setup

You will need Jupyter to run these exercises. I recommend installing the [Jupyter Extension](https://marketplace.visualstudio.com/items/?itemName=ms-toolsai.jupyter) in VS Code if you don't already have a Jupyter environment

After that, you'll need to create a virtual environment and install the packages in `requirements.txt`

```bash
$ pip install -r requirements.txt
```

## Customizing Game Play

This repo contains multiple references to a made-up game. If you want to customize that game with your own, you'll need to:

1. Modify `utils/game.py` and change RULES
1. Modify `utils/game.py` and update `determine_winner_programmatically()` with your new logic
1. Run `make_training_data_csv()` in `utils/game.py` to make a new `utils/game_training.csv` file

Note this isn't required, but if you want to do this yourself later on.

