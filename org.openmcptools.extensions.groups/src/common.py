from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
from typing import TypeVar, Generic

class AbstractBase(ABC):
    """
    Abstract base class for model objects
    """
    
    DEFAULT_SEPARATOR = "."
    
    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize AbstractBase with a name and optional name separator
        
        Args:
            name: The name of the object (must not be None)
            name_separator: The separator for fully qualified names (defaults to DEFAULT_SEPARATOR)
            
        Raises:
            ValueError: If name is None
        """
        if name is None:
            raise ValueError("name must not be null")
        self._name = name
        self._name_separator = name_separator if name_separator is not None else self.DEFAULT_SEPARATOR
        self._title: Optional[str] = None
        self._description: Optional[str] = None
        self._meta: Optional[Dict[str, Any]] = None
        self._icons: Optional[List['Icon']] = None
    
    @property
    def name(self) -> str:
        """Get the name"""
        return self._name
    
    @property
    def name_separator(self) -> str:
        """Get the name separator"""
        return self._name_separator
    
    def get_title(self) -> Optional[str]:
        """Get the title"""
        return self._title
    
    def set_title(self, title: str) -> None:
        """Set the title"""
        self._title = title
    
    @property
    def title(self) -> Optional[str]:
        """Get the title (property accessor)"""
        return self._title
    
    @title.setter
    def title(self, title: str) -> None:
        """Set the title (property setter)"""
        self._title = title
    
    def get_description(self) -> Optional[str]:
        """Get the description"""
        return self._description
    
    def set_description(self, description: str) -> None:
        """Set the description"""
        self._description = description
    
    @property
    def description(self) -> Optional[str]:
        """Get the description (property accessor)"""
        return self._description
    
    @description.setter
    def description(self, description: str) -> None:
        """Set the description (property setter)"""
        self._description = description
    
    def get_icons(self) -> Optional[List['Icon']]:
        """Get the icons list"""
        return self._icons
    
    def set_icons(self, icons: List['Icon']) -> None:
        """Set the icons list"""
        self._icons = icons
    
    @property
    def icons(self) -> Optional[List['Icon']]:
        """Get the icons (property accessor)"""
        return self._icons
    
    @icons.setter
    def icons(self, icons: List['Icon']) -> None:
        """Set the icons (property setter)"""
        self._icons = icons
    
    def get_meta(self) -> Optional[Dict[str, Any]]:
        """Get the meta dictionary"""
        return self._meta
    
    def set_meta(self, meta: Dict[str, Any]) -> None:
        """Set the meta dictionary"""
        self._meta = meta
    
    @property
    def meta(self) -> Optional[Dict[str, Any]]:
        """Get the meta (property accessor)"""
        return self._meta
    
    @meta.setter
    def meta(self, meta: Dict[str, Any]) -> None:
        """Set the meta (property setter)"""
        self._meta = meta
    
    def __hash__(self) -> int:
        """Generate hash code based on name"""
        return hash(self._name)
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality based on name
        
        Args:
            other: The object to compare with
            
        Returns:
            True if objects are equal, False otherwise
        """
        if self is other:
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        other_base = other
        return self._name == other_base._name
    
    @abstractmethod
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name
        
        Returns:
            The fully qualified name
        """
        pass


class Icon:
    """
    Icon definition
    """
    
    def __init__(self):
        """Initialize Icon with default values"""
        self._src: Optional[str] = None
        self._mime_type: Optional[str] = None
        self._sizes: Optional[List[str]] = None
        self._theme: Optional[str] = None
    
    def get_src(self) -> Optional[str]:
        """Get the source URL"""
        return self._src
    
    def set_src(self, src: str) -> None:
        """Set the source URL"""
        self._src = src
    
    @property
    def src(self) -> Optional[str]:
        """Get the source (property accessor)"""
        return self._src
    
    @src.setter
    def src(self, src: str) -> None:
        """Set the source (property setter)"""
        self._src = src
    
    def get_mime_type(self) -> Optional[str]:
        """Get the MIME type"""
        return self._mime_type
    
    def set_mime_type(self, mime_type: str) -> None:
        """Set the MIME type"""
        self._mime_type = mime_type
    
    @property
    def mime_type(self) -> Optional[str]:
        """Get the MIME type (property accessor)"""
        return self._mime_type
    
    @mime_type.setter
    def mime_type(self, mime_type: str) -> None:
        """Set the MIME type (property setter)"""
        self._mime_type = mime_type
    
    def get_sizes(self) -> Optional[List[str]]:
        """Get the sizes list"""
        return self._sizes
    
    def set_sizes(self, sizes: List[str]) -> None:
        """Set the sizes list"""
        self._sizes = sizes
    
    @property
    def sizes(self) -> Optional[List[str]]:
        """Get the sizes (property accessor)"""
        return self._sizes
    
    @sizes.setter
    def sizes(self, sizes: List[str]) -> None:
        """Set the sizes (property setter)"""
        self._sizes = sizes
    
    def get_theme(self) -> Optional[str]:
        """Get the theme"""
        return self._theme
    
    def set_theme(self, theme: str) -> None:
        """Set the theme"""
        self._theme = theme
    
    @property
    def theme(self) -> Optional[str]:
        """Get the theme (property accessor)"""
        return self._theme
    
    @theme.setter
    def theme(self, theme: str) -> None:
        """Set the theme (property setter)"""
        self._theme = theme
    
    def __str__(self) -> str:
        """String representation of Icon"""
        return f"Icon [src={self._src}, mimeType={self._mime_type}, sizes={self._sizes}, theme={self._theme}]"


class Role(Enum):
    """
    Role enumeration
    """
    
    USER = "USER"
    ASSISTANT = "ASSISTANT"



class Annotations:
    """
    Annotations class
    """
    
    def __init__(self, audience: Optional[List['Role']], priority: Optional[float], last_modified: Optional[str]):
        """
        Initialize Annotations
        
        Args:
            audience: List of roles for audience
            priority: Priority value
            last_modified: Last modified timestamp
        """
        self._audience = audience
        self._priority = priority
        self._last_modified = last_modified
    
    def get_audience(self) -> Optional[List['Role']]:
        """Get the audience list"""
        return self._audience
    
    def set_audience(self, audience: List['Role']) -> None:
        """Set the audience list"""
        self._audience = audience
    
    @property
    def audience(self) -> Optional[List['Role']]:
        """Get the audience (property accessor)"""
        return self._audience
    
    @audience.setter
    def audience(self, audience: List['Role']) -> None:
        """Set the audience (property setter)"""
        self._audience = audience
    
    def get_priority(self) -> Optional[float]:
        """Get the priority"""
        return self._priority
    
    def set_priority(self, priority: float) -> None:
        """Set the priority"""
        self._priority = priority
    
    @property
    def priority(self) -> Optional[float]:
        """Get the priority (property accessor)"""
        return self._priority
    
    @priority.setter
    def priority(self, priority: float) -> None:
        """Set the priority (property setter)"""
        self._priority = priority
    
    def get_last_modified(self) -> Optional[str]:
        """Get the last modified timestamp"""
        return self._last_modified
    
    def set_last_modified(self, last_modified: str) -> None:
        """Set the last modified timestamp"""
        self._last_modified = last_modified
    
    @property
    def last_modified(self) -> Optional[str]:
        """Get the last modified (property accessor)"""
        return self._last_modified
    
    @last_modified.setter
    def last_modified(self, last_modified: str) -> None:
        """Set the last modified (property setter)"""
        self._last_modified = last_modified
    
    def __str__(self) -> str:
        """String representation of Annotations"""
        return f"Annotations [audience={self._audience}, priority={self._priority}, lastModified={self._last_modified}]"


class AbstractLeaf(AbstractBase):
    """
    Abstract leaf class extending AbstractBase
    """
    
    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize AbstractLeaf
        
        Args:
            name: The name of the leaf
            name_separator: The separator for fully qualified names (optional)
        """
        if name_separator is not None:
            super().__init__(name, name_separator)
        else:
            super().__init__(name)
        # Using a list to simulate CopyOnWriteArrayList behavior
        self._parent_groups: List['Group'] = []
    
    @property
    def parent_groups(self) -> List['Group']:
        """Get the parent groups list"""
        return self._parent_groups
    
    def add_parent_group(self, parent_group: 'Group') -> bool:
        """
        Add a parent group
        
        Args:
            parent_group: The parent group to add (must not be None)
            
        Returns:
            True if the group was added, False otherwise
            
        Raises:
            ValueError: If parent_group is None
        """
        if parent_group is None:
            raise ValueError("parentGroup must not be null")
        self._parent_groups.append(parent_group)
        return True
    
    def remove_parent_group(self, parent_group: 'Group') -> bool:
        """
        Remove a parent group
        
        Args:
            parent_group: The parent group to remove
            
        Returns:
            True if the group was removed, False otherwise
        """
        try:
            self._parent_groups.remove(parent_group)
            return True
        except ValueError:
            return False
    
    def get_parent_groups(self) -> List['Group']:
        """Get the parent groups list"""
        return self._parent_groups
    
    def get_parent_group_roots(self) -> List['Group']:
        """
        Get the root groups of all parent groups
        
        Returns:
            List of root groups
        """
        parent_groups = self._parent_groups
        return [pg.get_root() for pg in parent_groups]
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name
        
        Returns:
            The name (for leaf objects, this is just the name)
        """
        return self._name


class Group(AbstractBase):
    """
    Group class extending AbstractBase
    """
    
    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize Group
        
        Args:
            name: The name of the group
            name_separator: The separator for fully qualified names (defaults to DEFAULT_SEPARATOR)
        """
        if name_separator is not None:
            super().__init__(name, name_separator)
        else:
            super().__init__(name, AbstractBase.DEFAULT_SEPARATOR)
        self._parent: Optional['Group'] = None
        # Using lists to simulate CopyOnWriteArrayList behavior
        self._child_groups: List['Group'] = []
        self._child_tools: List['Tool'] = []
        self._child_prompts: List['Prompt'] = []
        self._child_resources: List['Resource'] = []
    
    @property
    def parent(self) -> Optional['Group']:
        """Get the parent group"""
        return self._parent
    
    def get_parent(self) -> Optional['Group']:
        """Get the parent group"""
        return self._parent
    
    def set_parent(self, parent: 'Group') -> None:
        """Set the parent group"""
        self._parent = parent
    
    def get_root(self) -> 'Group':
        """
        Get the root group
        
        Returns:
            The root group in the hierarchy
        """
        parent = self._parent
        if parent is None:
            return self
        else:
            return parent.get_root()
    
    def is_root(self) -> bool:
        """
        Check if this group is a root group
        
        Returns:
            True if this is a root group, False otherwise
        """
        return self._parent is None
    
    def add_child_group(self, child_group: 'Group') -> bool:
        """
        Add a child group
        
        Args:
            child_group: The child group to add
            
        Returns:
            True if the group was added, False otherwise
        """
        self._child_groups.append(child_group)
        child_group._parent = self
        return True
    
    def remove_child_group(self, child_group: 'Group') -> bool:
        """
        Remove a child group
        
        Args:
            child_group: The child group to remove
            
        Returns:
            True if the group was removed, False otherwise
        """
        try:
            self._child_groups.remove(child_group)
            child_group._parent = None
            return True
        except ValueError:
            return False
    
    def get_children_groups(self) -> List['Group']:
        """Get the list of child groups"""
        return self._child_groups
    
    def add_child_tool(self, child_tool: 'Tool') -> bool:
        """
        Add a child tool
        
        Args:
            child_tool: The child tool to add
            
        Returns:
            True if the tool was added, False otherwise
        """
        self._child_tools.append(child_tool)
        child_tool.add_parent_group(self)
        return True
    
    def remove_child_tool(self, child_tool: 'Tool') -> bool:
        """
        Remove a child tool
        
        Args:
            child_tool: The child tool to remove
            
        Returns:
            True if the tool was removed, False otherwise
        """
        try:
            self._child_tools.remove(child_tool)
            child_tool.remove_parent_group(self)
            return True
        except ValueError:
            return False
    
    def get_children_tools(self) -> List['Tool']:
        """Get the list of child tools"""
        return self._child_tools
    
    def add_child_prompt(self, child_prompt: 'Prompt') -> bool:
        """
        Add a child prompt
        
        Args:
            child_prompt: The child prompt to add
            
        Returns:
            True if the prompt was added, False otherwise
        """
        self._child_prompts.append(child_prompt)
        child_prompt.add_parent_group(self)
        return True
    
    def remove_child_prompt(self, child_prompt: 'Prompt') -> bool:
        """
        Remove a child prompt
        
        Args:
            child_prompt: The child prompt to remove
            
        Returns:
            True if the prompt was removed, False otherwise
        """
        try:
            self._child_prompts.remove(child_prompt)
            child_prompt.remove_parent_group(self)
            return True
        except ValueError:
            return False
    
    def get_children_resources(self) -> List['Resource']:
        """Get the list of child resources"""
        return self._child_resources
    
    def add_child_resource(self, child_resource: 'Resource') -> bool:
        """
        Add a child resource
        
        Args:
            child_resource: The child resource to add
            
        Returns:
            True if the resource was added, False otherwise
        """
        self._child_resources.append(child_resource)
        child_resource.add_parent_group(self)
        return True
    
    def remove_child_resource(self, child_resource: 'Resource') -> bool:
        """
        Remove a child resource
        
        Args:
            child_resource: The child resource to remove
            
        Returns:
            True if the resource was removed, False otherwise
        """
        try:
            self._child_resources.remove(child_resource)
            child_resource.remove_parent_group(self)
            return True
        except ValueError:
            return False
    
    def get_children_prompts(self) -> List['Prompt']:
        """Get the list of child prompts"""
        return self._child_prompts
    
    def _get_fully_qualified_name_recursive(self, sb: str, tg: 'Group') -> str:
        """
        Recursively build the fully qualified name
        
        Args:
            sb: String buffer (not used in Python implementation)
            tg: The group to process
            
        Returns:
            The fully qualified name
        """
        parent = tg.get_parent()
        if parent is not None:
            parent_name = self._get_fully_qualified_name_recursive(sb, parent)
            return f"{parent_name}{self._name_separator}{tg.get_name()}"
        return tg.get_name()
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name
        
        Returns:
            The fully qualified name
        """
        return self._get_fully_qualified_name_recursive("", self)
    
    def get_name(self) -> str:
        """Get the name"""
        return self._name
    
    def __str__(self) -> str:
        """String representation of Group"""
        return (f"Group [name={self._name}, fqName={self.get_fully_qualified_name()}, isRoot={self.is_root()}, "
                f"title={self._title}, description={self._description}, meta={self._meta}, "
                f"childGroups={self._child_groups}, childTools={self._child_tools}, childPrompts={self._child_prompts}]")


class PromptArgument(AbstractBase):
    """
    PromptArgument class extending AbstractBase
    """
    
    def __init__(self, name: str):
        """
        Initialize PromptArgument
        
        Args:
            name: The name of the prompt argument
        """
        super().__init__(name)
        self._required: bool = False
    
    def set_required(self, required: bool) -> None:
        """Set the required flag"""
        self._required = required
    
    def is_required(self) -> bool:
        """
        Check if this argument is required
        
        Returns:
            True if required, False otherwise
        """
        return self._required
    
    @property
    def required(self) -> bool:
        """Get the required flag (property accessor)"""
        return self._required
    
    @required.setter
    def required(self, required: bool) -> None:
        """Set the required flag (property setter)"""
        self._required = required
    
    def __str__(self) -> str:
        """String representation of PromptArgument"""
        return (f"PromptArgument [required={self._required}, name={self._name}, title={self._title}, "
                f"description={self._description}, meta={self._meta}]")
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name
        
        Returns:
            The name (for prompt arguments, this is just the name)
        """
        return self._name


