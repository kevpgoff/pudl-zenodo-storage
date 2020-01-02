# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import re

from . import licenses
from . import contributors
from . import mediatype

"""
Provide datapackage details specific to the Eia860 archives
"""

eia860_archive = {
    "name": "Eia860",
    "title": "Eia860",
    "description":
        "Form Eia860 data for electric power plants with 1 megawatt "
        "greater compbined nameplate capacity.",

    "profile": "data-package",
    "keywords": [
        "electricity", "electric", "boiler", "generator", "plant", "utility",
        "fuel", "coal", "natural gas", " prime mover", "eia860", "retirement",
        "capacity", "planned", "proposed", "energy", "hydro", "solar", "wind",
        "nuclear", "form 860", "eia", "annual", "gas", "ownership", "steam",
        "turbine", "combustion", "combined cycle", "eia",
        "energy information administration"
    ],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Energy Information Administration",
            "path": "https://www.eia.gov/electricity/data/eia860/"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def archive_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file

    Args:
        name: str, file name
        url: str, url to download the file from Zenodo
        size: int, size it bytes
        md5_hash: str, the md5 checksum of the file

    Return: None
    """
    match = re.search(r"([\d]{4})", name)

    if match is None:
        raise ValueError("No year present in filename %s" % name)

    year = int(match.groups()[0])
    title, file_format = name.split(".")
    mt = mediatype.MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "title": title,
        "parts": {"year": year},
        "encoding": "utf-8",
        "mediatype": mt,
        "format": file_format,
        "bytes": size,
        "hash": md5_hash
    }


def datapackager(dfiles):
    """Produce the datapackage json for the eia860 archival collection."""
    resources = [
        archive_resource(
            x["filename"],
            x["links"]["self"],
            x["filesize"], x["checksum"])
        for x in dfiles]

    return dict(**eia860_archive,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})