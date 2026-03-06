import abc
from typing import List, Any, Dict, TypeVar, Generic, Callable

from enum import Enum

class Role(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class Icon:
    
    def __init__(self, src: str, mime_type: str = None, sizes: List[str] = None):
        self.str = src
        self.mime_type = mime_type
        self.sizes = sizes
        
    def get_src(self) -> str:
        return self.src

    def set_src(self, src: str):
        self.src = src

    def get_mime_type(self) -> str:
        return self.mime_type

    def set_mime_type(self, mime_type: str):
        self.mime_type = mime_type

    def get_sizes(self) -> List[str]:
        return self.sizes

    def set_sizes(self, sizes: List[str]):
        self.sizes = sizes

    def __str__(self) -> str:
        return f"Icon [src={self.src}, mimeType={self.mime_type}, sizes={self.sizes}]"

class Annotations:
    def __init__(self, audience: List[Role] = None, priority: float = None):
        self.audience = audience
        self.priority = priority

    def get_audience(self) -> List[Role]:
        return self.audience

    def set_audience(self, audience: List[Role]):
        self.audience = audience

    def get_priority(self) -> float:
        return self.priority

    def set_priority(self, priority: float):
        self.priority = priority

    def __str__(self) -> str:
        return f"Annotations [audience={self.audience}, priority={self.priority}]"

class AbstractBase(abc.ABC):
    DEFAULT_SEPARATOR = "."

    def __init__(self, name: str, name_separator = None, title: str = None, description: str = None, icons: List[Icon] = None, meta: dict[str,Any] = None):
        if name is None or name == '':
            raise ValueError("name must not be null or empty")
        self.name = name
        if (name_separator):
            self.name_separator = name_separator
        else:
            self.name_separator = AbstractBase.DEFAULT_SEPARATOR
        self.title = title
        self.description = description
        self.icons = icons
        self.meta = meta

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

    def get_icons(self) -> List[Icon]:
        return self.icons

    def set_icons(self, icons: List[Icon]):
        self.icons = icons

    def get_meta(self) -> Dict[str, Any]:
        return self.meta

    def set_meta(self, meta: Dict[str, Any]):
        self.meta = meta

    @abc.abstractmethod
    def get_fully_qualified_name(self) -> str:
        pass

class Group(AbstractBase):
    def __init__(self, name: str, name_separator: str = AbstractBase.DEFAULT_SEPARATOR, title: str = None, description: str = None, icons: List[Icon] = None, meta: Dict[str,Any] = None):
        super().__init__(name, name_separator, title, description, icons, meta)
        self.parent = None
        self.child_groups = []
        self.child_tools = []
        self.child_prompts = []
        self.child_resources = []

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
        if child_group in self.child_groups:
            return False
        self.child_groups.append(child_group)
        child_group.parent = self
        return True

    def remove_child_group(self, child_group: 'Group') -> bool:
        if child_group in self.child_groups:
            self.child_groups.remove(child_group)
            child_group.parent = None
            return True
        return False

    def get_children_groups(self) -> List['Group']:
        return self.child_groups

    def add_child_tool(self, child_tool: 'Tool') -> bool:
        if child_tool in self.child_tools:
            return False
        self.child_tools.append(child_tool)
        child_tool.add_parent_group(self)
        return True

    def remove_child_tool(self, child_tool: 'Tool') -> bool:
        if child_tool in self.child_tools:
            self.child_tools.remove(child_tool)
            child_tool.remove_parent_group(self)
            return True
        return False

    def get_children_tools(self) -> List['Tool']:
        return self.child_tools

    def add_child_prompt(self, child_prompt: 'Prompt') -> bool:
        if child_prompt in self.child_prompts:
            return False
        self.child_prompts.append(child_prompt)
        child_prompt.add_parent_group(self)
        return True

    def remove_child_prompt(self, child_prompt: 'Prompt') -> bool:
        if child_prompt in self.child_prompts:
            self.child_prompts.remove(child_prompt)
            child_prompt.remove_parent_group(self)
            return True
        return False

    def get_children_resources(self) -> List['Resource']:
        return self.child_resources

    def add_child_resource(self, child_resource: 'Resource') -> bool:
        if child_resource in self.child_resources:
            return False
        self.child_resources.append(child_resource)
        child_resource.add_parent_group(self)
        return True

    def remove_child_resource(self, child_resource: 'Resource') -> bool:
        if child_resource in self.child_resources:
            self.child_resources.remove(child_resource)
            child_resource.remove_parent_group(self)
            return True
        return False

    def get_children_prompts(self) -> List['Prompt']:
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
    def __init__(self, name: str, name_separator: str = None, title: str = None, description: str = None, icons: List[Icon] = None, meta: Dict[str,Any] = None):
        super().__init__(name, name_separator, title, description, icons, meta)
        self.parent_groups = []
        self.primary_parent_group_index = -1

    def add_parent_group(self, parent_group: Group) -> bool:
        if parent_group is None:
            raise ValueError("parentGroup must not be none")
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

    def get_parent_groups(self) -> List[Group]:
        return self.parent_groups

    def get_parent_group_roots(self) -> List[Group]:
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
    def __init__(self, name: str, name_separator: str = None, title: str = None, description: str = None, icons: List[Icon] = None, meta: Dict[str, Any] = None):
        super().__init__(name, name_separator, title, description, icons, meta)
        self.input_schema = None
        self.output_schema = None
        self.tool_annotations = None

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
    def __init__(self, name: str, uri: str, name_separator: str = None, title: str = None, description: str = None, mime_type: str = None, size: int = None, icons: list[Icon] = None, annotations: Annotations = None, meta: Dict[str, Any]  = None):
        super().__init__(name, name_separator, title, description, icons, meta)
        if uri is None:
            raise ValueError("uri must not be none")
        self.uri = uri
        self.mime_type = mime_type
        self.annotations = annotations
        self.size = size

    def get_uri(self) -> str:
        return self.uri
    
    def get_mime_type(self) -> str:
        return self.mime_type

    def set_mime_type(self, mime_type: str):
        self.mime_type = mime_type

    def get_annotations(self) -> Annotations:
        return self.size

    def set_size(self, size: int):
        self.size = size

    def get_size(self) -> Annotations:
        return self.size

    def set_annotations(self, annotations: Annotations):
        self.annotations = annotations

    def __str__(self) -> str:
        return f"Resource [name={self.name}, fqName={self.get_fully_qualified_name()}, title={self.title}, description={self.description}, meta={self.meta}, uri={self.uri}, size={self.size}, mimeType={self.mime_type}, annotations={self.annotations}]"

class PromptArgument():
    def __init__(self, name: str, description: str = None, required: bool = False):
        if name is None:
            raise ValueError("name must not be none")
        self.name = name
        self.description = description
        self.required = required

    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return self.description
    
    def set_description(self, description: str):
        self.description = description
    
    def set_required(self, required: bool):
        self.required = required

    def is_required(self) -> bool:
        return self.required

    def __str__(self) -> str:
        return f"PromptArgument [required={self.required}, name={self.name}, title={self.title}, description={self.description}, meta={self.meta}]"

    def get_fully_qualified_name(self) -> str:
        return self.name

class Prompt(AbstractLeaf):
    def __init__(self, name: str, name_separator: str = None, title: str = None, description: str = None, arguments: List[PromptArgument] = None, icons: List[Icon] = None, meta: Dict[str, Any] = None):
        super().__init__(name, name_separator, title, description, icons, meta)
        if arguments:
            self.arguments = arguments 
        else:
            self.arguments = []

    def get_arguments(self) -> List[PromptArgument]:
        return self.arguments

    def add_argument(self, argument: PromptArgument) -> bool:
        if argument is None:
            raise ValueError("argument must not be null")
        if argument in self.arguments:
            return False
        self.arguments.append(argument)
        return True

    def remove_argument(self, argument: PromptArgument) -> bool:
        if argument in self.arguments:
            self.arguments.remove(argument)
            return True
        return False

    def __str__(self) -> str:
        return f"Prompt [promptArguments={self.prompt_arguments}, name={self.name}, fqName={self.get_fully_qualified_name()}, title={self.title}, description={self.description}, meta={self.meta}]"

T = TypeVar('T')
F = TypeVar('F')

class Converter(Generic[T, F], abc.ABC):
    def convert_to_list(self, sources: List[F]) -> List[T]:
        if sources is None:
            raise ValueError("sources must not be null")
        return [self.convert_to(s) for s in sources]

    @abc.abstractmethod
    def convert_to(self, source: F) -> T:
        pass

    def convert_from_list(self, targets: List[T]) -> List[F]:
        if targets is None:
            raise ValueError("targets must not be null")
        return [self.convert_from(s) for s in targets]

    @abc.abstractmethod
    def convert_from(self, target: T) -> F:
        pass

U = TypeVar('U')

def convertAll(items: List[T], convertFn: Callable[T,U]) -> List[U]:
    l = [convertFn(i) for i in items]
    f = filter(lambda x: x != None, l)
    return list(f)
