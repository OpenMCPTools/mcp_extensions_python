import abc
import typing
from enum import Enum
from dataclasses import dataclass, field

# region model.content

class Role(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"

@dataclass
class Icon:
    src: str = None
    mime_type: str = None
    sizes: typing.List[str] = field(default_factory=list)
    theme: str = None

    def get_src(self) -> str:
        return self.src

    def set_src(self, src: str):
        self.src = src

    def get_mime_type(self) -> str:
        return self.mime_type

    def set_mime_type(self, mime_type: str):
        self.mime_type = mime_type

    def get_sizes(self) -> typing.List[str]:
        return self.sizes

    def set_sizes(self, sizes: typing.List[str]):
        self.sizes = sizes

    def get_theme(self) -> str:
        return self.theme

    def set_theme(self, theme: str):
        self.theme = theme

    def __str__(self) -> str:
        return f"Icon [src={self.src}, mimeType={self.mime_type}, sizes={self.sizes}, theme={self.theme}]"

class Annotations:
    def __init__(self, audience: typing.List[Role], priority: float, last_modified: str):
        self.audience = audience
        self.priority = priority
        self.last_modified = last_modified

    def get_audience(self) -> typing.List[Role]:
        return self.audience

    def set_audience(self, audience: typing.List[Role]):
        self.audience = audience

    def get_priority(self) -> float:
        return self.priority

    def set_priority(self, priority: float):
        self.priority = priority

    def get_last_modified(self) -> str:
        return self.last_modified

    def set_last_modified(self, last_modified: str):
        self.last_modified = last_modified

    def __str__(self) -> str:
        return f"Annotations [audience={self.audience}, priority={self.priority}, lastModified={self.last_modified}]"

# region model

class AbstractBase(abc.ABC):
    DEFAULT_SEPARATOR = "."

    def __init__(self, name: str, name_separator: str = DEFAULT_SEPARATOR):
        if name is None:
            raise ValueError("name must not be null")
        self.name = name
        self.name_separator = name_separator
        self.title = None
        self.description = None
        self.meta = None
        self.icons = None

    def get_name(self) -> str:
        return self.name

    def get_title(self) -> str:
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_icons(self) -> typing.List[Icon]:
        return self.icons

    def set_icons(self, icons: typing.List[Icon]):
        self.icons = icons

    def get_meta(self) -> typing.Dict[str, typing.Any]:
        return self.meta

    def set_meta(self, meta: typing.Dict[str, typing.Any]):
        self.meta = meta

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, AbstractBase):
            return False
        if self.__class__ != other.__class__:
            return False
        return self.name == other.name

    @abc.abstractmethod
    def get_fully_qualified_name(self) -> str:
        pass

