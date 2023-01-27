from flaskr import app
import jinja2.runtime

with app.app_context():
    @app.context_processor
    def utility_processor():
        def arg(arg, default_value):
            """
            Parameters
            - arg: テンプレート内で使う引数
            - default_value: 引数が渡されていなかった時の値
            """
            if isinstance(arg, jinja2.runtime.Undefined):
                return default_value
            else:
                return arg
        def tw_color():
            return '55acee'

        return dict(arg=arg, tw_color=tw_color)