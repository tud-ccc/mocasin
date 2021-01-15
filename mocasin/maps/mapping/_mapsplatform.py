# ./_mapsplatform.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:9b7b05350f8acb999b73feb36b75095a07ddad48
# Generated 2017-10-18 13:36:26.375200 by PyXB version 1.2.6 using Python 3.5.2.final.0
# Namespace mapsPlatform

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9341f590-b3f8-11e7-ba5a-e03f49145db8')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('mapsPlatform', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


class IdType (pyxb.binding.datatypes.ID):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IdType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 9, 2)
    _Documentation = None
IdType._CF_pattern = pyxb.binding.facets.CF_pattern()
IdType._CF_pattern.addPattern(pattern='[a-zA-Z0-9_.]+')
IdType._InitializeFacetMap(IdType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IdType', IdType)
_module_typeBindings.IdType = IdType

class RefType (pyxb.binding.datatypes.IDREF):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 14, 2)
    _Documentation = None
RefType._CF_pattern = pyxb.binding.facets.CF_pattern()
RefType._CF_pattern.addPattern(pattern='[a-zA-Z0-9_.]+')
RefType._InitializeFacetMap(RefType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'RefType', RefType)
_module_typeBindings.RefType = RefType

class NameType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NameType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 19, 2)
    _Documentation = None
NameType._CF_pattern = pyxb.binding.facets.CF_pattern()
NameType._CF_pattern.addPattern(pattern='[a-zA-Z0-9_.]+')
NameType._InitializeFacetMap(NameType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NameType', NameType)
_module_typeBindings.NameType = NameType

class FlagListType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FlagListType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 24, 2)
    _Documentation = None
FlagListType._CF_pattern = pyxb.binding.facets.CF_pattern()
FlagListType._CF_pattern.addPattern(pattern='[a-zA-Z0-9_.,]+')
FlagListType._InitializeFacetMap(FlagListType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'FlagListType', FlagListType)
_module_typeBindings.FlagListType = FlagListType

class VersionType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VersionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 29, 2)
    _Documentation = None
VersionType._CF_pattern = pyxb.binding.facets.CF_pattern()
VersionType._CF_pattern.addPattern(pattern='[0-9.]+')
VersionType._InitializeFacetMap(VersionType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'VersionType', VersionType)
_module_typeBindings.VersionType = VersionType

class FileNameType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FileNameType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 34, 2)
    _Documentation = None
FileNameType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'FileNameType', FileNameType)
_module_typeBindings.FileNameType = FileNameType

class BooleanType (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BooleanType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 37, 2)
    _Documentation = None
BooleanType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'BooleanType', BooleanType)
_module_typeBindings.BooleanType = BooleanType

class MinMaxEqualType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MinMaxEqualType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 40, 2)
    _Documentation = None
MinMaxEqualType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=MinMaxEqualType)
MinMaxEqualType.min = MinMaxEqualType._CF_enumeration.addEnumeration(unicode_value='min', tag='min')
MinMaxEqualType.max = MinMaxEqualType._CF_enumeration.addEnumeration(unicode_value='max', tag='max')
MinMaxEqualType.equal = MinMaxEqualType._CF_enumeration.addEnumeration(unicode_value='equal', tag='equal')
MinMaxEqualType._InitializeFacetMap(MinMaxEqualType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'MinMaxEqualType', MinMaxEqualType)
_module_typeBindings.MinMaxEqualType = MinMaxEqualType

class PositiveIntType (pyxb.binding.datatypes.positiveInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PositiveIntType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 47, 2)
    _Documentation = None
PositiveIntType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PositiveIntType', PositiveIntType)
_module_typeBindings.PositiveIntType = PositiveIntType

class NonNegativeIntType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NonNegativeIntType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 50, 2)
    _Documentation = None
NonNegativeIntType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'NonNegativeIntType', NonNegativeIntType)
_module_typeBindings.NonNegativeIntType = NonNegativeIntType


class PositiveFloatType (pyxb.binding.datatypes.double):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PositiveFloatType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 53, 2)
    _Documentation = None
PositiveFloatType._CF_minExclusive = pyxb.binding.facets.CF_minExclusive(value=pyxb.binding.datatypes._fp(0.0), value_datatype=pyxb.binding.datatypes.double)
PositiveFloatType._InitializeFacetMap(PositiveFloatType._CF_minExclusive)
Namespace.addCategoryObject('typeBinding', 'PositiveFloatType', PositiveFloatType)
_module_typeBindings.PositiveFloatType = PositiveFloatType


class NonNegativeFloatType (pyxb.binding.datatypes.double):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NonNegativeFloatType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 58, 2)
    _Documentation = None
NonNegativeFloatType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.double(0.0), value_datatype=NonNegativeFloatType)
NonNegativeFloatType._InitializeFacetMap(NonNegativeFloatType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'NonNegativeFloatType', NonNegativeFloatType)
_module_typeBindings.NonNegativeFloatType = NonNegativeFloatType


class TimeUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TimeUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 66, 2)
    _Documentation = None
TimeUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TimeUnitType)
TimeUnitType.ps = TimeUnitType._CF_enumeration.addEnumeration(unicode_value='ps', tag='ps')
TimeUnitType.ns = TimeUnitType._CF_enumeration.addEnumeration(unicode_value='ns', tag='ns')
TimeUnitType.us = TimeUnitType._CF_enumeration.addEnumeration(unicode_value='us', tag='us')
TimeUnitType.ms = TimeUnitType._CF_enumeration.addEnumeration(unicode_value='ms', tag='ms')
TimeUnitType.s = TimeUnitType._CF_enumeration.addEnumeration(unicode_value='s', tag='s')
TimeUnitType._InitializeFacetMap(TimeUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'TimeUnitType', TimeUnitType)
_module_typeBindings.TimeUnitType = TimeUnitType


class CyclesUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CyclesUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 78, 2)
    _Documentation = None
CyclesUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CyclesUnitType)
CyclesUnitType.cycles = CyclesUnitType._CF_enumeration.addEnumeration(unicode_value='cycles', tag='cycles')
CyclesUnitType.kcycles = CyclesUnitType._CF_enumeration.addEnumeration(unicode_value='kcycles', tag='kcycles')
CyclesUnitType.Mcycles = CyclesUnitType._CF_enumeration.addEnumeration(unicode_value='Mcycles', tag='Mcycles')
CyclesUnitType._InitializeFacetMap(CyclesUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CyclesUnitType', CyclesUnitType)
_module_typeBindings.CyclesUnitType = CyclesUnitType


class FrequencyUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 88, 2)
    _Documentation = None
FrequencyUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=FrequencyUnitType)
FrequencyUnitType.Hz = FrequencyUnitType._CF_enumeration.addEnumeration(unicode_value='Hz', tag='Hz')
FrequencyUnitType.kHz = FrequencyUnitType._CF_enumeration.addEnumeration(unicode_value='kHz', tag='kHz')
FrequencyUnitType.MHz = FrequencyUnitType._CF_enumeration.addEnumeration(unicode_value='MHz', tag='MHz')
FrequencyUnitType.GHz = FrequencyUnitType._CF_enumeration.addEnumeration(unicode_value='GHz', tag='GHz')
FrequencyUnitType._InitializeFacetMap(FrequencyUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'FrequencyUnitType', FrequencyUnitType)
_module_typeBindings.FrequencyUnitType = FrequencyUnitType


class VoltageUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 99, 2)
    _Documentation = None
VoltageUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=VoltageUnitType)
VoltageUnitType.mV = VoltageUnitType._CF_enumeration.addEnumeration(unicode_value='mV', tag='mV')
VoltageUnitType.V = VoltageUnitType._CF_enumeration.addEnumeration(unicode_value='V', tag='V')
VoltageUnitType._InitializeFacetMap(VoltageUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'VoltageUnitType', VoltageUnitType)
_module_typeBindings.VoltageUnitType = VoltageUnitType


class CurrentUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CurrentUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 108, 2)
    _Documentation = None
CurrentUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CurrentUnitType)
CurrentUnitType.pA = CurrentUnitType._CF_enumeration.addEnumeration(unicode_value='pA', tag='pA')
CurrentUnitType.nA = CurrentUnitType._CF_enumeration.addEnumeration(unicode_value='nA', tag='nA')
CurrentUnitType.uA = CurrentUnitType._CF_enumeration.addEnumeration(unicode_value='uA', tag='uA')
CurrentUnitType.mA = CurrentUnitType._CF_enumeration.addEnumeration(unicode_value='mA', tag='mA')
CurrentUnitType.A = CurrentUnitType._CF_enumeration.addEnumeration(unicode_value='A', tag='A')
CurrentUnitType._InitializeFacetMap(CurrentUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CurrentUnitType', CurrentUnitType)
_module_typeBindings.CurrentUnitType = CurrentUnitType


class PowerUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PowerUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 120, 2)
    _Documentation = None
PowerUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=PowerUnitType)
PowerUnitType.pW = PowerUnitType._CF_enumeration.addEnumeration(unicode_value='pW', tag='pW')
PowerUnitType.nW = PowerUnitType._CF_enumeration.addEnumeration(unicode_value='nW', tag='nW')
PowerUnitType.uW = PowerUnitType._CF_enumeration.addEnumeration(unicode_value='uW', tag='uW')
PowerUnitType.mW = PowerUnitType._CF_enumeration.addEnumeration(unicode_value='mW', tag='mW')
PowerUnitType.W = PowerUnitType._CF_enumeration.addEnumeration(unicode_value='W', tag='W')
PowerUnitType._InitializeFacetMap(PowerUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'PowerUnitType', PowerUnitType)
_module_typeBindings.PowerUnitType = PowerUnitType


class CapacitanceUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CapacitanceUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 132, 2)
    _Documentation = None
CapacitanceUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CapacitanceUnitType)
CapacitanceUnitType.fF = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='fF', tag='fF')
CapacitanceUnitType.pF = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='pF', tag='pF')
CapacitanceUnitType.nF = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='nF', tag='nF')
CapacitanceUnitType.uF = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='uF', tag='uF')
CapacitanceUnitType.mF = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='mF', tag='mF')
CapacitanceUnitType.F = CapacitanceUnitType._CF_enumeration.addEnumeration(unicode_value='F', tag='F')
CapacitanceUnitType._InitializeFacetMap(CapacitanceUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CapacitanceUnitType', CapacitanceUnitType)
_module_typeBindings.CapacitanceUnitType = CapacitanceUnitType


class SizeUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SizeUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 145, 2)
    _Documentation = None
SizeUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=SizeUnitType)
SizeUnitType.bit = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='bit', tag='bit')
SizeUnitType.B = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='B', tag='B')
SizeUnitType.kB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='kB', tag='kB')
SizeUnitType.KiB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='KiB', tag='KiB')
SizeUnitType.MB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='MB', tag='MB')
SizeUnitType.MiB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='MiB', tag='MiB')
SizeUnitType.GB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='GB', tag='GB')
SizeUnitType.GiB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='GiB', tag='GiB')
SizeUnitType.TB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='TB', tag='TB')
SizeUnitType.TiB = SizeUnitType._CF_enumeration.addEnumeration(unicode_value='TiB', tag='TiB')
SizeUnitType._InitializeFacetMap(SizeUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'SizeUnitType', SizeUnitType)
_module_typeBindings.SizeUnitType = SizeUnitType


class DataRateUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataRateUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 162, 2)
    _Documentation = None
DataRateUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=DataRateUnitType)
DataRateUnitType.bits = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='bit/s', tag='bits')
DataRateUnitType.Bs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='B/s', tag='Bs')
DataRateUnitType.kBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='kB/s', tag='kBs')
DataRateUnitType.KiBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='KiB/s', tag='KiBs')
DataRateUnitType.MBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='MB/s', tag='MBs')
DataRateUnitType.MiBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='MiB/s', tag='MiBs')
DataRateUnitType.GBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='GB/s', tag='GBs')
DataRateUnitType.GiBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='GiB/s', tag='GiBs')
DataRateUnitType.TBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='TB/s', tag='TBs')
DataRateUnitType.TiBs = DataRateUnitType._CF_enumeration.addEnumeration(unicode_value='TiB/s', tag='TiBs')
DataRateUnitType._InitializeFacetMap(DataRateUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'DataRateUnitType', DataRateUnitType)
_module_typeBindings.DataRateUnitType = DataRateUnitType


class ThroughputUnitType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ThroughputUnitType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 179, 2)
    _Documentation = None
ThroughputUnitType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=ThroughputUnitType)
ThroughputUnitType.bitcycle = ThroughputUnitType._CF_enumeration.addEnumeration(unicode_value='bit/cycle', tag='bitcycle')
ThroughputUnitType.Bcycle = ThroughputUnitType._CF_enumeration.addEnumeration(unicode_value='B/cycle', tag='Bcycle')
ThroughputUnitType.kBcycle = ThroughputUnitType._CF_enumeration.addEnumeration(unicode_value='kB/cycle', tag='kBcycle')
ThroughputUnitType.KiBcycle = ThroughputUnitType._CF_enumeration.addEnumeration(unicode_value='KiB/cycle', tag='KiBcycle')
ThroughputUnitType._InitializeFacetMap(ThroughputUnitType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ThroughputUnitType', ThroughputUnitType)
_module_typeBindings.ThroughputUnitType = ThroughputUnitType


class AccessType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AccessType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 187, 2)
    _Documentation = None
AccessType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=AccessType)
AccessType.read = AccessType._CF_enumeration.addEnumeration(unicode_value='read', tag='read')
AccessType.write = AccessType._CF_enumeration.addEnumeration(unicode_value='write', tag='write')
AccessType._InitializeFacetMap(AccessType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'AccessType', AccessType)
_module_typeBindings.AccessType = AccessType


class AddressType (pyxb.binding.datatypes.hexBinary):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AddressType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 193, 2)
    _Documentation = None
AddressType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'AddressType', AddressType)
_module_typeBindings.AddressType = AddressType


class SchedulingAlgorithmType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulingAlgorithmType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 302, 2)
    _Documentation = None
SchedulingAlgorithmType._CF_pattern = pyxb.binding.facets.CF_pattern()
SchedulingAlgorithmType._CF_pattern.addPattern(pattern='FIFO')
SchedulingAlgorithmType._CF_pattern.addPattern(pattern='Priority')
SchedulingAlgorithmType._CF_pattern.addPattern(pattern='RoundRobin')
SchedulingAlgorithmType._CF_pattern.addPattern(pattern='[a-zA-Z0-9_]+[.][a-zA-Z0-9_]+')
SchedulingAlgorithmType._InitializeFacetMap(SchedulingAlgorithmType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'SchedulingAlgorithmType', SchedulingAlgorithmType)
_module_typeBindings.SchedulingAlgorithmType = SchedulingAlgorithmType


class CoherencyType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CoherencyType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 469, 2)
    _Documentation = None
CoherencyType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CoherencyType)
CoherencyType.hard = CoherencyType._CF_enumeration.addEnumeration(unicode_value='hard', tag='hard')
CoherencyType.soft = CoherencyType._CF_enumeration.addEnumeration(unicode_value='soft', tag='soft')
CoherencyType.none = CoherencyType._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
CoherencyType._InitializeFacetMap(CoherencyType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CoherencyType', CoherencyType)
_module_typeBindings.CoherencyType = CoherencyType


class ReplacementType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ReplacementType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 476, 2)
    _Documentation = None
ReplacementType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=ReplacementType)
ReplacementType.lru = ReplacementType._CF_enumeration.addEnumeration(unicode_value='lru', tag='lru')
ReplacementType.fifo = ReplacementType._CF_enumeration.addEnumeration(unicode_value='fifo', tag='fifo')
ReplacementType.random = ReplacementType._CF_enumeration.addEnumeration(unicode_value='random', tag='random')
ReplacementType._InitializeFacetMap(ReplacementType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ReplacementType', ReplacementType)
_module_typeBindings.ReplacementType = ReplacementType


class PrefetchType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PrefetchType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 483, 2)
    _Documentation = None
PrefetchType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=PrefetchType)
PrefetchType.always = PrefetchType._CF_enumeration.addEnumeration(unicode_value='always', tag='always')
PrefetchType.never = PrefetchType._CF_enumeration.addEnumeration(unicode_value='never', tag='never')
PrefetchType.miss = PrefetchType._CF_enumeration.addEnumeration(unicode_value='miss', tag='miss')
PrefetchType.once = PrefetchType._CF_enumeration.addEnumeration(unicode_value='once', tag='once')
PrefetchType._InitializeFacetMap(PrefetchType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'PrefetchType', PrefetchType)
_module_typeBindings.PrefetchType = PrefetchType


class WriteAllocateType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'WriteAllocateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 491, 2)
    _Documentation = None
WriteAllocateType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=WriteAllocateType)
WriteAllocateType.always = WriteAllocateType._CF_enumeration.addEnumeration(unicode_value='always', tag='always')
WriteAllocateType.never = WriteAllocateType._CF_enumeration.addEnumeration(unicode_value='never', tag='never')
WriteAllocateType.noFetch = WriteAllocateType._CF_enumeration.addEnumeration(unicode_value='noFetch', tag='noFetch')
WriteAllocateType._InitializeFacetMap(WriteAllocateType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'WriteAllocateType', WriteAllocateType)
_module_typeBindings.WriteAllocateType = WriteAllocateType


class WriteBackType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'WriteBackType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 498, 2)
    _Documentation = None
WriteBackType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=WriteBackType)
WriteBackType.always = WriteBackType._CF_enumeration.addEnumeration(unicode_value='always', tag='always')
WriteBackType.never = WriteBackType._CF_enumeration.addEnumeration(unicode_value='never', tag='never')
WriteBackType.noFetch = WriteBackType._CF_enumeration.addEnumeration(unicode_value='noFetch', tag='noFetch')
WriteBackType._InitializeFacetMap(WriteBackType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'WriteBackType', WriteBackType)
_module_typeBindings.WriteBackType = WriteBackType


class TimeValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TimeValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 63, 2)
    _Documentation = None
TimeValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'TimeValueType', TimeValueType)
_module_typeBindings.TimeValueType = TimeValueType


class CyclesValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CyclesValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 75, 2)
    _Documentation = None
CyclesValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'CyclesValueType', CyclesValueType)
_module_typeBindings.CyclesValueType = CyclesValueType


class FrequencyValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 85, 2)
    _Documentation = None
FrequencyValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'FrequencyValueType', FrequencyValueType)
_module_typeBindings.FrequencyValueType = FrequencyValueType


class VoltageValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 96, 2)
    _Documentation = None
VoltageValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'VoltageValueType', VoltageValueType)
_module_typeBindings.VoltageValueType = VoltageValueType


class CurrentValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CurrentValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 105, 2)
    _Documentation = None
CurrentValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'CurrentValueType', CurrentValueType)
_module_typeBindings.CurrentValueType = CurrentValueType


class PowerValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PowerValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 117, 2)
    _Documentation = None
PowerValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PowerValueType', PowerValueType)
_module_typeBindings.PowerValueType = PowerValueType


class CapacitanceValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CapacitanceValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 129, 2)
    _Documentation = None
CapacitanceValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'CapacitanceValueType', CapacitanceValueType)
_module_typeBindings.CapacitanceValueType = CapacitanceValueType


class SizeValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SizeValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 142, 2)
    _Documentation = None
SizeValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SizeValueType', SizeValueType)
_module_typeBindings.SizeValueType = SizeValueType


class DataRateValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataRateValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 159, 2)
    _Documentation = None
DataRateValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'DataRateValueType', DataRateValueType)
_module_typeBindings.DataRateValueType = DataRateValueType


