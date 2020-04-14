# TDI-Project

## Overview
This project is the first part of a larger project that aims to predict sentiment from Twitch chatrooms. Our goal here is to provide a simple example of how this can be done. We proceed by cleaning our data and using a two different models: a bidirection LSTM neural network and a branched neural network. The bidirectional LSTM NN is a rough implementation of what is described in [this article](https://pdfs.semanticscholar.org/1260/f76d10ec66dda257070ce4dcdbab800ec501.pdf) and the branched model is used in [this article](https://vermaabhi23.github.io/publication/2017UEMCON1.pdf). In the future, we will further explore model selection, optimize parameters, and develop a user interface to make the analysis accessible and digestible.

## Data
The data used and its documentation can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VE0IVQ).

## Tokenizer
We use the [CMU Noah's Ark tokenizer](http://www.cs.cmu.edu/~ark/TweetNLP/), called twokenizer. It was initially developed for twitter, and it is suggested in Barbieri's article (linked above) that a modified version can be useful for Twitch. The twokenize.py file was downloaded from [here](https://github.com/myleott/ark-twokenize-py).

## Cleaning data
We include a few data cleaning functions in preprocessing.py and emotes.py. We use an [API](https://dev.twitch.tv/docs/v5/reference/chat/#get-all-chat-emoticons) in order to get a list of emotes from Twitch for each streamer. Since the amount of data is very large, we can only access the list of emotes from one channel at a time.

## Evaluation of models
There is a short analysis at the end of each notebook evaluating the accuracy of the corresponding model.
