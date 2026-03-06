import unittest
from typing import Any, Dict, List, Optional, TypeVar, Callable, Generic, Protocol
from enum import Enum

from common import (
    Role,
    Group,
    Tool,
    Prompt,
    Resource,
    AbstractBase,
    convertAll,
)

# =========================================================================
# AbstractBase
# =========================================================================

class TestAbstractBase(unittest.TestCase):
    def test_throws_when_name_is_empty(self):
        with self.assertRaisesRegex(ValueError, "name must not be null or empty"):
            Group(None)

    def test_uses_DEFAULT_SEPARATOR_by_default(self):
        g = Group("root")
        self.assertEqual(g.name_separator, AbstractBase.DEFAULT_SEPARATOR)

    def test_allows_a_custom_separator(self):
        g = Group("root", "/")
        self.assertEqual(g.name_separator, "/")

# =========================================================================
# Group — hierarchy & fully qualified names
# =========================================================================

class TestGroup(unittest.TestCase):
    def test_is_root_when_created_standalone(self):
        root = Group("root")
        self.assertTrue(root.is_root)
        self.assertIsNone(root.parent)
        self.assertEqual(root.get_root(), root)

    def test_build_a_parent_child_hierarchy(self):
        root = Group("com")
        mid = Group("example")
        leaf = Group("api")

        self.assertTrue(root.add_child_group(mid))
        self.assertTrue(mid.add_child_group(leaf))

        self.assertEqual(mid.parent, root)
        self.assertEqual(leaf.parent, mid)
        self.assertFalse(leaf.is_root())
        self.assertEqual(leaf.get_root(), root)

    def test_computes_fully_qualified_name_through_the_chain(self):
        root = Group("com")
        mid = Group("example")
        leaf = Group("api")

        root.add_child_group(mid)
        mid.add_child_group(leaf)

        self.assertEqual(root.get_fully_qualified_name(), "com")
        self.assertEqual(mid.get_fully_qualified_name(), "com.example")
        self.assertEqual(leaf.get_fully_qualified_name(), "com.example.api")

    def test_uses_custom_separator_in_fully_qualified_name(self):
        root = Group("com", "/")
        child = Group("api", "/")
        root.add_child_group(child)

        self.assertEqual(child.get_fully_qualified_name(), "com/api")

    def test_prevents_duplicate_child_groups(self):
        root = Group("root")
        child = Group("child")

        self.assertTrue(root.add_child_group(child))
        self.assertFalse(root.add_child_group(child))
        self.assertEqual(len(root.child_groups), 1)

    def test_removes_child_group_and_clears_parent(self):
        root = Group("root")
        child = Group("child")

        root.add_child_group(child)
        self.assertTrue(root.remove_child_group(child))
        self.assertEqual(len(root.child_groups), 0)
        self.assertIsNone(child.parent)

    def test_returns_false_when_removing_non_existent_child_group(self):
        root = Group("root")
        other = Group("other")
        self.assertFalse(root.remove_child_group(other))

    def test_stores_optional_properties_title_description_meta_icons(self):
        g = Group("g")
        g.title = "My Group"
        g.description = "A description"
        g.meta = {"key": "value"}
        icon: Icon = {"src": "icon.png", "mimeType": "image/png"}
        g.icons = [icon]

        self.assertEqual(g.title, "My Group")
        self.assertEqual(g.description, "A description")
        self.assertEqual(g.meta, {"key": "value"})
        self.assertEqual(len(g.icons), 1)
        self.assertEqual(g.icons[0]["src"], "icon.png")

# =========================================================================
# Group ↔ Tool bidirectional relationship
# =========================================================================

class TestGroupToolRelationship(unittest.TestCase):
    def test_adds_a_tool_and_links_parent_group_bidirectionally(self):
        group = Group("g")
        tool = Tool("t")

        self.assertTrue(group.add_child_tool(tool))
        self.assertIn(tool, group.child_tools)
        self.assertIn(group, tool.parent_groups)

    def test_prevents_duplicate_tool_additions(self):
        group = Group("g")
        tool = Tool("t")

        group.add_child_tool(tool)
        self.assertFalse(group.add_child_tool(tool))
        self.assertEqual(len(group.child_tools), 1)

    def test_removes_a_tool_and_unlinks_parent_group(self):
        group = Group("g")
        tool = Tool("t")

        group.add_child_tool(tool)
        self.assertTrue(group.remove_child_tool(tool))
        self.assertEqual(len(group.child_tools), 0)
        self.assertEqual(len(tool.parent_groups), 0)

    def test_returns_false_when_removing_non_existent_tool(self):
        group = Group("g")
        tool = Tool("t")
        self.assertFalse(group.remove_child_tool(tool))