class ThroughputValueType (NonNegativeFloatType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ThroughputValueType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 176, 2)
    _Documentation = None
ThroughputValueType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ThroughputValueType', ThroughputValueType)
_module_typeBindings.ThroughputValueType = ThroughputValueType


class VoltageFrequencyDomainConditionListType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageFrequencyDomainConditionListType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 268, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element VoltageDomainCondition uses Python identifier VoltageDomainCondition
    __VoltageDomainCondition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition'), 'VoltageDomainCondition', 'mapsPlatform_VoltageFrequencyDomainConditionListType_VoltageDomainCondition', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6), )

    
    VoltageDomainCondition = property(__VoltageDomainCondition.value, __VoltageDomainCondition.set, None, None)

    
    # Element FrequencyDomainCondition uses Python identifier FrequencyDomainCondition
    __FrequencyDomainCondition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition'), 'FrequencyDomainCondition', 'mapsPlatform_VoltageFrequencyDomainConditionListType_FrequencyDomainCondition', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6), )

    
    FrequencyDomainCondition = property(__FrequencyDomainCondition.value, __FrequencyDomainCondition.set, None, None)

    _ElementMap.update({
        __VoltageDomainCondition.name() : __VoltageDomainCondition,
        __FrequencyDomainCondition.name() : __FrequencyDomainCondition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.VoltageFrequencyDomainConditionListType = VoltageFrequencyDomainConditionListType
Namespace.addCategoryObject('typeBinding', 'VoltageFrequencyDomainConditionListType', VoltageFrequencyDomainConditionListType)



class VoltageFrequencyConditionListType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageFrequencyConditionListType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 294, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element VoltageCondition uses Python identifier VoltageCondition
    __VoltageCondition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VoltageCondition'), 'VoltageCondition', 'mapsPlatform_VoltageFrequencyConditionListType_VoltageCondition', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6), )

    
    VoltageCondition = property(__VoltageCondition.value, __VoltageCondition.set, None, None)

    
    # Element FrequencyCondition uses Python identifier FrequencyCondition
    __FrequencyCondition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FrequencyCondition'), 'FrequencyCondition', 'mapsPlatform_VoltageFrequencyConditionListType_FrequencyCondition', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6), )

    
    FrequencyCondition = property(__FrequencyCondition.value, __FrequencyCondition.set, None, None)

    
    # Element FrequencyVoltageCondition uses Python identifier FrequencyVoltageCondition
    __FrequencyVoltageCondition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition'), 'FrequencyVoltageCondition', 'mapsPlatform_VoltageFrequencyConditionListType_FrequencyVoltageCondition', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6), )

    
    FrequencyVoltageCondition = property(__FrequencyVoltageCondition.value, __FrequencyVoltageCondition.set, None, None)

    _ElementMap.update({
        __VoltageCondition.name() : __VoltageCondition,
        __FrequencyCondition.name() : __FrequencyCondition,
        __FrequencyVoltageCondition.name() : __FrequencyVoltageCondition
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.VoltageFrequencyConditionListType = VoltageFrequencyConditionListType
Namespace.addCategoryObject('typeBinding', 'VoltageFrequencyConditionListType', VoltageFrequencyConditionListType)



class CommunicationBufferType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommunicationBufferType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 763, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MemoryRef uses Python identifier MemoryRef
    __MemoryRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MemoryRef'), 'MemoryRef', 'mapsPlatform_CommunicationBufferType_MemoryRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 765, 6), )

    
    MemoryRef = property(__MemoryRef.value, __MemoryRef.set, None, None)

    
    # Element FifoRef uses Python identifier FifoRef
    __FifoRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FifoRef'), 'FifoRef', 'mapsPlatform_CommunicationBufferType_FifoRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 766, 6), )

    
    FifoRef = property(__FifoRef.value, __FifoRef.set, None, None)

    
    # Element CacheRef uses Python identifier CacheRef
    __CacheRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CacheRef'), 'CacheRef', 'mapsPlatform_CommunicationBufferType_CacheRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 767, 6), )

    
    CacheRef = property(__CacheRef.value, __CacheRef.set, None, None)

    _ElementMap.update({
        __MemoryRef.name() : __MemoryRef,
        __FifoRef.name() : __FifoRef,
        __CacheRef.name() : __CacheRef
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CommunicationBufferType = CommunicationBufferType
Namespace.addCategoryObject('typeBinding', 'CommunicationBufferType', CommunicationBufferType)



class CommunicationPhaseType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommunicationPhaseType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 770, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MemoryAccess uses Python identifier MemoryAccess
    __MemoryAccess = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MemoryAccess'), 'MemoryAccess', 'mapsPlatform_CommunicationPhaseType_MemoryAccess', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 772, 6), )

    
    MemoryAccess = property(__MemoryAccess.value, __MemoryAccess.set, None, None)

    
    # Element CacheAccess uses Python identifier CacheAccess
    __CacheAccess = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CacheAccess'), 'CacheAccess', 'mapsPlatform_CommunicationPhaseType_CacheAccess', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 773, 6), )

    
    CacheAccess = property(__CacheAccess.value, __CacheAccess.set, None, None)

    
    # Element FifoAccess uses Python identifier FifoAccess
    __FifoAccess = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FifoAccess'), 'FifoAccess', 'mapsPlatform_CommunicationPhaseType_FifoAccess', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 774, 6), )

    
    FifoAccess = property(__FifoAccess.value, __FifoAccess.set, None, None)

    
    # Element PhysicalLinkRef uses Python identifier PhysicalLinkRef
    __PhysicalLinkRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PhysicalLinkRef'), 'PhysicalLinkRef', 'mapsPlatform_CommunicationPhaseType_PhysicalLinkRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 775, 6), )

    
    PhysicalLinkRef = property(__PhysicalLinkRef.value, __PhysicalLinkRef.set, None, None)

    
    # Element DMAControllerRef uses Python identifier DMAControllerRef
    __DMAControllerRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DMAControllerRef'), 'DMAControllerRef', 'mapsPlatform_CommunicationPhaseType_DMAControllerRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 776, 6), )

    
    DMAControllerRef = property(__DMAControllerRef.value, __DMAControllerRef.set, None, None)

    
    # Element LogicalLinkRef uses Python identifier LogicalLinkRef
    __LogicalLinkRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'LogicalLinkRef'), 'LogicalLinkRef', 'mapsPlatform_CommunicationPhaseType_LogicalLinkRef', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 777, 6), )

    
    LogicalLinkRef = property(__LogicalLinkRef.value, __LogicalLinkRef.set, None, None)

    _ElementMap.update({
        __MemoryAccess.name() : __MemoryAccess,
        __CacheAccess.name() : __CacheAccess,
        __FifoAccess.name() : __FifoAccess,
        __PhysicalLinkRef.name() : __PhysicalLinkRef,
        __DMAControllerRef.name() : __DMAControllerRef,
        __LogicalLinkRef.name() : __LogicalLinkRef
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CommunicationPhaseType = CommunicationPhaseType
Namespace.addCategoryObject('typeBinding', 'CommunicationPhaseType', CommunicationPhaseType)



class SubsystemPlatformType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubsystemPlatformType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 827, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Subsystem uses Python identifier Subsystem
    __Subsystem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Subsystem'), 'Subsystem', 'mapsPlatform_SubsystemPlatformType_Subsystem', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 829, 6), )

    
    Subsystem = property(__Subsystem.value, __Subsystem.set, None, None)

    
    # Element VoltageDomain uses Python identifier VoltageDomain
    __VoltageDomain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VoltageDomain'), 'VoltageDomain', 'mapsPlatform_SubsystemPlatformType_VoltageDomain', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 830, 6), )

    
    VoltageDomain = property(__VoltageDomain.value, __VoltageDomain.set, None, None)

    
    # Element FrequencyDomain uses Python identifier FrequencyDomain
    __FrequencyDomain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FrequencyDomain'), 'FrequencyDomain', 'mapsPlatform_SubsystemPlatformType_FrequencyDomain', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 831, 6), )

    
    FrequencyDomain = property(__FrequencyDomain.value, __FrequencyDomain.set, None, None)

    
    # Element SchedulingPolicyList uses Python identifier SchedulingPolicyList
    __SchedulingPolicyList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SchedulingPolicyList'), 'SchedulingPolicyList', 'mapsPlatform_SubsystemPlatformType_SchedulingPolicyList', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 832, 6), )

    
    SchedulingPolicyList = property(__SchedulingPolicyList.value, __SchedulingPolicyList.set, None, None)

    
    # Element Scheduler uses Python identifier Scheduler
    __Scheduler = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Scheduler'), 'Scheduler', 'mapsPlatform_SubsystemPlatformType_Scheduler', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 833, 6), )

    
    Scheduler = property(__Scheduler.value, __Scheduler.set, None, None)

    
    # Element ProcessorPowerModel uses Python identifier ProcessorPowerModel
    __ProcessorPowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessorPowerModel'), 'ProcessorPowerModel', 'mapsPlatform_SubsystemPlatformType_ProcessorPowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 834, 6), )

    
    ProcessorPowerModel = property(__ProcessorPowerModel.value, __ProcessorPowerModel.set, None, None)

    
    # Element Processor uses Python identifier Processor
    __Processor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Processor'), 'Processor', 'mapsPlatform_SubsystemPlatformType_Processor', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 835, 6), )

    
    Processor = property(__Processor.value, __Processor.set, None, None)

    
    # Element MemoryPowerModel uses Python identifier MemoryPowerModel
    __MemoryPowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MemoryPowerModel'), 'MemoryPowerModel', 'mapsPlatform_SubsystemPlatformType_MemoryPowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 836, 6), )

    
    MemoryPowerModel = property(__MemoryPowerModel.value, __MemoryPowerModel.set, None, None)

    
    # Element Memory uses Python identifier Memory
    __Memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Memory'), 'Memory', 'mapsPlatform_SubsystemPlatformType_Memory', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 837, 6), )

    
    Memory = property(__Memory.value, __Memory.set, None, None)

    
    # Element CachePowerModel uses Python identifier CachePowerModel
    __CachePowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CachePowerModel'), 'CachePowerModel', 'mapsPlatform_SubsystemPlatformType_CachePowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 838, 6), )

    
    CachePowerModel = property(__CachePowerModel.value, __CachePowerModel.set, None, None)

    
    # Element Cache uses Python identifier Cache
    __Cache = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Cache'), 'Cache', 'mapsPlatform_SubsystemPlatformType_Cache', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 839, 6), )

    
    Cache = property(__Cache.value, __Cache.set, None, None)

    
    # Element FifoPowerModel uses Python identifier FifoPowerModel
    __FifoPowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FifoPowerModel'), 'FifoPowerModel', 'mapsPlatform_SubsystemPlatformType_FifoPowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 840, 6), )

    
    FifoPowerModel = property(__FifoPowerModel.value, __FifoPowerModel.set, None, None)

    
    # Element Fifo uses Python identifier Fifo
    __Fifo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Fifo'), 'Fifo', 'mapsPlatform_SubsystemPlatformType_Fifo', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 841, 6), )

    
    Fifo = property(__Fifo.value, __Fifo.set, None, None)

    
    # Element PhysicalLinkPowerModel uses Python identifier PhysicalLinkPowerModel
    __PhysicalLinkPowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerModel'), 'PhysicalLinkPowerModel', 'mapsPlatform_SubsystemPlatformType_PhysicalLinkPowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 842, 6), )

    
    PhysicalLinkPowerModel = property(__PhysicalLinkPowerModel.value, __PhysicalLinkPowerModel.set, None, None)

    
    # Element PhysicalLink uses Python identifier PhysicalLink
    __PhysicalLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PhysicalLink'), 'PhysicalLink', 'mapsPlatform_SubsystemPlatformType_PhysicalLink', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 843, 6), )

    
    PhysicalLink = property(__PhysicalLink.value, __PhysicalLink.set, None, None)

    
    # Element DMAControllerPowerModel uses Python identifier DMAControllerPowerModel
    __DMAControllerPowerModel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerModel'), 'DMAControllerPowerModel', 'mapsPlatform_SubsystemPlatformType_DMAControllerPowerModel', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 844, 6), )

    
    DMAControllerPowerModel = property(__DMAControllerPowerModel.value, __DMAControllerPowerModel.set, None, None)

    
    # Element DMAController uses Python identifier DMAController
    __DMAController = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DMAController'), 'DMAController', 'mapsPlatform_SubsystemPlatformType_DMAController', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 845, 6), )

    
    DMAController = property(__DMAController.value, __DMAController.set, None, None)

    
    # Element LogicalLink uses Python identifier LogicalLink
    __LogicalLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'LogicalLink'), 'LogicalLink', 'mapsPlatform_SubsystemPlatformType_LogicalLink', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 846, 6), )

    
    LogicalLink = property(__LogicalLink.value, __LogicalLink.set, None, None)

    
    # Element Communication uses Python identifier Communication
    __Communication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Communication'), 'Communication', 'mapsPlatform_SubsystemPlatformType_Communication', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 847, 6), )

    
    Communication = property(__Communication.value, __Communication.set, None, None)

    
    # Element Peripheral uses Python identifier Peripheral
    __Peripheral = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Peripheral'), 'Peripheral', 'mapsPlatform_SubsystemPlatformType_Peripheral', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 848, 6), )

    
    Peripheral = property(__Peripheral.value, __Peripheral.set, None, None)

    _ElementMap.update({
        __Subsystem.name() : __Subsystem,
        __VoltageDomain.name() : __VoltageDomain,
        __FrequencyDomain.name() : __FrequencyDomain,
        __SchedulingPolicyList.name() : __SchedulingPolicyList,
        __Scheduler.name() : __Scheduler,
        __ProcessorPowerModel.name() : __ProcessorPowerModel,
        __Processor.name() : __Processor,
        __MemoryPowerModel.name() : __MemoryPowerModel,
        __Memory.name() : __Memory,
        __CachePowerModel.name() : __CachePowerModel,
        __Cache.name() : __Cache,
        __FifoPowerModel.name() : __FifoPowerModel,
        __Fifo.name() : __Fifo,
        __PhysicalLinkPowerModel.name() : __PhysicalLinkPowerModel,
        __PhysicalLink.name() : __PhysicalLink,
        __DMAControllerPowerModel.name() : __DMAControllerPowerModel,
        __DMAController.name() : __DMAController,
        __LogicalLink.name() : __LogicalLink,
        __Communication.name() : __Communication,
        __Peripheral.name() : __Peripheral
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SubsystemPlatformType = SubsystemPlatformType
Namespace.addCategoryObject('typeBinding', 'SubsystemPlatformType', SubsystemPlatformType)



class VoltageInputType (VoltageFrequencyDomainConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageInputType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 205, 2)
    _ElementMap = VoltageFrequencyDomainConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyDomainConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyDomainConditionListType
    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_VoltageInputType_voltageDomain', _module_typeBindings.RefType, required=True)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 208, 8)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 208, 8)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __voltageDomain.name() : __voltageDomain
    })
_module_typeBindings.VoltageInputType = VoltageInputType
Namespace.addCategoryObject('typeBinding', 'VoltageInputType', VoltageInputType)



class FrequencyInputType (VoltageFrequencyDomainConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyInputType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 232, 2)
    _ElementMap = VoltageFrequencyDomainConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyDomainConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyDomainConditionListType
    

    

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_FrequencyInputType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 235, 8)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 235, 8)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute factor uses Python identifier factor
    __factor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'factor'), 'factor', 'mapsPlatform_FrequencyInputType_factor', _module_typeBindings.PositiveFloatType, unicode_default='1')
    __factor._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 238, 8)
    __factor._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 238, 8)
    
    factor = property(__factor.value, __factor.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __frequencyDomain.name() : __frequencyDomain,
        __factor.name() : __factor
    })
_module_typeBindings.FrequencyInputType = FrequencyInputType
Namespace.addCategoryObject('typeBinding', 'FrequencyInputType', FrequencyInputType)



class SchedulingPolicyListType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulingPolicyListType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 315, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SchedulingPolicy uses Python identifier SchedulingPolicy
    __SchedulingPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SchedulingPolicy'), 'SchedulingPolicy', 'mapsPlatform_SchedulingPolicyListType_SchedulingPolicy', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 317, 6), )

    
    SchedulingPolicy = property(__SchedulingPolicy.value, __SchedulingPolicy.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_SchedulingPolicyListType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 319, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 319, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __SchedulingPolicy.name() : __SchedulingPolicy
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.SchedulingPolicyListType = SchedulingPolicyListType
Namespace.addCategoryObject('typeBinding', 'SchedulingPolicyListType', SchedulingPolicyListType)



class SchedulerType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulerType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 321, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_SchedulerType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 322, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 322, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute schedulingPolicyList uses Python identifier schedulingPolicyList
    __schedulingPolicyList = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'schedulingPolicyList'), 'schedulingPolicyList', 'mapsPlatform_SchedulerType_schedulingPolicyList', _module_typeBindings.RefType, required=True)
    __schedulingPolicyList._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 323, 4)
    __schedulingPolicyList._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 323, 4)
    
    schedulingPolicyList = property(__schedulingPolicyList.value, __schedulingPolicyList.set, None, None)

    
    # Attribute maxTasks uses Python identifier maxTasks
    __maxTasks = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'maxTasks'), 'maxTasks', 'mapsPlatform_SchedulerType_maxTasks', _module_typeBindings.PositiveIntType)
    __maxTasks._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 326, 4)
    __maxTasks._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 326, 4)
    
    maxTasks = property(__maxTasks.value, __maxTasks.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __schedulingPolicyList.name() : __schedulingPolicyList,
        __maxTasks.name() : __maxTasks
    })
_module_typeBindings.SchedulerType = SchedulerType
Namespace.addCategoryObject('typeBinding', 'SchedulerType', SchedulerType)



class ProcessorRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 399, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute processor uses Python identifier processor
    __processor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processor'), 'processor', 'mapsPlatform_ProcessorRefType_processor', _module_typeBindings.RefType, required=True)
    __processor._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 400, 4)
    __processor._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 400, 4)
    
    processor = property(__processor.value, __processor.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __processor.name() : __processor
    })
_module_typeBindings.ProcessorRefType = ProcessorRefType
Namespace.addCategoryObject('typeBinding', 'ProcessorRefType', ProcessorRefType)



class MemoryRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MemoryRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 456, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute memory uses Python identifier memory
    __memory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', 'mapsPlatform_MemoryRefType_memory', _module_typeBindings.RefType, required=True)
    __memory._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 457, 4)
    __memory._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 457, 4)
    
    memory = property(__memory.value, __memory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __memory.name() : __memory
    })
_module_typeBindings.MemoryRefType = MemoryRefType
Namespace.addCategoryObject('typeBinding', 'MemoryRefType', MemoryRefType)



class CacheRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CacheRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 581, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute cache uses Python identifier cache
    __cache = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cache'), 'cache', 'mapsPlatform_CacheRefType_cache', _module_typeBindings.RefType, required=True)
    __cache._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 582, 4)
    __cache._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 582, 4)
    
    cache = property(__cache.value, __cache.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __cache.name() : __cache
    })
_module_typeBindings.CacheRefType = CacheRefType
Namespace.addCategoryObject('typeBinding', 'CacheRefType', CacheRefType)



class FifoRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FifoRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 645, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute fifo uses Python identifier fifo
    __fifo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'fifo'), 'fifo', 'mapsPlatform_FifoRefType_fifo', _module_typeBindings.RefType, required=True)
    __fifo._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 646, 4)
    __fifo._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 646, 4)
    
    fifo = property(__fifo.value, __fifo.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __fifo.name() : __fifo
    })
