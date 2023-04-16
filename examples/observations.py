"""
Example program how to use `phenodata` as a library to acquire observation information.

https://github.com/earthobservations/phenodata
"""
import pandas as pd

from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoDataClient, DwdPhenoDataHumanizer


def main():
    cdc_client = DwdCdcClient(ftp=FTPSession())

    humanizer = DwdPhenoDataHumanizer(
        language="german",
        long_station=True,
        show_ids=True,
    )
    client = DwdPhenoDataClient(cdc=cdc_client, humanizer=humanizer, dataset="immediate")

    # Query and filtering options.
    options = {

        'partition': 'recent',
        'filename': ['Hasel', 'Raps', 'Mais'],
        'year': [2018, 2019, 2020],

        # ID parameters
        'station-id': [13346],
        #'species-id': None,
        #'phase-id': None,
        #'quality-level': None,
        #'quality-byte': None,

        # Humanized parameters
        #'station': None,
        #'species': None,
        #'phase': None,
        #'quality': None,

    }

    print("Observations - raw data")
    observations: pd.DataFrame = client.get_observations(options, humanize=False)
    observations.info()
    print(observations)

    print("Observations - resolved")
    observations: pd.DataFrame = client.get_observations(options, humanize=True)
    observations.info()
    print(observations)


if __name__ == '__main__':
    main()
