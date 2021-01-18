# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens
#
# ./_parser.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2020-12-03 11:40:22.190730 by PyXB version 1.2.6 using Python 3.8.6.final.0
# Namespace AbsentNamespace0

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f1db88fc-3553-11eb-b58c-448500c8805c')

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
Namespace = pyxb.namespace.CreateAbsentNamespace()
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


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 4, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element applicationGraph uses Python identifier applicationGraph
    __applicationGraph = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'applicationGraph'), 'applicationGraph', '__AbsentNamespace0_CTD_ANON_applicationGraph', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 18, 2), )

    
    applicationGraph = property(__applicationGraph.value, __applicationGraph.set, None, None)

    
    # Element architectureGraph uses Python identifier architectureGraph
    __architectureGraph = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'architectureGraph'), 'architectureGraph', '__AbsentNamespace0_CTD_ANON_architectureGraph', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 221, 2), )

    
    architectureGraph = property(__architectureGraph.value, __architectureGraph.set, None, None)

    
    # Element mapping uses Python identifier mapping
    __mapping = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mapping'), 'mapping', '__AbsentNamespace0_CTD_ANON_mapping', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 300, 2), )

    
    mapping = property(__mapping.value, __mapping.set, None, None)

    
    # Element systemUsage uses Python identifier systemUsage
    __systemUsage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'systemUsage'), 'systemUsage', '__AbsentNamespace0_CTD_ANON_systemUsage', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 347, 2), )

    
    systemUsage = property(__systemUsage.value, __systemUsage.set, None, None)

    
    # Element storageThroughputTradeOffs uses Python identifier storageThroughputTradeOffs
    __storageThroughputTradeOffs = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'storageThroughputTradeOffs'), 'storageThroughputTradeOffs', '__AbsentNamespace0_CTD_ANON_storageThroughputTradeOffs', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 356, 2), )

    
    storageThroughputTradeOffs = property(__storageThroughputTradeOffs.value, __storageThroughputTradeOffs.set, None, None)

    
    # Element messagesSet uses Python identifier messagesSet
    __messagesSet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messagesSet'), 'messagesSet', '__AbsentNamespace0_CTD_ANON_messagesSet', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 385, 2), )

    
    messagesSet = property(__messagesSet.value, __messagesSet.set, None, None)

    
    # Element settings uses Python identifier settings
    __settings = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'settings'), 'settings', '__AbsentNamespace0_CTD_ANON_settings', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 412, 2), )

    
    settings = property(__settings.value, __settings.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 14, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 14, 6)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__AbsentNamespace0_CTD_ANON_version', pyxb.binding.datatypes.string, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 15, 6)
    __version._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 15, 6)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __applicationGraph.name() : __applicationGraph,
        __architectureGraph.name() : __architectureGraph,
        __mapping.name() : __mapping,
        __systemUsage.name() : __systemUsage,
        __storageThroughputTradeOffs.name() : __storageThroughputTradeOffs,
        __messagesSet.name() : __messagesSet,
        __settings.name() : __settings
    })
    _AttributeMap.update({
        __type.name() : __type,
        __version.name() : __version
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 19, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element sdf uses Python identifier sdf
    __sdf = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sdf'), 'sdf', '__AbsentNamespace0_CTD_ANON__sdf', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 27, 2), )

    
    sdf = property(__sdf.value, __sdf.set, None, None)

    
    # Element sdfProperties uses Python identifier sdfProperties
    __sdfProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sdfProperties'), 'sdfProperties', '__AbsentNamespace0_CTD_ANON__sdfProperties', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 68, 2), )

    
    sdfProperties = property(__sdfProperties.value, __sdfProperties.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON__name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 24, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 24, 6)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __sdf.name() : __sdf,
        __sdfProperties.name() : __sdfProperties
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 28, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element actor uses Python identifier actor
    __actor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'actor'), 'actor', '__AbsentNamespace0_CTD_ANON_2_actor', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2), )

    
    actor = property(__actor.value, __actor.set, None, None)

    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_2_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2), )

    
    channel = property(__channel.value, __channel.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_2_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 33, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 33, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_2_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 34, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 34, 6)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        __actor.name() : __actor,
        __channel.name() : __channel
    })
    _AttributeMap.update({
        __name.name() : __name,
        __type.name() : __type
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 38, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element port uses Python identifier port
    __port = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'port'), 'port', '__AbsentNamespace0_CTD_ANON_3_port', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 47, 2), )

    
    port = property(__port.value, __port.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_3_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 42, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 42, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_3_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 43, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 43, 6)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_CTD_ANON_3_size', pyxb.binding.datatypes.decimal)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 44, 6)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 44, 6)
    
    size = property(__size.value, __size.set, None, None)

    _ElementMap.update({
        __port.name() : __port
    })
    _AttributeMap.update({
        __name.name() : __name,
        __type.name() : __type,
        __size.name() : __size
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 48, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_4_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 49, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 49, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_4_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 50, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 50, 6)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute rate uses Python identifier rate
    __rate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'rate'), 'rate', '__AbsentNamespace0_CTD_ANON_4_rate', pyxb.binding.datatypes.decimal, required=True)
    __rate._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 51, 6)
    __rate._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 51, 6)
    
    rate = property(__rate.value, __rate.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __type.name() : __type,
        __rate.name() : __rate
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 55, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_5_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 56, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 56, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute srcActor uses Python identifier srcActor
    __srcActor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'srcActor'), 'srcActor', '__AbsentNamespace0_CTD_ANON_5_srcActor', pyxb.binding.datatypes.string)
    __srcActor._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 57, 6)
    __srcActor._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 57, 6)
    
    srcActor = property(__srcActor.value, __srcActor.set, None, None)

    
    # Attribute srcPort uses Python identifier srcPort
    __srcPort = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'srcPort'), 'srcPort', '__AbsentNamespace0_CTD_ANON_5_srcPort', pyxb.binding.datatypes.string)
    __srcPort._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 58, 6)
    __srcPort._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 58, 6)
    
    srcPort = property(__srcPort.value, __srcPort.set, None, None)

    
    # Attribute dstActor uses Python identifier dstActor
    __dstActor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dstActor'), 'dstActor', '__AbsentNamespace0_CTD_ANON_5_dstActor', pyxb.binding.datatypes.string)
    __dstActor._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 59, 6)
    __dstActor._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 59, 6)
    
    dstActor = property(__dstActor.value, __dstActor.set, None, None)

    
    # Attribute dstPort uses Python identifier dstPort
    __dstPort = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dstPort'), 'dstPort', '__AbsentNamespace0_CTD_ANON_5_dstPort', pyxb.binding.datatypes.string)
    __dstPort._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 60, 6)
    __dstPort._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 60, 6)
    
    dstPort = property(__dstPort.value, __dstPort.set, None, None)

    
    # Attribute initialTokens uses Python identifier initialTokens
    __initialTokens = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'initialTokens'), 'initialTokens', '__AbsentNamespace0_CTD_ANON_5_initialTokens', pyxb.binding.datatypes.decimal)
    __initialTokens._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 61, 6)
    __initialTokens._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 61, 6)
    
    initialTokens = property(__initialTokens.value, __initialTokens.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_CTD_ANON_5_size', pyxb.binding.datatypes.decimal)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 62, 6)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 62, 6)
    
    size = property(__size.value, __size.set, None, None)

    
    # Attribute nrConnections uses Python identifier nrConnections
    __nrConnections = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'nrConnections'), 'nrConnections', '__AbsentNamespace0_CTD_ANON_5_nrConnections', pyxb.binding.datatypes.decimal)
    __nrConnections._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 63, 6)
    __nrConnections._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 63, 6)
    
    nrConnections = property(__nrConnections.value, __nrConnections.set, None, None)

    
    # Attribute inBandwidth uses Python identifier inBandwidth
    __inBandwidth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'inBandwidth'), 'inBandwidth', '__AbsentNamespace0_CTD_ANON_5_inBandwidth', pyxb.binding.datatypes.double)
    __inBandwidth._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 64, 6)
    __inBandwidth._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 64, 6)
    
    inBandwidth = property(__inBandwidth.value, __inBandwidth.set, None, None)

    
    # Attribute outBandwidth uses Python identifier outBandwidth
    __outBandwidth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'outBandwidth'), 'outBandwidth', '__AbsentNamespace0_CTD_ANON_5_outBandwidth', pyxb.binding.datatypes.double)
    __outBandwidth._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 65, 6)
    __outBandwidth._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 65, 6)
    
    outBandwidth = property(__outBandwidth.value, __outBandwidth.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __srcActor.name() : __srcActor,
        __srcPort.name() : __srcPort,
        __dstActor.name() : __dstActor,
        __dstPort.name() : __dstPort,
        __initialTokens.name() : __initialTokens,
        __size.name() : __size,
        __nrConnections.name() : __nrConnections,
        __inBandwidth.name() : __inBandwidth,
        __outBandwidth.name() : __outBandwidth
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 69, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element actorProperties uses Python identifier actorProperties
    __actorProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'actorProperties'), 'actorProperties', '__AbsentNamespace0_CTD_ANON_6_actorProperties', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 77, 2), )

    
    actorProperties = property(__actorProperties.value, __actorProperties.set, None, None)

    
    # Element channelProperties uses Python identifier channelProperties
    __channelProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'channelProperties'), 'channelProperties', '__AbsentNamespace0_CTD_ANON_6_channelProperties', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 132, 2), )

    
    channelProperties = property(__channelProperties.value, __channelProperties.set, None, None)

    
    # Element graphProperties uses Python identifier graphProperties
    __graphProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'graphProperties'), 'graphProperties', '__AbsentNamespace0_CTD_ANON_6_graphProperties', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 166, 2), )

    
    graphProperties = property(__graphProperties.value, __graphProperties.set, None, None)

    _ElementMap.update({
        __actorProperties.name() : __actorProperties,
        __channelProperties.name() : __channelProperties,
        __graphProperties.name() : __graphProperties
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 78, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element processor uses Python identifier processor
    __processor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'processor'), 'processor', '__AbsentNamespace0_CTD_ANON_7_processor', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 85, 2), )

    
    processor = property(__processor.value, __processor.set, None, None)

    
    # Attribute actor uses Python identifier actor
    __actor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'actor'), 'actor', '__AbsentNamespace0_CTD_ANON_7_actor', pyxb.binding.datatypes.string, required=True)
    __actor._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 82, 6)
    __actor._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 82, 6)
    
    actor = property(__actor.value, __actor.set, None, None)

    _ElementMap.update({
        __processor.name() : __processor
    })
    _AttributeMap.update({
        __actor.name() : __actor
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 86, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element actor uses Python identifier actor
    __actor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'actor'), 'actor', '__AbsentNamespace0_CTD_ANON_8_actor', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2), )

    
    actor = property(__actor.value, __actor.set, None, None)

    
    # Element executionTime uses Python identifier executionTime
    __executionTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'executionTime'), 'executionTime', '__AbsentNamespace0_CTD_ANON_8_executionTime', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 107, 2), )

    
    executionTime = property(__executionTime.value, __executionTime.set, None, None)

    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'memory'), 'memory', '__AbsentNamespace0_CTD_ANON_8_memory', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 112, 2), )

    
    memory = property(__memory.value, __memory.set, None, None)

    
    # Element arbitration uses Python identifier arbitration
    __arbitration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'arbitration'), 'arbitration', '__AbsentNamespace0_CTD_ANON_8_arbitration', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 241, 2), )

    
    arbitration = property(__arbitration.value, __arbitration.set, None, None)

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schedule'), 'schedule', '__AbsentNamespace0_CTD_ANON_8_schedule', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 311, 2), )

    
    schedule = property(__schedule.value, __schedule.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_8_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 100, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 100, 6)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute default uses Python identifier default
    __default = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'default'), 'default', '__AbsentNamespace0_CTD_ANON_8_default', pyxb.binding.datatypes.string)
    __default._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 101, 6)
    __default._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 101, 6)
    
    default = property(__default.value, __default.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_8_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 102, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 102, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute timeslice uses Python identifier timeslice
    __timeslice = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timeslice'), 'timeslice', '__AbsentNamespace0_CTD_ANON_8_timeslice', pyxb.binding.datatypes.decimal)
    __timeslice._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 103, 6)
    __timeslice._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 103, 6)
    
    timeslice = property(__timeslice.value, __timeslice.set, None, None)

    
    # Attribute timeSlice uses Python identifier timeSlice
    __timeSlice = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timeSlice'), 'timeSlice', '__AbsentNamespace0_CTD_ANON_8_timeSlice', pyxb.binding.datatypes.decimal)
    __timeSlice._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 104, 6)
    __timeSlice._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 104, 6)
    
    timeSlice = property(__timeSlice.value, __timeSlice.set, None, None)

    _ElementMap.update({
        __actor.name() : __actor,
        __executionTime.name() : __executionTime,
        __memory.name() : __memory,
        __arbitration.name() : __arbitration,
        __schedule.name() : __schedule
    })
    _AttributeMap.update({
        __type.name() : __type,
        __default.name() : __default,
        __name.name() : __name,
        __timeslice.name() : __timeslice,
        __timeSlice.name() : __timeSlice
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 108, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute time uses Python identifier time
    __time = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'time'), 'time', '__AbsentNamespace0_CTD_ANON_9_time', pyxb.binding.datatypes.decimal, required=True)
    __time._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 109, 6)
    __time._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 109, 6)
    
    time = property(__time.value, __time.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __time.name() : __time
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 113, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element actor uses Python identifier actor
    __actor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'actor'), 'actor', '__AbsentNamespace0_CTD_ANON_10_actor', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2), )

    
    actor = property(__actor.value, __actor.set, None, None)

    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_10_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2), )

    
    channel = property(__channel.value, __channel.set, None, None)

    
    # Element stateSize uses Python identifier stateSize
    __stateSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'stateSize'), 'stateSize', '__AbsentNamespace0_CTD_ANON_10_stateSize', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 127, 2), )

    
    stateSize = property(__stateSize.value, __stateSize.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_10_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 123, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 123, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_CTD_ANON_10_size', pyxb.binding.datatypes.decimal)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 124, 6)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 124, 6)
    
    size = property(__size.value, __size.set, None, None)

    _ElementMap.update({
        __actor.name() : __actor,
        __channel.name() : __channel,
        __stateSize.name() : __stateSize
    })
    _AttributeMap.update({
        __name.name() : __name,
        __size.name() : __size
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 128, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute max uses Python identifier max
    __max = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'max'), 'max', '__AbsentNamespace0_CTD_ANON_11_max', pyxb.binding.datatypes.decimal, required=True)
    __max._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 129, 6)
    __max._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 129, 6)
    
    max = property(__max.value, __max.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __max.name() : __max
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 133, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element bufferSize uses Python identifier bufferSize
    __bufferSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'bufferSize'), 'bufferSize', '__AbsentNamespace0_CTD_ANON_12_bufferSize', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 143, 2), )

    
    bufferSize = property(__bufferSize.value, __bufferSize.set, None, None)

    
    # Element tokenSize uses Python identifier tokenSize
    __tokenSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tokenSize'), 'tokenSize', '__AbsentNamespace0_CTD_ANON_12_tokenSize', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 151, 2), )

    
    tokenSize = property(__tokenSize.value, __tokenSize.set, None, None)

    
    # Element bandwidth uses Python identifier bandwidth
    __bandwidth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'bandwidth'), 'bandwidth', '__AbsentNamespace0_CTD_ANON_12_bandwidth', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 156, 2), )

    
    bandwidth = property(__bandwidth.value, __bandwidth.set, None, None)

    
    # Element latency uses Python identifier latency
    __latency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'latency'), 'latency', '__AbsentNamespace0_CTD_ANON_12_latency', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 161, 2), )

    
    latency = property(__latency.value, __latency.set, None, None)

    
    # Attribute channel uses Python identifier channel
    __channel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_12_channel', pyxb.binding.datatypes.string, required=True)
    __channel._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 140, 6)
    __channel._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 140, 6)
    
    channel = property(__channel.value, __channel.set, None, None)

    _ElementMap.update({
        __bufferSize.name() : __bufferSize,
        __tokenSize.name() : __tokenSize,
        __bandwidth.name() : __bandwidth,
        __latency.name() : __latency
    })
    _AttributeMap.update({
        __channel.name() : __channel
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 144, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute sz uses Python identifier sz
    __sz = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sz'), 'sz', '__AbsentNamespace0_CTD_ANON_13_sz', pyxb.binding.datatypes.decimal, required=True)
    __sz._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 145, 6)
    __sz._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 145, 6)
    
    sz = property(__sz.value, __sz.set, None, None)

    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__AbsentNamespace0_CTD_ANON_13_src', pyxb.binding.datatypes.decimal, required=True)
    __src._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 146, 6)
    __src._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 146, 6)
    
    src = property(__src.value, __src.set, None, None)

    
    # Attribute dst uses Python identifier dst
    __dst = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dst'), 'dst', '__AbsentNamespace0_CTD_ANON_13_dst', pyxb.binding.datatypes.decimal, required=True)
    __dst._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 147, 6)
    __dst._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 147, 6)
    
    dst = property(__dst.value, __dst.set, None, None)

    
    # Attribute mem uses Python identifier mem
    __mem = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mem'), 'mem', '__AbsentNamespace0_CTD_ANON_13_mem', pyxb.binding.datatypes.decimal, required=True)
    __mem._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 148, 6)
    __mem._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 148, 6)
    
    mem = property(__mem.value, __mem.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __sz.name() : __sz,
        __src.name() : __src,
        __dst.name() : __dst,
        __mem.name() : __mem
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 152, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute sz uses Python identifier sz
    __sz = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sz'), 'sz', '__AbsentNamespace0_CTD_ANON_14_sz', pyxb.binding.datatypes.decimal, required=True)
    __sz._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 153, 6)
    __sz._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 153, 6)
    
    sz = property(__sz.value, __sz.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __sz.name() : __sz
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 157, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'min'), 'min', '__AbsentNamespace0_CTD_ANON_15_min', pyxb.binding.datatypes.double, required=True)
    __min._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 158, 6)
    __min._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 158, 6)
    
    min = property(__min.value, __min.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __min.name() : __min
    })
