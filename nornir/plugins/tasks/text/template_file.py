from typing import Any, Optional, Dict, Callable

from nornir.core.helpers import jinja_helper, merge_two_dicts
from nornir.core.task import Result, Task

FiltersDict = Optional[Dict[str, Callable[..., str]]]


def template_file(
    task: Task,
    template: str,
    path: str,
    jinja_filters: FiltersDict = None,
    **kwargs: Any
):
    """
    Renders contants of a file with jinja2. All the host data is available in the tempalte

    Arguments:
        template: filename
        path: path to dir with templates
        jinja_filters: jinja filters to enable. Defaults to nornir.config.jinja_filters
        **kwargs: additional data to pass to the template

    Returns:
        Result object with the following attributes set:
          * result (``string``): rendered string
    """
    jinja_filters = jinja_filters or {} or task.nornir.config.jinja_filters
    merged = merge_two_dicts(task.host, kwargs)
    text = jinja_helper.render_from_file(
        template=template,
        path=path,
        host=task.host,
        jinja_filters=jinja_filters,
        **merged
    )
    return Result(host=task.host, result=text)