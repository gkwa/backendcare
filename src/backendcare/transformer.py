from typing import Union

import libcst as cst


class ImportTransformer(cst.CSTTransformer):
    def __init__(self):
        self.import_map = {}
        self.seen_imports = set()  # Track imported base modules

    def _get_module_name(self, module_node) -> str:
        if isinstance(module_node, cst.Name):
            return module_node.value
        elif isinstance(module_node, cst.Attribute):
            return (
                f"{self._get_module_name(module_node.value)}.{module_node.attr.value}"
            )
        return ""

    def _create_dotted_name(self, full_name: str) -> cst.Attribute:
        parts = full_name.split(".")
        if len(parts) == 1:
            return cst.Name(value=parts[0])

        # Build nested Attribute nodes starting with first part
        result = cst.Name(value=parts[0])
        for part in parts[1:]:
            result = cst.Attribute(
                value=result, attr=cst.Name(value=part), dot=cst.Dot()
            )
        return result

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> Union[cst.Import, cst.FlattenSentinel[cst.Import], cst.RemovalSentinel]:
        if not original_node.relative:
            module = self._get_module_name(original_node.module)
            module_parts = module.split(".")
            base_module = module_parts[0]

            # If we've already seen this base module, just update the import map
            if base_module in self.seen_imports:
                # Update import map for each imported name
                for import_name in original_node.names:
                    name = import_name.name.value
                    asname = (
                        import_name.asname.name.value if import_name.asname else None
                    )
                    if asname:
                        self.import_map[asname] = f"{module}.{name}"
                    else:
                        self.import_map[name] = f"{module}.{name}"
                return cst.RemovalSentinel.REMOVE  # Remove duplicate import

            # First time seeing this base module
            self.seen_imports.add(base_module)
            new_imports = [
                cst.Import(names=[cst.ImportAlias(name=cst.Name(value=base_module))])
            ]

            # Update import map for each imported name
            for import_name in original_node.names:
                name = import_name.name.value
                asname = import_name.asname.name.value if import_name.asname else None
                if asname:
                    self.import_map[asname] = f"{module}.{name}"
                else:
                    self.import_map[name] = f"{module}.{name}"

            return cst.FlattenSentinel(new_imports)
        return updated_node

    def leave_Import(
        self, original_node: cst.Import, updated_node: cst.Import
    ) -> Union[cst.Import, None]:
        # Keep track of base modules for regular imports too
        for import_name in original_node.names:
            module = self._get_module_name(import_name.name)
            base_module = module.split(".")[0]
            self.seen_imports.add(base_module)
        return updated_node

    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> Union[cst.Name, cst.Attribute]:
        if original_node.value in self.import_map:
            return self._create_dotted_name(self.import_map[original_node.value])
        return updated_node
