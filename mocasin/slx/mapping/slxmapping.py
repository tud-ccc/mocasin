# ./slxmapping.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:935dfabbddbb2f05981df2ac13478c8868ccc4c4
# Generated 2017-10-18 13:36:26.377426 by PyXB version 1.2.6 using Python 3.5.2.final.0
# Namespace http://xsd.silexica.com/slxMapping

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
from . import _slxplatform as _ImportedBinding__slxplatform
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xsd.silexica.com/slxMapping', create_if_missing=True)
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


# Atomic simple type: {http://xsd.silexica.com/slxMapping}PriorityType
class PriorityType (_ImportedBinding__slxplatform.NonNegativeIntType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PriorityType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 14, 2)
    _Documentation = None
PriorityType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PriorityType', PriorityType)
_module_typeBindings.PriorityType = PriorityType

# Atomic simple type: {http://xsd.silexica.com/slxMapping}ChannelBoundType
class ChannelBoundType (_ImportedBinding__slxplatform.NonNegativeIntType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChannelBoundType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 18, 2)
    _Documentation = None
ChannelBoundType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ChannelBoundType', ChannelBoundType)
_module_typeBindings.ChannelBoundType = ChannelBoundType

# Atomic simple type: {http://xsd.silexica.com/slxMapping}WrapLengthType
class WrapLengthType (_ImportedBinding__slxplatform.NonNegativeIntType):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'WrapLengthType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 21, 2)
    _Documentation = None
WrapLengthType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'WrapLengthType', WrapLengthType)
_module_typeBindings.WrapLengthType = WrapLengthType

# Complex type {http://xsd.silexica.com/slxMapping}ProcessRefType with content type EMPTY
class ProcessRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ProcessRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessRefType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 42, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute process uses Python identifier process
    __process = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'process'), 'process', '__httpxsd_silexica_comslxMapping_ProcessRefType_process', _ImportedBinding__slxplatform.RefType, required=True)
    __process._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 43, 4)
    __process._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 43, 4)
    
    process = property(__process.value, __process.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __process.name() : __process
    })
_module_typeBindings.ProcessRefType = ProcessRefType
Namespace.addCategoryObject('typeBinding', 'ProcessRefType', ProcessRefType)


# Complex type {http://xsd.silexica.com/slxMapping}ChannelRefType with content type EMPTY
class ChannelRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ChannelRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChannelRefType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 60, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute channel uses Python identifier channel
    __channel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'channel'), 'channel', '__httpxsd_silexica_comslxMapping_ChannelRefType_channel', _ImportedBinding__slxplatform.RefType, required=True)
    __channel._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 61, 4)
    __channel._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 61, 4)
    
    channel = property(__channel.value, __channel.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __channel.name() : __channel
    })
_module_typeBindings.ChannelRefType = ChannelRefType
Namespace.addCategoryObject('typeBinding', 'ChannelRefType', ChannelRefType)


# Complex type {http://xsd.silexica.com/slxMapping}ProcessorRefType with content type EMPTY
class ProcessorRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ProcessorRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorRefType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 78, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute processor uses Python identifier processor
    __processor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processor'), 'processor', '__httpxsd_silexica_comslxMapping_ProcessorRefType_processor', _ImportedBinding__slxplatform.RefType, required=True)
    __processor._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 79, 4)
    __processor._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 79, 4)
    
    processor = property(__processor.value, __processor.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __processor.name() : __processor
    })
_module_typeBindings.ProcessorRefType = ProcessorRefType
Namespace.addCategoryObject('typeBinding', 'ProcessorRefType', ProcessorRefType)


# Complex type {http://xsd.silexica.com/slxMapping}CommPrimitiveType with content type EMPTY
class CommPrimitiveType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}CommPrimitiveType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommPrimitiveType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 85, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxsd_silexica_comslxMapping_CommPrimitiveType_id', _ImportedBinding__slxplatform.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 86, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 86, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.CommPrimitiveType = CommPrimitiveType
Namespace.addCategoryObject('typeBinding', 'CommPrimitiveType', CommPrimitiveType)