_module_typeBindings.FifoRefType = FifoRefType
Namespace.addCategoryObject('typeBinding', 'FifoRefType', FifoRefType)



class PhysicalLinkRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PhysicalLinkRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 696, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute physicalLink uses Python identifier physicalLink
    __physicalLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physicalLink'), 'physicalLink', 'mapsPlatform_PhysicalLinkRefType_physicalLink', _module_typeBindings.RefType, required=True)
    __physicalLink._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 697, 4)
    __physicalLink._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 697, 4)
    
    physicalLink = property(__physicalLink.value, __physicalLink.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __physicalLink.name() : __physicalLink
    })
_module_typeBindings.PhysicalLinkRefType = PhysicalLinkRefType
Namespace.addCategoryObject('typeBinding', 'PhysicalLinkRefType', PhysicalLinkRefType)



class DMAControllerRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DMAControllerRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 741, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute dmaController uses Python identifier dmaController
    __dmaController = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dmaController'), 'dmaController', 'mapsPlatform_DMAControllerRefType_dmaController', _module_typeBindings.RefType, required=True)
    __dmaController._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 742, 4)
    __dmaController._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 742, 4)
    
    dmaController = property(__dmaController.value, __dmaController.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __dmaController.name() : __dmaController
    })
_module_typeBindings.DMAControllerRefType = DMAControllerRefType
Namespace.addCategoryObject('typeBinding', 'DMAControllerRefType', DMAControllerRefType)



class LogicalLinkRefType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LogicalLinkRefType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 758, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute logicalLink uses Python identifier logicalLink
    __logicalLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logicalLink'), 'logicalLink', 'mapsPlatform_LogicalLinkRefType_logicalLink', _module_typeBindings.RefType, required=True)
    __logicalLink._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 759, 4)
    __logicalLink._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 759, 4)
    
    logicalLink = property(__logicalLink.value, __logicalLink.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __logicalLink.name() : __logicalLink
    })
_module_typeBindings.LogicalLinkRefType = LogicalLinkRefType
Namespace.addCategoryObject('typeBinding', 'LogicalLinkRefType', LogicalLinkRefType)



class CommunicationProducerType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommunicationProducerType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 780, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Buffer uses Python identifier Buffer
    __Buffer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Buffer'), 'Buffer', 'mapsPlatform_CommunicationProducerType_Buffer', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 782, 6), )

    
    Buffer = property(__Buffer.value, __Buffer.set, None, None)

    
    # Element Active uses Python identifier Active
    __Active = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Active'), 'Active', 'mapsPlatform_CommunicationProducerType_Active', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 783, 6), )

    
    Active = property(__Active.value, __Active.set, None, None)

    
    # Element Passive uses Python identifier Passive
    __Passive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Passive'), 'Passive', 'mapsPlatform_CommunicationProducerType_Passive', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 784, 6), )

    
    Passive = property(__Passive.value, __Passive.set, None, None)

    
    # Attribute processor uses Python identifier processor
    __processor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processor'), 'processor', 'mapsPlatform_CommunicationProducerType_processor', _module_typeBindings.RefType, required=True)
    __processor._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 786, 4)
    __processor._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 786, 4)
    
    processor = property(__processor.value, __processor.set, None, None)

    _ElementMap.update({
        __Buffer.name() : __Buffer,
        __Active.name() : __Active,
        __Passive.name() : __Passive
    })
    _AttributeMap.update({
        __processor.name() : __processor
    })
_module_typeBindings.CommunicationProducerType = CommunicationProducerType
Namespace.addCategoryObject('typeBinding', 'CommunicationProducerType', CommunicationProducerType)



class CommunicationConsumerType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommunicationConsumerType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 790, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Buffer uses Python identifier Buffer
    __Buffer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Buffer'), 'Buffer', 'mapsPlatform_CommunicationConsumerType_Buffer', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 792, 6), )

    
    Buffer = property(__Buffer.value, __Buffer.set, None, None)

    
    # Element Passive uses Python identifier Passive
    __Passive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Passive'), 'Passive', 'mapsPlatform_CommunicationConsumerType_Passive', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 793, 6), )

    
    Passive = property(__Passive.value, __Passive.set, None, None)

    
    # Element Active uses Python identifier Active
    __Active = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Active'), 'Active', 'mapsPlatform_CommunicationConsumerType_Active', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 794, 6), )

    
    Active = property(__Active.value, __Active.set, None, None)

    
    # Attribute processor uses Python identifier processor
    __processor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processor'), 'processor', 'mapsPlatform_CommunicationConsumerType_processor', _module_typeBindings.RefType, required=True)
    __processor._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 796, 4)
    __processor._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 796, 4)
    
    processor = property(__processor.value, __processor.set, None, None)

    _ElementMap.update({
        __Buffer.name() : __Buffer,
        __Passive.name() : __Passive,
        __Active.name() : __Active
    })
    _AttributeMap.update({
        __processor.name() : __processor
    })
_module_typeBindings.CommunicationConsumerType = CommunicationConsumerType
Namespace.addCategoryObject('typeBinding', 'CommunicationConsumerType', CommunicationConsumerType)



class CommunicationType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommunicationType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 800, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Buffer uses Python identifier Buffer
    __Buffer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Buffer'), 'Buffer', 'mapsPlatform_CommunicationType_Buffer', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 802, 6), )

    
    Buffer = property(__Buffer.value, __Buffer.set, None, None)

    
    # Element Producer uses Python identifier Producer
    __Producer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Producer'), 'Producer', 'mapsPlatform_CommunicationType_Producer', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 803, 6), )

    
    Producer = property(__Producer.value, __Producer.set, None, None)

    
    # Element Consumer uses Python identifier Consumer
    __Consumer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Consumer'), 'Consumer', 'mapsPlatform_CommunicationType_Consumer', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 804, 6), )

    
    Consumer = property(__Consumer.value, __Consumer.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_CommunicationType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 806, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 806, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute multicast uses Python identifier multicast
    __multicast = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'multicast'), 'multicast', 'mapsPlatform_CommunicationType_multicast', _module_typeBindings.BooleanType, required=True)
    __multicast._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 807, 4)
    __multicast._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 807, 4)
    
    multicast = property(__multicast.value, __multicast.set, None, None)

    
    # Attribute flags uses Python identifier flags
    __flags = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'flags'), 'flags', 'mapsPlatform_CommunicationType_flags', _module_typeBindings.FlagListType)
    __flags._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 808, 4)
    __flags._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 808, 4)
    
    flags = property(__flags.value, __flags.set, None, None)

    _ElementMap.update({
        __Buffer.name() : __Buffer,
        __Producer.name() : __Producer,
        __Consumer.name() : __Consumer
    })
    _AttributeMap.update({
        __id.name() : __id,
        __multicast.name() : __multicast,
        __flags.name() : __flags
    })
_module_typeBindings.CommunicationType = CommunicationType
Namespace.addCategoryObject('typeBinding', 'CommunicationType', CommunicationType)



class PeripheralEmulatorLibraryType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PeripheralEmulatorLibraryType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 811, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute library uses Python identifier library
    __library = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'library'), 'library', 'mapsPlatform_PeripheralEmulatorLibraryType_library', _module_typeBindings.FileNameType, required=True)
    __library._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 812, 4)
    __library._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 812, 4)
    
    library = property(__library.value, __library.set, None, None)

    
    # Attribute init uses Python identifier init
    __init = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'init'), 'init', 'mapsPlatform_PeripheralEmulatorLibraryType_init', _module_typeBindings.NameType, required=True)
    __init._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 813, 4)
    __init._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 813, 4)
    
    init = property(__init.value, __init.set, None, None)

    
    # Attribute exit uses Python identifier exit
    __exit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'exit'), 'exit', 'mapsPlatform_PeripheralEmulatorLibraryType_exit', _module_typeBindings.NameType, required=True)
    __exit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 814, 4)
    __exit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 814, 4)
    
    exit = property(__exit.value, __exit.set, None, None)

    
    # Attribute read uses Python identifier read
    __read = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'read'), 'read', 'mapsPlatform_PeripheralEmulatorLibraryType_read', _module_typeBindings.NameType, required=True)
    __read._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 815, 4)
    __read._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 815, 4)
    
    read = property(__read.value, __read.set, None, None)

    
    # Attribute write uses Python identifier write
    __write = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'write'), 'write', 'mapsPlatform_PeripheralEmulatorLibraryType_write', _module_typeBindings.NameType, required=True)
    __write._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 816, 4)
    __write._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 816, 4)
    
    write = property(__write.value, __write.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __library.name() : __library,
        __init.name() : __init,
        __exit.name() : __exit,
        __read.name() : __read,
        __write.name() : __write
    })
_module_typeBindings.PeripheralEmulatorLibraryType = PeripheralEmulatorLibraryType
Namespace.addCategoryObject('typeBinding', 'PeripheralEmulatorLibraryType', PeripheralEmulatorLibraryType)



class PeripheralType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PeripheralType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 818, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PeripheralEmulatorLibrary uses Python identifier PeripheralEmulatorLibrary
    __PeripheralEmulatorLibrary = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PeripheralEmulatorLibrary'), 'PeripheralEmulatorLibrary', 'mapsPlatform_PeripheralType_PeripheralEmulatorLibrary', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 820, 6), )

    
    PeripheralEmulatorLibrary = property(__PeripheralEmulatorLibrary.value, __PeripheralEmulatorLibrary.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_PeripheralType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 822, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 822, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute startAddress uses Python identifier startAddress
    __startAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'startAddress'), 'startAddress', 'mapsPlatform_PeripheralType_startAddress', _module_typeBindings.AddressType, required=True)
    __startAddress._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 823, 4)
    __startAddress._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 823, 4)
    
    startAddress = property(__startAddress.value, __startAddress.set, None, None)

    
    # Attribute endAddress uses Python identifier endAddress
    __endAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'endAddress'), 'endAddress', 'mapsPlatform_PeripheralType_endAddress', _module_typeBindings.AddressType, required=True)
    __endAddress._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 824, 4)
    __endAddress._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 824, 4)
    
    endAddress = property(__endAddress.value, __endAddress.set, None, None)

    _ElementMap.update({
        __PeripheralEmulatorLibrary.name() : __PeripheralEmulatorLibrary
    })
    _AttributeMap.update({
        __id.name() : __id,
        __startAddress.name() : __startAddress,
        __endAddress.name() : __endAddress
    })
_module_typeBindings.PeripheralType = PeripheralType
Namespace.addCategoryObject('typeBinding', 'PeripheralType', PeripheralType)



class SubsystemType (SubsystemPlatformType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubsystemType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 851, 2)
    _ElementMap = SubsystemPlatformType._ElementMap.copy()
    _AttributeMap = SubsystemPlatformType._AttributeMap.copy()
    # Base type is SubsystemPlatformType
    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_SubsystemType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 854, 8)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 854, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.SubsystemType = SubsystemType
Namespace.addCategoryObject('typeBinding', 'SubsystemType', SubsystemType)



class PlatformType (SubsystemPlatformType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PlatformType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 858, 2)
    _ElementMap = SubsystemPlatformType._ElementMap.copy()
    _AttributeMap = SubsystemPlatformType._AttributeMap.copy()
    # Base type is SubsystemPlatformType
    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', 'mapsPlatform_PlatformType_version', _module_typeBindings.VersionType, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 861, 8)
    __version._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 861, 8)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute generatorTarget uses Python identifier generatorTarget
    __generatorTarget = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'generatorTarget'), 'generatorTarget', 'mapsPlatform_PlatformType_generatorTarget', _module_typeBindings.NameType)
    __generatorTarget._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 862, 8)
    __generatorTarget._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 862, 8)
    
    generatorTarget = property(__generatorTarget.value, __generatorTarget.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __version.name() : __version,
        __generatorTarget.name() : __generatorTarget
    })
_module_typeBindings.PlatformType = PlatformType
Namespace.addCategoryObject('typeBinding', 'PlatformType', PlatformType)



class VoltageType (VoltageFrequencyDomainConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 197, 2)
    _ElementMap = VoltageFrequencyDomainConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyDomainConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyDomainConditionListType
    

    

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_VoltageType_value', _module_typeBindings.VoltageValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 200, 8)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 200, 8)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_VoltageType_unit', _module_typeBindings.VoltageUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 201, 8)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 201, 8)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.VoltageType = VoltageType
Namespace.addCategoryObject('typeBinding', 'VoltageType', VoltageType)



class VoltageDomainType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageDomainType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 214, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Voltage uses Python identifier Voltage
    __Voltage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Voltage'), 'Voltage', 'mapsPlatform_VoltageDomainType_Voltage', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 216, 6), )

    
    Voltage = property(__Voltage.value, __Voltage.set, None, None)

    
    # Element VoltageInput uses Python identifier VoltageInput
    __VoltageInput = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'VoltageInput'), 'VoltageInput', 'mapsPlatform_VoltageDomainType_VoltageInput', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 217, 6), )

    
    VoltageInput = property(__VoltageInput.value, __VoltageInput.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_VoltageDomainType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 219, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 219, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute switchTimeValue uses Python identifier switchTimeValue
    __switchTimeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchTimeValue'), 'switchTimeValue', 'mapsPlatform_VoltageDomainType_switchTimeValue', _module_typeBindings.TimeValueType, unicode_default='0')
    __switchTimeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 220, 4)
    __switchTimeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 220, 4)
    
    switchTimeValue = property(__switchTimeValue.value, __switchTimeValue.set, None, None)

    
    # Attribute switchTimeUnit uses Python identifier switchTimeUnit
    __switchTimeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchTimeUnit'), 'switchTimeUnit', 'mapsPlatform_VoltageDomainType_switchTimeUnit', _module_typeBindings.TimeUnitType, unicode_default='us')
    __switchTimeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 221, 4)
    __switchTimeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 221, 4)
    
    switchTimeUnit = property(__switchTimeUnit.value, __switchTimeUnit.set, None, None)

    _ElementMap.update({
        __Voltage.name() : __Voltage,
        __VoltageInput.name() : __VoltageInput
    })
    _AttributeMap.update({
        __id.name() : __id,
        __switchTimeValue.name() : __switchTimeValue,
        __switchTimeUnit.name() : __switchTimeUnit
    })
_module_typeBindings.VoltageDomainType = VoltageDomainType
Namespace.addCategoryObject('typeBinding', 'VoltageDomainType', VoltageDomainType)



class FrequencyType (VoltageFrequencyDomainConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 224, 2)
    _ElementMap = VoltageFrequencyDomainConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyDomainConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyDomainConditionListType
    

    

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_FrequencyType_value', _module_typeBindings.FrequencyValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 227, 8)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 227, 8)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_FrequencyType_unit', _module_typeBindings.FrequencyUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 228, 8)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 228, 8)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.FrequencyType = FrequencyType
Namespace.addCategoryObject('typeBinding', 'FrequencyType', FrequencyType)



class FrequencyDomainType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyDomainType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 242, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Frequency uses Python identifier Frequency
    __Frequency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Frequency'), 'Frequency', 'mapsPlatform_FrequencyDomainType_Frequency', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 244, 6), )

    
    Frequency = property(__Frequency.value, __Frequency.set, None, None)

    
    # Element FrequencyInput uses Python identifier FrequencyInput
    __FrequencyInput = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FrequencyInput'), 'FrequencyInput', 'mapsPlatform_FrequencyDomainType_FrequencyInput', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 245, 6), )

    
    FrequencyInput = property(__FrequencyInput.value, __FrequencyInput.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_FrequencyDomainType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 247, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 247, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute switchTimeValue uses Python identifier switchTimeValue
    __switchTimeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchTimeValue'), 'switchTimeValue', 'mapsPlatform_FrequencyDomainType_switchTimeValue', _module_typeBindings.TimeValueType, unicode_default='0')
    __switchTimeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 248, 4)
    __switchTimeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 248, 4)
    
    switchTimeValue = property(__switchTimeValue.value, __switchTimeValue.set, None, None)

    
    # Attribute switchTimeUnit uses Python identifier switchTimeUnit
    __switchTimeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchTimeUnit'), 'switchTimeUnit', 'mapsPlatform_FrequencyDomainType_switchTimeUnit', _module_typeBindings.TimeUnitType, unicode_default='us')
    __switchTimeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 249, 4)
    __switchTimeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 249, 4)
    
    switchTimeUnit = property(__switchTimeUnit.value, __switchTimeUnit.set, None, None)

    _ElementMap.update({
        __Frequency.name() : __Frequency,
        __FrequencyInput.name() : __FrequencyInput
    })
    _AttributeMap.update({
        __id.name() : __id,
        __switchTimeValue.name() : __switchTimeValue,
        __switchTimeUnit.name() : __switchTimeUnit
    })
_module_typeBindings.FrequencyDomainType = FrequencyDomainType
Namespace.addCategoryObject('typeBinding', 'FrequencyDomainType', FrequencyDomainType)



class VoltageDomainConditionType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageDomainConditionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 252, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_VoltageDomainConditionType_voltageDomain', _module_typeBindings.RefType, required=True)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 253, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 253, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute condition uses Python identifier condition
    __condition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'condition'), 'condition', 'mapsPlatform_VoltageDomainConditionType_condition', _module_typeBindings.MinMaxEqualType, required=True)
    __condition._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 256, 4)
    __condition._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 256, 4)
    
    condition = property(__condition.value, __condition.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_VoltageDomainConditionType_value', _module_typeBindings.VoltageValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 257, 4)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 257, 4)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_VoltageDomainConditionType_unit', _module_typeBindings.VoltageUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 258, 4)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 258, 4)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __voltageDomain.name() : __voltageDomain,
        __condition.name() : __condition,
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.VoltageDomainConditionType = VoltageDomainConditionType
Namespace.addCategoryObject('typeBinding', 'VoltageDomainConditionType', VoltageDomainConditionType)



class FrequencyDomainConditionType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyDomainConditionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 260, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_FrequencyDomainConditionType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 261, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 261, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute condition uses Python identifier condition
    __condition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'condition'), 'condition', 'mapsPlatform_FrequencyDomainConditionType_condition', _module_typeBindings.MinMaxEqualType, required=True)
    __condition._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 264, 4)
    __condition._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 264, 4)
    
    condition = property(__condition.value, __condition.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_FrequencyDomainConditionType_value', _module_typeBindings.FrequencyValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 265, 4)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 265, 4)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_FrequencyDomainConditionType_unit', _module_typeBindings.FrequencyUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 266, 4)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 266, 4)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __frequencyDomain.name() : __frequencyDomain,
        __condition.name() : __condition,
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.FrequencyDomainConditionType = FrequencyDomainConditionType
Namespace.addCategoryObject('typeBinding', 'FrequencyDomainConditionType', FrequencyDomainConditionType)



class VoltageConditionType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoltageConditionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 275, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute condition uses Python identifier condition
    __condition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'condition'), 'condition', 'mapsPlatform_VoltageConditionType_condition', _module_typeBindings.MinMaxEqualType, required=True)
    __condition._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 277, 4)
    __condition._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 277, 4)
    
    condition = property(__condition.value, __condition.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_VoltageConditionType_value', _module_typeBindings.VoltageValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 278, 4)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 278, 4)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_VoltageConditionType_unit', _module_typeBindings.VoltageUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 279, 4)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 279, 4)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __condition.name() : __condition,
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.VoltageConditionType = VoltageConditionType
Namespace.addCategoryObject('typeBinding', 'VoltageConditionType', VoltageConditionType)



