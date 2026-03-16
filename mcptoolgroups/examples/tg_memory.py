from mcptoolgroups import Group, ToolConverter, ToolGroupMCPServer
from mcp.types import ToolAnnotations

# two top-level groups, trusted and untrusted
trusted_groups=Group(name="trusted",title="Trusted Toolgroups", description="The tools and toolgroups in this group are trusted by this server")

# Create server
mcp = ToolGroupMCPServer("toolgroup server")

@mcp.toolgroup(parent=trusted_groups, title="Arithmetic", description="Arithmetic Group")
class Arithmetic:
    @mcp.tool(title="Add X and Y Integer", annotations=ToolAnnotations(read_only_hint=True), structured_output=True)
    def add(self, x: int, y: int) -> int:
        ''' add two numbers'''
        return x + y
    
    @mcp.tool(title="Multiply X and Y", annotations=ToolAnnotations(read_only_hint=True), structured_output=True)
    def multiply(self, x: int, y: int) -> int:
        '''multiply two numbers'''
        return x * y 

def op1():
    '''my operation one'''
    print("THIS IS UNTRUSTED OPERATION")
    
untrusted_group=Group(name="untrusted",title="Untrusted Tools Group", description="The tools in this group are not to be trusted")

mcp.add_tool_ex(op1, 
                title="Untrusted Operation1", 
                parent=untrusted_group,
                annotations=ToolAnnotations(read_only_hint=False))

from mcp.client import Client
import asyncio

'''test with in memory client'''
async def main():
    '''list the tools on server to assure that the added tool is in list'''
    server_tools = await mcp.list_tools()
    for t in server_tools:
        print(f"server tool={t}" + str(t))
        
    async with Client(mcp) as client:
        result = await client.list_tools()
        for t in result.tools:
            print(f"client tool={t}")
            print(f"converted tool={ToolConverter().convert_to(t)}")

if __name__ == "__main__":
    asyncio.run(main())
