import argparse
import json
import os
import re
import subprocess


def __extract_by_dir(path_code, path_code_origin, regex_file, log_types):
    codes_correct = []
    codes_incorrect = []

    for content in os.listdir(path_code):
        path_content = os.path.join(path_code, content)

        if os.path.isfile(path_content):
            if re.search(regex_file, path_content):
                correct, incorrect = __extract_by_file(path_content, log_types)
                codes_correct.extend(correct)
                codes_incorrect.extend(incorrect)

        elif os.path.isdir(path_content):
            correct, incorrect = __extract_by_dir(path_content, path_code_origin, regex_file, log_types)
            codes_correct.extend(correct)
            codes_incorrect.extend(incorrect)

    return codes_correct, codes_incorrect


def __extract_by_file(path_file, log_types):
    data = subprocess.run(
        'ctags --output-format=json --format=2 --fields=+line ' + path_file,
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    objs = []

    for function in data.split('\n'):
        if function == '':
            continue

        function = json.loads(function)

        if function['kind'] != 'function':
            continue

        if 'scopeKind' not in function or function['scopeKind'] != 'class':
            continue

        objs.append({
            'class': function['scope'],
            'method': function['name'],
            'startInLine': function['line'],
            'endInLine': function['end'],
        })

    objs = sorted(objs, key=lambda x: x['startInLine'])

    with open(path_file, 'r') as f:
        linhas = f.readlines()

    codes_correct = []
    codes_incorrect = []

    for obj in objs:
        start_line = obj['startInLine']
        end_line = obj['endInLine']
        check = obj['class'] + "::" + obj['method']

        for i in range(start_line - 1, end_line):
            text = linhas[i]

            for log_type in log_types:
                is_ok = __extract_by_line(
                    text=text,
                    log_type=log_type,
                    check=check,
                )

                if is_ok is None:
                    continue

                class_name = obj['class']
                method_name = obj['method']
                method_lines = ["void " + class_name + "::" + method_name + " {", text.strip(), "}"]

                if is_ok:
                    codes_correct.append("\n".join(method_lines))
                else:
                    codes_incorrect.append("\n".join(method_lines))

    return codes_correct, codes_incorrect


def __extract_by_line(text, log_type, check):
    if log_type in text:
        text = text[text.index(log_type) + len(log_type + "() << \""):]

        if not re.search(check, text):
            return False

        return True

    return None


def __extract(path):
    return __extract_by_dir(
        path_code=path,
        path_code_origin=path,
        regex_file=".*\\.h|.*\\.cpp",
        log_types=[
            "qDebug",
            "qInfo",
            "qWarning",
            "qCritical"
        ],
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--PATH_TRAINING')
    parser.add_argument('--PATH_TESTING')

    args = parser.parse_args()

    extracted_correct_code, extracted_incorrect_code = __extract(args.PATH_TRAINING)

    with open("dados/correct.json", 'w') as file:
        json.dump(extracted_correct_code, file, indent=True)

    with open("dados/incorrect.json", 'w') as file:
        json.dump(extracted_incorrect_code, file, indent=True)

    extracted_correct_code, extracted_incorrect_code = __extract(args.PATH_TESTING)

    with open("dados/correct_testing.json", 'w') as file:
        json.dump(extracted_correct_code, file, indent=True)

    with open("dados/incorrect_testing.json", 'w') as file:
        json.dump(extracted_incorrect_code, file, indent=True)
