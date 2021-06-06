"""Extract data on NEOs and Close Approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of
`NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import CloseApproach, NearEarthObject


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
    objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, "r") as infile:

        neos = csv.DictReader(infile)

        neos = [
            NearEarthObject(
                pdes=neo["pdes"],
                name=neo["name"],
                diameter=neo["diameter"],
                pha=neo["pha"]
            )
            for neo in neos
        ]

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close
    approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, "r") as infile:

        close_approaches = json.load(infile)

        idx_des = close_approaches["fields"].index("des")
        idx_cd = close_approaches["fields"].index("cd")
        idx_dist = close_approaches["fields"].index("dist")
        idx_v_rel = close_approaches["fields"].index("v_rel")

        close_approaches = [
            CloseApproach(
                des=close_approaches["data"][i][idx_des],
                cd=close_approaches["data"][i][idx_cd],
                dist=close_approaches["data"][i][idx_dist],
                v_rel=close_approaches["data"][i][idx_v_rel]
            )
            for i in range(int(close_approaches["count"]))
        ]

    return close_approaches