class FrequencyConditionType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyConditionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 281, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute condition uses Python identifier condition
    __condition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'condition'), 'condition', 'mapsPlatform_FrequencyConditionType_condition', _module_typeBindings.MinMaxEqualType, required=True)
    __condition._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 283, 4)
    __condition._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 283, 4)
    
    condition = property(__condition.value, __condition.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', 'mapsPlatform_FrequencyConditionType_value', _module_typeBindings.FrequencyValueType, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 284, 4)
    __value._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 284, 4)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute unit uses Python identifier unit
    __unit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unit'), 'unit', 'mapsPlatform_FrequencyConditionType_unit', _module_typeBindings.FrequencyUnitType, required=True)
    __unit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 285, 4)
    __unit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 285, 4)
    
    unit = property(__unit.value, __unit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __condition.name() : __condition,
        __value.name() : __value,
        __unit.name() : __unit
    })
_module_typeBindings.FrequencyConditionType = FrequencyConditionType
Namespace.addCategoryObject('typeBinding', 'FrequencyConditionType', FrequencyConditionType)



class FrequencyVoltageConditionType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FrequencyVoltageConditionType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 287, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute frequencyValue uses Python identifier frequencyValue
    __frequencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyValue'), 'frequencyValue', 'mapsPlatform_FrequencyVoltageConditionType_frequencyValue', _module_typeBindings.FrequencyValueType, required=True)
    __frequencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 289, 4)
    __frequencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 289, 4)
    
    frequencyValue = property(__frequencyValue.value, __frequencyValue.set, None, None)

    
    # Attribute frequencyUnit uses Python identifier frequencyUnit
    __frequencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyUnit'), 'frequencyUnit', 'mapsPlatform_FrequencyVoltageConditionType_frequencyUnit', _module_typeBindings.FrequencyUnitType, required=True)
    __frequencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 290, 4)
    __frequencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 290, 4)
    
    frequencyUnit = property(__frequencyUnit.value, __frequencyUnit.set, None, None)

    
    # Attribute voltageValue uses Python identifier voltageValue
    __voltageValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageValue'), 'voltageValue', 'mapsPlatform_FrequencyVoltageConditionType_voltageValue', _module_typeBindings.VoltageValueType, required=True)
    __voltageValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 291, 4)
    __voltageValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 291, 4)
    
    voltageValue = property(__voltageValue.value, __voltageValue.set, None, None)

    
    # Attribute voltageUnit uses Python identifier voltageUnit
    __voltageUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageUnit'), 'voltageUnit', 'mapsPlatform_FrequencyVoltageConditionType_voltageUnit', _module_typeBindings.VoltageUnitType, required=True)
    __voltageUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 292, 4)
    __voltageUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 292, 4)
    
    voltageUnit = property(__voltageUnit.value, __voltageUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __frequencyValue.name() : __frequencyValue,
        __frequencyUnit.name() : __frequencyUnit,
        __voltageValue.name() : __voltageValue,
        __voltageUnit.name() : __voltageUnit
    })
_module_typeBindings.FrequencyVoltageConditionType = FrequencyVoltageConditionType
Namespace.addCategoryObject('typeBinding', 'FrequencyVoltageConditionType', FrequencyVoltageConditionType)



class SchedulingPolicyType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulingPolicyType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 310, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute schedulingAlgorithm uses Python identifier schedulingAlgorithm
    __schedulingAlgorithm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'schedulingAlgorithm'), 'schedulingAlgorithm', 'mapsPlatform_SchedulingPolicyType_schedulingAlgorithm', _module_typeBindings.SchedulingAlgorithmType, required=True)
    __schedulingAlgorithm._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 311, 4)
    __schedulingAlgorithm._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 311, 4)
    
    schedulingAlgorithm = property(__schedulingAlgorithm.value, __schedulingAlgorithm.set, None, None)

    
    # Attribute timeSliceValue uses Python identifier timeSliceValue
    __timeSliceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timeSliceValue'), 'timeSliceValue', 'mapsPlatform_SchedulingPolicyType_timeSliceValue', _module_typeBindings.TimeValueType)
    __timeSliceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 312, 4)
    __timeSliceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 312, 4)
    
    timeSliceValue = property(__timeSliceValue.value, __timeSliceValue.set, None, None)

    
    # Attribute timeSliceUnit uses Python identifier timeSliceUnit
    __timeSliceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timeSliceUnit'), 'timeSliceUnit', 'mapsPlatform_SchedulingPolicyType_timeSliceUnit', _module_typeBindings.TimeUnitType, unicode_default='s')
    __timeSliceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 313, 4)
    __timeSliceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 313, 4)
    
    timeSliceUnit = property(__timeSliceUnit.value, __timeSliceUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __schedulingAlgorithm.name() : __schedulingAlgorithm,
        __timeSliceValue.name() : __timeSliceValue,
        __timeSliceUnit.name() : __timeSliceUnit
    })
_module_typeBindings.SchedulingPolicyType = SchedulingPolicyType
Namespace.addCategoryObject('typeBinding', 'SchedulingPolicyType', SchedulingPolicyType)



class ProcessorPowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorPowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 329, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_ProcessorPowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 332, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 332, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_ProcessorPowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 333, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 333, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_ProcessorPowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 334, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 334, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.ProcessorPowerStateType = ProcessorPowerStateType
Namespace.addCategoryObject('typeBinding', 'ProcessorPowerStateType', ProcessorPowerStateType)



class ProcessorPowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorPowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 338, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProcessorPowerState uses Python identifier ProcessorPowerState
    __ProcessorPowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessorPowerState'), 'ProcessorPowerState', 'mapsPlatform_ProcessorPowerModelType_ProcessorPowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 340, 6), )

    
    ProcessorPowerState = property(__ProcessorPowerState.value, __ProcessorPowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_ProcessorPowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 343, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 343, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_ProcessorPowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 344, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 344, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_ProcessorPowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 345, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 345, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 346, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 346, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 347, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 347, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute switchedCapacitanceIntAluValue uses Python identifier switchedCapacitanceIntAluValue
    __switchedCapacitanceIntAluValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntAluValue'), 'switchedCapacitanceIntAluValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntAluValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceIntAluValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 349, 4)
    __switchedCapacitanceIntAluValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 349, 4)
    
    switchedCapacitanceIntAluValue = property(__switchedCapacitanceIntAluValue.value, __switchedCapacitanceIntAluValue.set, None, None)

    
    # Attribute switchedCapacitanceIntAluUnit uses Python identifier switchedCapacitanceIntAluUnit
    __switchedCapacitanceIntAluUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntAluUnit'), 'switchedCapacitanceIntAluUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntAluUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceIntAluUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 350, 4)
    __switchedCapacitanceIntAluUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 350, 4)
    
    switchedCapacitanceIntAluUnit = property(__switchedCapacitanceIntAluUnit.value, __switchedCapacitanceIntAluUnit.set, None, None)

    
    # Attribute switchedCapacitanceIntMulValue uses Python identifier switchedCapacitanceIntMulValue
    __switchedCapacitanceIntMulValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntMulValue'), 'switchedCapacitanceIntMulValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntMulValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceIntMulValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 351, 4)
    __switchedCapacitanceIntMulValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 351, 4)
    
    switchedCapacitanceIntMulValue = property(__switchedCapacitanceIntMulValue.value, __switchedCapacitanceIntMulValue.set, None, None)

    
    # Attribute switchedCapacitanceIntMulUnit uses Python identifier switchedCapacitanceIntMulUnit
    __switchedCapacitanceIntMulUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntMulUnit'), 'switchedCapacitanceIntMulUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntMulUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceIntMulUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 352, 4)
    __switchedCapacitanceIntMulUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 352, 4)
    
    switchedCapacitanceIntMulUnit = property(__switchedCapacitanceIntMulUnit.value, __switchedCapacitanceIntMulUnit.set, None, None)

    
    # Attribute switchedCapacitanceIntDivValue uses Python identifier switchedCapacitanceIntDivValue
    __switchedCapacitanceIntDivValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntDivValue'), 'switchedCapacitanceIntDivValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntDivValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceIntDivValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 353, 4)
    __switchedCapacitanceIntDivValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 353, 4)
    
    switchedCapacitanceIntDivValue = property(__switchedCapacitanceIntDivValue.value, __switchedCapacitanceIntDivValue.set, None, None)

    
    # Attribute switchedCapacitanceIntDivUnit uses Python identifier switchedCapacitanceIntDivUnit
    __switchedCapacitanceIntDivUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceIntDivUnit'), 'switchedCapacitanceIntDivUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceIntDivUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceIntDivUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 354, 4)
    __switchedCapacitanceIntDivUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 354, 4)
    
    switchedCapacitanceIntDivUnit = property(__switchedCapacitanceIntDivUnit.value, __switchedCapacitanceIntDivUnit.set, None, None)

    
    # Attribute switchedCapacitanceFloatArithValue uses Python identifier switchedCapacitanceFloatArithValue
    __switchedCapacitanceFloatArithValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatArithValue'), 'switchedCapacitanceFloatArithValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatArithValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceFloatArithValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 355, 4)
    __switchedCapacitanceFloatArithValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 355, 4)
    
    switchedCapacitanceFloatArithValue = property(__switchedCapacitanceFloatArithValue.value, __switchedCapacitanceFloatArithValue.set, None, None)

    
    # Attribute switchedCapacitanceFloatArithUnit uses Python identifier switchedCapacitanceFloatArithUnit
    __switchedCapacitanceFloatArithUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatArithUnit'), 'switchedCapacitanceFloatArithUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatArithUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceFloatArithUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 356, 4)
    __switchedCapacitanceFloatArithUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 356, 4)
    
    switchedCapacitanceFloatArithUnit = property(__switchedCapacitanceFloatArithUnit.value, __switchedCapacitanceFloatArithUnit.set, None, None)

    
    # Attribute switchedCapacitanceFloatCompValue uses Python identifier switchedCapacitanceFloatCompValue
    __switchedCapacitanceFloatCompValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatCompValue'), 'switchedCapacitanceFloatCompValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatCompValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceFloatCompValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 357, 4)
    __switchedCapacitanceFloatCompValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 357, 4)
    
    switchedCapacitanceFloatCompValue = property(__switchedCapacitanceFloatCompValue.value, __switchedCapacitanceFloatCompValue.set, None, None)

    
    # Attribute switchedCapacitanceFloatCompUnit uses Python identifier switchedCapacitanceFloatCompUnit
    __switchedCapacitanceFloatCompUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatCompUnit'), 'switchedCapacitanceFloatCompUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatCompUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceFloatCompUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 358, 4)
    __switchedCapacitanceFloatCompUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 358, 4)
    
    switchedCapacitanceFloatCompUnit = property(__switchedCapacitanceFloatCompUnit.value, __switchedCapacitanceFloatCompUnit.set, None, None)

    
    # Attribute switchedCapacitanceFloatMulValue uses Python identifier switchedCapacitanceFloatMulValue
    __switchedCapacitanceFloatMulValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatMulValue'), 'switchedCapacitanceFloatMulValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatMulValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceFloatMulValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 359, 4)
    __switchedCapacitanceFloatMulValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 359, 4)
    
    switchedCapacitanceFloatMulValue = property(__switchedCapacitanceFloatMulValue.value, __switchedCapacitanceFloatMulValue.set, None, None)

    
    # Attribute switchedCapacitanceFloatMulUnit uses Python identifier switchedCapacitanceFloatMulUnit
    __switchedCapacitanceFloatMulUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatMulUnit'), 'switchedCapacitanceFloatMulUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatMulUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceFloatMulUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 360, 4)
    __switchedCapacitanceFloatMulUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 360, 4)
    
    switchedCapacitanceFloatMulUnit = property(__switchedCapacitanceFloatMulUnit.value, __switchedCapacitanceFloatMulUnit.set, None, None)

    
    # Attribute switchedCapacitanceFloatDivValue uses Python identifier switchedCapacitanceFloatDivValue
    __switchedCapacitanceFloatDivValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatDivValue'), 'switchedCapacitanceFloatDivValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatDivValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceFloatDivValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 361, 4)
    __switchedCapacitanceFloatDivValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 361, 4)
    
    switchedCapacitanceFloatDivValue = property(__switchedCapacitanceFloatDivValue.value, __switchedCapacitanceFloatDivValue.set, None, None)

    
    # Attribute switchedCapacitanceFloatDivUnit uses Python identifier switchedCapacitanceFloatDivUnit
    __switchedCapacitanceFloatDivUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceFloatDivUnit'), 'switchedCapacitanceFloatDivUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceFloatDivUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceFloatDivUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 362, 4)
    __switchedCapacitanceFloatDivUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 362, 4)
    
    switchedCapacitanceFloatDivUnit = property(__switchedCapacitanceFloatDivUnit.value, __switchedCapacitanceFloatDivUnit.set, None, None)

    
    # Attribute switchedCapacitanceLoadValue uses Python identifier switchedCapacitanceLoadValue
    __switchedCapacitanceLoadValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceLoadValue'), 'switchedCapacitanceLoadValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceLoadValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceLoadValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 363, 4)
    __switchedCapacitanceLoadValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 363, 4)
    
    switchedCapacitanceLoadValue = property(__switchedCapacitanceLoadValue.value, __switchedCapacitanceLoadValue.set, None, None)

    
    # Attribute switchedCapacitanceLoadUnit uses Python identifier switchedCapacitanceLoadUnit
    __switchedCapacitanceLoadUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceLoadUnit'), 'switchedCapacitanceLoadUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceLoadUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceLoadUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 364, 4)
    __switchedCapacitanceLoadUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 364, 4)
    
    switchedCapacitanceLoadUnit = property(__switchedCapacitanceLoadUnit.value, __switchedCapacitanceLoadUnit.set, None, None)

    
    # Attribute switchedCapacitanceStoreValue uses Python identifier switchedCapacitanceStoreValue
    __switchedCapacitanceStoreValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceStoreValue'), 'switchedCapacitanceStoreValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceStoreValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceStoreValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 365, 4)
    __switchedCapacitanceStoreValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 365, 4)
    
    switchedCapacitanceStoreValue = property(__switchedCapacitanceStoreValue.value, __switchedCapacitanceStoreValue.set, None, None)

    
    # Attribute switchedCapacitanceStoreUnit uses Python identifier switchedCapacitanceStoreUnit
    __switchedCapacitanceStoreUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceStoreUnit'), 'switchedCapacitanceStoreUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceStoreUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceStoreUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 366, 4)
    __switchedCapacitanceStoreUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 366, 4)
    
    switchedCapacitanceStoreUnit = property(__switchedCapacitanceStoreUnit.value, __switchedCapacitanceStoreUnit.set, None, None)

    
    # Attribute switchedCapacitanceControlValue uses Python identifier switchedCapacitanceControlValue
    __switchedCapacitanceControlValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceControlValue'), 'switchedCapacitanceControlValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceControlValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceControlValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 367, 4)
    __switchedCapacitanceControlValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 367, 4)
    
    switchedCapacitanceControlValue = property(__switchedCapacitanceControlValue.value, __switchedCapacitanceControlValue.set, None, None)

    
    # Attribute switchedCapacitanceControlUnit uses Python identifier switchedCapacitanceControlUnit
    __switchedCapacitanceControlUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceControlUnit'), 'switchedCapacitanceControlUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceControlUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceControlUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 368, 4)
    __switchedCapacitanceControlUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 368, 4)
    
    switchedCapacitanceControlUnit = property(__switchedCapacitanceControlUnit.value, __switchedCapacitanceControlUnit.set, None, None)

    
    # Attribute switchedCapacitanceOtherValue uses Python identifier switchedCapacitanceOtherValue
    __switchedCapacitanceOtherValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceOtherValue'), 'switchedCapacitanceOtherValue', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceOtherValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceOtherValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 369, 4)
    __switchedCapacitanceOtherValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 369, 4)
    
    switchedCapacitanceOtherValue = property(__switchedCapacitanceOtherValue.value, __switchedCapacitanceOtherValue.set, None, None)

    
    # Attribute switchedCapacitanceOtherUnit uses Python identifier switchedCapacitanceOtherUnit
    __switchedCapacitanceOtherUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceOtherUnit'), 'switchedCapacitanceOtherUnit', 'mapsPlatform_ProcessorPowerModelType_switchedCapacitanceOtherUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceOtherUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 370, 4)
    __switchedCapacitanceOtherUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 370, 4)
    
    switchedCapacitanceOtherUnit = property(__switchedCapacitanceOtherUnit.value, __switchedCapacitanceOtherUnit.set, None, None)

    _ElementMap.update({
        __ProcessorPowerState.name() : __ProcessorPowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __switchedCapacitanceIntAluValue.name() : __switchedCapacitanceIntAluValue,
        __switchedCapacitanceIntAluUnit.name() : __switchedCapacitanceIntAluUnit,
        __switchedCapacitanceIntMulValue.name() : __switchedCapacitanceIntMulValue,
        __switchedCapacitanceIntMulUnit.name() : __switchedCapacitanceIntMulUnit,
        __switchedCapacitanceIntDivValue.name() : __switchedCapacitanceIntDivValue,
        __switchedCapacitanceIntDivUnit.name() : __switchedCapacitanceIntDivUnit,
        __switchedCapacitanceFloatArithValue.name() : __switchedCapacitanceFloatArithValue,
        __switchedCapacitanceFloatArithUnit.name() : __switchedCapacitanceFloatArithUnit,
        __switchedCapacitanceFloatCompValue.name() : __switchedCapacitanceFloatCompValue,
        __switchedCapacitanceFloatCompUnit.name() : __switchedCapacitanceFloatCompUnit,
        __switchedCapacitanceFloatMulValue.name() : __switchedCapacitanceFloatMulValue,
        __switchedCapacitanceFloatMulUnit.name() : __switchedCapacitanceFloatMulUnit,
        __switchedCapacitanceFloatDivValue.name() : __switchedCapacitanceFloatDivValue,
        __switchedCapacitanceFloatDivUnit.name() : __switchedCapacitanceFloatDivUnit,
        __switchedCapacitanceLoadValue.name() : __switchedCapacitanceLoadValue,
        __switchedCapacitanceLoadUnit.name() : __switchedCapacitanceLoadUnit,
        __switchedCapacitanceStoreValue.name() : __switchedCapacitanceStoreValue,
        __switchedCapacitanceStoreUnit.name() : __switchedCapacitanceStoreUnit,
        __switchedCapacitanceControlValue.name() : __switchedCapacitanceControlValue,
        __switchedCapacitanceControlUnit.name() : __switchedCapacitanceControlUnit,
        __switchedCapacitanceOtherValue.name() : __switchedCapacitanceOtherValue,
        __switchedCapacitanceOtherUnit.name() : __switchedCapacitanceOtherUnit
    })
_module_typeBindings.ProcessorPowerModelType = ProcessorPowerModelType
Namespace.addCategoryObject('typeBinding', 'ProcessorPowerModelType', ProcessorPowerModelType)