# Complex type {http://xsd.silexica.com/slxMapping}CommPrimitiveRefType with content type EMPTY
class CommPrimitiveRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}CommPrimitiveRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CommPrimitiveRefType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 89, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute commPrimitive uses Python identifier commPrimitive
    __commPrimitive = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'commPrimitive'), 'commPrimitive', '__httpxsd_silexica_comslxMapping_CommPrimitiveRefType_commPrimitive', _ImportedBinding__slxplatform.RefType, required=True)
    __commPrimitive._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 90, 4)
    __commPrimitive._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 90, 4)
    
    commPrimitive = property(__commPrimitive.value, __commPrimitive.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __commPrimitive.name() : __commPrimitive
    })
_module_typeBindings.CommPrimitiveRefType = CommPrimitiveRefType
Namespace.addCategoryObject('typeBinding', 'CommPrimitiveRefType', CommPrimitiveRefType)


# Complex type {http://xsd.silexica.com/slxMapping}SchedulerType with content type ELEMENT_ONLY
class SchedulerType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}SchedulerType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulerType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 96, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProcessRef uses Python identifier ProcessRef
    __ProcessRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessRef'), 'ProcessRef', '__httpxsd_silexica_comslxMapping_SchedulerType_ProcessRef', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 98, 6), )

    
    ProcessRef = property(__ProcessRef.value, __ProcessRef.set, None, None)

    
    # Element ProcessorRef uses Python identifier ProcessorRef
    __ProcessorRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessorRef'), 'ProcessorRef', '__httpxsd_silexica_comslxMapping_SchedulerType_ProcessorRef', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 99, 6), )

    
    ProcessorRef = property(__ProcessorRef.value, __ProcessorRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxsd_silexica_comslxMapping_SchedulerType_id', _ImportedBinding__slxplatform.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 101, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 101, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __ProcessRef.name() : __ProcessRef,
        __ProcessorRef.name() : __ProcessorRef
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.SchedulerType = SchedulerType
Namespace.addCategoryObject('typeBinding', 'SchedulerType', SchedulerType)


# Complex type {http://xsd.silexica.com/slxMapping}SchedulerRefType with content type EMPTY
class SchedulerRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}SchedulerRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SchedulerRefType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 104, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute scheduler uses Python identifier scheduler
    __scheduler = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'scheduler'), 'scheduler', '__httpxsd_silexica_comslxMapping_SchedulerRefType_scheduler', _ImportedBinding__slxplatform.RefType, required=True)
    __scheduler._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 105, 4)
    __scheduler._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 105, 4)
    
    scheduler = property(__scheduler.value, __scheduler.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __scheduler.name() : __scheduler
    })
_module_typeBindings.SchedulerRefType = SchedulerRefType
Namespace.addCategoryObject('typeBinding', 'SchedulerRefType', SchedulerRefType)


