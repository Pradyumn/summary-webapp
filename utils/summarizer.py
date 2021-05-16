import tensorflow as tf
import pickle
from utils.model import Model
from utils.utils import build_dict, build_dataset, batch_iter

with open("./utils/args.pickle", "rb") as f:
    args = pickle.load(f)

word_dict, reversed_dict, article_max_len, summary_max_len = build_dict("valid", args.toy)

def getSummary(text):
    valid_x = build_dataset("string", word_dict, article_max_len, summary_max_len, args.toy, text)
    valid_x_len = [len([y for y in x if y != 0]) for x in valid_x]

    tf.reset_default_graph()
    with tf.Session() as sess:
        model = Model(reversed_dict, article_max_len, summary_max_len, args, forward_only=True)
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state("./utils/saved_model/")
        saver.restore(sess, ckpt.model_checkpoint_path)

        batches = batch_iter(valid_x, [0] * len(valid_x), args.batch_size, 1)
        
        for batch_x, _ in batches:
            batch_x_len = [len([y for y in x if y != 0]) for x in batch_x]

            valid_feed_dict = {
                model.batch_size: len(batch_x),
                model.X: batch_x,
                model.X_len: batch_x_len,
            }

            prediction = sess.run(model.prediction, feed_dict=valid_feed_dict)
            prediction_output = [[reversed_dict[y] for y in x] for x in prediction[:, 0, :]]

            
            for line in prediction_output:
                summary = list()
                for word in line:
                    if word == "</s>":
                        break
                    if word not in summary:
                        summary.append(word)
                
                return " ".join(summary)