# =========================================================================
# Group ↔ Prompt bidirectional relationship
# =========================================================================

class TestGroupPromptRelationship(unittest.TestCase):
    def test_adds_a_prompt_and_links_parent_group_bidirectionally(self):
        group = Group("g")
        prompt = Prompt("p")

        self.assertTrue(group.add_child_prompt(prompt))
        self.assertIn(prompt, group.child_prompts)
        self.assertIn(group, prompt.parent_groups)

    def test_prevents_duplicate_prompt_additions(self):
        group = Group("g")
        prompt = Prompt("p")

        group.add_child_prompt(prompt)
        self.assertFalse(group.add_child_prompt(prompt))

    def test_removes_a_prompt_and_unlinks_parent_group(self):
        group = Group("g")
        prompt = Prompt("p")

        group.add_child_prompt(prompt)
        self.assertTrue(group.remove_child_prompt(prompt))
        self.assertEqual(len(group.child_prompts), 0)
        self.assertEqual(len(prompt.parent_groups), 0)

# =========================================================================
# Group ↔ Resource bidirectional relationship
# =========================================================================

class TestGroupResourceRelationship(unittest.TestCase):
    def test_adds_a_resource_and_links_parent_group_bidirectionally(self):
        group = Group("g")
        resource = Resource("r","http://my/path")

        self.assertTrue(group.add_child_resource(resource))
        self.assertIn(resource, group.child_resources)
        self.assertIn(group, resource.parent_groups)

    def test_prevents_duplicate_resource_additions(self):
        group = Group("g")
        resource = Resource("r","http://my/path")

        group.add_child_resource(resource)
        self.assertFalse(group.add_child_resource(resource))

    def test_removes_a_resource_and_unlinks_parent_group(self):
        group = Group("g")
        resource = Resource("r", "http://my/path")

        group.add_child_resource(resource)
        self.assertTrue(group.remove_child_resource(resource))
        self.assertEqual(len(group.child_resources), 0)
        self.assertEqual(len(resource.parent_groups), 0)

# =========================================================================
# AbstractLeaf — shared leaf behavior
# =========================================================================

class TestAbstractLeaf(unittest.TestCase):
    def test_returns_its_name_as_fully_qualified_name(self):
        tool = Tool("myTool")
        self.assertEqual(tool.get_fully_qualified_name(), "myTool")

    def test_can_belong_to_multiple_parent_groups(self):
        g1 = Group("g1")
        g2 = Group("g2")
        tool = Tool("shared")

        g1.add_child_tool(tool)
        g2.add_child_tool(tool)

        self.assertEqual(len(tool.parent_groups), 2)
        self.assertIn(g1, tool.parent_groups)
        self.assertIn(g2, tool.parent_groups)

    def test_getParentGroupRoots_returns_roots_of_all_parent_groups(self):
        root = Group("root")
        child = Group("child")
        root.add_child_group(child)

        tool = Tool("tool")
        child.add_child_tool(tool)

        roots = tool.get_parent_group_roots()
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0], root)

    def test_prevents_duplicate_parent_group_registration(self):
        group = Group("g")
        tool = Tool("t")

        self.assertTrue(tool.add_parent_group(group))
        self.assertFalse(tool.add_parent_group(group))
        self.assertEqual(len(tool.parent_groups), 1)

    def test_returns_false_when_removing_non_existent_parent_group(self):
        tool = Tool("t")
        group = Group("g")
        self.assertFalse(tool.remove_parent_group(group))

# =========================================================================
# Tool
# =========================================================================