# Complex type {http://xsd.silexica.com/slxMapping}ProcessType with content type ELEMENT_ONLY
class ProcessType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ProcessType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 26, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProcessorAffinityRef uses Python identifier ProcessorAffinityRef
    __ProcessorAffinityRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessorAffinityRef'), 'ProcessorAffinityRef', '__httpxsd_silexica_comslxMapping_ProcessType_ProcessorAffinityRef', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 28, 6), )

    
    ProcessorAffinityRef = property(__ProcessorAffinityRef.value, __ProcessorAffinityRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxsd_silexica_comslxMapping_ProcessType_id', _ImportedBinding__slxplatform.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 30, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 30, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute priority uses Python identifier priority
    __priority = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'priority'), 'priority', '__httpxsd_silexica_comslxMapping_ProcessType_priority', _module_typeBindings.PriorityType, required=True)
    __priority._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 31, 4)
    __priority._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 31, 4)
    
    priority = property(__priority.value, __priority.set, None, None)

    
    # Attribute iterationCount uses Python identifier iterationCount
    __iterationCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'iterationCount'), 'iterationCount', '__httpxsd_silexica_comslxMapping_ProcessType_iterationCount', _ImportedBinding__slxplatform.PositiveIntType)
    __iterationCount._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 32, 4)
    __iterationCount._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 32, 4)
    
    iterationCount = property(__iterationCount.value, __iterationCount.set, None, None)

    
    # Attribute powerPriority uses Python identifier powerPriority
    __powerPriority = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerPriority'), 'powerPriority', '__httpxsd_silexica_comslxMapping_ProcessType_powerPriority', _module_typeBindings.PriorityType)
    __powerPriority._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 33, 4)
    __powerPriority._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 33, 4)
    
    powerPriority = property(__powerPriority.value, __powerPriority.set, None, None)

    
    # Attribute powerPeakValue uses Python identifier powerPeakValue
    __powerPeakValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerPeakValue'), 'powerPeakValue', '__httpxsd_silexica_comslxMapping_ProcessType_powerPeakValue', _ImportedBinding__slxplatform.PowerValueType)
    __powerPeakValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 34, 4)
    __powerPeakValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 34, 4)
    
    powerPeakValue = property(__powerPeakValue.value, __powerPeakValue.set, None, None)

    
    # Attribute powerPeakUnit uses Python identifier powerPeakUnit
    __powerPeakUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerPeakUnit'), 'powerPeakUnit', '__httpxsd_silexica_comslxMapping_ProcessType_powerPeakUnit', _ImportedBinding__slxplatform.PowerUnitType, unicode_default='W')
    __powerPeakUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 35, 4)
    __powerPeakUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 35, 4)
    
    powerPeakUnit = property(__powerPeakUnit.value, __powerPeakUnit.set, None, None)

    
    # Attribute powerFrequencyValue uses Python identifier powerFrequencyValue
    __powerFrequencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerFrequencyValue'), 'powerFrequencyValue', '__httpxsd_silexica_comslxMapping_ProcessType_powerFrequencyValue', _ImportedBinding__slxplatform.FrequencyValueType)
    __powerFrequencyValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 36, 4)
    __powerFrequencyValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 36, 4)
    
    powerFrequencyValue = property(__powerFrequencyValue.value, __powerFrequencyValue.set, None, None)

    
    # Attribute powerFrequencyUnit uses Python identifier powerFrequencyUnit
    __powerFrequencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerFrequencyUnit'), 'powerFrequencyUnit', '__httpxsd_silexica_comslxMapping_ProcessType_powerFrequencyUnit', _ImportedBinding__slxplatform.FrequencyUnitType, unicode_default='Hz')
    __powerFrequencyUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 37, 4)
    __powerFrequencyUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 37, 4)
    
    powerFrequencyUnit = property(__powerFrequencyUnit.value, __powerFrequencyUnit.set, None, None)

    
    # Attribute powerVoltageValue uses Python identifier powerVoltageValue
    __powerVoltageValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerVoltageValue'), 'powerVoltageValue', '__httpxsd_silexica_comslxMapping_ProcessType_powerVoltageValue', _ImportedBinding__slxplatform.VoltageValueType)
    __powerVoltageValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 38, 4)
    __powerVoltageValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 38, 4)
    
    powerVoltageValue = property(__powerVoltageValue.value, __powerVoltageValue.set, None, None)

    
    # Attribute powerVoltageUnit uses Python identifier powerVoltageUnit
    __powerVoltageUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerVoltageUnit'), 'powerVoltageUnit', '__httpxsd_silexica_comslxMapping_ProcessType_powerVoltageUnit', _ImportedBinding__slxplatform.VoltageUnitType, unicode_default='V')
    __powerVoltageUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 39, 4)
    __powerVoltageUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 39, 4)
    
    powerVoltageUnit = property(__powerVoltageUnit.value, __powerVoltageUnit.set, None, None)

    _ElementMap.update({
        __ProcessorAffinityRef.name() : __ProcessorAffinityRef
    })
    _AttributeMap.update({
        __id.name() : __id,
        __priority.name() : __priority,
        __iterationCount.name() : __iterationCount,
        __powerPriority.name() : __powerPriority,
        __powerPeakValue.name() : __powerPeakValue,
        __powerPeakUnit.name() : __powerPeakUnit,
        __powerFrequencyValue.name() : __powerFrequencyValue,
        __powerFrequencyUnit.name() : __powerFrequencyUnit,
        __powerVoltageValue.name() : __powerVoltageValue,
        __powerVoltageUnit.name() : __powerVoltageUnit
    })
_module_typeBindings.ProcessType = ProcessType
Namespace.addCategoryObject('typeBinding', 'ProcessType', ProcessType)


