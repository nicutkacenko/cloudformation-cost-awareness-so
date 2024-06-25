import os
import json
import subprocess
import re
from collections import defaultdict

from lxml import etree

CHUNK_SIZE = 128 * 1024 * 1024  # 128 MB


def export_json(output_filename, data):
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)


def print_xml_incrementally(archive_path, xml_filename):
    # Command to stream the content of the XML file from the 7z archive
    command = ['7z', 'e', archive_path, xml_filename, '-so']

    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE) as process:
        context = etree.iterparse(process.stdout, events=('start', 'end'))
        depth = 0

        for event, elem in context:
            if event == 'start':
                print("  " * depth + f"<{elem.tag} {dict(elem.attrib)}>")
                depth += 1
            elif event == 'end':
                depth -= 1
                print("  " * depth + f"</{elem.tag}>")
                elem.clear()


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)

def summarize_xml_structure(archive_path, xml_filename):
    command = ['7z', 'e', archive_path, xml_filename, '-so']

    # The nested structure to hold the unique tags and attributes at each depth level
    structure = recursive_defaultdict()
    current_hierarchy = [structure]

    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE) as process:
        context = etree.iterparse(process.stdout, events=('start', 'end'))

        for event, elem in context:
            if event == 'start':
                if elem.tag not in current_hierarchy[-1]:
                    current_hierarchy[-1][elem.tag] = {"children": {}, "attributes": set()}
                    current_hierarchy[-1][elem.tag]["attributes"].update(elem.attrib.keys())
                    print(elem.tag + f"{current_hierarchy[-1][elem.tag]}")
                current_hierarchy.append(current_hierarchy[-1][elem.tag]["children"])                
            elif event == 'end':
                current_hierarchy.pop()
                elem.clear()

    # Pretty print the resulting structure
    def pretty_print(d, indent=0):
        for key, value in d.items():
            print('  ' * indent + key, end="")
            if "attributes" in value and value["attributes"]:
                print(f" (Attributes: {', '.join(value['attributes'])})", end="")
            print()
            if "children" in value:
                pretty_print(value["children"], indent + 1)

    pretty_print(structure)


def print_xml_rows(archive_path, xml_filename, limit=5):
    command = ['7z', 'e', archive_path, xml_filename, '-so']

    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE) as process:
        context = etree.iterparse(process.stdout, events=('start', 'end'))
        depth = 0

        for event, elem in context:
            if limit < 0:
                break
            if event == 'start':
                print("  " * depth + f"<{elem.tag} {dict(elem.attrib)}>")
                depth += 1
                limit -= 1
            elif event == 'end':
                depth -= 1
                print("  " * depth + f"</{elem.tag}>")
                elem.clear()


def extract_posts(archive_path, xml_filename, filters):
    """
    Extract tags from the XML inside the 7z archive where the Tags attribute 
    contains the given tag_name. 

    :param archive_path: Path to the 7z archive.
    :param xml_filename: The filename of the XML inside the 7z archive.
    :param tag_name: The tag to search for in the Tags attribute.
    :return: A list of dictionaries where each dictionary is an extracted post with all its attributes.
    """
    command = ['7z', 'e', archive_path, xml_filename, '-so']

    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE) as process:
        context = etree.iterparse(process.stdout, events=('start', 'end'))

        for event, elem in context:
            if event == 'end' and elem.tag == 'row':
                if all(f[1](elem.attrib.get(f[0], '')) for f in filters):
                    yield dict(elem.attrib)
                elem.clear()


def get_post_ids(folder_path):
    pattern = r'post-(\d+)\.json'
    for filename in os.listdir(folder_path):
        match = re.match(pattern, filename)
        if match:
            yield match.group(1)


def extract_posts_section(archive_path, xml_filename, post_ids):
    command = ['7z', 'e', archive_path, xml_filename, '-so']

    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE) as process:
        context = etree.iterparse(process.stdout, events=('start', 'end'))

        for event, elem in context:
            if event == 'end' and elem.tag == 'row':
                pid = elem.attrib.get('PostId', '')
                if pid in post_ids:
                    yield (pid, dict(elem.attrib))
                elem.clear()


def update_posts(archive_path, xml_filename, posts_dir, section):
    post_ids = set(get_post_ids(posts_dir))
    for pid, comment in extract_posts_section(archive_path, xml_filename, post_ids):
        post_filename = os.path.join(posts_dir, f'post-{pid}.json')
        with open(post_filename) as f:
            post = json.load(f)
        if section not in post:
            post[section] = []
        post[section].append(comment)
        print(f"Updating {section} in post {pid}")
        export_json(post_filename, post)


def add_answers_to_question(questions_dir, answers_dir):
    answers_ids = set(get_post_ids(answers_dir))

    for aid in answers_ids:
        answer_filename = os.path.join(answers_dir, f'post-{aid}.json')
        with open(answer_filename) as f:
            answer = json.load(f)
        
        qid = answer['ParentId']
        question_filename = os.path.join(questions_dir, f'post-{qid}.json')
        with open(question_filename) as f:
            question = json.load(f)
        
        if 'answers' not in question:
            question['answers'] = []
        question['answers'].append(answer)
        print(f"Updating answers in question {qid}")
        export_json(question_filename, question)
