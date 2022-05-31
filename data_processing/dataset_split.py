# From https://github.com/JasonDing0401/ReVeal
import json
import random
import os

TRAIN = 0.8
VALID = 0.1
TEST = 0.1

def split_and_save(name, output, vuln, novuln, percent, balance=False):
    if balance:
        num_vuln = len(vuln)
        num_novuln = int(num_vuln * 100 / percent)
        novuln = novuln[:num_novuln]

    train_examples = []
    valid_examples = []
    test_examples = []

    num_vuln = len(vuln)
    num_train_vuln = int(num_vuln * TRAIN)
    num_valid_vuln = int(num_vuln * VALID)
    train_examples.extend(vuln[:num_train_vuln])
    valid_examples.extend(vuln[num_train_vuln:(num_train_vuln + num_valid_vuln)])
    test_examples.extend(vuln[(num_train_vuln + num_valid_vuln):])

    num_novuln = len(novuln)
    num_train_novuln = int(num_novuln * TRAIN)
    num_valid_novuln = int(num_novuln * VALID)
    train_examples.extend(novuln[:num_train_novuln])
    valid_examples.extend(novuln[num_train_novuln:(num_train_novuln + num_valid_novuln)])
    test_examples.extend(novuln[(num_train_novuln + num_valid_novuln):])

    final_vuln_percentage = int(num_vuln * 100 / (num_vuln + num_novuln))
    final_novuln_percentage = 100 - final_vuln_percentage
    file_name = os.path.join(output, name)
    if not balance:
        file_name = file_name + '-' + str(final_vuln_percentage) + '-' + str(final_novuln_percentage)
    if not os.path.exists(file_name):
        os.mkdir(file_name)

    for n, examples in zip(['train', 'valid', 'test'], [train_examples, valid_examples, test_examples]):
        f_name = os.path.join(
            file_name, n + '_GGNNinput.json' )
        print('Saving to, ' + f_name)
        with open(f_name, 'w') as fp:
            json.dump(examples, fp)
            fp.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path of the input file', required=True)
    parser.add_argument('--output', help='Output Directory', required=True)
    parser.add_argument('--percent', type=int, help='Percentage of vulnerable to all')
    parser.add_argument('--name', required=True)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        dataset = json.loads(f.read())

    random.shuffle(dataset)

    vuln = []
    novuln = []

    for dp in dataset:
        if dp['targets'][0][0] == 1:
            vuln.append(dp)
        else:
            novuln.append(dp)

    split_and_save(args.name, args.output, vuln, novuln, args.percent, args.percent != None)