# Complex type {http://xsd.silexica.com/slxMapping}ChannelType with content type ELEMENT_ONLY
class ChannelType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ChannelType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChannelType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 49, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ProcessReaderRef uses Python identifier ProcessReaderRef
    __ProcessReaderRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProcessReaderRef'), 'ProcessReaderRef', '__httpxsd_silexica_comslxMapping_ChannelType_ProcessReaderRef', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 51, 6), )

    
    ProcessReaderRef = property(__ProcessReaderRef.value, __ProcessReaderRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxsd_silexica_comslxMapping_ChannelType_id', _ImportedBinding__slxplatform.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 53, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 53, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute bound uses Python identifier bound
    __bound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'bound'), 'bound', '__httpxsd_silexica_comslxMapping_ChannelType_bound', _module_typeBindings.ChannelBoundType)
    __bound._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 54, 4)
    __bound._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 54, 4)
    
    bound = property(__bound.value, __bound.set, None, None)

    
    # Attribute wrapLength uses Python identifier wrapLength
    __wrapLength = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'wrapLength'), 'wrapLength', '__httpxsd_silexica_comslxMapping_ChannelType_wrapLength', _module_typeBindings.WrapLengthType)
    __wrapLength._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 55, 4)
    __wrapLength._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 55, 4)
    
    wrapLength = property(__wrapLength.value, __wrapLength.set, None, None)

    
    # Attribute commPrimitive uses Python identifier commPrimitive
    __commPrimitive = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'commPrimitive'), 'commPrimitive', '__httpxsd_silexica_comslxMapping_ChannelType_commPrimitive', _ImportedBinding__slxplatform.RefType, required=True)
    __commPrimitive._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 56, 4)
    __commPrimitive._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 56, 4)
    
    commPrimitive = property(__commPrimitive.value, __commPrimitive.set, None, None)

    
    # Attribute processWriter uses Python identifier processWriter
    __processWriter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'processWriter'), 'processWriter', '__httpxsd_silexica_comslxMapping_ChannelType_processWriter', _ImportedBinding__slxplatform.RefType, required=True)
    __processWriter._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 57, 4)
    __processWriter._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 57, 4)
    
    processWriter = property(__processWriter.value, __processWriter.set, None, None)

    _ElementMap.update({
        __ProcessReaderRef.name() : __ProcessReaderRef
    })
    _AttributeMap.update({
        __id.name() : __id,
        __bound.name() : __bound,
        __wrapLength.name() : __wrapLength,
        __commPrimitive.name() : __commPrimitive,
        __processWriter.name() : __processWriter
    })
_module_typeBindings.ChannelType = ChannelType
Namespace.addCategoryObject('typeBinding', 'ChannelType', ChannelType)


# Complex type {http://xsd.silexica.com/slxMapping}ProcessorType with content type EMPTY
class ProcessorType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}ProcessorType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProcessorType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 67, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxsd_silexica_comslxMapping_ProcessorType_id', _ImportedBinding__slxplatform.IdType, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 68, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 68, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpxsd_silexica_comslxMapping_ProcessorType_type', _ImportedBinding__slxplatform.NameType)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 69, 4)
    __type._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 69, 4)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute frequencyValue uses Python identifier frequencyValue
    __frequencyValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyValue'), 'frequencyValue', '__httpxsd_silexica_comslxMapping_ProcessorType_frequencyValue', _ImportedBinding__slxplatform.FrequencyValueType)
    __frequencyValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 70, 4)
    __frequencyValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 70, 4)
    
    frequencyValue = property(__frequencyValue.value, __frequencyValue.set, None, None)

    
    # Attribute frequencyUnit uses Python identifier frequencyUnit
    __frequencyUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'frequencyUnit'), 'frequencyUnit', '__httpxsd_silexica_comslxMapping_ProcessorType_frequencyUnit', _ImportedBinding__slxplatform.FrequencyUnitType, unicode_default='Hz')
    __frequencyUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 71, 4)
    __frequencyUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 71, 4)
    
    frequencyUnit = property(__frequencyUnit.value, __frequencyUnit.set, None, None)

    
    # Attribute voltageValue uses Python identifier voltageValue
    __voltageValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageValue'), 'voltageValue', '__httpxsd_silexica_comslxMapping_ProcessorType_voltageValue', _ImportedBinding__slxplatform.VoltageValueType)
    __voltageValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 72, 4)
    __voltageValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 72, 4)
    
    voltageValue = property(__voltageValue.value, __voltageValue.set, None, None)

    
    # Attribute voltageUnit uses Python identifier voltageUnit
    __voltageUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'voltageUnit'), 'voltageUnit', '__httpxsd_silexica_comslxMapping_ProcessorType_voltageUnit', _ImportedBinding__slxplatform.VoltageUnitType, unicode_default='V')
    __voltageUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 73, 4)
    __voltageUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 73, 4)
    
    voltageUnit = property(__voltageUnit.value, __voltageUnit.set, None, None)

    
    # Attribute powerIdleValue uses Python identifier powerIdleValue
    __powerIdleValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerIdleValue'), 'powerIdleValue', '__httpxsd_silexica_comslxMapping_ProcessorType_powerIdleValue', _ImportedBinding__slxplatform.PowerValueType)
    __powerIdleValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 74, 4)
    __powerIdleValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 74, 4)
    
    powerIdleValue = property(__powerIdleValue.value, __powerIdleValue.set, None, None)

    
    # Attribute powerIdleUnit uses Python identifier powerIdleUnit
    __powerIdleUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerIdleUnit'), 'powerIdleUnit', '__httpxsd_silexica_comslxMapping_ProcessorType_powerIdleUnit', _ImportedBinding__slxplatform.PowerUnitType, unicode_default='W')
    __powerIdleUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 75, 4)
    __powerIdleUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 75, 4)
    
    powerIdleUnit = property(__powerIdleUnit.value, __powerIdleUnit.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __type.name() : __type,
        __frequencyValue.name() : __frequencyValue,
        __frequencyUnit.name() : __frequencyUnit,
        __voltageValue.name() : __voltageValue,
        __voltageUnit.name() : __voltageUnit,
        __powerIdleValue.name() : __powerIdleValue,
        __powerIdleUnit.name() : __powerIdleUnit
    })
