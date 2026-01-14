from slugify import slugify
from utils import prettify_xml
from constants import LANG_IDS

class Category:
    def __init__(self, name, subcategories, parent_id, id=None, link=None):
        self.parent_id = parent_id
        self.id = None if id is None else id
        self.name = name
        self.subcategories = subcategories
        self.link = slugify(name) if link is None else link
        
    def __str__(self):
        return f"""Category (
    parent: {self.parent_id}
    id: {self.id}
    name: {self.name}
    link: {self.link}
)"""

    def to_dict(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "name": self.name,
            "link": self.link,
            "subcategories": [
                subcat.to_dict() for subcat in self.subcategories
            ]
        }
   
    @classmethod
    def from_dict(cls, data):
        subcategories = [
            cls.from_dict(subcat)
            for subcat in data.get("subcategories", [])
        ]

        category = cls(
            name=data["name"],
            parent_id=data["parent_id"],
            subcategories=subcategories
        )

        category.id = data.get("id")
        return category

    def to_xml(self):
        from xml.etree.ElementTree import Element, SubElement
        
        prestashop = Element("prestashop")
        prestashop.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

        category = SubElement(prestashop, "category")

        SubElement(category, "id_parent").text = str(self.parent_id)
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

    
    def unpack(self, is_top=True):
        result = [self] if is_top else []
        for cat in self.subcategories:
            result.append(cat)
            result.extend(cat.unpack(False))
            
        return result