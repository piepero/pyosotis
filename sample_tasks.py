"""
  sample_tasks.py

  A sample work process with both automatic and manual tasks.
"""

from pyosotis import Task
from sample_dummies import (
    build_binaries,
    clone_auxillary,
    clone_main,
    create_project_name,
)


def task_generate_project_name():
    return Task(
        title="generate project name",
        description="Generates a random project name.",
        run=create_project_name,
    )


def task_clone_main():
    return Task(
        title="clone main repositories",
        description="Clones the main project repositories.",
        run=clone_main,
        requires_func=[task_generate_project_name],
    )


def task_set_version():
    return Task(
        title="set release version in source",
        description="Manually update the code in the main repositories to reflect the new release version.",
        requires_func=[task_clone_main],
    )


def task_clone_auxillary():
    return Task(
        title="clone auxillary repositories",
        description="Clones auxillary repositories needed for the project.",
        run=clone_auxillary,
        requires_func=[task_generate_project_name],
    )


def task_build():
    return Task(
        title="build binaries",
        description="Build binaries from source.",
        run=build_binaries,
        requires_func=[task_set_version, task_clone_auxillary],
    )


def task_upload():
    return Task(
        title="upload release files",
        description="Manually upload the release files.",
        requires_func=[task_build],
    )


def task_push():
    return Task(
        title="push changes to repositories",
        description="Manually push the changes to the respective repositories.",
        requires_func=[task_build],
    )


def task_mark_old():
    return Task(
        title="mark old releases as obsolete",
        description="Manually deactivate the downloads of old releases and mark them as obsolete.",
        requires_func=[task_upload],
    )


def task_send_notifications():
    return Task(
        title="send notifications about new release",
        description="Manually send a bunch of notifications about the new release (E-Mail, Mastodon, WhatsApp, ...).",
        requires_func=[task_mark_old],
    )
