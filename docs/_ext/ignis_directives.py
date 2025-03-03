from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata
from sphinx.ext.autodoc import PropertyDocumenter, AttributeDocumenter
from sphinx.domains.python import PyProperty
from docutils import nodes
from docutils.statemachine import StringList
from typing import Any
from sphinx import addnodes
from sphinx.ext.autodoc.mock import mock


def create_prefix(name: str) -> list[nodes.Node]:
    prefix: list[nodes.Node] = []
    prefix.append(nodes.Text(name))
    prefix.append(addnodes.desc_sig_space())
    return prefix


class FakeGProperty(property): ...


class FakeSignal(property): ...


class GPropertyDocumenter(PropertyDocumenter):
    objtype = "gproperty"
    directivetype = "gproperty"
    priority = PropertyDocumenter.priority + 1

    @classmethod
    def can_document_member(
        cls, member: Any, membername: str, isattr: bool, parent: Any
    ) -> bool:
        return isinstance(member, FakeGProperty)

    def add_content(
        self,
        more_content: StringList | None,
    ) -> None:
        source_name = self.get_sourcename()
        obj = self.object

        if obj.fset:
            self.add_line("- read-write", source_name)
        else:
            self.add_line("- read-only", source_name)

        self.add_line("", source_name)

        super().add_content(more_content)


class SignalDocumenter(AttributeDocumenter):
    objtype = "signal"
    directivetype = "signal"
    priority = AttributeDocumenter.priority + 1

    @classmethod
    def can_document_member(
        cls, member: Any, membername: str, isattr: bool, parent: Any
    ) -> bool:
        return isinstance(member, FakeSignal)


class PropertyDirective(PyProperty):
    def get_signature_prefix(self, sig: str) -> list[nodes.Node]:
        return create_prefix("gproperty")


class SignalDirective(PyProperty):
    def get_signature_prefix(self, sig: str) -> list[nodes.Node]:
        return create_prefix("signal")


def patch(app: Sphinx) -> None:
    with mock(app.config.autodoc_mock_imports):
        import ignis.gobject

        ignis.gobject.IgnisProperty = FakeGProperty
        ignis.gobject.IgnisSignal = FakeSignal


def setup(app: Sphinx) -> ExtensionMetadata:
    patch(app)
    app.setup_extension("sphinx.ext.autodoc")  # Require autodoc extension
    app.add_autodocumenter(GPropertyDocumenter)
    app.add_autodocumenter(SignalDocumenter)
    app.add_directive_to_domain("py", "gproperty", PropertyDirective)
    app.add_directive_to_domain("py", "signal", SignalDirective)
    return {
        "version": "1",
        "parallel_read_safe": True,
    }
