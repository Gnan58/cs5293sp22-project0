import argparse

import project0


def main(url):
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
