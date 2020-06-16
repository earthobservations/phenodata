from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoData


def main():
    cdc_client = DwdCdcClient(ftp=FTPSession())
    client = DwdPhenoData(cdc=cdc_client, humanizer=None, dataset='immediate')

    options = {

        'partition': 'recent',
        'filename': ['Hasel', 'Raps', 'Mais'],
        'year': [2018, 2019, 2020],

        # ID parameters
        'station-id': [13346],
        'species-id': None,
        'phase-id': None,
        'quality-level': None,
        'quality-byte': None,

        # Humanized parameters
        'station': None,
        'species': None,
        'phase': None,
        'quality': None,

    }
    observations = client.get_observations(options)
    print(observations)


if __name__ == '__main__':
    main()
