import argparse

import project0


def main(url):
    """
    Takes URL from command line and prints nature and its no of occurances from an incident summary report.

    Parameter
    ---------
    url : str
    """
    data = project0.getincidentsdata(url)
    incidentsRows = project0.extractincidentsdata(data)
    connection = project0.createdb()
    project0.populatedb(connection, incidentsRows)
    project0.status(connection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--incidents", type=str, required=True, help="Incident summary url."
    )
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
