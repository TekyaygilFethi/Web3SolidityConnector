import os
import global_variables
import shutil

if os.path.isdir(global_variables.GLOBAL_COMPILATION_PATH):
    shutil.rmtree(global_variables.GLOBAL_COMPILATION_PATH, ignore_errors=True)
    print(f"{global_variables.GLOBAL_COMPILATION_PATH} has been deleted!")
else:
    print(
        f"{global_variables.GLOBAL_COMPILATION_PATH} folder does not exists, no action has been taken!"
    )
