import mcp.types as mcpt;
from typing import Self
from common import Converter, Role, Annotations, Icon, Group, Tool, Resource, Prompt, PromptArgument, ToolAnnotations

class RoleConverter(Converter[Role, mcpt.Role]):
    def convert_to(self, source: mcpt.Role) -> Role:
        return Role.USER if source.value == 'user' else Role.ASSISTANT
    def convert_from(self, target: Role) -> mcpt.Role:
        return mcpt.Role['user'] if target.value == 'USER' else mcpt.Role['assistant']
  
class AnnotationsConverter(Converter[Annotations, mcpt.Annotations]): 
    def __init__(self)->type[Self]:
        self.role_converter = RoleConverter()
    def convert_to(self, source: mcpt.Annotations) -> Annotations:
        return Annotations(self.role_converter.convert_to_list(source.audience), source.priority)
    def convert_from(self, target: Annotations) -> mcpt.Annotations:
        return mcpt.Annotations(self.role_converter.convert_from_list(target.get_audience()), target.get_priority())

class IconConverter(Converter[Icon, mcpt.Icon]): 
    def convert_to(self, source: mcpt.Icon) -> Icon:
        return Icon(source.src, source.mime_type, source.sizes)
    def convert_from(self, target: Icon) -> mcpt.Icon:
        return mcpt.Icon(target.get_src(), target.get_mime_type(), target.get_sizes())
         
class PromptArgumentConverter(Converter[PromptArgument,mcpt.PromptArgument]):  
    def convert_to(self, source: mcpt.PromptArgument) -> PromptArgument:
        return PromptArgument(source.name, source.description, source.required)
    def convert_from(self, target: PromptArgument) -> mcpt.PromptArgument:
        return PromptArgument(target.get_name(), target.get_description(), target.is_required())

class ResourceConverter(Converter[Resource,mcpt.Resource]):
    def __init__(self):
        self.annotations_converter = AnnotationsConverter()
    def convert_to(self, source: mcpt.Resource) -> Resource:
        return Resource(source.name, source.uri, source.title, source.description, source.mimeType, source.size, self.annotations_converter.convert_to(source.annotations), source.meta)
    def convert_from(self, target: Resource) -> mcpt.Resource:
        r = mcpt.Resource()
        r.name = target.get_name()
        r.uri = target.get_uri()
        r.title = target.get_title()
        r.description = target.get_description()
        r.annotations = self.annotations_converter.convert_from(target.get_annotations())
        r.size = target.get_size()
        r.mimeType = target.get_mime_type()        
        r.meta = target.get_meta()
        return r
    
class PromptConverter(Converter[Prompt,mcpt.Prompt]):
    def __init__(self):
        self.arguments_converter = PromptArgumentConverter()
    def convert_to(self, source: mcpt.Prompt) -> Prompt:
        return Prompt(source.name, source.title, source.description, self.arguments_converter.convert_to_list(source.arguments), source.meta)
    def convert_from(self, target: Prompt) -> mcpt.Prompt:
        r = mcpt.Prompt()
        r.name = target.get_name()
        r.title = target.get_title()
        r.description = target.get_description()
        r.arguments = self.arguments_converter.convert_from(target.get_arguments())
        r.size = target.get_size()
        r.mimeType = target.get_mime_type()        
        r.meta = target.get_meta()
        return r
    
class ToolConverter(Converter[Tool,mcpt.Tool]):
    def __init__(self):
        self.icon_converter = IconConverter()
        
    def convert_to(self, source: mcpt.Tool) -> Tool:
        r = Tool(source.name, source.title, source.description, IconConverter().convert_to(source.icons), source.meta)
        r.set_input_schema(source.inputSchema)
        r.set_output_schema(source.outputSchema)
        r.set_icons(self.icon_converter.convert_to_list(source.icons))
        sa = source.annotations
        if (sa):
            r.set_tool_annotations(ToolAnnotations(source.title, sa.readOnlyHint, sa.destructiveHint, sa.idempotent_hint, sa.openWorldHint, sa.return_direct))
        r.set_meta(source.meta)
        return r
    def convert_from(self, target: Tool) -> mcpt.Tool:
        r = mcpt.Tool()
        r.name = target.get_name()
        r.title = target.get_title()
        r.icons = self.icon_converter.convert_from_list(target.get_icons())
        r.description = target.get_description()
        r.annotations = mcpt.ToolAnnotations()
        ta = target.get_tool_annotations()
        if (ta):
            r.annotations.title = ta.get_title()
            r.annotations.readOnlyHint = ta.get_read_only_hint()
            r.annotations.destructiveHint = ta.get_destructive_hint()
            r.annotations.openWorldHint = ta.get_open_world_hint()
            r.annotations.idempotentHint = ta.get_idempotent_hint()
        r.meta = target.get_meta()
        return r

from groupext import Group as GroupEx

class ToolGroupConverter(Converter[Group, GroupEx]):
    def __init__(self):
        self.icon_converter = IconConverter()
    def convert_to(self, source: GroupEx) -> Group:
        ''' icons is currently not supported in GroupEx '''
        r = Group(source.name, source.title, source.description, None, source.meta)
        sp = source.parent
        if (sp):
            cp = self.convert_to(sp)
            cp.add_child_group(r)
        return r
            
    def convert_from(self, target: Group) -> GroupEx:
        r = GroupEx()
        r.name = target.get_name()
        r.title = target.get_title()
        r.description = target.get_description()
        r.meta = target.get_meta()
        tp = target.parent
        if (tp):
            r.parent = self.convert_from(tp)
        return r
        
    
