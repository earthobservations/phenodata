from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoData


def main():
    cdc_client = DwdCdcClient(ftp=FTPSession())
    client = DwdPhenoData(cdc=cdc_client, humanizer=None, dataset='immediate')
    stations = client.get_stations()
    print(stations)


if __name__ == '__main__':
    main()
