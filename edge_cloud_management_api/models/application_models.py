from pydantic import UUID4, BaseModel, HttpUrl, Field
from typing import List, Optional
from ipaddress import IPv4Address, IPv6Address
from enum import Enum

from edge_cloud_management_api.models.edge_cloud_models import EdgeCloudZone


# Enum definitions
class PackageType(str, Enum):
    QCOW2 = "QCOW2"
    OVA = "OVA"
    CONTAINER = "CONTAINER"
    HELM = "HELM"


class VisibilityType(str, Enum):
    VISIBILITY_EXTERNAL = "VISIBILITY_EXTERNAL"
    VISIBILITY_INTERNAL = "VISIBILITY_INTERNAL"


class AppInstanceStatus(str, Enum):
    ready = "ready"
    instantiating = "instantiating"
    failed = "failed"
    terminating = "terminating"
    unknown = "unknown"


class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ANY = "ANY"


# Model definitions
class NetworkInterface(BaseModel):
    interfaceId: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{3,31}$")
    protocol: str  # [ TCP, UDP, ANY ]
    port: int  # minimum: 1, maximum: 65535
    visibilityType: str  # [ VISIBILITY_EXTERNAL, VISIBILITY_INTERNAL ]


class AccessEndpoint(BaseModel):
    port: int  # min 0
    fqdn: Optional[str]
    ipv4Addresses: Optional[List[IPv4Address]]  # minItems: 1
    ipv6Addresses: Optional[List[IPv6Address]]  # minItems: 1

    class Config:
        schema_extra = {
            "example": {
                "port": 8080,
                "fqdn": "example.com",
                "ipv4Addresses": ["192.168.0.1"],
                "ipv6Addresses": ["2001:db8::1"],
            }
        }


class ComponentEndpointInfo(BaseModel):
    interfaceId: UUID4  # string pattern: ^[A-Za-z0-9][A-Za-z0-9_]{6,30}[A-Za-z0-9]$
    accessPoints: AccessEndpoint


class AppInstanceInfo(BaseModel):
    appInstanceId: UUID4  # str = Field(..., regex=r"^[0-9a-fA-F-]{36}$")
    status: AppInstanceStatus = AppInstanceStatus.unknown  # [ ready, instantiating, failed, terminating, unknown ]
    componentEndpointInfo: List[ComponentEndpointInfo]
    kubernetesClusterRef: Optional[UUID4]
    edgeCloudZone: EdgeCloudZone


class ComponentSpec(BaseModel):
    componentName: str
    networkInterfaces: List[NetworkInterface]  # min one occurrence


class AppRepoAuthType(str, Enum):
    DOCKER = "DOCKER"
    HTTP_BASIC = "HTTP_BASIC"
    HTTP_BEARER = "HTTP_BEARER"
    NONE = "NONE"


class AppRepo(BaseModel):
    type: str  # [ PRIVATEREPO, PUBLICREPO ]
    imagePath: HttpUrl
    userName: Optional[str]
    credentials: Optional[str]  # maxLength: 128
    authType: Optional[AppRepoAuthType]
    checksum: Optional[str]  # MD5 checksum for VM and file-based images, sha256 digest for containers


class RequiredResources(BaseModel):
    numCPU: int
    memory: int
    storage: int


class OperatingSystem(BaseModel):
    architecture: str  # [ x86_64, x86 ]
    family: str  # [ RHEL, UBUNTU, COREOS, WINDOWS, OTHER ]
    version: str  # Version of the OS # [ OS_VERSION_UBUNTU_2204_LTS, OS_VERSION_RHEL_8, OS_MS_WINDOWS_2022, OTHER ]
    license: str  # License needed to activate the OS # [ OS_LICENSE_TYPE_FREE, OS_LICENSE_TYPE_ON_DEMAND, OTHER ]


class AppManifest(BaseModel):
    appId: Optional[UUID4]
    name: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{1,63}$")
    appProvider: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{7,63}$")
    version: str  # application version
    packageType: PackageType
    operatingSystem: Optional[OperatingSystem]
    appRepo: AppRepo
    requiredResources: RequiredResources
    componentSpec: List[ComponentSpec]


class AppZones(BaseModel):
    kubernetesClusterRef: Optional[UUID4]
    EdgeCloudZone: EdgeCloudZone


class AppInstance(BaseModel):
    appId: UUID4
    appZones: List[AppZones]


###########################
###########################
###########################
###########################
###########################
###########################
###########################
###########################
###########################
from pydantic import UUID4, BaseModel, HttpUrl, Field, StringConstraints
from typing import Annotated, List, Optional
from ipaddress import IPv4Address, IPv6Address
from enum import Enum

from edge_cloud_management_api.models.edge_cloud_models import EdgeCloudZone