class Prompt(AbstractLeaf):
    """
    Prompt class extending AbstractLeaf
    """
    
    def __init__(self, name: str):
        """
        Initialize Prompt
        
        Args:
            name: The name of the prompt
        """
        super().__init__(name)
        # Using a list to simulate CopyOnWriteArrayList behavior
        self._prompt_arguments: List[PromptArgument] = []
    
    def get_prompt_arguments(self) -> List[PromptArgument]:
        """Get the list of prompt arguments"""
        return self._prompt_arguments
    
    @property
    def prompt_arguments(self) -> List[PromptArgument]:
        """Get the prompt arguments (property accessor)"""
        return self._prompt_arguments
    
    def add_prompt_argument(self, prompt_argument: PromptArgument) -> bool:
        """
        Add a prompt argument
        
        Args:
            prompt_argument: The prompt argument to add (must not be None)
            
        Returns:
            True if the argument was added, False otherwise
            
        Raises:
            ValueError: If prompt_argument is None
        """
        if prompt_argument is None:
            raise ValueError("promptArgument must not be null")
        self._prompt_arguments.append(prompt_argument)
        return True
    
    def remove_parent_group(self, prompt_argument: PromptArgument) -> bool:
        """
        Remove a prompt argument (note: method name in original is misleading)
        
        Args:
            prompt_argument: The prompt argument to remove
            
        Returns:
            True if the argument was removed, False otherwise
        """
        try:
            self._prompt_arguments.remove(prompt_argument)
            return True
        except ValueError:
            return False
    
    def __str__(self) -> str:
        """String representation of Prompt"""
        return (f"Prompt [promptArguments={self._prompt_arguments}, name={self._name}, "
                f"fqName={self.get_fully_qualified_name()}, title={self._title}, "
                f"description={self._description}, meta={self._meta}]")


