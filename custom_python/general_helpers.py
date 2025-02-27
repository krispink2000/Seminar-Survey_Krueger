import json
import datetime


def get_raw(path):
    """
    Loading json file with an inputted path and outputting dictionary.
    """
    with open(path, encoding="utf8") as f:
        temp = json.load(f)

    return temp


general_text = get_raw("_templates/global/global_text.json")


def get_display(j, variable_name, likert: bool = False):
    """
    input: j = dictionary generated from json file, variable_name = name of
    variable you want the label to be generated for as string
    output: label as string
    """
    if likert:
        names = []
        for i in j[variable_name]["labels"]:
            names.append(i)
        return names
    else:
        return j[variable_name]["label"]


def get_choices(j, variable_name, likert: bool = False):
    """
    Generating a list for choices so the size of the inputted choices is not
    fixed and you don't need to write down every choice.
    We cant just use the original list defined in the json file, because oTree
    needs a list in form of:
        [1, 'Low'],
        [2, 'Medium'],
        [3, 'High']]
    See https://otree.readthedocs.io/en/latest/forms.html
    Uses a specified dictionary of special values to set the right values in the
    fields.
    input: j = dictionary generated from json file, variable_name = name of
    variable you want the list of choices to be generated for as string
    output: list of choices in otree format
    """
    temp = []
    for count, _ in enumerate(j[variable_name]["choices"]):
        # if the choice is something with a special meaning, change value to
        # something custom
        if (
            j[variable_name]["choices"][count].lower()
            == general_text["no_knowledge"].lower()
        ):
            temp.append([-888, j[variable_name]["choices"][count]])
        elif (
            j[variable_name]["choices"][count].lower()
            == general_text["never_heard"].lower()
        ):
            temp.append([-777, j[variable_name]["choices"][count]])
        elif (
            j[variable_name]["choices"][count].lower()
            == general_text["not_specified"].lower()
        ):
            temp.append([-999, j[variable_name]["choices"][count]])
        elif likert:
            temp.append([count - 5, j[variable_name]["choices"][count]])
        else:
            # values start from 0!
            temp.append([count, j[variable_name]["choices"][count]])

    return temp


def make_field(
    path: str, variable_name: str, choices: bool = False, likert: bool = False
):
    """
    Extracts text from json files.
    input: path = valid path to json file, variable_name = name of variable you
    want the text to be extracted for as string,
    choices = set to true to also extract choices, likert = set to true to
    extract a list of labels
    output: label(s) as string or list of strings, list of choices in otree
    format
    """
    j = get_raw(path)

    if choices:
        x = get_display(j, variable_name)
        y = get_choices(j, variable_name)
        return x, y

    elif likert:
        x = get_display(j, variable_name, likert)
        y = get_choices(j, variable_name, likert)
        return x, y

    else:
        x = get_display(j, variable_name)
        return x


# helpers for quota
def calc_byear(age):
    return datetime.date.today().year - age