class TestTool(unittest.TestCase):
    def test_stores_optional_schemas_and_annotations(self):
        tool = Tool("myTool")
        tool.input_schema = '{ "type": "object" }'
        tool.output_schema = '{ "type": "string" }'
        tool.tool_annotations = {
            "title": "MyTool",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
            "returnDirect": True,
        }

        self.assertEqual(tool.input_schema, '{ "type": "object" }')
        self.assertEqual(tool.output_schema, '{ "type": "string" }')
        self.assertTrue(tool.tool_annotations["readOnlyHint"])
        self.assertTrue(tool.tool_annotations["returnDirect"])

# =========================================================================
# Prompt & PromptArgument
# =========================================================================

class TestPrompt(unittest.TestCase):
    def test_adds_and_removes_prompt_arguments(self):
        prompt = Prompt("myPrompt")
        arg: PromptArgument = {"name": "query", "required": True}

        self.assertTrue(prompt.add_argument(arg))
        self.assertEqual(len(prompt.arguments), 1)
        self.assertEqual(prompt.arguments[0]["name"], "query")
        self.assertTrue(prompt.arguments[0]["required"])

        self.assertTrue(prompt.remove_argument(arg))
        self.assertEqual(len(prompt.arguments), 0)

    def test_prevents_duplicate_prompt_arguments(self):
        prompt = Prompt("myPrompt")
        arg: PromptArgument = {"name": "query"}

        prompt.add_argument(arg)
        self.assertFalse(prompt.add_argument(arg))
        self.assertEqual(len(prompt.arguments), 1)

    def test_returns_false_when_removing_non_existent_argument(self):
        prompt = Prompt("myPrompt")
        arg: PromptArgument = {"name": "other"}
        self.assertFalse(prompt.remove_argument(arg))

# =========================================================================
# Resource
# =========================================================================

class TestResource(unittest.TestCase):
    def test_stores_optional_URI_size_mimeType_and_annotations(self):
        resource = Resource("doc", "file:///data.json")
        resource.size = 1024
        resource.mimeType = "application/json"
        resource.annotations = {
            "audience": [Role.USER],
            "priority": 1,
            "lastModified": "2026-01-01T00:00:00Z",
        }

        self.assertEqual(resource.uri, "file:///data.json")
        self.assertEqual(resource.size, 1024)
        self.assertEqual(resource.mimeType, "application/json")
        self.assertEqual(resource.annotations["audience"], [Role.USER])
        self.assertEqual(resource.annotations["priority"], 1)

# =========================================================================
# convertAll utility
# =========================================================================

class TestConvertAll(unittest.TestCase):
    def test_maps_and_filters_nullish_results(self):
        items = [1, 2, 3, 4, 5]
        result = convertAll(items, lambda n: f"even:{n}" if n % 2 == 0 else None)
        self.assertEqual(result, ["even:2", "even:4"])

    def test_returns_all_items_when_none_are_nullish(self):
        result = convertAll(["a", "b"], lambda s: s.upper())
        self.assertEqual(result, ["A", "B"])

    def test_returns_empty_array_from_empty_input(self):
        result = convertAll([], lambda x: x)
        self.assertEqual(result, [])

# =========================================================================
# Converter interface (structural typing check)
# =========================================================================

class TestConverterInterface(unittest.TestCase):
    def test_can_be_implemented_and_used_for_bidirectional_conversion(self):
        class ToolConverterImpl:
            def fromInternal(self, tool: Tool) -> Dict[str, str]:
                return {"n": tool.name}
            def toInternal(self, ext: Dict[str, str]) -> Tool:
                return Tool(ext["n"])

        toolConverter: Converter[Tool, Dict[str, str]] = ToolConverterImpl()

        tool = Tool("test")
        ext = toolConverter.fromInternal(tool)
        self.assertEqual(ext, {"n": "test"})

        back = toolConverter.toInternal(ext)
        self.assertEqual(back.name, "test")

# =========================================================================
# Complex tree scenario
# =========================================================================