class ToolAnnotations:
    """
    ToolAnnotations class
    """
    
    def __init__(self):
        """Initialize ToolAnnotations with default values"""
        self._title: Optional[str] = None
        self._read_only_hint: Optional[bool] = None
        self._destructive_hint: Optional[bool] = None
        self._idempotent_hint: Optional[bool] = None
        self._open_world_hint: Optional[bool] = None
        self._return_direct: Optional[bool] = None
    
    def get_title(self) -> Optional[str]:
        """Get the title"""
        return self._title
    
    def set_title(self, title: str) -> None:
        """Set the title"""
        self._title = title
    
    @property
    def title(self) -> Optional[str]:
        """Get the title (property accessor)"""
        return self._title
    
    @title.setter
    def title(self, title: str) -> None:
        """Set the title (property setter)"""
        self._title = title
    
    def get_read_only_hint(self) -> Optional[bool]:
        """Get the read only hint"""
        return self._read_only_hint
    
    def set_read_only_hint(self, read_only_hint: bool) -> None:
        """Set the read only hint"""
        self._read_only_hint = read_only_hint
    
    @property
    def read_only_hint(self) -> Optional[bool]:
        """Get the read only hint (property accessor)"""
        return self._read_only_hint
    
    @read_only_hint.setter
    def read_only_hint(self, read_only_hint: bool) -> None:
        """Set the read only hint (property setter)"""
        self._read_only_hint = read_only_hint
    
    def get_destructive_hint(self) -> Optional[bool]:
        """Get the destructive hint"""
        return self._destructive_hint
    
    def set_destructive_hint(self, destructive_hint: bool) -> None:
        """Set the destructive hint"""
        self._destructive_hint = destructive_hint
    
    @property
    def destructive_hint(self) -> Optional[bool]:
        """Get the destructive hint (property accessor)"""
        return self._destructive_hint
    
    @destructive_hint.setter
    def destructive_hint(self, destructive_hint: bool) -> None:
        """Set the destructive hint (property setter)"""
        self._destructive_hint = destructive_hint
    
    def get_idempotent_hint(self) -> Optional[bool]:
        """Get the idempotent hint"""
        return self._idempotent_hint
    
    def set_idempotent_hint(self, idempotent_hint: bool) -> None:
        """Set the idempotent hint"""
        self._idempotent_hint = idempotent_hint
    
    @property
    def idempotent_hint(self) -> Optional[bool]:
        """Get the idempotent hint (property accessor)"""
        return self._idempotent_hint
    
    @idempotent_hint.setter
    def idempotent_hint(self, idempotent_hint: bool) -> None:
        """Set the idempotent hint (property setter)"""
        self._idempotent_hint = idempotent_hint
    
    def get_open_world_hint(self) -> Optional[bool]:
        """Get the open world hint"""
        return self._open_world_hint
    
    def set_open_world_hint(self, open_world_hint: bool) -> None:
        """Set the open world hint"""
        self._open_world_hint = open_world_hint
    
    @property
    def open_world_hint(self) -> Optional[bool]:
        """Get the open world hint (property accessor)"""
        return self._open_world_hint
    
    @open_world_hint.setter
    def open_world_hint(self, open_world_hint: bool) -> None:
        """Set the open world hint (property setter)"""
        self._open_world_hint = open_world_hint
    
    def get_return_direct(self) -> Optional[bool]:
        """Get the return direct flag"""
        return self._return_direct
    
    def set_return_direct(self, return_direct: bool) -> None:
        """Set the return direct flag"""
        self._return_direct = return_direct
    
    @property
    def return_direct(self) -> Optional[bool]:
        """Get the return direct (property accessor)"""
        return self._return_direct
    
    @return_direct.setter
    def return_direct(self, return_direct: bool) -> None:
        """Set the return direct (property setter)"""
        self._return_direct = return_direct
    
    def __str__(self) -> str:
        """String representation of ToolAnnotations"""
        return (f"ToolAnnotation [title={self._title}, readOnlyHint={self._read_only_hint}, "
                f"destructiveHint={self._destructive_hint}, idempotentHint={self._idempotent_hint}, "
                f"openWorldHint={self._open_world_hint}, returnDirect={self._return_direct}]")


