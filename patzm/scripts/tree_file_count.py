import os.path

import click
from tree_format import print_tree


def count_files(path):
    tree = dict()
    n_files = 0

    for node in os.scandir(path):
        if node.is_dir():
            node_files, node_tree = count_files(node.path)
            n_files += node_files
            tree[node.name] = (node_files, node_tree)
        elif node.is_file():
            n_files += 1
        else:
            pass

    return n_files, tree


def format_node(node):
    return "{name}: {n_files}".format(name=node[0], n_files=node[1])


def get_children(descending):
    # noinspection PyUnusedLocal
    def _get_children(node):
        tree = node[2]
        for node_name, (node_files, node_tree) in sorted(
            tree.items(), key=lambda x: x[1][0], reverse=descending
        ):
            yield (node_name, node_files, node_tree)

    return _get_children


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--sort",
    "-s",
    default="descending",
    type=click.Choice(["descending", "ascending"], case_sensitive=False),
    help="In which order to sort the folders.",
)
def ls_file_count(path: str, sort: str):
    """List the files under the root file PATH."""
    path = os.path.expanduser(path)
    n_files, tree_counted = count_files(path)

    descending = sort.lower() == "descending"
    print_tree(
        (path, n_files, tree_counted),
        format_node=format_node,
        get_children=get_children(descending),
    )
