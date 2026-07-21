# Google-Style Docstring Guidelines for Distributed Design Optimizer
#
# All public modules, classes, methods, and functions should have docstrings.
# Private methods (starting with _) are optional but recommended.
#
# === MODULE DOCSTRING ===
# Every Python file should start with a module-level docstring describing its purpose.
#
# === FUNCTION/METHOD DOCSTRING ===
# Format:
#     """Brief one-line description.
#     
#     Longer description if needed. Can span multiple lines.
#     
#     Args:
#         param1: Description of param1.
#         param2: Description of param2.
#         
#     Returns:
#         Description of the return value.
#         
#     Raises:
#         ValueError: Description of when this is raised.
#     """
#
# === CLASS DOCSTRING ===
# Format:
#     """Brief one-line description of the class.
#     
#     Longer description if needed.
#     
#     Attributes:
#         attr1: Description of attr1.
#         attr2: Description of attr2.
#     """
#
# === VALIDATION RULES ===
# The following rules are checked automatically:
#
# --- Existence Rules ---
#
# [RULE] MODULE_DOCSTRING_REQUIRED
# Every .py file must have a module-level docstring.
#
# [RULE] CLASS_DOCSTRING_REQUIRED
# Every public class must have a docstring.
#
# [RULE] FUNCTION_DOCSTRING_REQUIRED
# Every public function/method must have a docstring.
#
# [RULE] INIT_DOCSTRING_REQUIRED
# Every __init__ method must have a docstring.
#
# --- Content/Style Rules ---
#
# [RULE] SUMMARY_LINE_REQUIRED
# Every docstring must begin with a concise one-line summary.
# The summary must be on the first line and end with a period.
#
# [RULE] ARGS_DOCUMENTED
# All parameters (except self/cls) must be listed in an Args: section.
# Each entry must follow the format: "param_name: Description."
# Parameters in the docstring must match the actual function signature.
#
# [RULE] RETURNS_DOCUMENTED
# Functions with a return type annotation (other than None) must have a Returns: section.
#
# [RULE] RAISES_DOCUMENTED
# If the docstring has a Raises: section, each entry must follow the format:
#     "ExceptionType: Description of when raised."
#
# [RULE] NO_UNDOCUMENTED_PARAMS
# The Args: section must not contain parameter names that do not exist
# in the function signature (guards against stale documentation).
#
# --- Type-Hint Rules ---
#
# [RULE] NO_UNION_OPTIONAL
# Type hints must use PEP 604 syntax: write "X | Y" instead of Union[X, Y]
# and "X | None" instead of Optional[X]. typing.Union and typing.Optional
# are flagged in parameter and return-type annotations.
#
# [RULE] NO_QUOTED_TYPE_HINTS
# Type hints must be direct, not quoted/forward-reference strings.
# Write "List[Tuple[int, str]]" instead of "'List[Tuple[int, str]]'".
#
# === REFERENCE ===
# https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