class Group(AbstractBase):
    def __init__(self, name: str, name_separator: str = AbstractBase.DEFAULT_SEPARATOR):
        super().__init__(name, name_separator)
        self.parent = None
        self.child_groups = []
        self.child_tools = []
        self.child_prompts = []
        self.child_resources = []

    @staticmethod
    def builder(name: str):
        return Group.Builder(name)

    class Builder:
        def __init__(self, name: str):
            self._name = name
            self._title = None
            self._description = None
            self._parent = None
            self._meta = None

        def title(self, title: str):
            self._title = title
            return self

        def description(self, description: str):
            self._description = description
            return self

        def parent(self, parent: 'Group'):
            self._parent = parent
            return self

        def meta(self, meta: typing.Dict[str, typing.Any]):
            self._meta = meta
            return self

        def build(self):
            result = Group(self._name)
            result.set_title(self._title)
            result.set_description(self._description)
            result.set_meta(self._meta)
            result.set_parent(self._parent)
            return result

    def get_parent(self) -> 'Group':
        return self.parent

    def set_parent(self, parent: 'Group'):
        self.parent = parent

    def get_root(self) -> 'Group':
        parent = self.parent
        if parent is None:
            return self
        else:
            return parent.get_root()

    def is_root(self) -> bool:
        return self.parent is None

    def add_child_group(self, child_group: 'Group') -> bool:
        self.child_groups.append(child_group)
        child_group.parent = self
        return True

    def remove_child_group(self, child_group: 'Group') -> bool:
        if child_group in self.child_groups:
            self.child_groups.remove(child_group)
            child_group.parent = None
            return True
        return False

    def get_children_groups(self) -> typing.List['Group']:
        return self.child_groups

    def add_child_tool(self, child_tool: 'Tool') -> bool:
        self.child_tools.append(child_tool)
        child_tool.add_parent_group(self)
        return True

    def remove_child_tool(self, child_tool: 'Tool') -> bool:
        if child_tool in self.child_tools:
            self.child_tools.remove(child_tool)
            child_tool.remove_parent_group(self)
            return True
        return False

    def get_children_tools(self) -> typing.List['Tool']:
        return self.child_tools

    def add_child_prompt(self, child_prompt: 'Prompt') -> bool:
        self.child_prompts.append(child_prompt)
        child_prompt.add_parent_group(self)
        return True

    def remove_child_prompt(self, child_prompt: 'Prompt') -> bool:
        if child_prompt in self.child_prompts:
            self.child_prompts.remove(child_prompt)
            child_prompt.remove_parent_group(self)
            return True
        return False

    def get_children_resources(self) -> typing.List['Resource']:
        return self.child_resources

    def add_child_resource(self, child_resource: 'Resource') -> bool:
        self.child_resources.append(child_resource)
        child_resource.add_parent_group(self)
        return True

    def remove_child_resource(self, child_resource: 'Resource') -> bool:
        if child_resource in self.child_resources:
            self.child_resources.remove(child_resource)
            child_resource.remove_parent_group(self)
            return True
        return False

    def get_children_prompts(self) -> typing.List['Prompt']:
        return self.child_prompts

    def _get_fq_name_recursive(self, tg: 'Group') -> str:
        parent = tg.get_parent()
        if parent is not None:
            parent_name = self._get_fq_name_recursive(parent)
            return parent_name + self.name_separator + tg.get_name()
        return tg.get_name()

    def get_fully_qualified_name(self) -> str:
        return self._get_fq_name_recursive(self)

    def __str__(self) -> str:
        return f"Group [name={self.name}, fqName={self.get_fully_qualified_name()}, isRoot={self.is_root()}, title={self.title}, description={self.description}, meta={self.meta}, childGroups={self.child_groups}, childTools={self.child_tools}, childPrompts={self.child_prompts}]"

class AbstractLeaf(AbstractBase):
    def __init__(self, name: str, name_separator: str = AbstractBase.DEFAULT_SEPARATOR):
        super().__init__(name, name_separator)
        self.parent_groups = []
        self.primary_parent_group_index = -1

    def add_parent_group(self, parent_group: Group) -> bool:
        if parent_group is None:
            raise ValueError("parentGroup must not be null")
        if parent_group in self.parent_groups:
            return False
        self.parent_groups.append(parent_group)
        if self.primary_parent_group_index == -1:
            self.primary_parent_group_index = 0
        return True

    def remove_parent_group(self, parent_group: Group) -> bool:
        try:
            current_index = self.parent_groups.index(parent_group)
        except ValueError:
            return False

        if current_index == self.primary_parent_group_index:
            self.parent_groups.pop(current_index)
            self.primary_parent_group_index = -1
            return True
        self.parent_groups.remove(parent_group)
        return True

    def get_parent_groups(self) -> typing.List[Group]:
        return self.parent_groups

    def get_parent_group_roots(self) -> typing.List[Group]:
        return [g.get_root() for g in self.parent_groups]

    def _get_first_parent_name(self) -> str:
        return self.parent_groups[self.primary_parent_group_index].get_fully_qualified_name() \
            if self.primary_parent_group_index > -1 else None

    def get_fully_qualified_name(self) -> str:
        first_parent_name = self._get_first_parent_name()
        return self.name if first_parent_name is None else first_parent_name + self.name_separator + self.name