class Tool(AbstractLeaf):
    """
    Tool class extending AbstractLeaf
    """
    
    def __init__(self, name: str):
        """
        Initialize Tool
        
        Args:
            name: The name of the tool
        """
        super().__init__(name)
        self._input_schema: Optional[str] = None
        self._output_schema: Optional[str] = None
        self._tool_annotations: Optional[ToolAnnotations] = None
    
    def get_input_schema(self) -> Optional[str]:
        """Get the input schema"""
        return self._input_schema
    
    def set_input_schema(self, input_schema: str) -> None:
        """Set the input schema"""
        self._input_schema = input_schema
    
    @property
    def input_schema(self) -> Optional[str]:
        """Get the input schema (property accessor)"""
        return self._input_schema
    
    @input_schema.setter
    def input_schema(self, input_schema: str) -> None:
        """Set the input schema (property setter)"""
        self._input_schema = input_schema
    
    def get_output_schema(self) -> Optional[str]:
        """Get the output schema"""
        return self._output_schema
    
    def set_output_schema(self, output_schema: str) -> None:
        """Set the output schema"""
        self._output_schema = output_schema
    
    @property
    def output_schema(self) -> Optional[str]:
        """Get the output schema (property accessor)"""
        return self._output_schema
    
    @output_schema.setter
    def output_schema(self, output_schema: str) -> None:
        """Set the output schema (property setter)"""
        self._output_schema = output_schema
    
    def get_tool_annotations(self) -> Optional[ToolAnnotations]:
        """Get the tool annotations"""
        return self._tool_annotations
    
    def set_tool_annotations(self, tool_annotations: ToolAnnotations) -> None:
        """Set the tool annotations"""
        self._tool_annotations = tool_annotations
    
    @property
    def tool_annotations(self) -> Optional[ToolAnnotations]:
        """Get the tool annotations (property accessor)"""
        return self._tool_annotations
    
    @tool_annotations.setter
    def tool_annotations(self, tool_annotations: ToolAnnotations) -> None:
        """Set the tool annotations (property setter)"""
        self._tool_annotations = tool_annotations
    
    def __str__(self) -> str:
        """String representation of Tool"""
        return (f"Tool [name={self._name}, fqName={self.get_fully_qualified_name()}, title={self._title}, "
                f"description={self._description}, meta={self._meta}, inputSchema={self._input_schema}, "
                f"outputSchema={self._output_schema}, toolAnnotation={self._tool_annotations}]")