class OperatingSystem(BaseModel):
    class OSArchitecture(str, Enum):
        x86_64 = "x86_64"
        x86 = "x86"

    class OSFamily(str, Enum):
        RHEL = "RHEL"
        UBUNTU = "UBUNTU"
        COREOS = "COREOS"
        WINDOWS = "WINDOWS"
        OTHER = "OTHER"

    class OSVersion(str, Enum):
        OS_VERSION_UBUNTU_2204_LTS = "OS_VERSION_UBUNTU_2204_LTS"
        OS_VERSION_RHEL_8 = "OS_VERSION_RHEL_8"
        OS_MS_WINDOWS_2022 = "OS_MS_WINDOWS_2022"
        OTHER = "OTHER"

    class OSLicense(str, Enum):
        OS_LICENSE_TYPE_FREE = "OS_LICENSE_TYPE_FREE"
        OS_LICENSE_TYPE_ON_DEMAND = "OS_LICENSE_TYPE_ON_DEMAND"
        OTHER = "OTHER"

    architecture: OSArchitecture
    family: OSFamily
    version: OSVersion
    license: OSLicense


class AppRepo(BaseModel):
    class AppRepoType(str, Enum):
        PRIVATEREPO = "PRIVATEREPO"
        PUBLICREPO = "PUBLICREPO"

    class AppRepoAuthType(str, Enum):
        DOCKER = "DOCKER"
        HTTP_BASIC = "HTTP_BASIC"
        HTTP_BEARER = "HTTP_BEARER"
        NONE = "NONE"

    type: AppRepoType
    imagePath: HttpUrl
    userName: Optional[str]
    credentials: Optional[Annotated[str, StringConstraints(max_length=128)]]
    authType: Optional[AppRepoAuthType]
    checksum: Optional[str]
    # MD5 checksum for VM and file-based images, sha256 digest for containers


from pydantic import BaseModel, Field
from typing import Union, Optional, List


class K8sNetworking(BaseModel):
    networkPolicy: Optional[str]
    serviceMesh: Optional[str]


class K8sAddons(BaseModel):
    monitoring: bool
    logging: bool
    autoscaling: bool


class GpuInfo(BaseModel):
    gpuCount: int
    gpuType: str


class AdditionalStorage(BaseModel):
    size: int  # in GB
    storageClass: Optional[str]


class RequiredResources(BaseModel):
    class KubernetesResources(BaseModel):
        infraKind: str = Field(..., description="Type of infrastructure: Kubernetes")
        applicationResources: dict
        isStandalone: bool
        version: Optional[str]
        additionalStorage: Optional[List[AdditionalStorage]]
        networking: Optional[K8sNetworking]
        addons: Optional[K8sAddons]

    class VmResources(BaseModel):
        infraKind: str = Field(..., description="Type of infrastructure: Virtual Machine")
        numCPU: int
        memory: int  # in MB
        additionalStorages: Optional[List[AdditionalStorage]]
        gpu: Optional[GpuInfo]

    class ContainerResources(BaseModel):
        infraKind: str = Field(..., description="Type of infrastructure: Container")
        numCPU: int
        memory: int  # in MB
        storage: Optional[AdditionalStorage]
        gpu: Optional[GpuInfo]

    class DockerComposeResources(BaseModel):
        infraKind: str = Field(..., description="Type of infrastructure: Docker Compose")
        numCPU: int
        memory: int  # in MB
        storage: Optional[AdditionalStorage]
        gpu: Optional[GpuInfo]

    __root__: Union[KubernetesResources, VmResources, ContainerResources, DockerComposeResources]


# class ComponentSpec(BaseModel):
#     class NetworkInterface(BaseModel):
#         interfaceId: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{3,31}$")
#         protocol: str  # [ TCP, UDP, ANY ]
#         port: int  # minimum: 1, maximum: 65535
#         visibilityType: str  # [ VISIBILITY_EXTERNAL, VISIBILITY_INTERNAL ]

#     componentName: str
#     networkInterfaces: List[NetworkInterface]  # min one occurrence


from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# Enums
class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ANY = "ANY"


class VisibilityType(str, Enum):
    VISIBILITY_EXTERNAL = "VISIBILITY_EXTERNAL"
    VISIBILITY_INTERNAL = "VISIBILITY_INTERNAL"


# Models
class NetworkInterface(BaseModel):
    interfaceId: str = Field(
        ...,
        regex=r"^[A-Za-z][A-Za-z0-9_]{3,31}$",
        description="Unique identifier for the network interface.",
    )
    protocol: Protocol = Field(..., description="IP transport communication protocol.")
    port: int = Field(..., ge=1, le=65535, description="Port number exposed by the component.")
    visibilityType: VisibilityType = Field(..., description="Defines whether the interface is external or internal.")


class ComponentSpec(BaseModel):
    componentName: str = Field(..., description="Unique name for the component within the application.")
    networkInterfaces: List[NetworkInterface] = Field(
        ...,
        min_items=1,
        description="List of network interfaces exposed by the component.",
    )


class AppManifest(BaseModel):
    class PackageType(str, Enum):
        QCOW2 = "QCOW2"
        OVA = "OVA"
        CONTAINER = "CONTAINER"
        HELM = "HELM"

    appId: Optional[UUID4]  # if not provided the backend has to create it
    name: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{1,63}$")
    appProvider: str = Field(..., regex=r"^[A-Za-z][A-Za-z0-9_]{7,63}$")
    version: str  # application version
    packageType: PackageType
    operatingSystem: Optional[OperatingSystem]
    appRepo: AppRepo
    requiredResources: RequiredResources
    componentSpec: List[ComponentSpec]
