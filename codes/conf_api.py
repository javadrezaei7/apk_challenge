import flask
import flask_restful
from apk import Log
log = Log()
class ConfApi(flask_restful.Resource):
    app = flask.Flask(__name__)
    app_rest = flask_restful.Api(app)

    def post(self):
        """
        {
            "config": "/usr/share/apk/config.json",
            "data": {}
        }
        """
        data = flask.request.get_json()
        if data:
            config = data.get("config", "config.json")
            with open(config, 'w+') as f:
                f.write(str(data).replace("'", '"'))
            log.logger.info("Config file modified.")
            return 'OK!', 200
        return "No data", 400

    def run(self):
        self.app_rest.add_resource(ConfApi, "/confapi")
        self.app.run(host='127.0.0.1', port=3000)


