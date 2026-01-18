def prettify_xml(element):
    from xml.dom import minidom
    from xml.etree.ElementTree import tostring
    
    rough = tostring(element, encoding='utf-8')
    return minidom.parseString(rough).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")