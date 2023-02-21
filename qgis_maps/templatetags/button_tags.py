from django import template
from django.utils.safestring import mark_safe
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def output_javascript(context):

    out = f"""

        function waitForElement(selector, callback) {{
          var intervalId = setInterval(function() {{
            var node = document.querySelector(selector);
            if (node) {{
              clearInterval(intervalId);
              callback(node);
            }}
          }}, 100);
        }};

        window.onload = function() {{
          waitForElement(".background-preview-button-frame", function(node) {{
            const ul = document.querySelector('div#ms-container nav.gn-menu.gn-primary .gn-menu-content-right .gn-menu-list');
            var newElement = '<li>' +
                             '<a class="nav-link btn btn-secondary btn-sm" ' +
                             'style="background-color: white;" target="_blank" ' +
                             'href="/qgis-maps/5de83f66-afaa-43ac-b326-dd5c3afd2e40/index.html">' +
                             '<span>3D VIEW</span>' +
                             '</a>' +
                             '</li>';
            ul.innerHTML = newElement + ul.innerHTML;
          }});
        }};
    """

    return mark_safe(out)

