from pydantic import BaseModel, HttpUrl, Field  # , UUID4
from typing import Any, List, Optional
from enum import Enum
# from ipaddress import IPv4Address, IPv6Address

# from edge_cloud_management_api.models.edge_cloud_models import EdgeCloudZone


# Enum definitions


# class VisibilityType(str, Enum):
#     VISIBILITY_EXTERNAL = "VISIBILITY_EXTERNAL"
#     VISIBILITY_INTERNAL = "VISIBILITY_INTERNAL"


# class AppInstanceStatus(str, Enum):
#     ready = "ready"
#     instantiating = "instantiating"
#     failed = "failed"
#     terminating = "terminating"
#     unknown = "unknown"


# class Protocol(str, Enum):
#     TCP = "TCP"
#     UDP = "UDP"
#     ANY = "ANY"


# Model definitions

# class AccessEndpoint(BaseModel):
#     port: int  # min 0
#     fqdn: Optional[str]
#     ipv4Addresses: Optional[List[IPv4Address]]  # minItems: 1
#     ipv6Addresses: Optional[List[IPv6Address]]  # minItems: 1

#     class Config:
#         schema_extra = {
#             "example": {
#                 "port": 8080,
#                 "fqdn": "example.com",
#                 "ipv4Addresses": ["192.168.0.1"],
#                 "ipv6Addresses": ["2001:db8::1"],
#             }
#         }


# class ComponentEndpointInfo(BaseModel):
#     interfaceId: UUID4  # string pattern: ^[A-Za-z0-9][A-Za-z0-9_]{6,30}[A-Za-z0-9]$
#     accessPoints: AccessEndpoint


# class AppInstanceInfo(BaseModel):
#     appInstanceId: UUID4  # str = Field(..., regex=r"^[0-9a-fA-F-]{36}$")
#     status: AppInstanceStatus = AppInstanceStatus.unknown  # [ ready, instantiating, failed, terminating, unknown ]
#     componentEndpointInfo: List[ComponentEndpointInfo]
#     kubernetesClusterRef: Optional[UUID4]
#     edgeCloudZone: EdgeCloudZone


class NetworkInterface(BaseModel):
    interfaceId: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{3,31}$")
    protocol: str  # [ TCP, UDP, ANY ]
    port: int  # minimum: 1, maximum: 65535
    visibilityType: str  # [ VISIBILITY_EXTERNAL, VISIBILITY_INTERNAL ]


class ComponentSpec(BaseModel):
    componentName: str
    networkInterfaces: List[NetworkInterface]  # min one occurrence


class AppRepo(BaseModel):
    class AppRepoAuthType(str, Enum):
        DOCKER = "DOCKER"
        HTTP_BASIC = "HTTP_BASIC"
        HTTP_BEARER = "HTTP_BEARER"
        NONE = "NONE"

    type: str  # [ PRIVATEREPO, PUBLICREPO ]
    imagePath: HttpUrl
    userName: Optional[str]
    credentials: Optional[str]  # maxLength: 128
    authType: Optional[AppRepoAuthType]
    checksum: Optional[str]  # MD5 checksum for VM and file-based images, sha256 digest for containers


class AppManifest(BaseModel):
    class PackageType(str, Enum):
        QCOW2 = "QCOW2"
        OVA = "OVA"
        CONTAINER = "CONTAINER"
        HELM = "HELM"

    class OperatingSystem(BaseModel):
        architecture: str  # [ x86_64, x86 ]
        family: str  # [ RHEL, UBUNTU, COREOS, WINDOWS, OTHER ]
        version: str  # Version of the OS # [ OS_VERSION_UBUNTU_2204_LTS, OS_VERSION_RHEL_8, OS_MS_WINDOWS_2022, OTHER ]
        license: str  # License needed to activate the OS # [ OS_LICENSE_TYPE_FREE, OS_LICENSE_TYPE_ON_DEMAND, OTHER ]

    class RequiredResources(BaseModel):
        numCPU: int
        memory: int
        storage: int

    # appId: Optional[UUID4]
    name: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{1,63}$")
    appProvider: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]{7,63}$")
    version: str  # application version
    packageType: PackageType
    operatingSystem: Optional[OperatingSystem]
    appRepo: AppRepo
    requiredResources: Any  # Optional[RequiredResources]
    componentSpec: List[ComponentSpec]


# class AppZones(BaseModel):
#     kubernetesClusterRef: Optional[UUID4]
#     EdgeCloudZone: EdgeCloudZone


# class AppInstance(BaseModel):
#     appId: UUID4
#     appZones: List[AppZones]
