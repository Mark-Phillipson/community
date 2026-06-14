from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: csharp
"""
ctx.lists["user.code_common_function"] = {
    "integer": "int.TryParse",
    "print": "Console.WriteLine",
    "string": ".ToString",
    "length": ".Length",
    "order by": "OrderBy",
    "order by descending": "OrderByDescending",
    "then by": "ThenBy",
    "then by descending": "ThenByDescending",
    "include": "Include",
    "group by": "GroupBy",
    "select": "Select",
    "where": "Where",
    "first or default": "FirstOrDefault",
    "first": "First",
    "first or default async": "FirstOrDefaultAsync",
    "first async": "FirstAsync",
    "single or default": "SingleOrDefault",
    "contains": "Contains",
    "count": "Count",
    "to list": "ToList",
    "to list async": "ToListAsync",
    "to array": "ToArray",
    "to dictionary": "ToDictionary",
    "to lower": "ToLower",
    "to upper": "ToUpper",
    "trim": "Trim",
    "trim start": "TrimStart",
    "trim end": "TrimEnd",
    "substring": "Substring",
    "replace": "Replace",
    "split": "Split",
}

ctx.lists["user.code_keyword"] = {
    "abstract": " abstract ",
    "add": " add ",
    "alias": " alias ",
    "ascending": " ascending ",
    "async": " async ",
    "await": " await ",
    "base": " base ",
    "boolean": " bool ",
    "break": " break ",
    "case": " case ",
    "catch": " catch ",
    "class": " class ",
    "const": " const ",
    "continue": " continue ",
    "default": " default ",
    "delegate": " delegate ",
    "descending": " descending ",
    "double": " double ",
    "dynamic": " dynamic ",
    "else": " else ",
    "enum": " enum ",
    "equals": " equals ",
    "event": " event ",
    "explicit": " explicit ",
    "extern": " extern ",
    "false": " false ",
    "finally": " finally ",
    "for": " for ",
    "foreach": " foreach ",
    "from": " from ",
    "get": " get ",
    "global": " global ",
    "group": " group ",
    "if": " if ",
    "implicit": " implicit ",
    "in": " in ",
    "integer": " int ",
    "interface": " interface ",
    "internal": " internal ",
    "into": " into ",
    "is": " is ",
    "join": " join ",
    "let": " let ",
    "lock": " lock ",
    "name of": " nameof ",
    "namespace": " namespace ",
    "new": " new ",
    "null": " null ",
    "operator": " operator ",
    "order by": " orderby ",
    "out": " out ",
    "override": " override ",
    "params": " params ",
    "partial": " partial ",
    "private": " private ",
    "protected": " protected ",
    "public": " public ",
    "read only": " readonly ",
    "ref": " ref ",
    "remove": " remove ",
    "required": " required ",
    "return": " return ",
    "sealed": " sealed ",
    "select": " select ",
    "set": " set ",
    "size of": " sizeof ",
    "static": " static ",
    "string": " string ",
    "struct": " struct ",
    "switch": " switch ",
    "this": " this ",
    "throw": " throw ",
    "true": " true ",
    "try": " try ",
    "type of": " typeof ",
    "unsafe": " unsafe ",
    "using": " using ",
    "value": " value ",
    "var": " var ",
    "virtual": " virtual ",
    "volatile": " volatile ",
    "void": " void ",
    "where": " where ",
    "while": " while ",
    "yield": " yield ",
}



operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    ASSIGNMENT_INCREMENT="++",
    # code_operators_bitwise
    BITWISE_NOT="~",
    BITWISE_AND=" & ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_OR=" | ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA="=>",
    # code_operators_pointer
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_OR=" || ",
    MATH_AND=" && ",
    MATH_NOT="!",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_LESS_THAN=" < ",
    # code_operators_pointer
    POINTER_ADDRESS_OF="&",
    POINTER_INDIRECTION="*",
    POINTER_STRUCTURE_DEREFERENCE="->",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.insert("this")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_insert_null():
        actions.insert("null")

    def code_insert_is_null():
        actions.insert(" == null ")

    def code_insert_is_not_null():
        actions.insert(" != null")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "private static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_static_function(text: str):
        result = "protected static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "public void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_static_function(text: str):
        result = "public static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
