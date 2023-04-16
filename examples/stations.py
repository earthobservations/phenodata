"""
Example program how to use `phenodata` as a library to acquire station information.

https://github.com/earthobservations/phenodata
"""
import pandas as pd

from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoDataClient


def main():
    cdc_client = DwdCdcClient(ftp=FTPSession())
    client = DwdPhenoDataClient(cdc=cdc_client, dataset="immediate")
    stations: pd.DataFrame = client.get_stations()
    stations.info()
    print(stations)


if __name__ == '__main__':
    main()
