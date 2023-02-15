from typing import Dict, Any
from jinja2 import Template
from mkdocs import plugins
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.config import config_options
from mkdocs.structure.pages import Page
from mkdocs.utils import copy_file
import os

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError
    
PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(PLUGIN_DIR, "templates/list.html")
EXTRA_CSS = ["css/navlist.css"]

class DocTree():
    def __init__(self):
        self.typeof = None
        self.can_link = False
        self.url = None
        self.title = None
        self.children = []

class NavTocPlugin(plugins.BasePlugin):
    config_scheme = ()

    nav_cache = {}

    def on_config(self, config: config_options.Config, **kwargs) -> Dict[str, Any]:
        config["extra_css"] = EXTRA_CSS + config["extra_css"]

    def on_nav(self, nav, *, config: MkDocsConfig, files):
        self.nav = nav

    def on_post_build(self, config: Dict[str, Any], **kwargs):
        for file in EXTRA_CSS:
            dest_file_path = os.path.join(config["site_dir"], file)
            src_file_path = os.path.join(PLUGIN_DIR, file)
            assert os.path.exists(src_file_path)
            copy_file(src_file_path, dest_file_path)

    def get_cache(self, item: Page):
        return self.nav_cache.get(item.title)
    
    def set_cache(self, item: Page, doc: DocTree):
        self.nav_cache[item.title] = doc
    
    def generate_navtoc(self, item: Page, page: Page):
        if self.get_cache(item):
            return self.get_cache(item)

        doc = DocTree()
        if item == page or (item.is_page and item.is_index):
            pass
        elif item.is_page or item.is_link:
            doc.can_link = True
            doc.title = item.title
            doc.url = item.abs_url
        elif item.is_section:
            doc.title = item.title
            for child_item in item.children:
                if child_item.is_page and child_item.is_index:
                    doc.can_link = True
                    doc.url = child_item.abs_url
                else:
                    doc.children.append(self.generate_navtoc(child_item, page))
        self.set_cache(item, doc)
        return self.get_cache(item)

    def format_navtoc(self, items, page):
        docs = []
        for item in items:
            docs.append(self.generate_navtoc(item, page))
        
        with open(TEMPLATE_DIR, "r", encoding="utf-8") as file:
            TEMPLATE = file.read()
        return Template(TEMPLATE).render(docs=docs)

    def on_page_context(
            self, context: Dict[str, Any], *, page: Page, config: MkDocsConfig, nav
    ):
        if page.meta.get("navtoc"):
            children = page.parent.children if page.parent else self.nav.items
            context['page'].content += self.format_navtoc(children, page)
            return context


if __name__ == "__main__":
    
    pass