class Resource(AbstractLeaf):
    """
    Resource class extending AbstractLeaf
    """
    
    def __init__(self, name: str):
        """
        Initialize Resource
        
        Args:
            name: The name of the resource
        """
        super().__init__(name)
        self._uri: Optional[str] = None
        self._size: Optional[int] = None
        self._mime_type: Optional[str] = None
        self._annotations: Optional[Annotations] = None
    
    def get_uri(self) -> Optional[str]:
        """Get the URI"""
        return self._uri
    
    def set_uri(self, uri: str) -> None:
        """Set the URI"""
        self._uri = uri
    
    @property
    def uri(self) -> Optional[str]:
        """Get the URI (property accessor)"""
        return self._uri
    
    @uri.setter
    def uri(self, uri: str) -> None:
        """Set the URI (property setter)"""
        self._uri = uri
    
    def get_size(self) -> Optional[int]:
        """Get the size"""
        return self._size
    
    def set_size(self, size: int) -> None:
        """Set the size"""
        self._size = size
    
    @property
    def size(self) -> Optional[int]:
        """Get the size (property accessor)"""
        return self._size
    
    @size.setter
    def size(self, size: int) -> None:
        """Set the size (property setter)"""
        self._size = size
    
    def get_mime_type(self) -> Optional[str]:
        """Get the MIME type"""
        return self._mime_type
    
    def set_mime_type(self, mime_type: str) -> None:
        """Set the MIME type"""
        self._mime_type = mime_type
    
    @property
    def mime_type(self) -> Optional[str]:
        """Get the MIME type (property accessor)"""
        return self._mime_type
    
    @mime_type.setter
    def mime_type(self, mime_type: str) -> None:
        """Set the MIME type (property setter)"""
        self._mime_type = mime_type
    
    def get_annotations(self) -> Optional[Annotations]:
        """Get the annotations"""
        return self._annotations
    
    def set_annotations(self, annotations: Annotations) -> None:
        """Set the annotations"""
        self._annotations = annotations
    
    @property
    def annotations(self) -> Optional[Annotations]:
        """Get the annotations (property accessor)"""
        return self._annotations
    
    @annotations.setter
    def annotations(self, annotations: Annotations) -> None:
        """Set the annotations (property setter)"""
        self._annotations = annotations
    
    def __str__(self) -> str:
        """String representation of Resource"""
        return (f"Resource [name={self._name}, fqName={self.get_fully_qualified_name()}, title={self._title}, "
                f"description={self._description}, meta={self._meta}, uri={self._uri}, size={self._size}, "
                f"mimeType={self._mime_type}, annotations={self._annotations}]")


