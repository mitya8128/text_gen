from textgenrnn import textgenrnn

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--epoches", help="number of epoches",
                    type=int)
parser.add_argument("--textgenrnn_use", help="use of textgenrnn library",
                    type=bool)

args = parser.parse_args()
num_epoches = args.epoches
textgenrnn_use = args.textgenrnn_use


if textgenrnn_use:
    textgen = textgenrnn()
    textgen.train_from_file('data/base_train.txt', num_epochs=num_epoches)

else:
    pass