_module_typeBindings.ProcessorType = ProcessorType
Namespace.addCategoryObject('typeBinding', 'ProcessorType', ProcessorType)


# Complex type {http://xsd.silexica.com/slxMapping}MappingType with content type ELEMENT_ONLY
class MappingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://xsd.silexica.com/slxMapping}MappingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MappingType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 111, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Process uses Python identifier Process
    __Process = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Process'), 'Process', '__httpxsd_silexica_comslxMapping_MappingType_Process', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 114, 8), )

    
    Process = property(__Process.value, __Process.set, None, None)

    
    # Element Channel uses Python identifier Channel
    __Channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Channel'), 'Channel', '__httpxsd_silexica_comslxMapping_MappingType_Channel', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 115, 8), )

    
    Channel = property(__Channel.value, __Channel.set, None, None)

    
    # Element Processor uses Python identifier Processor
    __Processor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Processor'), 'Processor', '__httpxsd_silexica_comslxMapping_MappingType_Processor', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 116, 8), )

    
    Processor = property(__Processor.value, __Processor.set, None, None)

    
    # Element CommPrimitive uses Python identifier CommPrimitive
    __CommPrimitive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CommPrimitive'), 'CommPrimitive', '__httpxsd_silexica_comslxMapping_MappingType_CommPrimitive', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 117, 8), )

    
    CommPrimitive = property(__CommPrimitive.value, __CommPrimitive.set, None, None)

    
    # Element Scheduler uses Python identifier Scheduler
    __Scheduler = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Scheduler'), 'Scheduler', '__httpxsd_silexica_comslxMapping_MappingType_Scheduler', True, pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 118, 8), )

    
    Scheduler = property(__Scheduler.value, __Scheduler.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpxsd_silexica_comslxMapping_MappingType_version', _ImportedBinding__slxplatform.VersionType, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 121, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 121, 4)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute platformName uses Python identifier platformName
    __platformName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'platformName'), 'platformName', '__httpxsd_silexica_comslxMapping_MappingType_platformName', _ImportedBinding__slxplatform.NameType, required=True)
    __platformName._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 122, 4)
    __platformName._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 122, 4)
    
    platformName = property(__platformName.value, __platformName.set, None, None)

    
    # Attribute applicationName uses Python identifier applicationName
    __applicationName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'applicationName'), 'applicationName', '__httpxsd_silexica_comslxMapping_MappingType_applicationName', _ImportedBinding__slxplatform.NameType, required=True)
    __applicationName._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 123, 4)
    __applicationName._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 123, 4)
    
    applicationName = property(__applicationName.value, __applicationName.set, None, None)

    
    # Attribute globalChannelBound uses Python identifier globalChannelBound
    __globalChannelBound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'globalChannelBound'), 'globalChannelBound', '__httpxsd_silexica_comslxMapping_MappingType_globalChannelBound', _module_typeBindings.ChannelBoundType)
    __globalChannelBound._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 124, 4)
    __globalChannelBound._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 124, 4)
    
    globalChannelBound = property(__globalChannelBound.value, __globalChannelBound.set, None, None)

    
    # Attribute powerBudgetValue uses Python identifier powerBudgetValue
    __powerBudgetValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerBudgetValue'), 'powerBudgetValue', '__httpxsd_silexica_comslxMapping_MappingType_powerBudgetValue', _ImportedBinding__slxplatform.PowerValueType)
    __powerBudgetValue._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 125, 4)
    __powerBudgetValue._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 125, 4)
    
    powerBudgetValue = property(__powerBudgetValue.value, __powerBudgetValue.set, None, None)

    
    # Attribute powerBudgetUnit uses Python identifier powerBudgetUnit
    __powerBudgetUnit = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'powerBudgetUnit'), 'powerBudgetUnit', '__httpxsd_silexica_comslxMapping_MappingType_powerBudgetUnit', _ImportedBinding__slxplatform.PowerUnitType, unicode_default='W')
    __powerBudgetUnit._DeclarationLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 126, 4)
    __powerBudgetUnit._UseLocation = pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 126, 4)
    
    powerBudgetUnit = property(__powerBudgetUnit.value, __powerBudgetUnit.set, None, None)

    _ElementMap.update({
        __Process.name() : __Process,
        __Channel.name() : __Channel,
        __Processor.name() : __Processor,
        __CommPrimitive.name() : __CommPrimitive,
        __Scheduler.name() : __Scheduler
    })
    _AttributeMap.update({
        __version.name() : __version,
        __platformName.name() : __platformName,
        __applicationName.name() : __applicationName,
        __globalChannelBound.name() : __globalChannelBound,
        __powerBudgetValue.name() : __powerBudgetValue,
        __powerBudgetUnit.name() : __powerBudgetUnit
    })
