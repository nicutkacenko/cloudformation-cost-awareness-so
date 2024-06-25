import os
import shutil
import helper


def extract_tags(archives_dir, archives_dict, output_dir):
    ap = archives_dir+archives_dict["tags"]["archive_path"]
    xf = archives_dict["tags"]["xml_filename"]

    tags = [t for t in helper.extract_tags(ap, xf, "terraform")]
    helper.export_json(output_dir+"terraform-tags.json", tags)


def extract_posts(archives_dir, archives_dict, output_dir, filters):
    ap = archives_dir+archives_dict["posts"]["archive_path"]
    xf = archives_dict["posts"]["xml_filename"]

    for p in helper.extract_posts(ap, xf, filters):
        print(p["Id"])
        helper.export_json(f'{output_dir}post-{p["Id"]}.json', p)


def update_posts(archives_dir, archives_dict, dict_key, posts_dir, section):
    ap = archives_dir+archives_dict[dict_key]["archive_path"]
    xf = archives_dict[dict_key]["xml_filename"]

    helper.update_posts(ap, xf, posts_dir, section)


if __name__ == '__main__':
    data_files = {
        "posts": {"archive_path": "stackoverflow.com-Posts.7z", "xml_filename": "Posts.xml"},
        "comments": {"archive_path": "stackoverflow.com-Comments.7z", "xml_filename": "Comments.xml"},
        "posthistory": {"archive_path": "stackoverflow.com-PostHistory.7z", "xml_filename": "PostHistory.xml"},
    }
    os.makedirs(archives_dir := "../step-1-data/", exist_ok=True)
    os.makedirs(output_dir := "../step-1-output/", exist_ok=True)
    os.makedirs(output_questions := output_dir+"questions/", exist_ok=True)
    os.makedirs(output_answers := output_dir+"answers/", exist_ok=True)

    # Look into the archives
    # helper.print_xml_rows(output_dir+data_files["tags"]["archive_path"], data_files["posts"]["xml_filename"], 1)

    # STEP 1 - Extract question posts and associated data
    # question_filters = [
    #     ('PostTypeId', lambda x: x == '1'),
    #     ('Tags', lambda x: 'terraform' in x),
    # ]
    # extract_posts(archives_dir, data_files, output_questions, question_filters)
    # update_posts(archives_dir, data_files, "comments", output_questions, "comments")
    # update_posts(archives_dir, data_files, "posthistory", output_questions, "history")

    # STEP 2 - Extract answer posts and associated data
    # question_ids = set(helper.get_post_ids(output_questions))
    # answer_filters = [
    #     ('PostTypeId', lambda x: x == '2'),
    #     ('ParentId', lambda x: x in question_ids),
    # ]
    # extract_posts(archives_dir, data_files, output_answers, answer_filters)
    # update_posts(archives_dir, data_files, "comments", output_answers, "comments")
    # update_posts(archives_dir, data_files, "posthistory", output_answers, "history")

    # STEP 3 - Add answer posts to question posts and cleanup
    # helper.add_answers_to_question(output_questions, output_answers)
    # try:
    #     shutil.rmtree(output_answers)
    # except FileNotFoundError:
    #     pass
    