GroupType = TypeVar('GroupType')


class GroupConverter(ABC, Generic[GroupType]):
    """
    Interface for converting between Group and other group types
    """
    
    def convert_from_groups(self, groups: List[Group]) -> List[GroupType]:
        """
        Convert from a list of Group objects to a list of GroupType objects
        
        Args:
            groups: List of Group objects to convert
            
        Returns:
            List of converted GroupType objects (filtered to remove None values)
        """
        result = []
        for gn in groups:
            converted = self.convert_from_group(gn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_from_group(self, group: Group) -> Optional[GroupType]:
        """
        Convert from a Group object to a GroupType object
        
        Args:
            group: The Group object to convert
            
        Returns:
            The converted GroupType object or None
        """
        pass
    
    def convert_to_groups(self, groups: List[GroupType]) -> List[Group]:
        """
        Convert from a list of GroupType objects to a list of Group objects
        
        Args:
            groups: List of GroupType objects to convert
            
        Returns:
            List of converted Group objects (filtered to remove None values)
        """
        result = []
        for g in groups:
            converted = self.convert_to_group(g)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_to_group(self, group: GroupType) -> Optional[Group]:
        """
        Convert from a GroupType object to a Group object
        
        Args:
            group: The GroupType object to convert
            
        Returns:
            The converted Group object or None
        """
        pass


PromptType = TypeVar('PromptType')


class PromptConverter(ABC, Generic[PromptType]):
    """
    Interface for converting between Prompt and other prompt types
    """
    
    def convert_from_prompts(self, prompts: List[Prompt]) -> List[PromptType]:
        """
        Convert from a list of Prompt objects to a list of PromptType objects
        
        Args:
            prompts: List of Prompt objects to convert
            
        Returns:
            List of converted PromptType objects (filtered to remove None values)
        """
        result = []
        for pn in prompts:
            converted = self.convert_from_prompt(pn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_from_prompt(self, prompt: Prompt) -> Optional[PromptType]:
        """
        Convert from a Prompt object to a PromptType object
        
        Args:
            prompt: The Prompt object to convert
            
        Returns:
            The converted PromptType object or None
        """
        pass
    
    def convert_to_prompts(self, prompts: List[PromptType]) -> List[Prompt]:
        """
        Convert from a list of PromptType objects to a list of Prompt objects
        
        Args:
            prompts: List of PromptType objects to convert
            
        Returns:
            List of converted Prompt objects (filtered to remove None values)
        """
        result = []
        for p in prompts:
            converted = self.convert_to_prompt(p)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_to_prompt(self, prompt: PromptType) -> Optional[Prompt]:
        """
        Convert from a PromptType object to a Prompt object
        
        Args:
            prompt: The PromptType object to convert
            
        Returns:
            The converted Prompt object or None
        """
        pass


ResourceType = TypeVar('ResourceType')

class ResourceConverter(ABC, Generic[ResourceType]):
    """
    Interface for converting between Resource and other resource types
    """
    
    def convert_from_resources(self, resources: List[Resource]) -> List[ResourceType]:
        """
        Convert from a list of Resource objects to a list of ResourceType objects
        
        Args:
            resources: List of Resource objects to convert
            
        Returns:
            List of converted ResourceType objects (filtered to remove None values)
        """
        result = []
        for rn in resources:
            converted = self.convert_from_resource(rn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_from_resource(self, resource: Resource) -> Optional[ResourceType]:
        """
        Convert from a Resource object to a ResourceType object
        
        Args:
            resource: The Resource object to convert
            
        Returns:
            The converted ResourceType object or None
        """
        pass
    
    def convert_to_resources(self, resources: List[ResourceType]) -> List[Resource]:
        """
        Convert from a list of ResourceType objects to a list of Resource objects
        
        Args:
            resources: List of ResourceType objects to convert
            
        Returns:
            List of converted Resource objects (filtered to remove None values)
        """
        result = []
        for rn in resources:
            converted = self.convert_to_resource(rn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_to_resource(self, resource: ResourceType) -> Optional[Resource]:
        """
        Convert from a ResourceType object to a Resource object
        
        Args:
            resource: The ResourceType object to convert
            
        Returns:
            The converted Resource object or None
        """
        pass


ToolAnnotationsType = TypeVar('ToolAnnotationsType')


class ToolAnnotationsConverter(ABC, Generic[ToolAnnotationsType]):
    """
    Interface for converting between ToolAnnotations and other tool annotations types
    """
    
    def convert_from_tool_annotations_list(self, tool_annotations: List[ToolAnnotations]) -> List[ToolAnnotationsType]:
        """
        Convert from a list of ToolAnnotations objects to a list of ToolAnnotationsType objects
        
        Args:
            tool_annotations: List of ToolAnnotations objects to convert
            
        Returns:
            List of converted ToolAnnotationsType objects (filtered to remove None values)
        """
        result = []
        for tn in tool_annotations:
            converted = self.convert_from_tool_annotations(tn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_from_tool_annotations(self, tool: ToolAnnotations) -> Optional[ToolAnnotationsType]:
        """
        Convert from a ToolAnnotations object to a ToolAnnotationsType object
        
        Args:
            tool: The ToolAnnotations object to convert
            
        Returns:
            The converted ToolAnnotationsType object or None
        """
        pass
    
    def convert_to_tool_annotations_list(self, tool_annotations: List[ToolAnnotationsType]) -> List[ToolAnnotations]:
        """
        Convert from a list of ToolAnnotationsType objects to a list of ToolAnnotations objects
        
        Args:
            tool_annotations: List of ToolAnnotationsType objects to convert
            
        Returns:
            List of converted ToolAnnotations objects (filtered to remove None values)
        """
        result = []
        for t in tool_annotations:
            converted = self.convert_to_tool_annotations(t)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_to_tool_annotations(self, tool_annotations: ToolAnnotationsType) -> Optional[ToolAnnotations]:
        """
        Convert from a ToolAnnotationsType object to a ToolAnnotations object
        
        Args:
            tool_annotations: The ToolAnnotationsType object to convert
            
        Returns:
            The converted ToolAnnotations object or None
        """
        pass

ToolType = TypeVar('ToolType')


class ToolConverter(ABC, Generic[ToolType]):
    """
    Interface for converting between Tool and other tool types
    """
    
    def convert_from_tools(self, tools: List[Tool]) -> List[ToolType]:
        """
        Convert from a list of Tool objects to a list of ToolType objects
        
        Args:
            tools: List of Tool objects to convert
            
        Returns:
            List of converted ToolType objects (filtered to remove None values)
        """
        result = []
        for tn in tools:
            converted = self.convert_from_tool(tn)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_from_tool(self, tool: Tool) -> Optional[ToolType]:
        """
        Convert from a Tool object to a ToolType object
        
        Args:
            tool: The Tool object to convert
            
        Returns:
            The converted ToolType object or None
        """
        pass
    
    def convert_to_tools(self, tools: List[ToolType]) -> List[Tool]:
        """
        Convert from a list of ToolType objects to a list of Tool objects
        
        Args:
            tools: List of ToolType objects to convert
            
        Returns:
            List of converted Tool objects (filtered to remove None values)
        """
        result = []
        for t in tools:
            converted = self.convert_to_tool(t)
            if converted is not None:
                result.append(converted)
        return result
    
    @abstractmethod
    def convert_to_tool(self, tool: ToolType) -> Optional[Tool]:
        """
        Convert from a ToolType object to a Tool object
        
        Args:
            tool: The ToolType object to convert
            
        Returns:
            The converted Tool object or None
        """
        pass
