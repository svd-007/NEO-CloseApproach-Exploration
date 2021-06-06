"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w', newline='') as outfile:

        writer = csv.DictWriter(outfile, fieldnames)

        writer.writeheader()

        if results:
            writer.writerows([
                {
                    fieldnames[0]: approach.time,
                    fieldnames[1]: approach.distance,
                    fieldnames[2]: approach.velocity,
                    fieldnames[3]: approach.neo.designation,
                    fieldnames[4]: approach.neo.name
                    if approach.neo.name else '',
                    fieldnames[5]: approach.neo.diameter
                    if approach.neo.diameter else 'nan',
                    fieldnames[6]: str(approach.neo.hazardous)
                }
                for approach in results
            ])


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output
    is a list containing dictionaries, each mapping `CloseApproach` attributes
    to their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    with open(filename, 'w') as outfile:

        json_data = json.dumps(
            [approach.serialize() for approach in results] if results else [],
            indent=2
        )

        outfile.write(json_data)
