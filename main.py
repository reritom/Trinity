from meshcore.examples import x_ping_all
from renderer.template_handler import TemplateHandler
import os

handler = TemplateHandler()

logs = x_ping_all()
list_tuple_logs = logs.items()
simple_list = []

for element in list_tuple_logs:
    simple_list.append(element[1])

context = {'logs':simple_list}

rendered = handler.render_template('test.html', context)


print(rendered)

with open(os.path.join('logs', 'log3.html'), 'w') as html_file:
    html_file.write(rendered)
