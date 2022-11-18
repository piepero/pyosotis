def task_clone_main():
    return {
        "message": "clone main repositories",
    }


def task_set_version():
    return {
        "message": "set release version in source",
        "requires": [task_clone_main],
    }


def task_clone_remaining():
    return {
        "message": "clone remaining repositories",
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
        "message": "upload release files",
        "requires": [task_build],
    }


def task_alte_inaktiv():
    return {
        "message": "alte Downloads inaktiv setzen",
        "requires": [task_upload],
    }


def task_push_release_erstellen():
    return {
        "message": "interne Mail mit Infos zum neuen Release",
        "requires": [task_alte_inaktiv],
    }


def task_send_mail():
    return {
        "message": "interne Mail mit Infos zum neuen Release",
        "requires": [task_alte_inaktiv],
    }