_module_typeBindings.CTD_ANON_15 = CTD_ANON_15


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 162, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'min'), 'min', '__AbsentNamespace0_CTD_ANON_16_min', pyxb.binding.datatypes.decimal, required=True)
    __min._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 163, 6)
    __min._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 163, 6)
    
    min = property(__min.value, __min.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __min.name() : __min
    })
_module_typeBindings.CTD_ANON_16 = CTD_ANON_16


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 167, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element timeConstraints uses Python identifier timeConstraints
    __timeConstraints = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'timeConstraints'), 'timeConstraints', '__AbsentNamespace0_CTD_ANON_17_timeConstraints', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 174, 2), )

    
    timeConstraints = property(__timeConstraints.value, __timeConstraints.set, None, None)

    
    # Element maxplusSchedules uses Python identifier maxplusSchedules
    __maxplusSchedules = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'maxplusSchedules'), 'maxplusSchedules', '__AbsentNamespace0_CTD_ANON_17_maxplusSchedules', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 182, 2), )

    
    maxplusSchedules = property(__maxplusSchedules.value, __maxplusSchedules.set, None, None)

    _ElementMap.update({
        __timeConstraints.name() : __timeConstraints,
        __maxplusSchedules.name() : __maxplusSchedules
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_17 = CTD_ANON_17


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 175, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element throughput uses Python identifier throughput
    __throughput = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'throughput'), 'throughput', '__AbsentNamespace0_CTD_ANON_18_throughput', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 181, 2), )

    
    throughput = property(__throughput.value, __throughput.set, None, None)

    _ElementMap.update({
        __throughput.name() : __throughput
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_18 = CTD_ANON_18


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 183, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mpschedule_steadystate uses Python identifier mpschedule_steadystate
    __mpschedule_steadystate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_steadystate'), 'mpschedule_steadystate', '__AbsentNamespace0_CTD_ANON_19_mpschedule_steadystate', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 191, 2), )

    
    mpschedule_steadystate = property(__mpschedule_steadystate.value, __mpschedule_steadystate.set, None, None)

    
    # Element mpschedule_initial uses Python identifier mpschedule_initial
    __mpschedule_initial = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_initial'), 'mpschedule_initial', '__AbsentNamespace0_CTD_ANON_19_mpschedule_initial', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 198, 2), )

    
    mpschedule_initial = property(__mpschedule_initial.value, __mpschedule_initial.set, None, None)

    
    # Element mpperiod uses Python identifier mpperiod
    __mpperiod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mpperiod'), 'mpperiod', '__AbsentNamespace0_CTD_ANON_19_mpperiod', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 220, 2), )

    
    mpperiod = property(__mpperiod.value, __mpperiod.set, None, None)

    _ElementMap.update({
        __mpschedule_steadystate.name() : __mpschedule_steadystate,
        __mpschedule_initial.name() : __mpschedule_initial,
        __mpperiod.name() : __mpperiod
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_19 = CTD_ANON_19


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 192, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_20_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 194, 8), )

    
    channel = property(__channel.value, __channel.set, None, None)

    _ElementMap.update({
        __channel.name() : __channel
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_20 = CTD_ANON_20


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 199, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_21_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 201, 8), )

    
    channel = property(__channel.value, __channel.set, None, None)

    _ElementMap.update({
        __channel.name() : __channel
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_21 = CTD_ANON_21


# Complex type mpschedule_channel with content type ELEMENT_ONLY
class mpschedule_channel (pyxb.binding.basis.complexTypeDefinition):
    """Complex type mpschedule_channel with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'mpschedule_channel')
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 205, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element token uses Python identifier token
    __token = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'token'), 'token', '__AbsentNamespace0_mpschedule_channel_token', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 211, 2), )

    
    token = property(__token.value, __token.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_mpschedule_channel_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 209, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 209, 4)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __token.name() : __token
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.mpschedule_channel = mpschedule_channel
Namespace.addCategoryObject('typeBinding', 'mpschedule_channel', mpschedule_channel)


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.decimal
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 212, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.decimal
    
    # Attribute number uses Python identifier number
    __number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'number'), 'number', '__AbsentNamespace0_CTD_ANON_22_number', pyxb.binding.datatypes.decimal, required=True)
    __number._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 215, 10)
    __number._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 215, 10)
    
    number = property(__number.value, __number.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __number.name() : __number
    })
_module_typeBindings.CTD_ANON_22 = CTD_ANON_22


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 222, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tile uses Python identifier tile
    __tile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tile'), 'tile', '__AbsentNamespace0_CTD_ANON_23_tile', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2), )

    
    tile = property(__tile.value, __tile.set, None, None)

    
    # Element connection uses Python identifier connection
    __connection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'connection'), 'connection', '__AbsentNamespace0_CTD_ANON_23_connection', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 258, 2), )

    
    connection = property(__connection.value, __connection.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'network'), 'network', '__AbsentNamespace0_CTD_ANON_23_network', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2), )

    
    network = property(__network.value, __network.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_23_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 228, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 228, 6)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __tile.name() : __tile,
        __connection.name() : __connection,
        __network.name() : __network
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_23 = CTD_ANON_23


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_24 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 232, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element processor uses Python identifier processor
    __processor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'processor'), 'processor', '__AbsentNamespace0_CTD_ANON_24_processor', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 85, 2), )

    
    processor = property(__processor.value, __processor.set, None, None)

    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'memory'), 'memory', '__AbsentNamespace0_CTD_ANON_24_memory', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 112, 2), )

    
    memory = property(__memory.value, __memory.set, None, None)

    
    # Element networkInterface uses Python identifier networkInterface
    __networkInterface = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'networkInterface'), 'networkInterface', '__AbsentNamespace0_CTD_ANON_24_networkInterface', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 247, 2), )

    
    networkInterface = property(__networkInterface.value, __networkInterface.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_24_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 238, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 238, 6)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __processor.name() : __processor,
        __memory.name() : __memory,
        __networkInterface.name() : __networkInterface
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_24 = CTD_ANON_24


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 242, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_25_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 243, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 243, 6)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute wheelsize uses Python identifier wheelsize
    __wheelsize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'wheelsize'), 'wheelsize', '__AbsentNamespace0_CTD_ANON_25_wheelsize', pyxb.binding.datatypes.decimal, required=True)
    __wheelsize._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 244, 6)
    __wheelsize._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 244, 6)
    
    wheelsize = property(__wheelsize.value, __wheelsize.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __wheelsize.name() : __wheelsize
    })
_module_typeBindings.CTD_ANON_25 = CTD_ANON_25


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_26 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 248, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_26_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2), )

    
    channel = property(__channel.value, __channel.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_26_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 252, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 252, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute nrConnections uses Python identifier nrConnections
    __nrConnections = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'nrConnections'), 'nrConnections', '__AbsentNamespace0_CTD_ANON_26_nrConnections', pyxb.binding.datatypes.decimal)
    __nrConnections._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 253, 6)
    __nrConnections._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 253, 6)
    
    nrConnections = property(__nrConnections.value, __nrConnections.set, None, None)

    
    # Attribute inBandwidth uses Python identifier inBandwidth
    __inBandwidth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'inBandwidth'), 'inBandwidth', '__AbsentNamespace0_CTD_ANON_26_inBandwidth', pyxb.binding.datatypes.double)
    __inBandwidth._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 254, 6)
    __inBandwidth._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 254, 6)
    
    inBandwidth = property(__inBandwidth.value, __inBandwidth.set, None, None)

    
    # Attribute outBandwidth uses Python identifier outBandwidth
    __outBandwidth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'outBandwidth'), 'outBandwidth', '__AbsentNamespace0_CTD_ANON_26_outBandwidth', pyxb.binding.datatypes.double)
    __outBandwidth._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 255, 6)
    __outBandwidth._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 255, 6)
    
    outBandwidth = property(__outBandwidth.value, __outBandwidth.set, None, None)

    _ElementMap.update({
        __channel.name() : __channel
    })
    _AttributeMap.update({
        __name.name() : __name,
        __nrConnections.name() : __nrConnections,
        __inBandwidth.name() : __inBandwidth,
        __outBandwidth.name() : __outBandwidth
    })
_module_typeBindings.CTD_ANON_26 = CTD_ANON_26


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 259, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element channel uses Python identifier channel
    __channel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_27_channel', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2), )

    
    channel = property(__channel.value, __channel.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_27_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 263, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 263, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute srcTile uses Python identifier srcTile
    __srcTile = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'srcTile'), 'srcTile', '__AbsentNamespace0_CTD_ANON_27_srcTile', pyxb.binding.datatypes.string)
    __srcTile._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 264, 6)
    __srcTile._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 264, 6)
    
    srcTile = property(__srcTile.value, __srcTile.set, None, None)

    
    # Attribute dstTile uses Python identifier dstTile
    __dstTile = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dstTile'), 'dstTile', '__AbsentNamespace0_CTD_ANON_27_dstTile', pyxb.binding.datatypes.string)
    __dstTile._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 265, 6)
    __dstTile._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 265, 6)
    
    dstTile = property(__dstTile.value, __dstTile.set, None, None)

    
    # Attribute delay uses Python identifier delay
    __delay = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'delay'), 'delay', '__AbsentNamespace0_CTD_ANON_27_delay', pyxb.binding.datatypes.decimal)
    __delay._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 266, 6)
    __delay._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 266, 6)
    
    delay = property(__delay.value, __delay.set, None, None)

    _ElementMap.update({
        __channel.name() : __channel
    })
    _AttributeMap.update({
        __name.name() : __name,
        __srcTile.name() : __srcTile,
        __dstTile.name() : __dstTile,
        __delay.name() : __delay
    })
_module_typeBindings.CTD_ANON_27 = CTD_ANON_27


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_28 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 270, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tile uses Python identifier tile
    __tile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tile'), 'tile', '__AbsentNamespace0_CTD_ANON_28_tile', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2), )

    
    tile = property(__tile.value, __tile.set, None, None)

    
    # Element router uses Python identifier router
    __router = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'router'), 'router', '__AbsentNamespace0_CTD_ANON_28_router', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 287, 2), )

    
    router = property(__router.value, __router.set, None, None)

    
    # Element link uses Python identifier link
    __link = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'link'), 'link', '__AbsentNamespace0_CTD_ANON_28_link', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 292, 2), )

    
    link = property(__link.value, __link.set, None, None)

    
    # Element messages uses Python identifier messages
    __messages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messages'), 'messages', '__AbsentNamespace0_CTD_ANON_28_messages', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 324, 2), )

    
    messages = property(__messages.value, __messages.set, None, None)

    
    # Attribute slotTableSize uses Python identifier slotTableSize
    __slotTableSize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'slotTableSize'), 'slotTableSize', '__AbsentNamespace0_CTD_ANON_28_slotTableSize', pyxb.binding.datatypes.decimal)
    __slotTableSize._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 281, 6)
    __slotTableSize._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 281, 6)
    
    slotTableSize = property(__slotTableSize.value, __slotTableSize.set, None, None)

    
    # Attribute packetHeaderSize uses Python identifier packetHeaderSize
    __packetHeaderSize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'packetHeaderSize'), 'packetHeaderSize', '__AbsentNamespace0_CTD_ANON_28_packetHeaderSize', pyxb.binding.datatypes.decimal)
    __packetHeaderSize._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 282, 6)
    __packetHeaderSize._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 282, 6)
    
    packetHeaderSize = property(__packetHeaderSize.value, __packetHeaderSize.set, None, None)

    
    # Attribute flitSize uses Python identifier flitSize
    __flitSize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'flitSize'), 'flitSize', '__AbsentNamespace0_CTD_ANON_28_flitSize', pyxb.binding.datatypes.decimal)
    __flitSize._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 283, 6)
    __flitSize._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 283, 6)
    
    flitSize = property(__flitSize.value, __flitSize.set, None, None)

    
    # Attribute reconfigurationTimeNI uses Python identifier reconfigurationTimeNI
    __reconfigurationTimeNI = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'reconfigurationTimeNI'), 'reconfigurationTimeNI', '__AbsentNamespace0_CTD_ANON_28_reconfigurationTimeNI', pyxb.binding.datatypes.decimal)
    __reconfigurationTimeNI._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 284, 6)
    __reconfigurationTimeNI._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 284, 6)
    
    reconfigurationTimeNI = property(__reconfigurationTimeNI.value, __reconfigurationTimeNI.set, None, None)

    _ElementMap.update({
        __tile.name() : __tile,
        __router.name() : __router,
        __link.name() : __link,
        __messages.name() : __messages
    })
    _AttributeMap.update({
        __slotTableSize.name() : __slotTableSize,
        __packetHeaderSize.name() : __packetHeaderSize,
        __flitSize.name() : __flitSize,
        __reconfigurationTimeNI.name() : __reconfigurationTimeNI
    })
_module_typeBindings.CTD_ANON_28 = CTD_ANON_28


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_29 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 288, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_29_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 289, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 289, 6)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_29 = CTD_ANON_29


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_30 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 293, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_30_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 294, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 294, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__AbsentNamespace0_CTD_ANON_30_src', pyxb.binding.datatypes.string)
    __src._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 295, 6)
    __src._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 295, 6)
    
    src = property(__src.value, __src.set, None, None)

    
    # Attribute dst uses Python identifier dst
    __dst = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dst'), 'dst', '__AbsentNamespace0_CTD_ANON_30_dst', pyxb.binding.datatypes.string)
    __dst._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 296, 6)
    __dst._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 296, 6)
    
    dst = property(__dst.value, __dst.set, None, None)

    
    # Attribute occupiedSlots uses Python identifier occupiedSlots
    __occupiedSlots = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'occupiedSlots'), 'occupiedSlots', '__AbsentNamespace0_CTD_ANON_30_occupiedSlots', pyxb.binding.datatypes.string)
    __occupiedSlots._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 297, 6)
    __occupiedSlots._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 297, 6)
    
    occupiedSlots = property(__occupiedSlots.value, __occupiedSlots.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __src.name() : __src,
        __dst.name() : __dst,
        __occupiedSlots.name() : __occupiedSlots
    })
_module_typeBindings.CTD_ANON_30 = CTD_ANON_30


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_31 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 301, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tile uses Python identifier tile
    __tile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tile'), 'tile', '__AbsentNamespace0_CTD_ANON_31_tile', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2), )

    
    tile = property(__tile.value, __tile.set, None, None)

    
    # Element connection uses Python identifier connection
    __connection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'connection'), 'connection', '__AbsentNamespace0_CTD_ANON_31_connection', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 258, 2), )

    
    connection = property(__connection.value, __connection.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'network'), 'network', '__AbsentNamespace0_CTD_ANON_31_network', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2), )

    
    network = property(__network.value, __network.set, None, None)

    
    # Attribute appGraph uses Python identifier appGraph
    __appGraph = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'appGraph'), 'appGraph', '__AbsentNamespace0_CTD_ANON_31_appGraph', pyxb.binding.datatypes.string, required=True)
    __appGraph._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 307, 6)
    __appGraph._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 307, 6)
    
    appGraph = property(__appGraph.value, __appGraph.set, None, None)

    
    # Attribute archGraph uses Python identifier archGraph
    __archGraph = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'archGraph'), 'archGraph', '__AbsentNamespace0_CTD_ANON_31_archGraph', pyxb.binding.datatypes.string, required=True)
    __archGraph._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 308, 6)
    __archGraph._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 308, 6)
    
    archGraph = property(__archGraph.value, __archGraph.set, None, None)

    _ElementMap.update({
        __tile.name() : __tile,
        __connection.name() : __connection,
        __network.name() : __network
    })
    _AttributeMap.update({
        __appGraph.name() : __appGraph,
        __archGraph.name() : __archGraph
    })
_module_typeBindings.CTD_ANON_31 = CTD_ANON_31


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_32 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 312, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element state uses Python identifier state
    __state = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'state'), 'state', '__AbsentNamespace0_CTD_ANON_32_state', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 318, 2), )

    
    state = property(__state.value, __state.set, None, None)

    _ElementMap.update({
        __state.name() : __state
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_32 = CTD_ANON_32


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_33 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 319, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute actor uses Python identifier actor
    __actor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'actor'), 'actor', '__AbsentNamespace0_CTD_ANON_33_actor', pyxb.binding.datatypes.string, required=True)
    __actor._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 320, 6)
    __actor._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 320, 6)
    
    actor = property(__actor.value, __actor.set, None, None)

    
    # Attribute startOfPeriodicRegime uses Python identifier startOfPeriodicRegime
    __startOfPeriodicRegime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'startOfPeriodicRegime'), 'startOfPeriodicRegime', '__AbsentNamespace0_CTD_ANON_33_startOfPeriodicRegime', pyxb.binding.datatypes.boolean)
    __startOfPeriodicRegime._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 321, 6)
    __startOfPeriodicRegime._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 321, 6)
    
    startOfPeriodicRegime = property(__startOfPeriodicRegime.value, __startOfPeriodicRegime.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __actor.name() : __actor,
        __startOfPeriodicRegime.name() : __startOfPeriodicRegime
    })
_module_typeBindings.CTD_ANON_33 = CTD_ANON_33


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_34 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 325, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element schedulingEntity uses Python identifier schedulingEntity
    __schedulingEntity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'schedulingEntity'), 'schedulingEntity', '__AbsentNamespace0_CTD_ANON_34_schedulingEntity', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 338, 2), )

    
    schedulingEntity = property(__schedulingEntity.value, __schedulingEntity.set, None, None)

    
    # Element message uses Python identifier message
    __message = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'message'), 'message', '__AbsentNamespace0_CTD_ANON_34_message', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 393, 2), )

    
    message = property(__message.value, __message.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_34_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 334, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 334, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute period uses Python identifier period
    __period = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'period'), 'period', '__AbsentNamespace0_CTD_ANON_34_period', pyxb.binding.datatypes.decimal)
    __period._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 335, 6)
    __period._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 335, 6)
    
    period = property(__period.value, __period.set, None, None)

    _ElementMap.update({
        __schedulingEntity.name() : __schedulingEntity,
        __message.name() : __message
    })
    _AttributeMap.update({
        __name.name() : __name,
        __period.name() : __period
    })
_module_typeBindings.CTD_ANON_34 = CTD_ANON_34


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_35 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 339, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute msg uses Python identifier msg
    __msg = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'msg'), 'msg', '__AbsentNamespace0_CTD_ANON_35_msg', pyxb.binding.datatypes.string, required=True)
    __msg._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 340, 6)
    __msg._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 340, 6)
    
    msg = property(__msg.value, __msg.set, None, None)

    
    # Attribute startTime uses Python identifier startTime
    __startTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'startTime'), 'startTime', '__AbsentNamespace0_CTD_ANON_35_startTime', pyxb.binding.datatypes.decimal, required=True)
    __startTime._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 341, 6)
    __startTime._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 341, 6)
    
    startTime = property(__startTime.value, __startTime.set, None, None)

    
    # Attribute duration uses Python identifier duration
    __duration = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__AbsentNamespace0_CTD_ANON_35_duration', pyxb.binding.datatypes.decimal, required=True)
    __duration._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 342, 6)
    __duration._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 342, 6)
    
    duration = property(__duration.value, __duration.set, None, None)

    
    # Attribute route uses Python identifier route
    __route = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'route'), 'route', '__AbsentNamespace0_CTD_ANON_35_route', pyxb.binding.datatypes.string, required=True)
    __route._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 343, 6)
    __route._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 343, 6)
    
    route = property(__route.value, __route.set, None, None)

    
    # Attribute slots uses Python identifier slots
    __slots = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'slots'), 'slots', '__AbsentNamespace0_CTD_ANON_35_slots', pyxb.binding.datatypes.string, required=True)
    __slots._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 344, 6)
    __slots._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 344, 6)
    
    slots = property(__slots.value, __slots.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __msg.name() : __msg,
        __startTime.name() : __startTime,
        __duration.name() : __duration,
        __route.name() : __route,
        __slots.name() : __slots
    })
_module_typeBindings.CTD_ANON_35 = CTD_ANON_35


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_36 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 348, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tile uses Python identifier tile
    __tile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tile'), 'tile', '__AbsentNamespace0_CTD_ANON_36_tile', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2), )

    
    tile = property(__tile.value, __tile.set, None, None)

    
    # Element network uses Python identifier network
    __network = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'network'), 'network', '__AbsentNamespace0_CTD_ANON_36_network', False, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2), )

    
    network = property(__network.value, __network.set, None, None)

    
    # Attribute archGraph uses Python identifier archGraph
    __archGraph = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'archGraph'), 'archGraph', '__AbsentNamespace0_CTD_ANON_36_archGraph', pyxb.binding.datatypes.string, required=True)
    __archGraph._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 353, 6)
    __archGraph._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 353, 6)
    
    archGraph = property(__archGraph.value, __archGraph.set, None, None)

    _ElementMap.update({
        __tile.name() : __tile,
        __network.name() : __network
    })
    _AttributeMap.update({
        __archGraph.name() : __archGraph
    })
_module_typeBindings.CTD_ANON_36 = CTD_ANON_36


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_37 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 357, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element distributionsSet uses Python identifier distributionsSet
    __distributionsSet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'distributionsSet'), 'distributionsSet', '__AbsentNamespace0_CTD_ANON_37_distributionsSet', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 363, 2), )

    
    distributionsSet = property(__distributionsSet.value, __distributionsSet.set, None, None)

    _ElementMap.update({
        __distributionsSet.name() : __distributionsSet
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_37 = CTD_ANON_37


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_38 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 364, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element distribution uses Python identifier distribution
    __distribution = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'distribution'), 'distribution', '__AbsentNamespace0_CTD_ANON_38_distribution', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 372, 2), )

    
    distribution = property(__distribution.value, __distribution.set, None, None)

    
    # Attribute sz uses Python identifier sz
    __sz = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sz'), 'sz', '__AbsentNamespace0_CTD_ANON_38_sz', pyxb.binding.datatypes.decimal, required=True)
    __sz._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 368, 6)
    __sz._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 368, 6)
    
    sz = property(__sz.value, __sz.set, None, None)

    
    # Attribute thr uses Python identifier thr
    __thr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'thr'), 'thr', '__AbsentNamespace0_CTD_ANON_38_thr', pyxb.binding.datatypes.double, required=True)
    __thr._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 369, 6)
    __thr._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 369, 6)
    
    thr = property(__thr.value, __thr.set, None, None)

    _ElementMap.update({
        __distribution.name() : __distribution
    })
    _AttributeMap.update({
        __sz.name() : __sz,
        __thr.name() : __thr
    })
_module_typeBindings.CTD_ANON_38 = CTD_ANON_38


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_39 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 373, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ch uses Python identifier ch
    __ch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ch'), 'ch', '__AbsentNamespace0_CTD_ANON_39_ch', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 379, 2), )

    
    ch = property(__ch.value, __ch.set, None, None)

    _ElementMap.update({
        __ch.name() : __ch
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_39 = CTD_ANON_39


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_40 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 380, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_40_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 381, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 381, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute sz uses Python identifier sz
    __sz = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sz'), 'sz', '__AbsentNamespace0_CTD_ANON_40_sz', pyxb.binding.datatypes.decimal, required=True)
    __sz._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 382, 6)
    __sz._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 382, 6)
    
    sz = property(__sz.value, __sz.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __sz.name() : __sz
    })
_module_typeBindings.CTD_ANON_40 = CTD_ANON_40


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_41 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 386, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element messages uses Python identifier messages
    __messages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messages'), 'messages', '__AbsentNamespace0_CTD_ANON_41_messages', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 324, 2), )

    
    messages = property(__messages.value, __messages.set, None, None)

    
    # Element switch uses Python identifier switch
    __switch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'switch'), 'switch', '__AbsentNamespace0_CTD_ANON_41_switch', True, pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 405, 2), )

    
    switch = property(__switch.value, __switch.set, None, None)

    _ElementMap.update({
        __messages.name() : __messages,
        __switch.name() : __switch
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_41 = CTD_ANON_41


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_42 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 394, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute nr uses Python identifier nr
    __nr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'nr'), 'nr', '__AbsentNamespace0_CTD_ANON_42_nr', pyxb.binding.datatypes.decimal, required=True)
    __nr._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 395, 6)
    __nr._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 395, 6)
    
    nr = property(__nr.value, __nr.set, None, None)

    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__AbsentNamespace0_CTD_ANON_42_src', pyxb.binding.datatypes.string, required=True)
    __src._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 396, 6)
    __src._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 396, 6)
    
    src = property(__src.value, __src.set, None, None)

    
    # Attribute dst uses Python identifier dst
    __dst = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dst'), 'dst', '__AbsentNamespace0_CTD_ANON_42_dst', pyxb.binding.datatypes.string, required=True)
    __dst._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 397, 6)
    __dst._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 397, 6)
    
    dst = property(__dst.value, __dst.set, None, None)

    
    # Attribute channel uses Python identifier channel
    __channel = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'channel'), 'channel', '__AbsentNamespace0_CTD_ANON_42_channel', pyxb.binding.datatypes.string, required=True)
    __channel._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 398, 6)
    __channel._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 398, 6)
    
    channel = property(__channel.value, __channel.set, None, None)

    
    # Attribute seqNr uses Python identifier seqNr
    __seqNr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'seqNr'), 'seqNr', '__AbsentNamespace0_CTD_ANON_42_seqNr', pyxb.binding.datatypes.decimal, required=True)
    __seqNr._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 399, 6)
    __seqNr._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 399, 6)
    
    seqNr = property(__seqNr.value, __seqNr.set, None, None)

    
    # Attribute startTime uses Python identifier startTime
    __startTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'startTime'), 'startTime', '__AbsentNamespace0_CTD_ANON_42_startTime', pyxb.binding.datatypes.decimal, required=True)
    __startTime._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 400, 6)
    __startTime._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 400, 6)
    
    startTime = property(__startTime.value, __startTime.set, None, None)

    
    # Attribute duration uses Python identifier duration
    __duration = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__AbsentNamespace0_CTD_ANON_42_duration', pyxb.binding.datatypes.decimal, required=True)
    __duration._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 401, 6)
    __duration._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 401, 6)
    
    duration = property(__duration.value, __duration.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_CTD_ANON_42_size', pyxb.binding.datatypes.decimal, required=True)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 402, 6)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 402, 6)
    
    size = property(__size.value, __size.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __nr.name() : __nr,
        __src.name() : __src,
        __dst.name() : __dst,
        __channel.name() : __channel,
        __seqNr.name() : __seqNr,
        __startTime.name() : __startTime,
        __duration.name() : __duration,
        __size.name() : __size
    })
_module_typeBindings.CTD_ANON_42 = CTD_ANON_42


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_43 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 406, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute from uses Python identifier from_
    __from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'from'), 'from_', '__AbsentNamespace0_CTD_ANON_43_from', pyxb.binding.datatypes.string, required=True)
    __from._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 407, 6)
    __from._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 407, 6)
    
    from_ = property(__from.value, __from.set, None, None)

    
    # Attribute to uses Python identifier to
    __to = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'to'), 'to', '__AbsentNamespace0_CTD_ANON_43_to', pyxb.binding.datatypes.string, required=True)
    __to._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 408, 6)
    __to._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 408, 6)
    
    to = property(__to.value, __to.set, None, None)

    
    # Attribute overlap uses Python identifier overlap
    __overlap = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'overlap'), 'overlap', '__AbsentNamespace0_CTD_ANON_43_overlap', pyxb.binding.datatypes.decimal, required=True)
    __overlap._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 409, 6)
    __overlap._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 409, 6)
    
    overlap = property(__overlap.value, __overlap.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __from.name() : __from,
        __to.name() : __to,
        __overlap.name() : __overlap
    })
_module_typeBindings.CTD_ANON_43 = CTD_ANON_43


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_44 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 413, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_CTD_ANON_44_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 417, 6)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 417, 6)
    
    type = property(__type.value, __type.set, None, None)

    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type
    })
_module_typeBindings.CTD_ANON_44 = CTD_ANON_44


throughput = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'throughput'), pyxb.binding.datatypes.decimal, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 181, 2))
Namespace.addCategoryObject('elementBinding', throughput.name().localName(), throughput)

mpperiod = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpperiod'), pyxb.binding.datatypes.decimal, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 220, 2))
Namespace.addCategoryObject('elementBinding', mpperiod.name().localName(), mpperiod)

sdf3 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sdf3'), CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 3, 2))
Namespace.addCategoryObject('elementBinding', sdf3.name().localName(), sdf3)

applicationGraph = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationGraph'), CTD_ANON_, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 18, 2))
Namespace.addCategoryObject('elementBinding', applicationGraph.name().localName(), applicationGraph)

sdf = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sdf'), CTD_ANON_2, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 27, 2))
Namespace.addCategoryObject('elementBinding', sdf.name().localName(), sdf)

actor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actor'), CTD_ANON_3, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2))
Namespace.addCategoryObject('elementBinding', actor.name().localName(), actor)

port = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'port'), CTD_ANON_4, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 47, 2))
Namespace.addCategoryObject('elementBinding', port.name().localName(), port)

channel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channel'), CTD_ANON_5, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2))
Namespace.addCategoryObject('elementBinding', channel.name().localName(), channel)

sdfProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sdfProperties'), CTD_ANON_6, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 68, 2))
Namespace.addCategoryObject('elementBinding', sdfProperties.name().localName(), sdfProperties)

actorProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actorProperties'), CTD_ANON_7, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 77, 2))
Namespace.addCategoryObject('elementBinding', actorProperties.name().localName(), actorProperties)

processor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'processor'), CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 85, 2))
Namespace.addCategoryObject('elementBinding', processor.name().localName(), processor)

executionTime = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'executionTime'), CTD_ANON_9, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 107, 2))
Namespace.addCategoryObject('elementBinding', executionTime.name().localName(), executionTime)

memory = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'memory'), CTD_ANON_10, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 112, 2))
Namespace.addCategoryObject('elementBinding', memory.name().localName(), memory)

stateSize = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'stateSize'), CTD_ANON_11, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 127, 2))
Namespace.addCategoryObject('elementBinding', stateSize.name().localName(), stateSize)

channelProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channelProperties'), CTD_ANON_12, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 132, 2))
Namespace.addCategoryObject('elementBinding', channelProperties.name().localName(), channelProperties)

bufferSize = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'bufferSize'), CTD_ANON_13, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 143, 2))
Namespace.addCategoryObject('elementBinding', bufferSize.name().localName(), bufferSize)

tokenSize = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tokenSize'), CTD_ANON_14, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 151, 2))
Namespace.addCategoryObject('elementBinding', tokenSize.name().localName(), tokenSize)

bandwidth = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'bandwidth'), CTD_ANON_15, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 156, 2))
Namespace.addCategoryObject('elementBinding', bandwidth.name().localName(), bandwidth)

latency = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'latency'), CTD_ANON_16, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 161, 2))
Namespace.addCategoryObject('elementBinding', latency.name().localName(), latency)

graphProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'graphProperties'), CTD_ANON_17, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 166, 2))
Namespace.addCategoryObject('elementBinding', graphProperties.name().localName(), graphProperties)

timeConstraints = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'timeConstraints'), CTD_ANON_18, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 174, 2))
Namespace.addCategoryObject('elementBinding', timeConstraints.name().localName(), timeConstraints)

maxplusSchedules = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'maxplusSchedules'), CTD_ANON_19, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 182, 2))
Namespace.addCategoryObject('elementBinding', maxplusSchedules.name().localName(), maxplusSchedules)

mpschedule_steadystate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_steadystate'), CTD_ANON_20, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 191, 2))
Namespace.addCategoryObject('elementBinding', mpschedule_steadystate.name().localName(), mpschedule_steadystate)

mpschedule_initial = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_initial'), CTD_ANON_21, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 198, 2))
Namespace.addCategoryObject('elementBinding', mpschedule_initial.name().localName(), mpschedule_initial)

token = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'token'), CTD_ANON_22, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 211, 2))
Namespace.addCategoryObject('elementBinding', token.name().localName(), token)

architectureGraph = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'architectureGraph'), CTD_ANON_23, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 221, 2))
Namespace.addCategoryObject('elementBinding', architectureGraph.name().localName(), architectureGraph)

tile = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tile'), CTD_ANON_24, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2))
Namespace.addCategoryObject('elementBinding', tile.name().localName(), tile)

arbitration = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'arbitration'), CTD_ANON_25, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 241, 2))
Namespace.addCategoryObject('elementBinding', arbitration.name().localName(), arbitration)

networkInterface = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'networkInterface'), CTD_ANON_26, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 247, 2))
Namespace.addCategoryObject('elementBinding', networkInterface.name().localName(), networkInterface)

connection = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'connection'), CTD_ANON_27, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 258, 2))
Namespace.addCategoryObject('elementBinding', connection.name().localName(), connection)

network = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'network'), CTD_ANON_28, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2))
Namespace.addCategoryObject('elementBinding', network.name().localName(), network)

router = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'router'), CTD_ANON_29, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 287, 2))
Namespace.addCategoryObject('elementBinding', router.name().localName(), router)

link = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'link'), CTD_ANON_30, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 292, 2))
Namespace.addCategoryObject('elementBinding', link.name().localName(), link)

mapping = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mapping'), CTD_ANON_31, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 300, 2))
Namespace.addCategoryObject('elementBinding', mapping.name().localName(), mapping)

schedule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schedule'), CTD_ANON_32, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 311, 2))
Namespace.addCategoryObject('elementBinding', schedule.name().localName(), schedule)

state = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'state'), CTD_ANON_33, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 318, 2))
Namespace.addCategoryObject('elementBinding', state.name().localName(), state)

messages = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messages'), CTD_ANON_34, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 324, 2))
Namespace.addCategoryObject('elementBinding', messages.name().localName(), messages)

schedulingEntity = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schedulingEntity'), CTD_ANON_35, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 338, 2))
Namespace.addCategoryObject('elementBinding', schedulingEntity.name().localName(), schedulingEntity)

systemUsage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'systemUsage'), CTD_ANON_36, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 347, 2))
Namespace.addCategoryObject('elementBinding', systemUsage.name().localName(), systemUsage)

storageThroughputTradeOffs = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storageThroughputTradeOffs'), CTD_ANON_37, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 356, 2))
Namespace.addCategoryObject('elementBinding', storageThroughputTradeOffs.name().localName(), storageThroughputTradeOffs)

distributionsSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'distributionsSet'), CTD_ANON_38, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 363, 2))
Namespace.addCategoryObject('elementBinding', distributionsSet.name().localName(), distributionsSet)

distribution = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'distribution'), CTD_ANON_39, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 372, 2))
Namespace.addCategoryObject('elementBinding', distribution.name().localName(), distribution)

ch = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ch'), CTD_ANON_40, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 379, 2))
Namespace.addCategoryObject('elementBinding', ch.name().localName(), ch)

messagesSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messagesSet'), CTD_ANON_41, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 385, 2))
Namespace.addCategoryObject('elementBinding', messagesSet.name().localName(), messagesSet)

message = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'message'), CTD_ANON_42, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 393, 2))
Namespace.addCategoryObject('elementBinding', message.name().localName(), message)

switch = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'switch'), CTD_ANON_43, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 405, 2))
Namespace.addCategoryObject('elementBinding', switch.name().localName(), switch)

settings = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'settings'), CTD_ANON_44, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 412, 2))
Namespace.addCategoryObject('elementBinding', settings.name().localName(), settings)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'applicationGraph'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 18, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'architectureGraph'), CTD_ANON_23, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 221, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mapping'), CTD_ANON_31, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 300, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'systemUsage'), CTD_ANON_36, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 347, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storageThroughputTradeOffs'), CTD_ANON_37, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 356, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messagesSet'), CTD_ANON_41, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 385, 2)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'settings'), CTD_ANON_44, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 412, 2)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 6, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 7, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 8, 8))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 9, 8))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 10, 8))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 11, 8))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 12, 8))
    counters.add(cc_6)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'applicationGraph')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 6, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'architectureGraph')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 7, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mapping')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 8, 8))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'systemUsage')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 9, 8))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storageThroughputTradeOffs')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 10, 8))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messagesSet')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 11, 8))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'settings')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 12, 8))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sdf'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 27, 2)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sdfProperties'), CTD_ANON_6, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 68, 2)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 22, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sdf')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 21, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sdfProperties')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 22, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actor'), CTD_ANON_3, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channel'), CTD_ANON_5, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 31, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'actor')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 30, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 31, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'port'), CTD_ANON_4, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 47, 2)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 40, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'port')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 40, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actorProperties'), CTD_ANON_7, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 77, 2)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channelProperties'), CTD_ANON_12, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 132, 2)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'graphProperties'), CTD_ANON_17, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 166, 2)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 72, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 73, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'actorProperties')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 71, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'channelProperties')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 72, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'graphProperties')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 73, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_4()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'processor'), CTD_ANON_8, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 85, 2)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'processor')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 80, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_5()




CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actor'), CTD_ANON_3, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2)))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'executionTime'), CTD_ANON_9, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 107, 2)))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'memory'), CTD_ANON_10, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 112, 2)))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'arbitration'), CTD_ANON_25, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 241, 2)))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schedule'), CTD_ANON_32, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 311, 2)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 90, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 96, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 97, 10))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'executionTime')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 89, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'memory')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 90, 10))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'arbitration')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 93, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'actor')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 96, 10))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schedule')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 97, 10))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_8._Automaton = _BuildAutomaton_6()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'actor'), CTD_ANON_3, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 37, 2)))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channel'), CTD_ANON_5, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2)))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'stateSize'), CTD_ANON_11, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 127, 2)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 119, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 120, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'stateSize')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 116, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'actor')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 119, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 120, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_7()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'bufferSize'), CTD_ANON_13, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 143, 2)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tokenSize'), CTD_ANON_14, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 151, 2)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'bandwidth'), CTD_ANON_15, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 156, 2)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'latency'), CTD_ANON_16, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 161, 2)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 135, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 136, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 137, 8))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 138, 8))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'bufferSize')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 135, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tokenSize')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 136, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'bandwidth')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 137, 8))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'latency')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 138, 8))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_8()




CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'timeConstraints'), CTD_ANON_18, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 174, 2)))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'maxplusSchedules'), CTD_ANON_19, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 182, 2)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 169, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 170, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'timeConstraints')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 169, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'maxplusSchedules')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 170, 8))
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
CTD_ANON_17._Automaton = _BuildAutomaton_9()




CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'throughput'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_18, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 181, 2)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 177, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'throughput')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 177, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_18._Automaton = _BuildAutomaton_10()




CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_steadystate'), CTD_ANON_20, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 191, 2)))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_initial'), CTD_ANON_21, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 198, 2)))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mpperiod'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 220, 2)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 185, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 186, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 187, 8))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_steadystate')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 185, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mpschedule_initial')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 186, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mpperiod')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 187, 8))
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
CTD_ANON_19._Automaton = _BuildAutomaton_11()




CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'channel'), mpschedule_channel, scope=CTD_ANON_20, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 194, 8)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 194, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_20._Automaton = _BuildAutomaton_12()




CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'channel'), mpschedule_channel, scope=CTD_ANON_21, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 201, 8)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(None, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 201, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_21._Automaton = _BuildAutomaton_13()




mpschedule_channel._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'token'), CTD_ANON_22, scope=mpschedule_channel, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 211, 2)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(mpschedule_channel._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'token')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 207, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
mpschedule_channel._Automaton = _BuildAutomaton_14()




CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tile'), CTD_ANON_24, scope=CTD_ANON_23, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2)))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'connection'), CTD_ANON_27, scope=CTD_ANON_23, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 258, 2)))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'network'), CTD_ANON_28, scope=CTD_ANON_23, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 225, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 226, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tile')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 224, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'connection')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 225, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'network')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 226, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_23._Automaton = _BuildAutomaton_15()




CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'processor'), CTD_ANON_8, scope=CTD_ANON_24, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 85, 2)))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'memory'), CTD_ANON_10, scope=CTD_ANON_24, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 112, 2)))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'networkInterface'), CTD_ANON_26, scope=CTD_ANON_24, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 247, 2)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'processor')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 234, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'memory')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 235, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'networkInterface')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 236, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_24._Automaton = _BuildAutomaton_16()




CTD_ANON_26._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channel'), CTD_ANON_5, scope=CTD_ANON_26, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 250, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 250, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_26._Automaton = _BuildAutomaton_17()




CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'channel'), CTD_ANON_5, scope=CTD_ANON_27, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 54, 2)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 261, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'channel')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 261, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_27._Automaton = _BuildAutomaton_18()




CTD_ANON_28._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tile'), CTD_ANON_24, scope=CTD_ANON_28, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2)))

CTD_ANON_28._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'router'), CTD_ANON_29, scope=CTD_ANON_28, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 287, 2)))

CTD_ANON_28._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'link'), CTD_ANON_30, scope=CTD_ANON_28, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 292, 2)))

CTD_ANON_28._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messages'), CTD_ANON_34, scope=CTD_ANON_28, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 324, 2)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 273, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 274, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 278, 10))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_28._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tile')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 273, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_28._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'router')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 274, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_28._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'link')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 275, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_28._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messages')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 278, 10))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_28._Automaton = _BuildAutomaton_19()




CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tile'), CTD_ANON_24, scope=CTD_ANON_31, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2)))

CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'connection'), CTD_ANON_27, scope=CTD_ANON_31, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 258, 2)))

CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'network'), CTD_ANON_28, scope=CTD_ANON_31, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 303, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 304, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 305, 8))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tile')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 303, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'connection')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 304, 8))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'network')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 305, 8))
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
CTD_ANON_31._Automaton = _BuildAutomaton_20()




CTD_ANON_32._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'state'), CTD_ANON_33, scope=CTD_ANON_32, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 318, 2)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 314, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_32._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'state')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 314, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_32._Automaton = _BuildAutomaton_21()




CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schedulingEntity'), CTD_ANON_35, scope=CTD_ANON_34, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 338, 2)))

CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'message'), CTD_ANON_42, scope=CTD_ANON_34, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 393, 2)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 328, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 331, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'schedulingEntity')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 328, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'message')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 331, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_34._Automaton = _BuildAutomaton_22()




CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tile'), CTD_ANON_24, scope=CTD_ANON_36, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 231, 2)))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'network'), CTD_ANON_28, scope=CTD_ANON_36, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 269, 2)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 350, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 351, 8))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tile')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 350, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'network')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 351, 8))
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
CTD_ANON_36._Automaton = _BuildAutomaton_23()




CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'distributionsSet'), CTD_ANON_38, scope=CTD_ANON_37, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 363, 2)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'distributionsSet')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 359, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_37._Automaton = _BuildAutomaton_24()




CTD_ANON_38._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'distribution'), CTD_ANON_39, scope=CTD_ANON_38, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 372, 2)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_38._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'distribution')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 366, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_38._Automaton = _BuildAutomaton_25()




CTD_ANON_39._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ch'), CTD_ANON_40, scope=CTD_ANON_39, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 379, 2)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_39._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ch')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 375, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_39._Automaton = _BuildAutomaton_26()




CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messages'), CTD_ANON_34, scope=CTD_ANON_41, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 324, 2)))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'switch'), CTD_ANON_43, scope=CTD_ANON_41, location=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 405, 2)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 389, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messages')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 388, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'switch')), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 389, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_41._Automaton = _BuildAutomaton_27()




def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 415, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/cmenard/third-party/src/sdf3/sdf/xsd/sdf3-sdf.xsd', 415, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_44._Automaton = _BuildAutomaton_28()