_module_typeBindings.MappingType = MappingType
Namespace.addCategoryObject('typeBinding', 'MappingType', MappingType)


Mapping = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Mapping'), MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 130, 2))
Namespace.addCategoryObject('elementBinding', Mapping.name().localName(), Mapping)



SchedulerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessRef'), ProcessRefType, scope=SchedulerType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 98, 6)))

SchedulerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessorRef'), ProcessorRefType, scope=SchedulerType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 99, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 98, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SchedulerType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessRef')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 98, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SchedulerType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorRef')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 99, 6))
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
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SchedulerType._Automaton = _BuildAutomaton()




ProcessType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessorAffinityRef'), ProcessorRefType, scope=ProcessType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 28, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 28, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProcessType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessorAffinityRef')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 28, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ProcessType._Automaton = _BuildAutomaton_()




ChannelType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProcessReaderRef'), ProcessRefType, scope=ChannelType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 51, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ChannelType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProcessReaderRef')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ChannelType._Automaton = _BuildAutomaton_2()




MappingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Process'), ProcessType, scope=MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 114, 8)))

MappingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Channel'), ChannelType, scope=MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 115, 8)))

MappingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Processor'), ProcessorType, scope=MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 116, 8)))

MappingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CommPrimitive'), CommPrimitiveType, scope=MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 117, 8)))

MappingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Scheduler'), SchedulerType, scope=MappingType, location=pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 118, 8)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MappingType._UseForTag(pyxb.namespace.ExpandedName(None, 'Process')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 114, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MappingType._UseForTag(pyxb.namespace.ExpandedName(None, 'Channel')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 115, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MappingType._UseForTag(pyxb.namespace.ExpandedName(None, 'Processor')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 116, 8))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MappingType._UseForTag(pyxb.namespace.ExpandedName(None, 'CommPrimitive')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 117, 8))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MappingType._UseForTag(pyxb.namespace.ExpandedName(None, 'Scheduler')), pyxb.utils.utility.Location('/opt/maps/mnt/slx-git/libraries/xsd/slxMappingDescriptor/SlxMappingDescriptor.xsd', 118, 8))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MappingType._Automaton = _BuildAutomaton_3()

