import argparse
import json
import os
import uuid
import shutil
import os.path
from datetime import date
from datetime import timedelta


def main():
    config = get_config()
    init(config)
    populated_latex_src = populate_latex_src(config)
    populated_latex_file_name = create_populated_latex_file(populated_latex_src, config)
    compile_populated_latex_file(populated_latex_file_name)
    clean_up(populated_latex_file_name)
    shutil.move(config["output_file_name"] + ".pdf", "../")


def get_config():
    config_file_name = parse_args()["config"]
    config = {}
    with open(config_file_name) as config_file:
        config = json.load(config_file)
    config["output_file_name"] = get_output_file_name(config_file_name)
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    return vars(parser.parse_args())


def get_output_file_name(config_file_name):
    return config_file_name.replace("json", "").replace(".", "")


def init(config):
    file = config["output_file_name"] + ".pdf"
    os.path.isfile(file)
    if os.path.isfile(file):
        os.system(f"rm {file}")


def populate_latex_src(config):
    with open("src/src.tex", "r") as file:
        content = file.read()
    content = (
        content.replace("#bank_details#", config["bank_details"])
        .replace("#my_name#", get_my_name(config["address"]))
        .replace("#email#", config["email"])
        .replace("#phone#", config["phone"])
        .replace("#address#", make_latex_string(config["address"]))
        .replace("#client_name#", get_client_name(config["client_address"]))
        .replace("#client_address#", make_latex_string(config["client_address"]))
        .replace("#id#", str(uuid.uuid4())[:4])
        .replace("#due_date#", get_due_date())
        .replace("#current_date#", date.today().strftime("%d.%m.%Y"))
        .replace("#work_realized#", get_work_realized(config["work_realized"]))
        .replace("#payment_sum#", calculate_sum(config["work_realized"]))
        .replace("#custom_text#", config["custom_text"])
        .replace("#footer#", get_footer(config))
        .replace("#bank_details#", config["bank_details"])
    )
    return content


def get_client_name(client_address):
    return client_address[0]


def get_my_name(address):
    return address[0]


def get_due_date():
    return (date.today() + timedelta(days=14)).strftime("%d.%m.%Y")


def make_latex_string(arr):
    res = ""
    for item in arr:
        res += f"{item}\\\\"
    return res


def get_work_realized(work_realized):
    res = ""
    for item in work_realized:
        description = item["description"]
        payment = item["payment"]
        res += f"{description}& {payment} €\\\\"
    res += "~&~\\\\"
    sum = calculate_sum(work_realized)
    res += f"\\textbf{{SUMME}} & \\textbf{{{sum}}} €"
    return res


def calculate_sum(work_realized):
    sum = 0
    for item in work_realized:
        sum += int(item["payment"])
    return str(sum)


def get_footer(config):
    res = ""
    for item in config["address"]:
        res += item + " | "
    res += config["tax_id"] + " | "
    res += config["homepage"]
    return res


def create_populated_latex_file(content, config):
    file_name = config["output_file_name"] + ".tex"
    with open("src/" + file_name, "w") as the_file:
        the_file.write(content)

    return file_name


def compile_populated_latex_file(filename):
    os.chdir("src")
    os.system(f"xelatex {filename}")
    os.system(f"xelatex {filename}")


def clean_up(populated_latex_file_name):
    os.system("rm *.aux")
    os.system("rm *.log")
    os.system("rm *.out")
    os.system(f"rm {populated_latex_file_name}")


if __name__ == "__main__":
    main()
