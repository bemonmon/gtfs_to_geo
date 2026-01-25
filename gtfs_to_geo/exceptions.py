class GTFSError(Exception):
    """Base exception for GTFS-related errors."""
    pass


class MissingGTFSFileError(GTFSError):
    """Raised when a required GTFS file is missing."""
    pass


class InvalidGTFSError(GTFSError):
    """Raised when a GTFS file is invalid or missing required columns."""
    pass
