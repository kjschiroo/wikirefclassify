import argparse
import mwparserfromhell as mwp
import csv
import sys
import re


def transform_ref_text(ref_text):
    wikicode = mwp.parse(ref_text)
    templates = wikicode.filter_templates()
    if len(templates) > 0:
        return _transform_template(templates[0])
    else:
        return _transform_free_text(ref_text)


def _transform_template(ref):
    ref_type = 'type-{0}'.format(str(ref.name).strip().replace(' ', '-').lower())
    param_names = []
    arg_vals = []
    all_wds = []
    for p in ref.params:
        name = str(p.name).strip()
        param_names.append('pn-{0}'.format(name))
        value = str(p.value).lower().strip()
        # Break values on dividing characters
        s_values = [v.strip() for v in re.split(r'[/.?\- \n\t\[\]\{\}]',
                                                value) if v != '']
        all_wds.extend(['wd-{0}'.format(v) for v in s_values])
        arg_vals.extend(['{0}-{1}'.format(name, v) for v in s_values])
    return ' '.join([ref_type] + param_names + arg_vals + all_wds)


def _transform_free_text(text):
    s_values = [v.strip() for v in re.split(r'[/.,?\- \n\t\[\]\{\}]',
                                            text.lower()) if v != '']
    return ['wd-{0}'.format(v) for v in s_values]


def transform_ref_text_set(ref_text_set):
    for ref_text in ref_text_set:
        yield transform_ref_text(ref_text)


def transform_file(infile, outfile):
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        writer.writerow([' '.join(transform_ref_text(row[1])), row[2]])


def main():
    parser = argparse.ArgumentParser(
                        description=("Pull out reference tags "
                                     "from provided wikitext"))
    parser.add_argument('-i',
                        '--infile',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('-o',
                        '--outfile',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()
    transform_file(args.infile,
                   args.outfile)


if __name__ == "__main__":
    main()