class TestComplexTreeScenario(unittest.TestCase):
    def test_builds_a_full_tree_and_verifies_all_relationships(self):
        # com.example.api
        com = Group("com")
        example = Group("example")
        api = Group("api")

        com.add_child_group(example)
        example.add_child_group(api)

        # Tools under api
        listTool = Tool("list")
        createTool = Tool("create")
        api.add_child_tool(listTool)
        api.add_child_tool(createTool)

        # Prompts under example
        helpPrompt = Prompt("help")
        example.add_child_prompt(helpPrompt)

        # Resources under com
        readme = Resource("readme", "file:///README.md")
        com.add_child_resource(readme)

        # Verify structure
        self.assertEqual(len(com.child_groups), 1)
        self.assertEqual(len(example.child_groups), 1)
        self.assertEqual(len(api.child_tools), 2)
        self.assertEqual(len(example.child_prompts), 1)
        self.assertEqual(len(com.child_resources), 1)

        # Verify FQN
        self.assertEqual(api.get_fully_qualified_name(), "com.example.api")

        # Verify roots from leaves
        self.assertEqual(listTool.get_parent_group_roots()[0], com)
        self.assertEqual(helpPrompt.get_parent_group_roots()[0], com)
        self.assertEqual(readme.get_parent_group_roots()[0], com)

        # Remove tool and check cleanup
        api.remove_child_tool(listTool)
        self.assertEqual(len(api.child_tools), 1)
        self.assertEqual(len(listTool.parent_groups), 0)

# =========================================================================
# FAILURE / EDGE CASE / STATE CONSISTENCY TESTS
# =========================================================================

class TestAbstractBaseFailureCases(unittest.TestCase):
    def test_throws_when_name_is_null_ish_undefined_coerced(self):
        # testing runtime guard for python None
        with self.assertRaises(Exception):
            Group(None)

    def test_throws_when_name_is_null(self):
        with self.assertRaises(Exception):
            Group(None)

    def test_name_remains_the_value_set_at_construction_readonly_intent(self):
        g = Group("immutable")
        self.assertEqual(g.name, "immutable")
        # In Python, unless __setattr__ is overridden, there's no strict enforcement 
        # but this verifies the value is consistent.

class TestGroupConsistency(unittest.TestCase):
    def test_double_removing_a_child_group_is_idempotent_returns_false_second_time(self):
        root = Group("root")
        child = Group("child")

        root.add_child_group(child)
        self.assertTrue(root.remove_child_group(child))
        self.assertFalse(root.remove_child_group(child))
        self.assertEqual(len(root.child_groups), 0)
        self.assertIsNone(child.parent)

    def test_double_removing_a_child_tool_is_idempotent(self):
        group = Group("g")
        tool = Tool("t")

        group.add_child_tool(tool)
        group.remove_child_tool(tool)
        self.assertFalse(group.remove_child_tool(tool))
        self.assertEqual(len(group.child_tools), 0)
        self.assertEqual(len(tool.parent_groups), 0)

    def test_double_removing_a_child_prompt_is_idempotent(self):
        group = Group("g")
        prompt = Prompt("p")

        group.add_child_prompt(prompt)
        group.remove_child_prompt(prompt)
        self.assertFalse(group.remove_child_prompt(prompt))

    def test_double_removing_a_child_resource_is_idempotent(self):
        group = Group("g")
        resource = Resource("r","file:///foo")

        group.add_child_resource(resource)
        group.remove_child_resource(resource)
        self.assertFalse(group.remove_child_resource(resource))

    def test_re_adding_a_child_group_after_removal_works_correctly(self):
        root = Group("root")
        child = Group("child")

        root.add_child_group(child)
        root.remove_child_group(child)
        self.assertIsNone(child.parent)

        self.assertTrue(root.add_child_group(child))
        self.assertEqual(child.parent, root)
        self.assertEqual(len(root.child_groups), 1)

    def test_re_adding_a_tool_after_removal_restores_bidirectional_link(self):
        group = Group("g")
        tool = Tool("t")

        group.add_child_tool(tool)
        group.remove_child_tool(tool)

        self.assertTrue(group.add_child_tool(tool))
        self.assertIn(tool, group.child_tools)
        self.assertIn(group, tool.parent_groups)

    def test_removing_child_group_from_wrong_parent_returns_false_and_keeps_the_link_intact(self):
        parent1 = Group("p1")
        parent2 = Group("p2")
        child = Group("child")

        parent1.add_child_group(child)

        # trying to remove from parent2 where it was never added
        self.assertFalse(parent2.remove_child_group(child))

        # original relationship still intact
        self.assertEqual(child.parent, parent1)
        self.assertIn(child, parent1.child_groups)

