"""Provide datapackage details specific to the EPA CEMS Hourly archives."""

from datetime import datetime, timezone
import re

from . import core
from . import licenses
from . import contributors
from pudl.metadata.classes import DataSource


def epacems_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file.

    Args:
        name (str): file name: must include a 4 digit year, and no other 4 digits.
        url (str): url to download the file from Zenodo.
        size (int): size it bytes.
        md5_hash (str): the md5 checksum of the file.

    Returns:
        frictionless datapackage file resource descriptor, per
        https://frictionlessdata.io/specs/data-resource/
    """
    match = re.search(r"([\d]{4})-([\w]{2})", name)

    if match is None:
        raise ValueError(f"Invalid filename {name}")

    year, state = match.groups()
    year = int(year)

    title, file_format = name.split(".")
    mt = core.MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "remote_url": url,
        "title": title,
        "parts": {"year": year, "state": state},
        "encoding": "utf-8",
        "mediatype": mt,
        "format": file_format,
        "bytes": size,
        "hash": md5_hash
    }


def datapackager(dfiles):
    """
    Produce the datapackage json for the epacems archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    resources = [epacems_resource(
        x["filename"],
        x["links"]["download"],
        x["filesize"], x["checksum"])

        for x in dfiles]

    return dict(**DataSource.from_id("epacems").to_raw_datapackage_dict(),
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})
