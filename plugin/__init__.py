from typing import Dict, Any
from mkdocs import plugins
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError


class NavTocPlugin(plugins.BasePlugin):
    config_scheme = ()

    nav_header = '<h2 id="navtoc">Table of Contents<a class="headerlink" href="#navtoc" title="Permanent link">¶</a></h2> '
    nav_cache = {}

    def on_nav(self, nav, *, config: MkDocsConfig, files):
        self.nav = nav

    def _format_navtoc(self, item: Page, page: Page):

        if self.nav_cache.get(item.title + item.__class__.__qualname__):
            return self.nav_cache[item.title + item.__class__.__qualname__]
        result = ""
        if item == page or (item.is_page and item.is_index):
            pass
        elif item.is_page or item.is_link:
            result = f"<li><a href=\"{item.abs_url}\">{item.title}</a></li>"
        elif item.is_section:
            toc_front = item.title
            toc = ""
            for child_item in item.children:
                if child_item.is_page and child_item.is_index:
                    toc_front = f"<a href=\"{child_item.abs_url}\">{item.title}</a>"
                else:
                    toc += self._format_navtoc(child_item, page)
            result = f"<li>{toc_front}<ul>{toc}</ul></li>"

        self.nav_cache[item.title + item.__class__.__qualname__] = result
        return result

    def format_navtoc(self, items, page):
        toc = ""
        for item in items:
            toc += self._format_navtoc(item, page)
        return f"<ul>{toc}</ul>"

    def on_page_context(
            self, context: Dict[str, Any], *, page: Page, config: MkDocsConfig, nav
    ):
        if page.meta.get("navtoc"):
            children = page.parent.children if page.parent else self.nav.items
            context['page'].content += f"{self.nav_header}\n{self.format_navtoc(children, page)}"
            return context