class ProcessorType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 372, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DataCacheRef uses Python identifier DataCacheRef
    __DataCacheRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataCacheRef'), 'DataCacheRef', 'mapsPlatform_ProcessorType_DataCacheRef', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 374, 6), )

    
    DataCacheRef = property(__DataCacheRef.value, __DataCacheRef.set, None, None)

    
    # Element InstructionCacheRef uses Python identifier InstructionCacheRef
    __InstructionCacheRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'InstructionCacheRef'), 'InstructionCacheRef', 'mapsPlatform_ProcessorType_InstructionCacheRef', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 375, 6), )

    
    InstructionCacheRef = property(__InstructionCacheRef.value, __InstructionCacheRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_ProcessorType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 377, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 377, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute core uses Python identifier core
    __core = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'core'), 'core', 'mapsPlatform_ProcessorType_core', _module_typeBindings.NameType, required=True)
    __core._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 378, 4)
    __core._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 378, 4)
    
    core = property(__core.value, __core.set, None, None)

    
    # Attribute isHardware uses Python identifier isHardware
    __isHardware = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isHardware'), 'isHardware', 'mapsPlatform_ProcessorType_isHardware', _module_typeBindings.BooleanType, unicode_default='false')
    __isHardware._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 379, 4)
    __isHardware._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 379, 4)
    
    isHardware = property(__isHardware.value, __isHardware.set, None, None)

    
    # Attribute isAccelerator uses Python identifier isAccelerator
    __isAccelerator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isAccelerator'), 'isAccelerator', 'mapsPlatform_ProcessorType_isAccelerator', _module_typeBindings.BooleanType, unicode_default='false')
    __isAccelerator._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 380, 4)
    __isAccelerator._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 380, 4)
    
    isAccelerator = property(__isAccelerator.value, __isAccelerator.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_ProcessorType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 381, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 381, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute clockGating uses Python identifier clockGating
    __clockGating = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'clockGating'), 'clockGating', 'mapsPlatform_ProcessorType_clockGating', _module_typeBindings.BooleanType, required=True)
    __clockGating._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 384, 4)
    __clockGating._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 384, 4)
    
    clockGating = property(__clockGating.value, __clockGating.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_ProcessorType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 385, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 385, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute processorPowerModel uses Python identifier processorPowerModel
    __processorPowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processorPowerModel'), 'processorPowerModel', 'mapsPlatform_ProcessorType_processorPowerModel', _module_typeBindings.RefType)
    __processorPowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 388, 4)
    __processorPowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 388, 4)
    
    processorPowerModel = property(__processorPowerModel.value, __processorPowerModel.set, None, None)

    
    # Attribute scheduler uses Python identifier scheduler
    __scheduler = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'scheduler'), 'scheduler', 'mapsPlatform_ProcessorType_scheduler', _module_typeBindings.RefType)
    __scheduler._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 391, 4)
    __scheduler._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 391, 4)
    
    scheduler = property(__scheduler.value, __scheduler.set, None, None)

    
    # Attribute contextLoadValue uses Python identifier contextLoadValue
    __contextLoadValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'contextLoadValue'), 'contextLoadValue', 'mapsPlatform_ProcessorType_contextLoadValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __contextLoadValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 394, 4)
    __contextLoadValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 394, 4)
    
    contextLoadValue = property(__contextLoadValue.value, __contextLoadValue.set, None, None)

    
    # Attribute contextLoadUnit uses Python identifier contextLoadUnit
    __contextLoadUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'contextLoadUnit'), 'contextLoadUnit', 'mapsPlatform_ProcessorType_contextLoadUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __contextLoadUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 395, 4)
    __contextLoadUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 395, 4)
    
    contextLoadUnit = property(__contextLoadUnit.value, __contextLoadUnit.set, None, None)

    
    # Attribute contextStoreValue uses Python identifier contextStoreValue
    __contextStoreValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'contextStoreValue'), 'contextStoreValue', 'mapsPlatform_ProcessorType_contextStoreValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __contextStoreValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 396, 4)
    __contextStoreValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 396, 4)
    
    contextStoreValue = property(__contextStoreValue.value, __contextStoreValue.set, None, None)

    
    # Attribute contextStoreUnit uses Python identifier contextStoreUnit
    __contextStoreUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'contextStoreUnit'), 'contextStoreUnit', 'mapsPlatform_ProcessorType_contextStoreUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __contextStoreUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 397, 4)
    __contextStoreUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 397, 4)
    
    contextStoreUnit = property(__contextStoreUnit.value, __contextStoreUnit.set, None, None)

    _ElementMap.update({
        __DataCacheRef.name() : __DataCacheRef,
        __InstructionCacheRef.name() : __InstructionCacheRef
    })
    _AttributeMap.update({
        __id.name() : __id,
        __core.name() : __core,
        __isHardware.name() : __isHardware,
        __isAccelerator.name() : __isAccelerator,
        __frequencyDomain.name() : __frequencyDomain,
        __clockGating.name() : __clockGating,
        __voltageDomain.name() : __voltageDomain,
        __processorPowerModel.name() : __processorPowerModel,
        __scheduler.name() : __scheduler,
        __contextLoadValue.name() : __contextLoadValue,
        __contextLoadUnit.name() : __contextLoadUnit,
        __contextStoreValue.name() : __contextStoreValue,
        __contextStoreUnit.name() : __contextStoreUnit
    })
_module_typeBindings.ProcessorType = ProcessorType
Namespace.addCategoryObject('typeBinding', 'ProcessorType', ProcessorType)



class MemoryPowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MemoryPowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 406, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_MemoryPowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 409, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 409, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_MemoryPowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 410, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 410, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_MemoryPowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 411, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 411, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.MemoryPowerStateType = MemoryPowerStateType
Namespace.addCategoryObject('typeBinding', 'MemoryPowerStateType', MemoryPowerStateType)



class MemoryPowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MemoryPowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 415, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MemoryPowerState uses Python identifier MemoryPowerState
    __MemoryPowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MemoryPowerState'), 'MemoryPowerState', 'mapsPlatform_MemoryPowerModelType_MemoryPowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 417, 6), )

    
    MemoryPowerState = property(__MemoryPowerState.value, __MemoryPowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_MemoryPowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 420, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 420, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_MemoryPowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 421, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 421, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_MemoryPowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 422, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 422, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute cellLeakageCurrentValue uses Python identifier cellLeakageCurrentValue
    __cellLeakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentValue'), 'cellLeakageCurrentValue', 'mapsPlatform_MemoryPowerModelType_cellLeakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __cellLeakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 423, 4)
    __cellLeakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 423, 4)
    
    cellLeakageCurrentValue = property(__cellLeakageCurrentValue.value, __cellLeakageCurrentValue.set, None, None)

    
    # Attribute cellLeakageCurrentUnit uses Python identifier cellLeakageCurrentUnit
    __cellLeakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentUnit'), 'cellLeakageCurrentUnit', 'mapsPlatform_MemoryPowerModelType_cellLeakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __cellLeakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 424, 4)
    __cellLeakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 424, 4)
    
    cellLeakageCurrentUnit = property(__cellLeakageCurrentUnit.value, __cellLeakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_MemoryPowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 425, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 425, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_MemoryPowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 426, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 426, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute cellSwitchedCapacitanceValue uses Python identifier cellSwitchedCapacitanceValue
    __cellSwitchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceValue'), 'cellSwitchedCapacitanceValue', 'mapsPlatform_MemoryPowerModelType_cellSwitchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __cellSwitchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 427, 4)
    __cellSwitchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 427, 4)
    
    cellSwitchedCapacitanceValue = property(__cellSwitchedCapacitanceValue.value, __cellSwitchedCapacitanceValue.set, None, None)

    
    # Attribute cellSwitchedCapacitanceUnit uses Python identifier cellSwitchedCapacitanceUnit
    __cellSwitchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceUnit'), 'cellSwitchedCapacitanceUnit', 'mapsPlatform_MemoryPowerModelType_cellSwitchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __cellSwitchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 428, 4)
    __cellSwitchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 428, 4)
    
    cellSwitchedCapacitanceUnit = property(__cellSwitchedCapacitanceUnit.value, __cellSwitchedCapacitanceUnit.set, None, None)

    
    # Attribute readCapacitanceValue uses Python identifier readCapacitanceValue
    __readCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readCapacitanceValue'), 'readCapacitanceValue', 'mapsPlatform_MemoryPowerModelType_readCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __readCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 429, 4)
    __readCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 429, 4)
    
    readCapacitanceValue = property(__readCapacitanceValue.value, __readCapacitanceValue.set, None, None)

    
    # Attribute readCapacitanceUnit uses Python identifier readCapacitanceUnit
    __readCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readCapacitanceUnit'), 'readCapacitanceUnit', 'mapsPlatform_MemoryPowerModelType_readCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __readCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 430, 4)
    __readCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 430, 4)
    
    readCapacitanceUnit = property(__readCapacitanceUnit.value, __readCapacitanceUnit.set, None, None)

    
    # Attribute writeCapacitanceValue uses Python identifier writeCapacitanceValue
    __writeCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeCapacitanceValue'), 'writeCapacitanceValue', 'mapsPlatform_MemoryPowerModelType_writeCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __writeCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 431, 4)
    __writeCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 431, 4)
    
    writeCapacitanceValue = property(__writeCapacitanceValue.value, __writeCapacitanceValue.set, None, None)

    
    # Attribute writeCapacitanceUnit uses Python identifier writeCapacitanceUnit
    __writeCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeCapacitanceUnit'), 'writeCapacitanceUnit', 'mapsPlatform_MemoryPowerModelType_writeCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __writeCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 432, 4)
    __writeCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 432, 4)
    
    writeCapacitanceUnit = property(__writeCapacitanceUnit.value, __writeCapacitanceUnit.set, None, None)

    _ElementMap.update({
        __MemoryPowerState.name() : __MemoryPowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __cellLeakageCurrentValue.name() : __cellLeakageCurrentValue,
        __cellLeakageCurrentUnit.name() : __cellLeakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __cellSwitchedCapacitanceValue.name() : __cellSwitchedCapacitanceValue,
        __cellSwitchedCapacitanceUnit.name() : __cellSwitchedCapacitanceUnit,
        __readCapacitanceValue.name() : __readCapacitanceValue,
        __readCapacitanceUnit.name() : __readCapacitanceUnit,
        __writeCapacitanceValue.name() : __writeCapacitanceValue,
        __writeCapacitanceUnit.name() : __writeCapacitanceUnit
    })
_module_typeBindings.MemoryPowerModelType = MemoryPowerModelType
Namespace.addCategoryObject('typeBinding', 'MemoryPowerModelType', MemoryPowerModelType)



class MemoryType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MemoryType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 434, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_MemoryType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 435, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 435, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute sizeValue uses Python identifier sizeValue
    __sizeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sizeValue'), 'sizeValue', 'mapsPlatform_MemoryType_sizeValue', _module_typeBindings.SizeValueType, required=True)
    __sizeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 436, 4)
    __sizeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 436, 4)
    
    sizeValue = property(__sizeValue.value, __sizeValue.set, None, None)

    
    # Attribute sizeUnit uses Python identifier sizeUnit
    __sizeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sizeUnit'), 'sizeUnit', 'mapsPlatform_MemoryType_sizeUnit', _module_typeBindings.SizeUnitType, required=True)
    __sizeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 437, 4)
    __sizeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 437, 4)
    
    sizeUnit = property(__sizeUnit.value, __sizeUnit.set, None, None)

    
    # Attribute readThroughputValue uses Python identifier readThroughputValue
    __readThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readThroughputValue'), 'readThroughputValue', 'mapsPlatform_MemoryType_readThroughputValue', _module_typeBindings.ThroughputValueType)
    __readThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 438, 4)
    __readThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 438, 4)
    
    readThroughputValue = property(__readThroughputValue.value, __readThroughputValue.set, None, None)

    
    # Attribute readThroughputUnit uses Python identifier readThroughputUnit
    __readThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readThroughputUnit'), 'readThroughputUnit', 'mapsPlatform_MemoryType_readThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __readThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 439, 4)
    __readThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 439, 4)
    
    readThroughputUnit = property(__readThroughputUnit.value, __readThroughputUnit.set, None, None)

    
    # Attribute readLatencyValue uses Python identifier readLatencyValue
    __readLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readLatencyValue'), 'readLatencyValue', 'mapsPlatform_MemoryType_readLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __readLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 440, 4)
    __readLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 440, 4)
    
    readLatencyValue = property(__readLatencyValue.value, __readLatencyValue.set, None, None)

    
    # Attribute readLatencyUnit uses Python identifier readLatencyUnit
    __readLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readLatencyUnit'), 'readLatencyUnit', 'mapsPlatform_MemoryType_readLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __readLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 441, 4)
    __readLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 441, 4)
    
    readLatencyUnit = property(__readLatencyUnit.value, __readLatencyUnit.set, None, None)

    
    # Attribute writeThroughputValue uses Python identifier writeThroughputValue
    __writeThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeThroughputValue'), 'writeThroughputValue', 'mapsPlatform_MemoryType_writeThroughputValue', _module_typeBindings.ThroughputValueType)
    __writeThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 442, 4)
    __writeThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 442, 4)
    
    writeThroughputValue = property(__writeThroughputValue.value, __writeThroughputValue.set, None, None)

    
    # Attribute writeThroughputUnit uses Python identifier writeThroughputUnit
    __writeThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeThroughputUnit'), 'writeThroughputUnit', 'mapsPlatform_MemoryType_writeThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __writeThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 443, 4)
    __writeThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 443, 4)
    
    writeThroughputUnit = property(__writeThroughputUnit.value, __writeThroughputUnit.set, None, None)

    
    # Attribute writeLatencyValue uses Python identifier writeLatencyValue
    __writeLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeLatencyValue'), 'writeLatencyValue', 'mapsPlatform_MemoryType_writeLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __writeLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 444, 4)
    __writeLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 444, 4)
    
    writeLatencyValue = property(__writeLatencyValue.value, __writeLatencyValue.set, None, None)

    
    # Attribute writeLatencyUnit uses Python identifier writeLatencyUnit
    __writeLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeLatencyUnit'), 'writeLatencyUnit', 'mapsPlatform_MemoryType_writeLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __writeLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 445, 4)
    __writeLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 445, 4)
    
    writeLatencyUnit = property(__writeLatencyUnit.value, __writeLatencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_MemoryType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 446, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 446, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_MemoryType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 449, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 449, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute memoryPowerModel uses Python identifier memoryPowerModel
    __memoryPowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'memoryPowerModel'), 'memoryPowerModel', 'mapsPlatform_MemoryType_memoryPowerModel', _module_typeBindings.RefType)
    __memoryPowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 452, 4)
    __memoryPowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 452, 4)
    
    memoryPowerModel = property(__memoryPowerModel.value, __memoryPowerModel.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __sizeValue.name() : __sizeValue,
        __sizeUnit.name() : __sizeUnit,
        __readThroughputValue.name() : __readThroughputValue,
        __readThroughputUnit.name() : __readThroughputUnit,
        __readLatencyValue.name() : __readLatencyValue,
        __readLatencyUnit.name() : __readLatencyUnit,
        __writeThroughputValue.name() : __writeThroughputValue,
        __writeThroughputUnit.name() : __writeThroughputUnit,
        __writeLatencyValue.name() : __writeLatencyValue,
        __writeLatencyUnit.name() : __writeLatencyUnit,
        __frequencyDomain.name() : __frequencyDomain,
        __voltageDomain.name() : __voltageDomain,
        __memoryPowerModel.name() : __memoryPowerModel
    })
_module_typeBindings.MemoryType = MemoryType
Namespace.addCategoryObject('typeBinding', 'MemoryType', MemoryType)



class MemoryAccessType (MemoryRefType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MemoryAccessType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 461, 2)
    _ElementMap = MemoryRefType._ElementMap.copy()
    _AttributeMap = MemoryRefType._AttributeMap.copy()
    # Base type is MemoryRefType
    

    
    # Attribute access uses Python identifier access
    __access = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'access'), 'access', 'mapsPlatform_MemoryAccessType_access', _module_typeBindings.AccessType, required=True)
    __access._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 464, 8)
    __access._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 464, 8)
    
    access = property(__access.value, __access.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __access.name() : __access
    })
_module_typeBindings.MemoryAccessType = MemoryAccessType
Namespace.addCategoryObject('typeBinding', 'MemoryAccessType', MemoryAccessType)



class CachePowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CachePowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 506, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_CachePowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 509, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 509, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_CachePowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 510, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 510, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_CachePowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 511, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 511, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.CachePowerStateType = CachePowerStateType
Namespace.addCategoryObject('typeBinding', 'CachePowerStateType', CachePowerStateType)



class CachePowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CachePowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 515, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CachePowerState uses Python identifier CachePowerState
    __CachePowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CachePowerState'), 'CachePowerState', 'mapsPlatform_CachePowerModelType_CachePowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 517, 6), )

    
    CachePowerState = property(__CachePowerState.value, __CachePowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_CachePowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 520, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 520, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_CachePowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 521, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 521, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_CachePowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 522, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 522, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute cellLeakageCurrentValue uses Python identifier cellLeakageCurrentValue
    __cellLeakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentValue'), 'cellLeakageCurrentValue', 'mapsPlatform_CachePowerModelType_cellLeakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __cellLeakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 523, 4)
    __cellLeakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 523, 4)
    
    cellLeakageCurrentValue = property(__cellLeakageCurrentValue.value, __cellLeakageCurrentValue.set, None, None)

    
    # Attribute cellLeakageCurrentUnit uses Python identifier cellLeakageCurrentUnit
    __cellLeakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentUnit'), 'cellLeakageCurrentUnit', 'mapsPlatform_CachePowerModelType_cellLeakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __cellLeakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 524, 4)
    __cellLeakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 524, 4)
    
    cellLeakageCurrentUnit = property(__cellLeakageCurrentUnit.value, __cellLeakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_CachePowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 525, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 525, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_CachePowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 526, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 526, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute cellSwitchedCapacitanceValue uses Python identifier cellSwitchedCapacitanceValue
    __cellSwitchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceValue'), 'cellSwitchedCapacitanceValue', 'mapsPlatform_CachePowerModelType_cellSwitchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __cellSwitchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 527, 4)
    __cellSwitchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 527, 4)
    
    cellSwitchedCapacitanceValue = property(__cellSwitchedCapacitanceValue.value, __cellSwitchedCapacitanceValue.set, None, None)

    
    # Attribute cellSwitchedCapacitanceUnit uses Python identifier cellSwitchedCapacitanceUnit
    __cellSwitchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceUnit'), 'cellSwitchedCapacitanceUnit', 'mapsPlatform_CachePowerModelType_cellSwitchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __cellSwitchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 528, 4)
    __cellSwitchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 528, 4)
    
    cellSwitchedCapacitanceUnit = property(__cellSwitchedCapacitanceUnit.value, __cellSwitchedCapacitanceUnit.set, None, None)

    
    # Attribute readHitCapacitanceValue uses Python identifier readHitCapacitanceValue
    __readHitCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitCapacitanceValue'), 'readHitCapacitanceValue', 'mapsPlatform_CachePowerModelType_readHitCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __readHitCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 529, 4)
    __readHitCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 529, 4)
    
    readHitCapacitanceValue = property(__readHitCapacitanceValue.value, __readHitCapacitanceValue.set, None, None)

    
    # Attribute readHitCapacitanceUnit uses Python identifier readHitCapacitanceUnit
    __readHitCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitCapacitanceUnit'), 'readHitCapacitanceUnit', 'mapsPlatform_CachePowerModelType_readHitCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __readHitCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 530, 4)
    __readHitCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 530, 4)
    
    readHitCapacitanceUnit = property(__readHitCapacitanceUnit.value, __readHitCapacitanceUnit.set, None, None)

    
    # Attribute writeHitCapacitanceValue uses Python identifier writeHitCapacitanceValue
    __writeHitCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitCapacitanceValue'), 'writeHitCapacitanceValue', 'mapsPlatform_CachePowerModelType_writeHitCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __writeHitCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 531, 4)
    __writeHitCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 531, 4)
    
    writeHitCapacitanceValue = property(__writeHitCapacitanceValue.value, __writeHitCapacitanceValue.set, None, None)

    
    # Attribute writeHitCapacitanceUnit uses Python identifier writeHitCapacitanceUnit
    __writeHitCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitCapacitanceUnit'), 'writeHitCapacitanceUnit', 'mapsPlatform_CachePowerModelType_writeHitCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __writeHitCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 532, 4)
    __writeHitCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 532, 4)
    
    writeHitCapacitanceUnit = property(__writeHitCapacitanceUnit.value, __writeHitCapacitanceUnit.set, None, None)

    
    # Attribute readMissCapacitanceValue uses Python identifier readMissCapacitanceValue
    __readMissCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissCapacitanceValue'), 'readMissCapacitanceValue', 'mapsPlatform_CachePowerModelType_readMissCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __readMissCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 533, 4)
    __readMissCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 533, 4)
    
    readMissCapacitanceValue = property(__readMissCapacitanceValue.value, __readMissCapacitanceValue.set, None, None)

    
    # Attribute readMissCapacitanceUnit uses Python identifier readMissCapacitanceUnit
    __readMissCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissCapacitanceUnit'), 'readMissCapacitanceUnit', 'mapsPlatform_CachePowerModelType_readMissCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __readMissCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 534, 4)
    __readMissCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 534, 4)
    
    readMissCapacitanceUnit = property(__readMissCapacitanceUnit.value, __readMissCapacitanceUnit.set, None, None)

    
    # Attribute writeMissCapacitanceValue uses Python identifier writeMissCapacitanceValue
    __writeMissCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissCapacitanceValue'), 'writeMissCapacitanceValue', 'mapsPlatform_CachePowerModelType_writeMissCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __writeMissCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 535, 4)
    __writeMissCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 535, 4)
    
    writeMissCapacitanceValue = property(__writeMissCapacitanceValue.value, __writeMissCapacitanceValue.set, None, None)

    
    # Attribute writeMissCapacitanceUnit uses Python identifier writeMissCapacitanceUnit
    __writeMissCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissCapacitanceUnit'), 'writeMissCapacitanceUnit', 'mapsPlatform_CachePowerModelType_writeMissCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __writeMissCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 536, 4)
    __writeMissCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 536, 4)
    
    writeMissCapacitanceUnit = property(__writeMissCapacitanceUnit.value, __writeMissCapacitanceUnit.set, None, None)

    _ElementMap.update({
        __CachePowerState.name() : __CachePowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __cellLeakageCurrentValue.name() : __cellLeakageCurrentValue,
        __cellLeakageCurrentUnit.name() : __cellLeakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __cellSwitchedCapacitanceValue.name() : __cellSwitchedCapacitanceValue,
        __cellSwitchedCapacitanceUnit.name() : __cellSwitchedCapacitanceUnit,
        __readHitCapacitanceValue.name() : __readHitCapacitanceValue,
        __readHitCapacitanceUnit.name() : __readHitCapacitanceUnit,
        __writeHitCapacitanceValue.name() : __writeHitCapacitanceValue,
        __writeHitCapacitanceUnit.name() : __writeHitCapacitanceUnit,
        __readMissCapacitanceValue.name() : __readMissCapacitanceValue,
        __readMissCapacitanceUnit.name() : __readMissCapacitanceUnit,
        __writeMissCapacitanceValue.name() : __writeMissCapacitanceValue,
        __writeMissCapacitanceUnit.name() : __writeMissCapacitanceUnit
    })
_module_typeBindings.CachePowerModelType = CachePowerModelType
Namespace.addCategoryObject('typeBinding', 'CachePowerModelType', CachePowerModelType)



class CacheType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CacheType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 538, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ParentCacheRef uses Python identifier ParentCacheRef
    __ParentCacheRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ParentCacheRef'), 'ParentCacheRef', 'mapsPlatform_CacheType_ParentCacheRef', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 540, 6), )

    
    ParentCacheRef = property(__ParentCacheRef.value, __ParentCacheRef.set, None, None)

    
    # Element ParentMemoryRef uses Python identifier ParentMemoryRef
    __ParentMemoryRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ParentMemoryRef'), 'ParentMemoryRef', 'mapsPlatform_CacheType_ParentMemoryRef', False, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 541, 6), )

    
    ParentMemoryRef = property(__ParentMemoryRef.value, __ParentMemoryRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_CacheType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 543, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 543, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute coherency uses Python identifier coherency
    __coherency = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'coherency'), 'coherency', 'mapsPlatform_CacheType_coherency', _module_typeBindings.CoherencyType)
    __coherency._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 544, 4)
    __coherency._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 544, 4)
    
    coherency = property(__coherency.value, __coherency.set, None, None)

    
    # Attribute sizeValue uses Python identifier sizeValue
    __sizeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sizeValue'), 'sizeValue', 'mapsPlatform_CacheType_sizeValue', _module_typeBindings.SizeValueType, required=True)
    __sizeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 545, 4)
    __sizeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 545, 4)
    
    sizeValue = property(__sizeValue.value, __sizeValue.set, None, None)

    
    # Attribute sizeUnit uses Python identifier sizeUnit
    __sizeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sizeUnit'), 'sizeUnit', 'mapsPlatform_CacheType_sizeUnit', _module_typeBindings.SizeUnitType, required=True)
    __sizeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 546, 4)
    __sizeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 546, 4)
    
    sizeUnit = property(__sizeUnit.value, __sizeUnit.set, None, None)

    
    # Attribute lineSizeValue uses Python identifier lineSizeValue
    __lineSizeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lineSizeValue'), 'lineSizeValue', 'mapsPlatform_CacheType_lineSizeValue', _module_typeBindings.SizeValueType, required=True)
    __lineSizeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 547, 4)
    __lineSizeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 547, 4)
    
    lineSizeValue = property(__lineSizeValue.value, __lineSizeValue.set, None, None)

    
    # Attribute lineSizeUnit uses Python identifier lineSizeUnit
    __lineSizeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lineSizeUnit'), 'lineSizeUnit', 'mapsPlatform_CacheType_lineSizeUnit', _module_typeBindings.SizeUnitType, required=True)
    __lineSizeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 548, 4)
    __lineSizeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 548, 4)
    
    lineSizeUnit = property(__lineSizeUnit.value, __lineSizeUnit.set, None, None)

    
    # Attribute ways uses Python identifier ways
    __ways = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ways'), 'ways', 'mapsPlatform_CacheType_ways', _module_typeBindings.PositiveIntType)
    __ways._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 549, 4)
    __ways._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 549, 4)
    
    ways = property(__ways.value, __ways.set, None, None)

    
    # Attribute replacement uses Python identifier replacement
    __replacement = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'replacement'), 'replacement', 'mapsPlatform_CacheType_replacement', _module_typeBindings.ReplacementType)
    __replacement._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 550, 4)
    __replacement._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 550, 4)
    
    replacement = property(__replacement.value, __replacement.set, None, None)

    
    # Attribute prefetch uses Python identifier prefetch
    __prefetch = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'prefetch'), 'prefetch', 'mapsPlatform_CacheType_prefetch', _module_typeBindings.PrefetchType)
    __prefetch._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 551, 4)
    __prefetch._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 551, 4)
    
    prefetch = property(__prefetch.value, __prefetch.set, None, None)

    
    # Attribute prefetchDistance uses Python identifier prefetchDistance
    __prefetchDistance = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'prefetchDistance'), 'prefetchDistance', 'mapsPlatform_CacheType_prefetchDistance', pyxb.binding.datatypes.positiveInteger)
    __prefetchDistance._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 552, 4)
    __prefetchDistance._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 552, 4)
    
    prefetchDistance = property(__prefetchDistance.value, __prefetchDistance.set, None, None)

    
    # Attribute writeAllocate uses Python identifier writeAllocate
    __writeAllocate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeAllocate'), 'writeAllocate', 'mapsPlatform_CacheType_writeAllocate', _module_typeBindings.WriteAllocateType)
    __writeAllocate._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 553, 4)
    __writeAllocate._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 553, 4)
    
    writeAllocate = property(__writeAllocate.value, __writeAllocate.set, None, None)

    
    # Attribute writeBack uses Python identifier writeBack
    __writeBack = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeBack'), 'writeBack', 'mapsPlatform_CacheType_writeBack', _module_typeBindings.WriteBackType)
    __writeBack._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 554, 4)
    __writeBack._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 554, 4)
    
    writeBack = property(__writeBack.value, __writeBack.set, None, None)

    
    # Attribute readHitThroughputValue uses Python identifier readHitThroughputValue
    __readHitThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitThroughputValue'), 'readHitThroughputValue', 'mapsPlatform_CacheType_readHitThroughputValue', _module_typeBindings.ThroughputValueType)
    __readHitThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 555, 4)
    __readHitThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 555, 4)
    
    readHitThroughputValue = property(__readHitThroughputValue.value, __readHitThroughputValue.set, None, None)

    
    # Attribute readHitThroughputUnit uses Python identifier readHitThroughputUnit
    __readHitThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitThroughputUnit'), 'readHitThroughputUnit', 'mapsPlatform_CacheType_readHitThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __readHitThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 556, 4)
    __readHitThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 556, 4)
    
    readHitThroughputUnit = property(__readHitThroughputUnit.value, __readHitThroughputUnit.set, None, None)

    
    # Attribute readHitLatencyValue uses Python identifier readHitLatencyValue
    __readHitLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitLatencyValue'), 'readHitLatencyValue', 'mapsPlatform_CacheType_readHitLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __readHitLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 557, 4)
    __readHitLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 557, 4)
    
    readHitLatencyValue = property(__readHitLatencyValue.value, __readHitLatencyValue.set, None, None)

    
    # Attribute readHitLatencyUnit uses Python identifier readHitLatencyUnit
    __readHitLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readHitLatencyUnit'), 'readHitLatencyUnit', 'mapsPlatform_CacheType_readHitLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __readHitLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 558, 4)
    __readHitLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 558, 4)
    
    readHitLatencyUnit = property(__readHitLatencyUnit.value, __readHitLatencyUnit.set, None, None)

    
    # Attribute writeHitThroughputValue uses Python identifier writeHitThroughputValue
    __writeHitThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitThroughputValue'), 'writeHitThroughputValue', 'mapsPlatform_CacheType_writeHitThroughputValue', _module_typeBindings.ThroughputValueType)
    __writeHitThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 559, 4)
    __writeHitThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 559, 4)
    
    writeHitThroughputValue = property(__writeHitThroughputValue.value, __writeHitThroughputValue.set, None, None)

    
    # Attribute writeHitThroughputUnit uses Python identifier writeHitThroughputUnit
    __writeHitThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitThroughputUnit'), 'writeHitThroughputUnit', 'mapsPlatform_CacheType_writeHitThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __writeHitThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 560, 4)
    __writeHitThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 560, 4)
    
    writeHitThroughputUnit = property(__writeHitThroughputUnit.value, __writeHitThroughputUnit.set, None, None)

    
    # Attribute writeHitLatencyValue uses Python identifier writeHitLatencyValue
    __writeHitLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitLatencyValue'), 'writeHitLatencyValue', 'mapsPlatform_CacheType_writeHitLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __writeHitLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 561, 4)
    __writeHitLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 561, 4)
    
    writeHitLatencyValue = property(__writeHitLatencyValue.value, __writeHitLatencyValue.set, None, None)

    
    # Attribute writeHitLatencyUnit uses Python identifier writeHitLatencyUnit
    __writeHitLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeHitLatencyUnit'), 'writeHitLatencyUnit', 'mapsPlatform_CacheType_writeHitLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __writeHitLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 562, 4)
    __writeHitLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 562, 4)
    
    writeHitLatencyUnit = property(__writeHitLatencyUnit.value, __writeHitLatencyUnit.set, None, None)

    
    # Attribute readMissThroughputValue uses Python identifier readMissThroughputValue
    __readMissThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissThroughputValue'), 'readMissThroughputValue', 'mapsPlatform_CacheType_readMissThroughputValue', _module_typeBindings.ThroughputValueType)
    __readMissThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 563, 4)
    __readMissThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 563, 4)
    
    readMissThroughputValue = property(__readMissThroughputValue.value, __readMissThroughputValue.set, None, None)

    
    # Attribute readMissThroughputUnit uses Python identifier readMissThroughputUnit
    __readMissThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissThroughputUnit'), 'readMissThroughputUnit', 'mapsPlatform_CacheType_readMissThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __readMissThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 564, 4)
    __readMissThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 564, 4)
    
    readMissThroughputUnit = property(__readMissThroughputUnit.value, __readMissThroughputUnit.set, None, None)

    
    # Attribute readMissLatencyValue uses Python identifier readMissLatencyValue
    __readMissLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissLatencyValue'), 'readMissLatencyValue', 'mapsPlatform_CacheType_readMissLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __readMissLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 565, 4)
    __readMissLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 565, 4)
    
    readMissLatencyValue = property(__readMissLatencyValue.value, __readMissLatencyValue.set, None, None)

    
    # Attribute readMissLatencyUnit uses Python identifier readMissLatencyUnit
    __readMissLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readMissLatencyUnit'), 'readMissLatencyUnit', 'mapsPlatform_CacheType_readMissLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __readMissLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 566, 4)
    __readMissLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 566, 4)
    
    readMissLatencyUnit = property(__readMissLatencyUnit.value, __readMissLatencyUnit.set, None, None)

    
    # Attribute writeMissThroughputValue uses Python identifier writeMissThroughputValue
    __writeMissThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissThroughputValue'), 'writeMissThroughputValue', 'mapsPlatform_CacheType_writeMissThroughputValue', _module_typeBindings.ThroughputValueType)
    __writeMissThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 567, 4)
    __writeMissThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 567, 4)
    
    writeMissThroughputValue = property(__writeMissThroughputValue.value, __writeMissThroughputValue.set, None, None)

    
    # Attribute writeMissThroughputUnit uses Python identifier writeMissThroughputUnit
    __writeMissThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissThroughputUnit'), 'writeMissThroughputUnit', 'mapsPlatform_CacheType_writeMissThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __writeMissThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 568, 4)
    __writeMissThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 568, 4)
    
    writeMissThroughputUnit = property(__writeMissThroughputUnit.value, __writeMissThroughputUnit.set, None, None)

    
    # Attribute writeMissLatencyValue uses Python identifier writeMissLatencyValue
    __writeMissLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissLatencyValue'), 'writeMissLatencyValue', 'mapsPlatform_CacheType_writeMissLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __writeMissLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 569, 4)
    __writeMissLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 569, 4)
    
    writeMissLatencyValue = property(__writeMissLatencyValue.value, __writeMissLatencyValue.set, None, None)

    
    # Attribute writeMissLatencyUnit uses Python identifier writeMissLatencyUnit
    __writeMissLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeMissLatencyUnit'), 'writeMissLatencyUnit', 'mapsPlatform_CacheType_writeMissLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __writeMissLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 570, 4)
    __writeMissLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 570, 4)
    
    writeMissLatencyUnit = property(__writeMissLatencyUnit.value, __writeMissLatencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_CacheType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 571, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 571, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_CacheType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 574, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 574, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute cachePowerModel uses Python identifier cachePowerModel
    __cachePowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cachePowerModel'), 'cachePowerModel', 'mapsPlatform_CacheType_cachePowerModel', _module_typeBindings.RefType)
    __cachePowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 577, 4)
    __cachePowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 577, 4)
    
    cachePowerModel = property(__cachePowerModel.value, __cachePowerModel.set, None, None)

    _ElementMap.update({
        __ParentCacheRef.name() : __ParentCacheRef,
        __ParentMemoryRef.name() : __ParentMemoryRef
    })
    _AttributeMap.update({
        __id.name() : __id,
        __coherency.name() : __coherency,
        __sizeValue.name() : __sizeValue,
        __sizeUnit.name() : __sizeUnit,
        __lineSizeValue.name() : __lineSizeValue,
        __lineSizeUnit.name() : __lineSizeUnit,
        __ways.name() : __ways,
        __replacement.name() : __replacement,
        __prefetch.name() : __prefetch,
        __prefetchDistance.name() : __prefetchDistance,
        __writeAllocate.name() : __writeAllocate,
        __writeBack.name() : __writeBack,
        __readHitThroughputValue.name() : __readHitThroughputValue,
        __readHitThroughputUnit.name() : __readHitThroughputUnit,
        __readHitLatencyValue.name() : __readHitLatencyValue,
        __readHitLatencyUnit.name() : __readHitLatencyUnit,
        __writeHitThroughputValue.name() : __writeHitThroughputValue,
        __writeHitThroughputUnit.name() : __writeHitThroughputUnit,
        __writeHitLatencyValue.name() : __writeHitLatencyValue,
        __writeHitLatencyUnit.name() : __writeHitLatencyUnit,
        __readMissThroughputValue.name() : __readMissThroughputValue,
        __readMissThroughputUnit.name() : __readMissThroughputUnit,
        __readMissLatencyValue.name() : __readMissLatencyValue,
        __readMissLatencyUnit.name() : __readMissLatencyUnit,
        __writeMissThroughputValue.name() : __writeMissThroughputValue,
        __writeMissThroughputUnit.name() : __writeMissThroughputUnit,
        __writeMissLatencyValue.name() : __writeMissLatencyValue,
        __writeMissLatencyUnit.name() : __writeMissLatencyUnit,
        __frequencyDomain.name() : __frequencyDomain,
        __voltageDomain.name() : __voltageDomain,
        __cachePowerModel.name() : __cachePowerModel
    })
_module_typeBindings.CacheType = CacheType
Namespace.addCategoryObject('typeBinding', 'CacheType', CacheType)



class CacheAccessType (CacheRefType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CacheAccessType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 586, 2)
    _ElementMap = CacheRefType._ElementMap.copy()
    _AttributeMap = CacheRefType._AttributeMap.copy()
    # Base type is CacheRefType
    

    
    # Attribute access uses Python identifier access
    __access = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'access'), 'access', 'mapsPlatform_CacheAccessType_access', _module_typeBindings.AccessType, required=True)
    __access._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 589, 8)
    __access._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 589, 8)
    
    access = property(__access.value, __access.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __access.name() : __access
    })
_module_typeBindings.CacheAccessType = CacheAccessType
Namespace.addCategoryObject('typeBinding', 'CacheAccessType', CacheAccessType)



class FifoPowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FifoPowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 594, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_FifoPowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 597, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 597, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_FifoPowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 598, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 598, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_FifoPowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 599, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 599, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.FifoPowerStateType = FifoPowerStateType
Namespace.addCategoryObject('typeBinding', 'FifoPowerStateType', FifoPowerStateType)



class FifoPowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FifoPowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 603, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FifoPowerState uses Python identifier FifoPowerState
    __FifoPowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FifoPowerState'), 'FifoPowerState', 'mapsPlatform_FifoPowerModelType_FifoPowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 605, 6), )

    
    FifoPowerState = property(__FifoPowerState.value, __FifoPowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_FifoPowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 608, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 608, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_FifoPowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 609, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 609, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_FifoPowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 610, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 610, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute cellLeakageCurrentValue uses Python identifier cellLeakageCurrentValue
    __cellLeakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentValue'), 'cellLeakageCurrentValue', 'mapsPlatform_FifoPowerModelType_cellLeakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __cellLeakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 611, 4)
    __cellLeakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 611, 4)
    
    cellLeakageCurrentValue = property(__cellLeakageCurrentValue.value, __cellLeakageCurrentValue.set, None, None)

    
    # Attribute cellLeakageCurrentUnit uses Python identifier cellLeakageCurrentUnit
    __cellLeakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellLeakageCurrentUnit'), 'cellLeakageCurrentUnit', 'mapsPlatform_FifoPowerModelType_cellLeakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __cellLeakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 612, 4)
    __cellLeakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 612, 4)
    
    cellLeakageCurrentUnit = property(__cellLeakageCurrentUnit.value, __cellLeakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_FifoPowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 613, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 613, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_FifoPowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 614, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 614, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute cellSwitchedCapacitanceValue uses Python identifier cellSwitchedCapacitanceValue
    __cellSwitchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceValue'), 'cellSwitchedCapacitanceValue', 'mapsPlatform_FifoPowerModelType_cellSwitchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __cellSwitchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 615, 4)
    __cellSwitchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 615, 4)
    
    cellSwitchedCapacitanceValue = property(__cellSwitchedCapacitanceValue.value, __cellSwitchedCapacitanceValue.set, None, None)

    
    # Attribute cellSwitchedCapacitanceUnit uses Python identifier cellSwitchedCapacitanceUnit
    __cellSwitchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cellSwitchedCapacitanceUnit'), 'cellSwitchedCapacitanceUnit', 'mapsPlatform_FifoPowerModelType_cellSwitchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __cellSwitchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 616, 4)
    __cellSwitchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 616, 4)
    
    cellSwitchedCapacitanceUnit = property(__cellSwitchedCapacitanceUnit.value, __cellSwitchedCapacitanceUnit.set, None, None)

    
    # Attribute readCapacitanceValue uses Python identifier readCapacitanceValue
    __readCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readCapacitanceValue'), 'readCapacitanceValue', 'mapsPlatform_FifoPowerModelType_readCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __readCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 617, 4)
    __readCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 617, 4)
    
    readCapacitanceValue = property(__readCapacitanceValue.value, __readCapacitanceValue.set, None, None)

    
    # Attribute readCapacitanceUnit uses Python identifier readCapacitanceUnit
    __readCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readCapacitanceUnit'), 'readCapacitanceUnit', 'mapsPlatform_FifoPowerModelType_readCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __readCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 618, 4)
    __readCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 618, 4)
    
    readCapacitanceUnit = property(__readCapacitanceUnit.value, __readCapacitanceUnit.set, None, None)

    
    # Attribute writeCapacitanceValue uses Python identifier writeCapacitanceValue
    __writeCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeCapacitanceValue'), 'writeCapacitanceValue', 'mapsPlatform_FifoPowerModelType_writeCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __writeCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 619, 4)
    __writeCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 619, 4)
    
    writeCapacitanceValue = property(__writeCapacitanceValue.value, __writeCapacitanceValue.set, None, None)

    
    # Attribute writeCapacitanceUnit uses Python identifier writeCapacitanceUnit
    __writeCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeCapacitanceUnit'), 'writeCapacitanceUnit', 'mapsPlatform_FifoPowerModelType_writeCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __writeCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 620, 4)
    __writeCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 620, 4)
    
    writeCapacitanceUnit = property(__writeCapacitanceUnit.value, __writeCapacitanceUnit.set, None, None)

    _ElementMap.update({
        __FifoPowerState.name() : __FifoPowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __cellLeakageCurrentValue.name() : __cellLeakageCurrentValue,
        __cellLeakageCurrentUnit.name() : __cellLeakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __cellSwitchedCapacitanceValue.name() : __cellSwitchedCapacitanceValue,
        __cellSwitchedCapacitanceUnit.name() : __cellSwitchedCapacitanceUnit,
        __readCapacitanceValue.name() : __readCapacitanceValue,
        __readCapacitanceUnit.name() : __readCapacitanceUnit,
        __writeCapacitanceValue.name() : __writeCapacitanceValue,
        __writeCapacitanceUnit.name() : __writeCapacitanceUnit
    })
_module_typeBindings.FifoPowerModelType = FifoPowerModelType
Namespace.addCategoryObject('typeBinding', 'FifoPowerModelType', FifoPowerModelType)



class FifoType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FifoType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 622, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_FifoType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 623, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 623, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute entrySizeValue uses Python identifier entrySizeValue
    __entrySizeValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'entrySizeValue'), 'entrySizeValue', 'mapsPlatform_FifoType_entrySizeValue', _module_typeBindings.SizeValueType, required=True)
    __entrySizeValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 624, 4)
    __entrySizeValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 624, 4)
    
    entrySizeValue = property(__entrySizeValue.value, __entrySizeValue.set, None, None)

    
    # Attribute entrySizeUnit uses Python identifier entrySizeUnit
    __entrySizeUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'entrySizeUnit'), 'entrySizeUnit', 'mapsPlatform_FifoType_entrySizeUnit', _module_typeBindings.SizeUnitType, required=True)
    __entrySizeUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 625, 4)
    __entrySizeUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 625, 4)
    
    entrySizeUnit = property(__entrySizeUnit.value, __entrySizeUnit.set, None, None)

    
    # Attribute entryCount uses Python identifier entryCount
    __entryCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'entryCount'), 'entryCount', 'mapsPlatform_FifoType_entryCount', _module_typeBindings.PositiveIntType, required=True)
    __entryCount._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 626, 4)
    __entryCount._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 626, 4)
    
    entryCount = property(__entryCount.value, __entryCount.set, None, None)

    
    # Attribute readThroughputValue uses Python identifier readThroughputValue
    __readThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readThroughputValue'), 'readThroughputValue', 'mapsPlatform_FifoType_readThroughputValue', _module_typeBindings.ThroughputValueType)
    __readThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 627, 4)
    __readThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 627, 4)
    
    readThroughputValue = property(__readThroughputValue.value, __readThroughputValue.set, None, None)

    
    # Attribute readThroughputUnit uses Python identifier readThroughputUnit
    __readThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readThroughputUnit'), 'readThroughputUnit', 'mapsPlatform_FifoType_readThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __readThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 628, 4)
    __readThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 628, 4)
    
    readThroughputUnit = property(__readThroughputUnit.value, __readThroughputUnit.set, None, None)

    
    # Attribute readLatencyValue uses Python identifier readLatencyValue
    __readLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readLatencyValue'), 'readLatencyValue', 'mapsPlatform_FifoType_readLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __readLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 629, 4)
    __readLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 629, 4)
    
    readLatencyValue = property(__readLatencyValue.value, __readLatencyValue.set, None, None)

    
    # Attribute readLatencyUnit uses Python identifier readLatencyUnit
    __readLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'readLatencyUnit'), 'readLatencyUnit', 'mapsPlatform_FifoType_readLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __readLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 630, 4)
    __readLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 630, 4)
    
    readLatencyUnit = property(__readLatencyUnit.value, __readLatencyUnit.set, None, None)

    
    # Attribute writeThroughputValue uses Python identifier writeThroughputValue
    __writeThroughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeThroughputValue'), 'writeThroughputValue', 'mapsPlatform_FifoType_writeThroughputValue', _module_typeBindings.ThroughputValueType)
    __writeThroughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 631, 4)
    __writeThroughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 631, 4)
    
    writeThroughputValue = property(__writeThroughputValue.value, __writeThroughputValue.set, None, None)

    
    # Attribute writeThroughputUnit uses Python identifier writeThroughputUnit
    __writeThroughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeThroughputUnit'), 'writeThroughputUnit', 'mapsPlatform_FifoType_writeThroughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __writeThroughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 632, 4)
    __writeThroughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 632, 4)
    
    writeThroughputUnit = property(__writeThroughputUnit.value, __writeThroughputUnit.set, None, None)

    
    # Attribute writeLatencyValue uses Python identifier writeLatencyValue
    __writeLatencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeLatencyValue'), 'writeLatencyValue', 'mapsPlatform_FifoType_writeLatencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __writeLatencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 633, 4)
    __writeLatencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 633, 4)
    
    writeLatencyValue = property(__writeLatencyValue.value, __writeLatencyValue.set, None, None)

    
    # Attribute writeLatencyUnit uses Python identifier writeLatencyUnit
    __writeLatencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writeLatencyUnit'), 'writeLatencyUnit', 'mapsPlatform_FifoType_writeLatencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __writeLatencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 634, 4)
    __writeLatencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 634, 4)
    
    writeLatencyUnit = property(__writeLatencyUnit.value, __writeLatencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_FifoType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 635, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 635, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_FifoType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 638, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 638, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute fifoPowerModel uses Python identifier fifoPowerModel
    __fifoPowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'fifoPowerModel'), 'fifoPowerModel', 'mapsPlatform_FifoType_fifoPowerModel', _module_typeBindings.RefType)
    __fifoPowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 641, 4)
    __fifoPowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 641, 4)
    
    fifoPowerModel = property(__fifoPowerModel.value, __fifoPowerModel.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __entrySizeValue.name() : __entrySizeValue,
        __entrySizeUnit.name() : __entrySizeUnit,
        __entryCount.name() : __entryCount,
        __readThroughputValue.name() : __readThroughputValue,
        __readThroughputUnit.name() : __readThroughputUnit,
        __readLatencyValue.name() : __readLatencyValue,
        __readLatencyUnit.name() : __readLatencyUnit,
        __writeThroughputValue.name() : __writeThroughputValue,
        __writeThroughputUnit.name() : __writeThroughputUnit,
        __writeLatencyValue.name() : __writeLatencyValue,
        __writeLatencyUnit.name() : __writeLatencyUnit,
        __frequencyDomain.name() : __frequencyDomain,
        __voltageDomain.name() : __voltageDomain,
        __fifoPowerModel.name() : __fifoPowerModel
    })
_module_typeBindings.FifoType = FifoType
Namespace.addCategoryObject('typeBinding', 'FifoType', FifoType)



class FifoAccessType (FifoRefType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FifoAccessType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 650, 2)
    _ElementMap = FifoRefType._ElementMap.copy()
    _AttributeMap = FifoRefType._AttributeMap.copy()
    # Base type is FifoRefType
    

    
    # Attribute access uses Python identifier access
    __access = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'access'), 'access', 'mapsPlatform_FifoAccessType_access', _module_typeBindings.AccessType, required=True)
    __access._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 653, 8)
    __access._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 653, 8)
    
    access = property(__access.value, __access.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __access.name() : __access
    })
_module_typeBindings.FifoAccessType = FifoAccessType
Namespace.addCategoryObject('typeBinding', 'FifoAccessType', FifoAccessType)



class PhysicalLinkPowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PhysicalLinkPowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 658, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_PhysicalLinkPowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 661, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 661, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_PhysicalLinkPowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 662, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 662, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_PhysicalLinkPowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 663, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 663, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.PhysicalLinkPowerStateType = PhysicalLinkPowerStateType
Namespace.addCategoryObject('typeBinding', 'PhysicalLinkPowerStateType', PhysicalLinkPowerStateType)



class PhysicalLinkPowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PhysicalLinkPowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 667, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PhysicalLinkPowerState uses Python identifier PhysicalLinkPowerState
    __PhysicalLinkPowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerState'), 'PhysicalLinkPowerState', 'mapsPlatform_PhysicalLinkPowerModelType_PhysicalLinkPowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 669, 6), )

    
    PhysicalLinkPowerState = property(__PhysicalLinkPowerState.value, __PhysicalLinkPowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_PhysicalLinkPowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 672, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 672, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_PhysicalLinkPowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 673, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 673, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_PhysicalLinkPowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 674, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 674, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_PhysicalLinkPowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 675, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 675, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_PhysicalLinkPowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 676, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 676, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute transferCapacitanceValue uses Python identifier transferCapacitanceValue
    __transferCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'transferCapacitanceValue'), 'transferCapacitanceValue', 'mapsPlatform_PhysicalLinkPowerModelType_transferCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __transferCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 677, 4)
    __transferCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 677, 4)
    
    transferCapacitanceValue = property(__transferCapacitanceValue.value, __transferCapacitanceValue.set, None, None)

    
    # Attribute transferCapacitanceUnit uses Python identifier transferCapacitanceUnit
    __transferCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'transferCapacitanceUnit'), 'transferCapacitanceUnit', 'mapsPlatform_PhysicalLinkPowerModelType_transferCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __transferCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 678, 4)
    __transferCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 678, 4)
    
    transferCapacitanceUnit = property(__transferCapacitanceUnit.value, __transferCapacitanceUnit.set, None, None)

    _ElementMap.update({
        __PhysicalLinkPowerState.name() : __PhysicalLinkPowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __transferCapacitanceValue.name() : __transferCapacitanceValue,
        __transferCapacitanceUnit.name() : __transferCapacitanceUnit
    })
_module_typeBindings.PhysicalLinkPowerModelType = PhysicalLinkPowerModelType
Namespace.addCategoryObject('typeBinding', 'PhysicalLinkPowerModelType', PhysicalLinkPowerModelType)



class PhysicalLinkType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PhysicalLinkType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 680, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_PhysicalLinkType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 681, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 681, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute throughputValue uses Python identifier throughputValue
    __throughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputValue'), 'throughputValue', 'mapsPlatform_PhysicalLinkType_throughputValue', _module_typeBindings.ThroughputValueType)
    __throughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 682, 4)
    __throughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 682, 4)
    
    throughputValue = property(__throughputValue.value, __throughputValue.set, None, None)

    
    # Attribute throughputUnit uses Python identifier throughputUnit
    __throughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputUnit'), 'throughputUnit', 'mapsPlatform_PhysicalLinkType_throughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __throughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 683, 4)
    __throughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 683, 4)
    
    throughputUnit = property(__throughputUnit.value, __throughputUnit.set, None, None)

    
    # Attribute latencyValue uses Python identifier latencyValue
    __latencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyValue'), 'latencyValue', 'mapsPlatform_PhysicalLinkType_latencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __latencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 684, 4)
    __latencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 684, 4)
    
    latencyValue = property(__latencyValue.value, __latencyValue.set, None, None)

    
    # Attribute latencyUnit uses Python identifier latencyUnit
    __latencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyUnit'), 'latencyUnit', 'mapsPlatform_PhysicalLinkType_latencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __latencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 685, 4)
    __latencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 685, 4)
    
    latencyUnit = property(__latencyUnit.value, __latencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_PhysicalLinkType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 686, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 686, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_PhysicalLinkType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 689, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 689, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute physicalLinkPowerModel uses Python identifier physicalLinkPowerModel
    __physicalLinkPowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physicalLinkPowerModel'), 'physicalLinkPowerModel', 'mapsPlatform_PhysicalLinkType_physicalLinkPowerModel', _module_typeBindings.RefType)
    __physicalLinkPowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 692, 4)
    __physicalLinkPowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 692, 4)
    
    physicalLinkPowerModel = property(__physicalLinkPowerModel.value, __physicalLinkPowerModel.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __throughputValue.name() : __throughputValue,
        __throughputUnit.name() : __throughputUnit,
        __latencyValue.name() : __latencyValue,
        __latencyUnit.name() : __latencyUnit,
        __frequencyDomain.name() : __frequencyDomain,
        __voltageDomain.name() : __voltageDomain,
        __physicalLinkPowerModel.name() : __physicalLinkPowerModel
    })
_module_typeBindings.PhysicalLinkType = PhysicalLinkType
Namespace.addCategoryObject('typeBinding', 'PhysicalLinkType', PhysicalLinkType)



class DMAControllerPowerStateType (VoltageFrequencyConditionListType):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DMAControllerPowerStateType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 702, 2)
    _ElementMap = VoltageFrequencyConditionListType._ElementMap.copy()
    _AttributeMap = VoltageFrequencyConditionListType._AttributeMap.copy()
    # Base type is VoltageFrequencyConditionListType
    

    

    

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', 'mapsPlatform_DMAControllerPowerStateType_name', _module_typeBindings.NameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 705, 8)
    __name._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 705, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute powerValue uses Python identifier powerValue
    __powerValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerValue'), 'powerValue', 'mapsPlatform_DMAControllerPowerStateType_powerValue', _module_typeBindings.PowerValueType)
    __powerValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 706, 8)
    __powerValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 706, 8)
    
    powerValue = property(__powerValue.value, __powerValue.set, None, None)

    
    # Attribute powerUnit uses Python identifier powerUnit
    __powerUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerUnit'), 'powerUnit', 'mapsPlatform_DMAControllerPowerStateType_powerUnit', _module_typeBindings.PowerUnitType, unicode_default='pW')
    __powerUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 707, 8)
    __powerUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 707, 8)
    
    powerUnit = property(__powerUnit.value, __powerUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __powerValue.name() : __powerValue,
        __powerUnit.name() : __powerUnit
    })
_module_typeBindings.DMAControllerPowerStateType = DMAControllerPowerStateType
Namespace.addCategoryObject('typeBinding', 'DMAControllerPowerStateType', DMAControllerPowerStateType)



class DMAControllerPowerModelType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DMAControllerPowerModelType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 711, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DMAControllerPowerState uses Python identifier DMAControllerPowerState
    __DMAControllerPowerState = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerState'), 'DMAControllerPowerState', 'mapsPlatform_DMAControllerPowerModelType_DMAControllerPowerState', True, pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 713, 6), )

    
    DMAControllerPowerState = property(__DMAControllerPowerState.value, __DMAControllerPowerState.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_DMAControllerPowerModelType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 716, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 716, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute leakageCurrentValue uses Python identifier leakageCurrentValue
    __leakageCurrentValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentValue'), 'leakageCurrentValue', 'mapsPlatform_DMAControllerPowerModelType_leakageCurrentValue', _module_typeBindings.CurrentValueType, unicode_default='0')
    __leakageCurrentValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 717, 4)
    __leakageCurrentValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 717, 4)
    
    leakageCurrentValue = property(__leakageCurrentValue.value, __leakageCurrentValue.set, None, None)

    
    # Attribute leakageCurrentUnit uses Python identifier leakageCurrentUnit
    __leakageCurrentUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'leakageCurrentUnit'), 'leakageCurrentUnit', 'mapsPlatform_DMAControllerPowerModelType_leakageCurrentUnit', _module_typeBindings.CurrentUnitType, unicode_default='pA')
    __leakageCurrentUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 718, 4)
    __leakageCurrentUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 718, 4)
    
    leakageCurrentUnit = property(__leakageCurrentUnit.value, __leakageCurrentUnit.set, None, None)

    
    # Attribute switchedCapacitanceValue uses Python identifier switchedCapacitanceValue
    __switchedCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceValue'), 'switchedCapacitanceValue', 'mapsPlatform_DMAControllerPowerModelType_switchedCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __switchedCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 719, 4)
    __switchedCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 719, 4)
    
    switchedCapacitanceValue = property(__switchedCapacitanceValue.value, __switchedCapacitanceValue.set, None, None)

    
    # Attribute switchedCapacitanceUnit uses Python identifier switchedCapacitanceUnit
    __switchedCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'switchedCapacitanceUnit'), 'switchedCapacitanceUnit', 'mapsPlatform_DMAControllerPowerModelType_switchedCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __switchedCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 720, 4)
    __switchedCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 720, 4)
    
    switchedCapacitanceUnit = property(__switchedCapacitanceUnit.value, __switchedCapacitanceUnit.set, None, None)

    
    # Attribute transferCapacitanceValue uses Python identifier transferCapacitanceValue
    __transferCapacitanceValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'transferCapacitanceValue'), 'transferCapacitanceValue', 'mapsPlatform_DMAControllerPowerModelType_transferCapacitanceValue', _module_typeBindings.CapacitanceValueType, unicode_default='0')
    __transferCapacitanceValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 721, 4)
    __transferCapacitanceValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 721, 4)
    
    transferCapacitanceValue = property(__transferCapacitanceValue.value, __transferCapacitanceValue.set, None, None)

    
    # Attribute transferCapacitanceUnit uses Python identifier transferCapacitanceUnit
    __transferCapacitanceUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'transferCapacitanceUnit'), 'transferCapacitanceUnit', 'mapsPlatform_DMAControllerPowerModelType_transferCapacitanceUnit', _module_typeBindings.CapacitanceUnitType, unicode_default='pF')
    __transferCapacitanceUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 722, 4)
    __transferCapacitanceUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 722, 4)
    
    transferCapacitanceUnit = property(__transferCapacitanceUnit.value, __transferCapacitanceUnit.set, None, None)

    _ElementMap.update({
        __DMAControllerPowerState.name() : __DMAControllerPowerState
    })
    _AttributeMap.update({
        __id.name() : __id,
        __leakageCurrentValue.name() : __leakageCurrentValue,
        __leakageCurrentUnit.name() : __leakageCurrentUnit,
        __switchedCapacitanceValue.name() : __switchedCapacitanceValue,
        __switchedCapacitanceUnit.name() : __switchedCapacitanceUnit,
        __transferCapacitanceValue.name() : __transferCapacitanceValue,
        __transferCapacitanceUnit.name() : __transferCapacitanceUnit
    })