class ToolAnnotations:
    def __init__(self):
        self.title = None
        self.read_only_hint = None
        self.destructive_hint = None
        self.idempotent_hint = None
        self.open_world_hint = None
        self.return_direct = None

    def get_title(self) -> str:
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_read_only_hint(self) -> bool:
        return self.read_only_hint

    def set_read_only_hint(self, read_only_hint: bool):
        self.read_only_hint = read_only_hint

    def get_destructive_hint(self) -> bool:
        return self.destructive_hint

    def set_destructive_hint(self, destructive_hint: bool):
        self.destructive_hint = destructive_hint

    def get_idempotent_hint(self) -> bool:
        return self.idempotent_hint

    def set_idempotent_hint(self, idempotent_hint: bool):
        self.idempotent_hint = idempotent_hint

    def get_open_world_hint(self) -> bool:
        return self.open_world_hint

    def set_open_world_hint(self, open_world_hint: bool):
        self.open_world_hint = open_world_hint

    def get_return_direct(self) -> bool:
        return self.return_direct

    def set_return_direct(self, return_direct: bool):
        self.return_direct = return_direct

    def __str__(self) -> str:
        return f"ToolAnnotation [title={self.title}, readOnlyHint={self.read_only_hint}, destructiveHint={self.destructive_hint}, idempotentHint={self.idempotent_hint}, openWorldHint={self.open_world_hint}, returnDirect={self.return_direct}]"

class Tool(AbstractLeaf):
    def __init__(self, name: str):
        super().__init__(name)
        self.input_schema = None
        self.output_schema = None
        self.tool_annotations = None

    @staticmethod
    def builder(name: str):
        return Tool.Builder(name)

    class Builder:
        def __init__(self, name: str):
            if name is None:
                raise ValueError("name must not be null")
            self._name = name
            self._title = None
            self._description = None
            self._input_schema = None
            self._output_schema = None
            self._annotations = None
            self._meta = None
            self._parents = []

        def title(self, title: str):
            self._title = title
            return self

        def description(self, description: str):
            self._description = description
            return self

        def inputSchema(self, input_schema: str):
            self._input_schema = input_schema
            return self

        def outputSchema(self, output_schema: str):
            self._output_schema = output_schema
            return self

        def annotations(self, annotations: ToolAnnotations):
            self._annotations = annotations
            return self

        def meta(self, meta: typing.Dict[str, typing.Any]):
            self._meta = meta
            return self

        def addParent(self, g: Group):
            if g is not None:
                self._parents.append(g)
            return self

        def build(self) -> 'Tool':
            t = Tool(self._name)
            t.set_description(self._description)
            t.set_title(self._title)
            t.set_input_schema(self._input_schema)
            t.set_output_schema(self._output_schema)
            t.set_tool_annotations(self._annotations)
            for pg in self._parents:
                t.add_parent_group(pg)
            t.set_meta(self._meta)
            return t

    def get_input_schema(self) -> str:
        return self.input_schema

    def set_input_schema(self, input_schema: str):
        self.input_schema = input_schema

    def get_output_schema(self) -> str:
        return self.output_schema

    def set_output_schema(self, output_schema: str):
        self.output_schema = output_schema

    def get_tool_annotations(self) -> ToolAnnotations:
        return self.tool_annotations

    def set_tool_annotations(self, tool_annotations: ToolAnnotations):
        self.tool_annotations = tool_annotations

    def __str__(self) -> str:
        return f"Tool [name={self.name}, fqName={self.get_fully_qualified_name()}, title={self.title}, description={self.description}, meta={self.meta}, inputSchema={self.input_schema}, outputSchema={self.output_schema}, toolAnnotation={self.tool_annotations}]"

