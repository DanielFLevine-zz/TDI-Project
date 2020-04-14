import pandas as pd
import emotes
import re
import twokenize
import os


# A few functions for cleaning data.

def clean_dataframe(streamer):
    df = emotes.streamer_df(streamer)

    # Tokenize and clean data. Removes hyperlinks, non-ASCII characters, and rows with less than 5 tokens. Then lowercases all tokens.
    df['body'] = df['body'].apply(lambda x: twokenize.tokenizeRawTweetText(x))
    df['body'] = df['body'].apply(lambda x: [re.sub(r"http\S+", "", i) for i in x])
    df['body'] = df['body'].apply(lambda x: [re.sub(r'[^\x00-\x7F]', '', i) for i in x])
    indexNames = df[df['body'].str.len() <= 4].index
    df.drop(indexNames, inplace=True)
    df['body'] = df['body'].apply(lambda x: [i.lower() for i in x])

    # Grab global and streamer emotes and then lowercase them.
    X = emotes.global_streamer_emotes(streamer)
    X = [i.lower() for i in X]

    # Drop rows containing at least 2 distinct emotes.
    df['unique emotes'] = df['body'].apply(set)
    df['unique emotes'] = df['unique emotes'].apply(lambda x: x.intersection(set(X)))
    df['number of unique emotes'] = df['unique emotes'].apply(len)
    indexNames1 = df[df['number of unique emotes'] != 1].index
    df.drop(indexNames1, inplace=True)

    # Drop unnecessary (for now) columns.
    df = df.drop(['channel_id', 'commenter_id', 'commenter_type', 'created_at', 'fragments',
                  'offset', 'updated_at', 'video_id', 'number of unique emotes'], axis=1)

    # Turn unique emotes column into column of strings instead of set.
    df['unique emotes'] = df['unique emotes'].apply(lambda x: list(x)[0])

    # Remove identical messages (spam).
    df['body_str'] = df['body'].apply(lambda x: ' '.join(x))
    df = df.drop_duplicates(subset=['body_str'])
    df = df.drop(columns=['body_str'])

    return df


def clean_emote_count(streamer):

    df = clean_dataframe(streamer)
    # Grab list of emotes appearing in cleaned data.
    df['unique emotes'].nunique()
    Y = df['unique emotes'].unique()

    # One-hot encode labels
    for i in Y:
        df[i] = 0
    for i in Y:
        df.loc[df['unique emotes'] == i, i] = 1

    # Drop labels that do not meet threshold.
    emote_counts = []
    for i in Y:
        emote_counts = emote_counts+[[i, df[i].sum()]]
    return emote_counts


def emotes_to_labels(streamer, thresh):
    # thresh determines threshold for keeping emotes in list. For example, if thresh=100, then we only keep emotes that appear at least 100 times.

    df = clean_dataframe(streamer)

    # Grab list of emotes appearing in cleaned data.
    df['unique emotes'].nunique()
    Y = df['unique emotes'].unique()

    # One-hot encode labels
    for i in Y:
        df[i] = 0
    for i in Y:
        df.loc[df['unique emotes'] == i, i] = 1

    # Drop labels that do not meet threshold.
    emote_counts = []
    for i in Y:
        emote_counts = emote_counts+[[i, df[i].sum()]]

    keep_emotes = []
    keep_emotes = [emote_counts[i]
                   for i in range(len(emote_counts)) if emote_counts[i][1] >= thresh]

    drop_emotes = []
    drop_emotes = [emote_counts[i] for i in range(len(emote_counts)) if emote_counts[i][1] < thresh]
    for i in drop_emotes:
        df.drop(df[df[i[0]] == 1].index, inplace=True)

    df = df.drop([i[0] for i in drop_emotes], axis=1)

    # Remove emote from message and drop rows if they are empty after removing emotes.
    df['body'] = df['body'].apply(lambda x: [i for i in x if i not in Y])
    df['length'] = df['body'].apply(lambda x: len(x))
    df.drop(df[df['length'] == 0].index, inplace=True)

    # Drop unnecessary columns
    df = df.drop(['unique emotes', 'length'], axis=1)
    return df
