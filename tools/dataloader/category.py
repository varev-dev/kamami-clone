from slugify import slugify
from utils import prettify_xml
from constants import LANG_IDS

class Category:
    _ID = 3
    
    def __init__(self, name, parentId):
        self.parentId = parentId
        self.id = self._ID
        self.name = name
        self.link = slugify(name)
        self._ID += 1
        
    def __str__(self):
        return f"""Category (
    parent: {self.parentId}
    id: {self.id}
    name: {self.name}
    link: {self.link}
)"""

    def to_xml(self):
        from xml.etree.ElementTree import Element, SubElement
        
        prestashop = Element("prestashop")
        prestashop.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

        category = SubElement(prestashop, "category")

        SubElement(category, "id_parent").text = str(self.parentId)
        SubElement(category, "active").text = "1"
        SubElement(category, "is_root_category").text = "0"

        name_el = SubElement(category, "name")
        for lang_id in LANG_IDS:
            SubElement(name_el, "language", {"id": str(lang_id)}).text = self.name

        link = SubElement(category, "link_rewrite")
        for lang_id in LANG_IDS:
            SubElement(link, "language", {"id": str(lang_id)}).text = self.link

        desc = SubElement(category, "description")
        for lang_id in LANG_IDS:
            SubElement(desc, "language", {"id": str(lang_id)}).text = ""

        meta_title = SubElement(category, "meta_title")
        for lang_id in LANG_IDS:
            SubElement(meta_title, "language", {"id": str(lang_id)}).text = self.name

        meta_desc = SubElement(category, "meta_description")
        for lang_id in LANG_IDS:
            SubElement(meta_desc, "language", {"id": str(lang_id)}).text = ""

        meta_keywords = SubElement(category, "meta_keywords")
        for lang_id in LANG_IDS:
            SubElement(meta_keywords, "language", {"id": str(lang_id)}).text = ""

        return prettify_xml(prestashop)