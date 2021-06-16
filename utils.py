from datatypes import AnswerSet
from os import listdir
import audiofile


# Process chunk of audio file
def read_chunk(smile, file, start, duration):
    signal, sampling_rate = audiofile.read(file, always_2d=True, offset=start, duration=duration)
    process = smile.process_signal(
        signal,
        sampling_rate
    )
    return process.values


#  Filter answers from annotation file
def read_groundtruth(file):
    with open(file) as f:
        answers = []
        w = 0
        b = 0
        g = 0
        for line in f.readlines():
            # Annotation
            answer_string = line.split()[2]

            # Save current dataset and reset data if walking sequence
            if answer_string[:1] == 'l':
                rows = line.split()
                answers.append(AnswerSet(int(w), int(b), g, float(rows[0]), float(rows[1])))
                w = 0
                b = 0
                g = 0
                continue

            # Parse answers
            sequence = answer_string[:2]
            if sequence == 'aw':
                w = answer_string[3:]
            elif sequence == 'ab':
                b = answer_string[3:]
            elif sequence == 'au':
                g = answer_string[3:]
        return answers


#  Create dict of wav filenames with according groundtruth
def create_dict(path):
    dict = {}
    for file in listdir(path):
        if file.endswith('.wav'):
            rects = read_groundtruth(path + file.split('.')[0] + '.txt')
            dict[path + file] = rects

    return dict
