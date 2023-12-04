import argparse
import pandas as pd
import json
from collections import defaultdict, Counter
import re
from pathlib import Path

STOPWORDS = {
    "a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", "already",
    "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything",
    "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b",
    "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before",
    "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came",
    "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did",
    "differ", "different", "differently", "do", "does", "done", "down", "down", "downed", "downing", "downs",
    "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly",
    "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts",
    "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further",
    "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given",
    "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped",
    "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "high",
    "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in",
    "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k",
    "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest",
    "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making",
    "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much",
    "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer",
    "newest", "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o",
    "of", "off", "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens",
    "or", "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted",
    "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible",
    "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r",
    "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second",
    "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show",
    "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some",
    "somebody", "someone", "something", "somewhere", "state", "states", "still", "still", "such", "sure", "t",
    "take", "taken", "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing",
    "things", "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to",
    "today", "together", "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until",
    "up", "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way",
    "ways", "we", "well", "wells", "went", "were", "what", "when", "where", "whether", "which", "while", "who",
    "whole", "whose", "why", "will", "with", "within", "without", "work", "worked", "working", "works", "would", "x",
    "y", "year", "years", "yet", "you", "young", "younger", "youngest", "your", "yours", "z"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", required=True, help="Output JSON file path")
    parser.add_argument("-d", required=True, help="Input CSV file path")
    args = parser.parse_args()

    dialog_data = pd.read_csv(args.d)

    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    stopwords = STOPWORDS

    word_counts = defaultdict(Counter)
    for _, row in dialog_data.iterrows():
        if row['pony'].lower() in ponies:
            dialogue = re.sub(r'[^\w\s]', ' ', row['dialog']).lower()
            words = [word for word in dialogue.split() if word.isalpha() and word not in stopwords]
            for word in words:
                word_counts[row['pony'].lower()][word] += 1

    for pony in ponies:
        word_counts[pony] = {word: count for word, count in word_counts[pony].items() if count >= 5}

    output_path = Path(args.o)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w') as json_file:
        json.dump(word_counts, json_file, indent=4)


if __name__ == "__main__":
    main()