class Resource(AbstractLeaf):
    def __init__(self, name: str, uri: str):
        super().__init__(name)
        if uri is None:
            raise ValueError("uri must not be null")
        self.uri = uri
        self.size = None
        self.mime_type = None
        self.annotations = None

    @staticmethod
    def builder():
        return Resource.Builder()

    class Builder:
        def __init__(self):
            self._uri = None
            self._name = None
            self._title = None
            self._description = None
            self._mime_type = None
            self._size = None
            self._annotations = None
            self._meta = None

        def uri(self, uri: str):
            self._uri = uri
            return self

        def name(self, name: str):
            self._name = name
            return self

        def title(self, title: str):
            self._title = title
            return self

        def description(self, description: str):
            self._description = description
            return self

        def mimeType(self, mime_type: str):
            self._mime_type = mime_type
            return self

        def size(self, size: int):
            self._size = size
            return self

        def annotations(self, annotations: Annotations):
            self._annotations = annotations
            return self

        def meta(self, meta: typing.Dict[str, typing.Any]):
            self._meta = meta
            return self

        def build(self) -> 'Resource':
            result = Resource(self._name, self._uri)
            result.set_title(self._title)
            result.set_description(self._description)
            result.set_size(self._size)
            result.set_meta(self._meta)
            result.set_mime_type(self._mime_type)
            result.set_annotations(self._annotations)
            return result

    def get_uri(self) -> str:
        return self.uri

    def get_size(self) -> int:
        return self.size

    def set_size(self, size: int):
        self.size = size

    def get_mime_type(self) -> str:
        return self.mime_type

    def set_mime_type(self, mime_type: str):
        self.mime_type = mime_type

    def get_annotations(self) -> Annotations:
        return self.annotations

    def set_annotations(self, annotations: Annotations):
        self.annotations = annotations

    def __str__(self) -> str:
        return f"Resource [name={self.name}, fqName={self.get_fully_qualified_name()}, title={self.title}, description={self.description}, meta={self.meta}, uri={self.uri}, size={self.size}, mimeType={self.mime_type}, annotations={self.annotations}]"

class PromptArgument(AbstractBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.required = False

    def set_required(self, required: bool):
        self.required = required

    def is_required(self) -> bool:
        return self.required

    def __str__(self) -> str:
        return f"PromptArgument [required={self.required}, name={self.name}, title={self.title}, description={self.description}, meta={self.meta}]"

    def get_fully_qualified_name(self) -> str:
        return self.name

class Prompt(AbstractLeaf):
    def __init__(self, name: str):
        super().__init__(name)
        self.prompt_arguments = []

    def get_prompt_arguments(self) -> typing.List[PromptArgument]:
        return self.prompt_arguments

    def add_prompt_argument(self, prompt_argument: PromptArgument) -> bool:
        if prompt_argument is None:
            raise ValueError("promptArgument must not be null")
        self.prompt_arguments.append(prompt_argument)
        return True

    def remove_prompt_argument(self, prompt_argument: PromptArgument) -> bool:
        if prompt_argument in self.prompt_arguments:
            self.prompt_arguments.remove(prompt_argument)
            return True
        return False

    def __str__(self) -> str:
        return f"Prompt [promptArguments={self.prompt_arguments}, name={self.name}, fqName={self.get_fully_qualified_name()}, title={self.title}, description={self.description}, meta={self.meta}]"

T = typing.TypeVar('T')
F = typing.TypeVar('F')

class Converter(typing.Generic[T, F], abc.ABC):
    def convert_to_list(self, sources: typing.List[F]) -> typing.List[T]:
        if sources is None:
            raise ValueError("sources must not be null")
        return [self.convert_to(s) for s in sources]

    @abc.abstractmethod
    def convert_to(self, source: F) -> T:
        pass

    def convert_from_list(self, targets: typing.List[T]) -> typing.List[F]:
        if targets is None:
            raise ValueError("targets must not be null")
        return [self.convert_from(s) for s in targets]

    @abc.abstractmethod
    def convert_from(self, target: T) -> F:
        pass

# endregion