class TestDeeplyNestedTree(unittest.TestCase):
    def test_get_root_traverses_5_levels_deep(self):
        g1 = Group("l1")
        g2 = Group("l2")
        g3 = Group("l3")
        g4 = Group("l4")
        g5 = Group("l5")

        g1.add_child_group(g2)
        g2.add_child_group(g3)
        g3.add_child_group(g4)
        g4.add_child_group(g5)

        self.assertEqual(g5.get_root(), g1)
        self.assertEqual(g5.get_fully_qualified_name(), "l1.l2.l3.l4.l5")

    def test_FQN_updates_correctly_after_re_parenting_a_subtree(self):
        root1 = Group("com")
        root2 = Group("org")
        child = Group("api")

        root1.add_child_group(child)
        self.assertEqual(child.get_fully_qualified_name(), "com.api")

        root1.remove_child_group(child)
        root2.add_child_group(child)
        self.assertEqual(child.get_fully_qualified_name(), "org.api")
        self.assertEqual(child.get_root(), root2)

class TestAbstractLeafFailureCases(unittest.TestCase):
    def test_removing_parent_group_from_tool_not_in_that_group_returns_false(self):
        g1 = Group("g1")
        g2 = Group("g2")
        tool = Tool("t")

        g1.add_child_tool(tool)

        self.assertFalse(tool.remove_parent_group(g2))
        self.assertEqual(len(tool.parent_groups), 1)
        self.assertIn(g1, tool.parent_groups)

    def test_getParentGroupRoots_with_multiple_disjoint_trees(self):
        rootA = Group("rootA")
        childA = Group("childA")
        rootA.add_child_group(childA)

        rootB = Group("rootB")

        tool = Tool("shared")
        childA.add_child_tool(tool)
        rootB.add_child_tool(tool)

        roots = tool.get_parent_group_roots()
        self.assertEqual(len(roots), 2)
        self.assertIn(rootA, roots)
        self.assertIn(rootB, roots)

class TestPromptFailureCases(unittest.TestCase):
    def test_double_removing_a_prompt_argument_is_idempotent(self):
        prompt = Prompt("p")
        arg: PromptArgument = {"name": "x"}

        prompt.add_argument(arg)
        prompt.remove_argument(arg)
        self.assertFalse(prompt.remove_argument(arg))
        self.assertEqual(len(prompt.arguments), 0)

    def test_re_adding_a_prompt_argument_after_removal_works(self):
        prompt = Prompt("p")
        arg: PromptArgument = {"name": "x", "required": True}

        prompt.add_argument(arg)
        prompt.remove_argument(arg)
        self.assertTrue(prompt.add_argument(arg))
        self.assertEqual(len(prompt.arguments), 1)

class TestOptionalPropertiesDefault(unittest.TestCase):
    def test_Group_optional_properties_are_None_when_not_set(self):
        g = Group("g")
        # In Python, properties are usually None if not set, corresponding to undefined
        self.assertIsNone(g.title)
        self.assertIsNone(g.description)
        self.assertIsNone(g.meta)
        self.assertIsNone(g.icons)

    def test_Tool_optional_properties_are_None_when_not_set(self):
        t = Tool("t")
        self.assertIsNone(t.input_schema)
        self.assertIsNone(t.output_schema)
        self.assertIsNone(t.tool_annotations)

    def test_Resource_optional_properties_are_None_when_not_set(self):
        r = Resource("r","http://nothinness")
        self.assertIsNone(r.size)
        self.assertIsNone(r.mime_type)
        self.assertIsNone(r.annotations)

class TestConvertAllEdgeFailureCases(unittest.TestCase):
    def test_filters_out_all_items_when_every_conversion_returns_None(self):
        result = convertAll([1, 2, 3], lambda x: None)
        self.assertEqual(result, [])

    def test_filters_out_all_items_when_every_conversion_returns_undefined_mapped_to_None(self):
        # Python doesn't have undefined, so we test None
        result = convertAll([1, 2, 3], lambda x: None)
        self.assertEqual(result, [])

    def test_handles_mixed_null_undefined_valid_results(self):
        def mixed_conv(n):
            if n == 1: return None
            if n == 2: return None # mapping undefined to None
            return f"ok:{n}"
        
        result = convertAll([1, 2, 3, 4], mixed_conv)
        self.assertEqual(result, ["ok:3", "ok:4"])

if __name__ == "__main__":
    unittest.main()

    