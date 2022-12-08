import errno
import os
import shutil
import fnmatch
import sys


def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.6+
    count = len(it)

    def show(j):
        x = int(size * j / count)
        print(f"{prefix}[{u'█' * x}{('.' * (size - x))}] {j}/{count}", end='\r', file=out, flush=True)

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)


def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise


class DartModule:

    def __str__(self) -> str:
        return self.name

    def __init__(self, name, deps):
        self.name = name
        self.dependencies = deps

    name = ""
    dependencies = []


numberOfModules = 800
maxDependenciesPerModule = 5
generated_path = os.path.join(".")


def generate_module_structure(module_names):
    def make_chunks(l, n):
        """Yield n number of striped chunks from l."""
        for i in range(0, n):
            yield l[i::n]

    module_root = module_names.pop(0)
    dependencies = []
    if len(module_names) > maxDependenciesPerModule:
        for chunk in make_chunks(module_names, maxDependenciesPerModule):
            dependencies.append(generate_module_structure(chunk))
    else:
        formatted_names = ["module_{}".format(x) for x in module_names]
        dependencies = [DartModule(x, []) for x in formatted_names]
    root_module_name = "module_{}".format(module_root)
    dart_module = DartModule(root_module_name, dependencies)
    return dart_module


def get_all_modules(dart_module: DartModule):
    result = [dart_module]
    for x in dart_module.dependencies:
        result.extend(get_all_modules(x))
    return result


def write_module(dart_module: DartModule):
    def find_and_replace(directory, find, replace, file_pattern):
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in fnmatch.filter(files, file_pattern):
                filepath = os.path.join(path, filename)
                with open(filepath) as f:
                    s = f.read()
                s = s.replace(find, replace)
                with open(filepath, "w") as f:
                    f.write(s)

    def rename_example_module(location):
        find_and_replace(location, "ExampleModule", dart_module.name, "*.dart")
        find_and_replace(location, "example_module", dart_module.name, "*.dart")
        find_and_replace(location, "example_module", dart_module.name, "*.yaml")

    def perform_template_replacement(location):
        def generate_deps_import():
            deps_to_return = [
                "import 'package:{}/index.dart';".format(x.name)
                for x in dart_module.dependencies
            ]
            return "\n".join(deps_to_return)

        def generate_view_layout():
            items_to_return = ["        const {}Component(),".format(x.name) for x in dart_module.dependencies]
            return "\n".join(items_to_return)

        def generate_pubspec_dependencies():
            items_to_return = []
            for dependency in dart_module.dependencies:
                dependency_path = os.path.join("..", dependency.name)
                items_to_return.append(
                    """  {module_name}:
    path: {module_path}""".format(module_name=dependency.name, module_path=dependency_path)
                )
            return "\n".join(items_to_return)

        imports = generate_deps_import()
        views = generate_view_layout()
        pubspec_deps = generate_pubspec_dependencies()
        find_and_replace(location, "// [Replace] widget_deps", imports, "*.dart")
        find_and_replace(location, "// [Replace] children", views, "*.dart")
        find_and_replace(location, "# <Dependencies>", pubspec_deps, "*.yaml")

    example_dir = os.path.join(".", "lib", "example_module")
    target_dir = os.path.join(generated_path, dart_module.name)

    copy_anything(example_dir, target_dir)
    rename_example_module(target_dir)
    perform_template_replacement(target_dir)


# if os.path.isdir(generated_path):
#     shutil.rmtree(generated_path)
# if not os.path.isdir(generated_path):
#     os.mkdir(generated_path)
for folder in os.listdir(generated_path):
    folder_path = os.path.join(generated_path, folder)
    if os.path.isdir(folder_path) and "module_" in folder:
        shutil.rmtree(folder_path)

root = generate_module_structure([x for x in range(0, numberOfModules)])
all_modules = get_all_modules(root)
for module in progressbar(all_modules, "Generating: ", 80):
    write_module(module)