_module_typeBindings.DMAControllerPowerModelType = DMAControllerPowerModelType
Namespace.addCategoryObject('typeBinding', 'DMAControllerPowerModelType', DMAControllerPowerModelType)



class DMAControllerType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DMAControllerType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 724, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_DMAControllerType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 725, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 725, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute channelCount uses Python identifier channelCount
    __channelCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'channelCount'), 'channelCount', 'mapsPlatform_DMAControllerType_channelCount', _module_typeBindings.PositiveIntType)
    __channelCount._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 726, 4)
    __channelCount._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 726, 4)
    
    channelCount = property(__channelCount.value, __channelCount.set, None, None)

    
    # Attribute throughputValue uses Python identifier throughputValue
    __throughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputValue'), 'throughputValue', 'mapsPlatform_DMAControllerType_throughputValue', _module_typeBindings.ThroughputValueType)
    __throughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 727, 4)
    __throughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 727, 4)
    
    throughputValue = property(__throughputValue.value, __throughputValue.set, None, None)

    
    # Attribute throughputUnit uses Python identifier throughputUnit
    __throughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputUnit'), 'throughputUnit', 'mapsPlatform_DMAControllerType_throughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __throughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 728, 4)
    __throughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 728, 4)
    
    throughputUnit = property(__throughputUnit.value, __throughputUnit.set, None, None)

    
    # Attribute latencyValue uses Python identifier latencyValue
    __latencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyValue'), 'latencyValue', 'mapsPlatform_DMAControllerType_latencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __latencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 729, 4)
    __latencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 729, 4)
    
    latencyValue = property(__latencyValue.value, __latencyValue.set, None, None)

    
    # Attribute latencyUnit uses Python identifier latencyUnit
    __latencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyUnit'), 'latencyUnit', 'mapsPlatform_DMAControllerType_latencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __latencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 730, 4)
    __latencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 730, 4)
    
    latencyUnit = property(__latencyUnit.value, __latencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_DMAControllerType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 731, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 731, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    
    # Attribute voltageDomain uses Python identifier voltageDomain
    __voltageDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageDomain'), 'voltageDomain', 'mapsPlatform_DMAControllerType_voltageDomain', _module_typeBindings.RefType)
    __voltageDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 734, 4)
    __voltageDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 734, 4)
    
    voltageDomain = property(__voltageDomain.value, __voltageDomain.set, None, None)

    
    # Attribute dmaControllerPowerModel uses Python identifier dmaControllerPowerModel
    __dmaControllerPowerModel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dmaControllerPowerModel'), 'dmaControllerPowerModel', 'mapsPlatform_DMAControllerType_dmaControllerPowerModel', _module_typeBindings.RefType)
    __dmaControllerPowerModel._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 737, 4)
    __dmaControllerPowerModel._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 737, 4)
    
    dmaControllerPowerModel = property(__dmaControllerPowerModel.value, __dmaControllerPowerModel.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __channelCount.name() : __channelCount,
        __throughputValue.name() : __throughputValue,
        __throughputUnit.name() : __throughputUnit,
        __latencyValue.name() : __latencyValue,
        __latencyUnit.name() : __latencyUnit,
        __frequencyDomain.name() : __frequencyDomain,
        __voltageDomain.name() : __voltageDomain,
        __dmaControllerPowerModel.name() : __dmaControllerPowerModel
    })
_module_typeBindings.DMAControllerType = DMAControllerType
Namespace.addCategoryObject('typeBinding', 'DMAControllerType', DMAControllerType)



class LogicalLinkType (pyxb.binding.basis.complexTypeDefinition):
    
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LogicalLinkType')
    _XSDLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 748, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', 'mapsPlatform_LogicalLinkType_id', _module_typeBindings.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 749, 4)
    __id._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 749, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute throughputValue uses Python identifier throughputValue
    __throughputValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputValue'), 'throughputValue', 'mapsPlatform_LogicalLinkType_throughputValue', _module_typeBindings.ThroughputValueType)
    __throughputValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 750, 4)
    __throughputValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 750, 4)
    
    throughputValue = property(__throughputValue.value, __throughputValue.set, None, None)

    
    # Attribute throughputUnit uses Python identifier throughputUnit
    __throughputUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'throughputUnit'), 'throughputUnit', 'mapsPlatform_LogicalLinkType_throughputUnit', _module_typeBindings.ThroughputUnitType, unicode_default='bit/cycle')
    __throughputUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 751, 4)
    __throughputUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 751, 4)
    
    throughputUnit = property(__throughputUnit.value, __throughputUnit.set, None, None)

    
    # Attribute latencyValue uses Python identifier latencyValue
    __latencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyValue'), 'latencyValue', 'mapsPlatform_LogicalLinkType_latencyValue', _module_typeBindings.CyclesValueType, unicode_default='0')
    __latencyValue._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 752, 4)
    __latencyValue._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 752, 4)
    
    latencyValue = property(__latencyValue.value, __latencyValue.set, None, None)

    
    # Attribute latencyUnit uses Python identifier latencyUnit
    __latencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'latencyUnit'), 'latencyUnit', 'mapsPlatform_LogicalLinkType_latencyUnit', _module_typeBindings.CyclesUnitType, unicode_default='cycles')
    __latencyUnit._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 753, 4)
    __latencyUnit._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 753, 4)
    
    latencyUnit = property(__latencyUnit.value, __latencyUnit.set, None, None)

    
    # Attribute frequencyDomain uses Python identifier frequencyDomain
    __frequencyDomain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyDomain'), 'frequencyDomain', 'mapsPlatform_LogicalLinkType_frequencyDomain', _module_typeBindings.RefType, required=True)
    __frequencyDomain._DeclarationLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 754, 4)
    __frequencyDomain._UseLocation = pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 754, 4)
    
    frequencyDomain = property(__frequencyDomain.value, __frequencyDomain.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __throughputValue.name() : __throughputValue,
        __throughputUnit.name() : __throughputUnit,
        __latencyValue.name() : __latencyValue,
        __latencyUnit.name() : __latencyUnit,
        __frequencyDomain.name() : __frequencyDomain
    })
_module_typeBindings.LogicalLinkType = LogicalLinkType
Namespace.addCategoryObject('typeBinding', 'LogicalLinkType', LogicalLinkType)


Platform = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Platform'), PlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 867, 2))
Namespace.addCategoryObject('elementBinding', Platform.name().localName(), Platform)



VoltageFrequencyDomainConditionListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition'), VoltageDomainConditionType, scope=VoltageFrequencyDomainConditionListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6)))

VoltageFrequencyDomainConditionListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition'), FrequencyDomainConditionType, scope=VoltageFrequencyDomainConditionListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 269, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageFrequencyDomainConditionListType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageFrequencyDomainConditionListType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VoltageFrequencyDomainConditionListType._Automaton = _BuildAutomaton()




VoltageFrequencyConditionListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VoltageCondition'), VoltageConditionType, scope=VoltageFrequencyConditionListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6)))

VoltageFrequencyConditionListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FrequencyCondition'), FrequencyConditionType, scope=VoltageFrequencyConditionListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6)))

VoltageFrequencyConditionListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition'), FrequencyVoltageConditionType, scope=VoltageFrequencyConditionListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageFrequencyConditionListType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageFrequencyConditionListType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageFrequencyConditionListType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VoltageFrequencyConditionListType._Automaton = _BuildAutomaton_()




CommunicationBufferType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MemoryRef'), MemoryRefType, scope=CommunicationBufferType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 765, 6)))

CommunicationBufferType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FifoRef'), FifoRefType, scope=CommunicationBufferType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 766, 6)))

CommunicationBufferType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CacheRef'), CacheRefType, scope=CommunicationBufferType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 767, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 764, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationBufferType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 765, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationBufferType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 766, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationBufferType._UseForTag(pyxb.namespace.ExpandedName(None, 'CacheRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 767, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CommunicationBufferType._Automaton = _BuildAutomaton_2()




CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MemoryAccess'), MemoryAccessType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 772, 6)))

CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CacheAccess'), CacheAccessType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 773, 6)))

CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FifoAccess'), FifoAccessType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 774, 6)))

CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PhysicalLinkRef'), PhysicalLinkRefType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 775, 6)))

CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DMAControllerRef'), DMAControllerRefType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 776, 6)))

CommunicationPhaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'LogicalLinkRef'), LogicalLinkRefType, scope=CommunicationPhaseType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 777, 6)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 771, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryAccess')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 772, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'CacheAccess')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 773, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoAccess')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 774, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLinkRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 775, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAControllerRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 776, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationPhaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'LogicalLinkRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 777, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CommunicationPhaseType._Automaton = _BuildAutomaton_3()




SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Subsystem'), SubsystemType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 829, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VoltageDomain'), VoltageDomainType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 830, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FrequencyDomain'), FrequencyDomainType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 831, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SchedulingPolicyList'), SchedulingPolicyListType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 832, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Scheduler'), SchedulerType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 833, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessorPowerModel'), ProcessorPowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 834, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Processor'), ProcessorType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 835, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MemoryPowerModel'), MemoryPowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 836, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Memory'), MemoryType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 837, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CachePowerModel'), CachePowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 838, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Cache'), CacheType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 839, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FifoPowerModel'), FifoPowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 840, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Fifo'), FifoType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 841, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerModel'), PhysicalLinkPowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 842, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PhysicalLink'), PhysicalLinkType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 843, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerModel'), DMAControllerPowerModelType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 844, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DMAController'), DMAControllerType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 845, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'LogicalLink'), LogicalLinkType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 846, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Communication'), CommunicationType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 847, 6)))

SubsystemPlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Peripheral'), PeripheralType, scope=SubsystemPlatformType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 848, 6)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 828, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Subsystem')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 829, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 830, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 831, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'SchedulingPolicyList')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 832, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Scheduler')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 833, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 834, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Processor')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 835, 6))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 836, 6))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Memory')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 837, 6))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'CachePowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 838, 6))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Cache')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 839, 6))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 840, 6))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Fifo')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 841, 6))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 842, 6))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 843, 6))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 844, 6))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAController')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 845, 6))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'LogicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 846, 6))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Communication')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 847, 6))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemPlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Peripheral')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 848, 6))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubsystemPlatformType._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 269, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageInputType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageInputType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VoltageInputType._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 269, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyInputType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyInputType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FrequencyInputType._Automaton = _BuildAutomaton_6()




SchedulingPolicyListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SchedulingPolicy'), SchedulingPolicyType, scope=SchedulingPolicyListType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 317, 6)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SchedulingPolicyListType._UseForTag(pyxb.namespace.ExpandedName(None, 'SchedulingPolicy')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 317, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SchedulingPolicyListType._Automaton = _BuildAutomaton_7()




CommunicationProducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Buffer'), CommunicationBufferType, scope=CommunicationProducerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 782, 6)))

CommunicationProducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Active'), CommunicationPhaseType, scope=CommunicationProducerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 783, 6)))

CommunicationProducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Passive'), CommunicationPhaseType, scope=CommunicationProducerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 784, 6)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 782, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 783, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 784, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationProducerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Buffer')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 782, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationProducerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Active')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 783, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationProducerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Passive')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 784, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CommunicationProducerType._Automaton = _BuildAutomaton_8()




CommunicationConsumerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Buffer'), CommunicationBufferType, scope=CommunicationConsumerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 792, 6)))

CommunicationConsumerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Passive'), CommunicationPhaseType, scope=CommunicationConsumerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 793, 6)))

CommunicationConsumerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Active'), CommunicationPhaseType, scope=CommunicationConsumerType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 794, 6)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 792, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 793, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 794, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationConsumerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Buffer')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 792, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationConsumerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Passive')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 793, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CommunicationConsumerType._UseForTag(pyxb.namespace.ExpandedName(None, 'Active')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 794, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CommunicationConsumerType._Automaton = _BuildAutomaton_9()




CommunicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Buffer'), CommunicationBufferType, scope=CommunicationType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 802, 6)))

CommunicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Producer'), CommunicationProducerType, scope=CommunicationType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 803, 6)))

CommunicationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Consumer'), CommunicationConsumerType, scope=CommunicationType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 804, 6)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 802, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CommunicationType._UseForTag(pyxb.namespace.ExpandedName(None, 'Buffer')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 802, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CommunicationType._UseForTag(pyxb.namespace.ExpandedName(None, 'Producer')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 803, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CommunicationType._UseForTag(pyxb.namespace.ExpandedName(None, 'Consumer')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 804, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CommunicationType._Automaton = _BuildAutomaton_10()




PeripheralType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PeripheralEmulatorLibrary'), PeripheralEmulatorLibraryType, scope=PeripheralType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 820, 6)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 820, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PeripheralType._UseForTag(pyxb.namespace.ExpandedName(None, 'PeripheralEmulatorLibrary')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 820, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
PeripheralType._Automaton = _BuildAutomaton_11()




def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 828, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Subsystem')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 829, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 830, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 831, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'SchedulingPolicyList')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 832, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Scheduler')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 833, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 834, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Processor')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 835, 6))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 836, 6))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Memory')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 837, 6))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'CachePowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 838, 6))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Cache')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 839, 6))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 840, 6))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Fifo')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 841, 6))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 842, 6))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 843, 6))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 844, 6))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAController')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 845, 6))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'LogicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 846, 6))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Communication')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 847, 6))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubsystemType._UseForTag(pyxb.namespace.ExpandedName(None, 'Peripheral')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 848, 6))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubsystemType._Automaton = _BuildAutomaton_12()




def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 828, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Subsystem')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 829, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 830, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomain')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 831, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'SchedulingPolicyList')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 832, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Scheduler')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 833, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 834, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Processor')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 835, 6))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 836, 6))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Memory')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 837, 6))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'CachePowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 838, 6))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Cache')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 839, 6))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 840, 6))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Fifo')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 841, 6))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 842, 6))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 843, 6))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerModel')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 844, 6))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAController')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 845, 6))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'LogicalLink')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 846, 6))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Communication')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 847, 6))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, 'Peripheral')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 848, 6))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
PlatformType._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 269, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VoltageType._Automaton = _BuildAutomaton_14()




VoltageDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Voltage'), VoltageType, scope=VoltageDomainType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 216, 6)))

VoltageDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'VoltageInput'), VoltageInputType, scope=VoltageDomainType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 217, 6)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 215, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageDomainType._UseForTag(pyxb.namespace.ExpandedName(None, 'Voltage')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 216, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VoltageDomainType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageInput')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 217, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VoltageDomainType._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 269, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 270, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyDomainCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 271, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FrequencyType._Automaton = _BuildAutomaton_16()




FrequencyDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Frequency'), FrequencyType, scope=FrequencyDomainType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 244, 6)))

FrequencyDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FrequencyInput'), FrequencyInputType, scope=FrequencyDomainType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 245, 6)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 243, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyDomainType._UseForTag(pyxb.namespace.ExpandedName(None, 'Frequency')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 244, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FrequencyDomainType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyInput')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 245, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FrequencyDomainType._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProcessorPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProcessorPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProcessorPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ProcessorPowerStateType._Automaton = _BuildAutomaton_18()




ProcessorPowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessorPowerState'), ProcessorPowerStateType, scope=ProcessorPowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 340, 6)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ProcessorPowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorPowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 340, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ProcessorPowerModelType._Automaton = _BuildAutomaton_19()




ProcessorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataCacheRef'), CacheRefType, scope=ProcessorType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 374, 6)))

ProcessorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'InstructionCacheRef'), CacheRefType, scope=ProcessorType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 375, 6)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 374, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 375, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProcessorType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataCacheRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 374, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ProcessorType._UseForTag(pyxb.namespace.ExpandedName(None, 'InstructionCacheRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 375, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ProcessorType._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MemoryPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MemoryPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MemoryPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MemoryPowerStateType._Automaton = _BuildAutomaton_21()




MemoryPowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MemoryPowerState'), MemoryPowerStateType, scope=MemoryPowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 417, 6)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MemoryPowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'MemoryPowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 417, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MemoryPowerModelType._Automaton = _BuildAutomaton_22()




def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CachePowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CachePowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CachePowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CachePowerStateType._Automaton = _BuildAutomaton_23()




CachePowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CachePowerState'), CachePowerStateType, scope=CachePowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 517, 6)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CachePowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'CachePowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 517, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CachePowerModelType._Automaton = _BuildAutomaton_24()




CacheType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ParentCacheRef'), CacheRefType, scope=CacheType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 540, 6)))

CacheType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ParentMemoryRef'), MemoryRefType, scope=CacheType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 541, 6)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 539, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CacheType._UseForTag(pyxb.namespace.ExpandedName(None, 'ParentCacheRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 540, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CacheType._UseForTag(pyxb.namespace.ExpandedName(None, 'ParentMemoryRef')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 541, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CacheType._Automaton = _BuildAutomaton_25()




def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FifoPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FifoPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FifoPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FifoPowerStateType._Automaton = _BuildAutomaton_26()




FifoPowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FifoPowerState'), FifoPowerStateType, scope=FifoPowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 605, 6)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FifoPowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'FifoPowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 605, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FifoPowerModelType._Automaton = _BuildAutomaton_27()




def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PhysicalLinkPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PhysicalLinkPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PhysicalLinkPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
PhysicalLinkPowerStateType._Automaton = _BuildAutomaton_28()




PhysicalLinkPowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerState'), PhysicalLinkPowerStateType, scope=PhysicalLinkPowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 669, 6)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PhysicalLinkPowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'PhysicalLinkPowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 669, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
PhysicalLinkPowerModelType._Automaton = _BuildAutomaton_29()




def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 295, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DMAControllerPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'VoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 296, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DMAControllerPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 297, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DMAControllerPowerStateType._UseForTag(pyxb.namespace.ExpandedName(None, 'FrequencyVoltageCondition')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 298, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DMAControllerPowerStateType._Automaton = _BuildAutomaton_30()




DMAControllerPowerModelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerState'), DMAControllerPowerStateType, scope=DMAControllerPowerModelType, location=pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 713, 6)))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DMAControllerPowerModelType._UseForTag(pyxb.namespace.ExpandedName(None, 'DMAControllerPowerState')), pyxb.utils.utility.Location('MapsPlatformDescriptor.xsd', 713, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DMAControllerPowerModelType._Automaton = _BuildAutomaton_31()

