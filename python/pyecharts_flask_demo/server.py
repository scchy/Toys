# python3
# Author: Scc_hy
# Create date:  2021-12-08
# Func: flask demo
# ======================================================================================


from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

CurrentConfig.GLOBAL_ENV = Environment(
    loader=FileSystemLoader('./templates')
)

from pyecharts import options as opts
from pyecharts.charts import Bar



def bar_base():
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

app = Flask(__name__, static_folder='templates')

@app.route('/')
def index():
    c = bar_base()
    return Markup(c.render_embed())

if __name__ == '__main__':
    app.run()