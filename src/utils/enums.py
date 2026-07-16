"""
Application-wide enumerations.

Using enums prevents magic strings and ensures
consistent values across the application.
"""

from enum import Enum


class ProjectStatus(str, Enum):
    PLANNING = "Planning"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELLED = "Cancelled"


class EnumeratorStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    TRAINING = "Training"
    SUSPENDED = "Suspended"


class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class AlertPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class AlertStatus(str, Enum):
    OPEN = "Open"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class AlertType(str, Enum):
    MISSING_GPS = "Missing GPS"
    DUPLICATE_HOUSEHOLD = "Duplicate Household"
    SPEEDER = "Speeder"
    PROJECT_DELAY = "Project Delay"
    INACTIVE_ENUMERATOR = "Inactive Enumerator"
    OUTSIDE_GEOFENCE = "Outside Geofence"
    ML_ANOMALY = "ML Anomaly"
    DUPLICATE_DEVICE = "Duplicate Device"


class MLAlgorithm(str, Enum):
    ISOLATION_FOREST = "Isolation Forest"
    LOCAL_OUTLIER_FACTOR = "Local Outlier Factor"
    ECOD = "ECOD"
    COPOD = "COPOD"
    KNN = "KNN"