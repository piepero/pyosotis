from sample_dummies import clone_main, clone_remaining


def task_clone_main():
    return {
        "message": "clone main repositories",
        "run": clone_main,
    }


def task_set_version():
    return {
        "message": "set release version in source",
        "requires": [task_clone_main],
    }


def task_clone_remaining():
    return {
        "message": "clone remaining repositories",
        "run": clone_remaining,
    }


def task_build():
    return {
        "message": "build binaries",
        "requires": [task_set_version, task_clone_remaining],
    }


def task_upload():
    return {
        "message": "upload release files",
        "requires": [task_build],
    }


def task_push():
    return {
        "message": "push changes to repositories",
        "requires": [task_build],
    }


def task_mark_old():
    return {
        "message": "mark old releases as obsolete",
        "requires": [task_upload],
    }


def task_send_notofications():
    return {
        "message": "send notifications about new release",
        "requires": [task_mark_old],
    }
