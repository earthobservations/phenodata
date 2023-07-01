import asyncio
import logging
from pathlib import Path

import uvicorn
from datasette.app import Datasette
from datasette.cli import check_databases
from datasette.utils import SpatialiteNotFound, StartupError


logger = logging.getLogger(__name__)

here = Path(__file__).parent


def main():
    #datasette.cli.serve()

    files = ["phenodata-dwd-annual-recent.sqlite"]
    options = {"config_dir": here}
    #print("options:", options)
    #scsdc

    try:
        ds = Datasette(files, **options)
    except SpatialiteNotFound:
        raise IOError("Could not find SpatiaLite extension")
    except StartupError as e:
        raise IOError(e.args[0])

    # Run the "startup" plugin hooks
    asyncio.get_event_loop().run_until_complete(ds.invoke_startup())

    # Run async soundness checks - but only if we're not under pytest
    asyncio.get_event_loop().run_until_complete(check_databases(ds))

    url = None
    host = "localhost"
    port = 7777

    # Start the server
    url = "http://{}:{}{}?token={}".format(
        host, port, ds.urls.path("-/auth-token"), ds._root_token
    )
    logger.info(url)
    uvicorn_kwargs = dict(
        host=host, port=port, log_level="info", lifespan="on", workers=1
    )

    # Bind to a Unix domain socket
    #if uds:
    #    uvicorn_kwargs["uds"] = uds
    uvicorn.run(ds.app(), **uvicorn_kwargs)


if __name__ == "__main__":
    main()
