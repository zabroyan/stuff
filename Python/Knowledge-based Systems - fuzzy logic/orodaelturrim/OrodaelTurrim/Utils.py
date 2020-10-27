import sys
import traceback
from pathlib import Path
import uuid
from datetime import datetime
from PyQt5 import QtWidgets
from OrodaelTurrim.config import Config
from OrodaelTurrim import __version__

html_template = """
<html>
<head>
<style>

.collapsible {{
  background-color: #eee;
  color: #444;
  cursor: pointer;
  padding: 18px;
  width: 20%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}}


.active, .collapsible:hover {{
  background-color: #ccc;
}}


.content {{
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #f1f1f1;
}}
</style>

</head>
<body>
    <h1> Meta info </h1>
        Datetime: {datetime} <br>
        Orodael Turrim version: {version}
        
    <h1> Exception </h1>
        <pre>
{traceback}
        </pre>
        
    <h1> Config </h1>
{config}

    <h1> History </h1>
        <button type="button" class="collapsible">Show history</button>
        <div class="content">{history}</div>
                
    <h1> Implementation </h1>
        <button type="button" class="collapsible">Show implementation</button>
        <div class="content">{implementation}</div>


<script>
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {{
        coll[i].addEventListener("click", function() {{
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {{
                content.style.display = "none";
            }} else {{
                content.style.display = "block";
            }}
        }});
    }}
</script>

</body>
</html>
"""


def bug_report(game_engine, exc_type, exc_value, exc_traceback):
    # Create config text
    attributes = dict([(key, value) for key, value in Config.__dict__.items() if key[:1] != '_'])

    config = '<table>'
    for key, value in attributes.items():
        config += f'<tr><td>{key}</td> <td>{value}</td></tr>'
    config += '</table>'

    # Create exception text
    exception = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # Create history text
    history = game_engine.get_game_history().to_html()

    # Create timestamp text
    time = datetime.now().strftime("%d. %m. %Y, %H:%M:%S")

    # create user implementation
    implementation = ''
    for file in (Path(__file__).parent.parent / 'User').iterdir():
        if not file.is_dir():
            with open(file, 'r') as f:
                data = f.read()

            implementation += '<h2>{name}</h2> <pre>{code}</pre>'.format(name=file.name, code=data)

    bug_reports_path = Path(__file__).absolute().parent.parent / 'bug_reports'

    if not bug_reports_path.exists():
        try:
            bug_reports_path.mkdir()
        except (FileNotFoundError, OSError):
            sys.stderr.write(f'Problem with creating {bug_reports_path} folder. Bug report won\'t be generated')
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

    file_name = f'bug_report_{str(uuid.uuid4())[0:7]}.html'
    while (bug_reports_path / file_name).exists():
        file_name = f'bug_report_{uuid.uuid4()[0:7]}.html'

    with open(bug_reports_path / file_name, 'w') as f:
        text = html_template.format(traceback=exception, config=config, history=history, datetime=time,
                                    version=__version__, implementation=implementation)
        f.write(text)

    QtWidgets.QApplication.quit()

    sys.stderr.write(
        f"""Orodael Turrim crashed! 
If you think that problem is in the framework, please create an issue at GitLab or GitHub.
Please attach a bug report HTML file {file_name} to issue. 
Thanks for making Orodael Turrim better.\n\n""")

    sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.exit(1)
